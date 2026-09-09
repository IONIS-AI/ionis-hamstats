-- Serving layer for ham-stats. Applied by refresh.py (idempotent, every run).
--
-- WHY THIS EXISTS. publish.py used to query ClickHouse directly on every run: 123,962,343,315
-- rows read to publish 4,398 -- 28 million rows scanned per row published, eight times a day.
-- ClickHouse remains the source of truth and the only place the raw data lives; this holds the
-- already-aggregated results so the site is served from an OLTP store instead of re-deriving
-- them from 10.8 billion WSPR spots to render a table that moves by a rounding error.
--
-- ONE TABLE, JSONB PAYLOAD, DELIBERATELY. The 23 queries have 23 different shapes and publish.py
-- consumes all of them as {query_name: [row dicts]}. Normalising them into 23 typed tables would
-- mean a ClickHouse-to-PostgreSQL type mapping maintained by hand, which is a whole class of
-- silent corruption for no benefit -- nothing queries this relationally, it is read whole and
-- handed to a template renderer. JSONB round-trips the shape exactly.

CREATE SCHEMA IF NOT EXISTS serving;

CREATE TABLE IF NOT EXISTS serving.query_results (
    name              text        PRIMARY KEY,
    payload           jsonb       NOT NULL,
    row_count         integer     NOT NULL,

    -- Staleness must be answerable without knowing the refresh schedule. max_age is the
    -- contract the refresh cadence promises to keep; publish compares against it rather than
    -- against a number hardcoded on the reading side, so changing a cadence cannot leave a
    -- consumer silently trusting a result far older than it believes.
    refreshed_at      timestamptz NOT NULL,
    max_age           interval    NOT NULL,

    -- What it cost in ClickHouse, kept so the reason this layer exists stays measurable
    -- rather than remembered.
    source_rows_read  bigint,
    source_elapsed_ms integer,

    CONSTRAINT row_count_matches CHECK (row_count = jsonb_array_length(payload))
);

COMMENT ON TABLE serving.query_results IS
    'Materialised ClickHouse aggregate results served to ham-stats publish. '
    'ClickHouse is the source of truth; this is a cache with an explicit staleness contract.';

CREATE OR REPLACE VIEW serving.stale_results AS
    SELECT name,
           refreshed_at,
           max_age,
           now() - refreshed_at AS age,
           (now() - refreshed_at) - max_age AS overdue_by
      FROM serving.query_results
     WHERE now() - refreshed_at > max_age;

COMMENT ON VIEW serving.stale_results IS
    'Results past their promised max_age. Empty is the healthy state; publish reports any rows.';
