#!/usr/bin/env python3
"""Checks that the IONIS model actually loads and produces predictions.

    python3 test_predictions.py

WHY THIS EXISTS. The prediction sections — "What Can You Work Right Now?", the contest
prediction table, the DXpedition bands — all sit behind `{% if predictions %}`. When the
model failed to load, publish.py printed one WARNING, rendered every page without them and
exited 0. The site kept updating and kept advertising "AI-powered predictions" in its own
meta description while showing none. That ran from 2026-03-16 until someone read the journal.

The cause was four hardcoded constants pointing into a sibling repo's on-disk layout
(/mnt/ai-stack/ionis-ai/ionis-training/versions/{common,v22}/) that does not exist on this
host. The model, its config and its weights are package data inside ionis-validate; this
pins that we ask the package, and that a load failure is no longer silent.

clickhouse_connect is stubbed because publish.py imports it at module scope and nothing here
touches a database.
"""
import sys
import types
from pathlib import Path

if "clickhouse_connect" not in sys.modules:
    try:
        import clickhouse_connect  # noqa: F401
    except ModuleNotFoundError:
        sys.modules["clickhouse_connect"] = types.ModuleType("clickhouse_connect")

sys.path.insert(0, str(Path(__file__).parent))
import publish  # noqa: E402

failures = []


def check(label, got, want):
    if got == want:
        print(f"  PASS  {label}")
    else:
        print(f"  FAIL  {label}: got {got!r}, want {want!r}")
        failures.append(label)


print("== the paths that rotted are gone, not repointed ==")
# Comments are excluded deliberately: the note explaining what rotted names the old path
# on purpose, and a check that forbids describing the bug is a check that punishes the fix.
code = "\n".join(l for l in Path(publish.__file__).read_text().splitlines()
                 if not l.lstrip().startswith("#"))
for dead in ("_V22_CONFIG", "_V22_CHECKPOINT", "_COMMON_DIR", "_TRAINING_DIR",
             "/mnt/ai-stack/ionis-ai/ionis-training"):
    check(f"no live reference to {dead}", dead in code, False)
check("model comes from the installed package",
      "from ionis_validate.model import load_model" in code, True)

print("== the model loads ==")
model, device = publish.load_ionis_model()
check("load_ionis_model returns a model", model is not None, True)
check("on CPU", str(device), "cpu")
if model is None:
    print("\n  cannot continue without a model")
    sys.exit(1)

print("== and produces usable predictions ==")
preds = publish.generate_predictions(model, device, sfi=110.0, kp=2.67)
check("predictions is a non-empty list", bool(preds) and isinstance(preds, list), True)
check("one entry per destination", len(preds), len(publish.PREDICTION_DESTINATIONS))

first = preds[0]
check("entries carry a destination label", bool(first.get("label")), True)
check("every prediction band is present",
      sorted(first["bands"]), sorted(publish.PREDICTION_BANDS))
check("band values are rendered strings",
      all(isinstance(v, str) and v for v in first["bands"].values()), True)
# A table of nothing-but-dashes renders as a section with no information in it, which is
# the same user-visible outcome as having no model at all.
check("not every band on every path is a dash",
      any(v != "\u2014" for p in preds for v in p["bands"].values()), True)

print("== the model responds to its inputs ==")
# A model that ignores SFI/Kp would render the same table under any conditions, which would
# look exactly like a working prediction. Storm conditions must not read identically to quiet.
quiet = publish.generate_predictions(model, device, sfi=110.0, kp=1.0)
storm = publish.generate_predictions(model, device, sfi=110.0, kp=8.0)
check("a severe Kp changes the outcome", quiet == storm, False)
low = publish.generate_predictions(model, device, sfi=70.0, kp=1.0)
high = publish.generate_predictions(model, device, sfi=200.0, kp=1.0)
check("a large SFI swing changes the outcome", low == high, False)

print()
if failures:
    print(f"  {len(failures)} FAILED")
    sys.exit(1)
print("  all checks passed")
