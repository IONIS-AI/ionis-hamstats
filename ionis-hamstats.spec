%global debug_package %{nil}

Name:           ionis-hamstats
Version:        1.1.1
Release:        1%{?dist}
Summary:        Ham Stats publishing pipeline — ClickHouse aggregates to a static site

License:        GPL-3.0-or-later
URL:            https://github.com/IONIS-AI/ionis-hamstats
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  systemd-rpm-macros

Requires:       git
Requires:       systemd

%description
Systemd units and launchers for the Ham Stats publishing pipeline. refresh.py materialises
ClickHouse aggregate results into a PostgreSQL serving layer on a per-query cadence;
publish.py reads that layer, renders the site with Jinja2 and pushes it.

THIS PACKAGE SHIPS UNITS, NOT CODE. The units were hand-written into /etc/systemd/system,
owned by no package and no playbook -- upgrades never touched them and nothing recorded what
was deployed. That is what needed fixing, and it is what this fixes.

The code runs from the git checkout on the host that owns it (default
/srv/ionis/repos/ionis-hamstats, override with HAMSTATS_ROOT). hamstats-1 is where ham-stats
is developed as well as published, so shipping publish.py inside an RPM would mean a tag, a
build and an install for every edit made on the machine the file already lives on -- and the
installed copy would shadow the edited one, silently. Each unit pulls before it runs, so what
executes is what is committed to main.

Python dependencies (jinja2, psycopg, clickhouse-connect, pyyaml, ionis-validate) live in the
service virtualenv, managed separately. This package owns the units and the launchers.

%prep
%autosetup -n %{name}-%{version}

%build
# Nothing to compile — Python and SQL.

%install
install -d -m 0755 %{buildroot}%{_bindir}
install -d -m 0755 %{buildroot}%{_unitdir}
install -d -m 0755 %{buildroot}%{_sysconfdir}/hamstats

# Launchers. The code lives in the checkout; these resolve it and the interpreter so the unit
# files carry no paths of their own, and so an operator can run exactly what the timer runs.
cat > %{buildroot}%{_bindir}/hamstats-publish <<'EOF'
#!/bin/bash
# The checkout is both the code and the content: publish.py renders into its docs/ and commits
# there. They were separate when this package shipped the code; they are the same tree now.
export HAMSTATS_ROOT="${HAMSTATS_ROOT:-/srv/ionis/repos/ionis-hamstats}"
export HAMSTATS_CONTENT_DIR="${HAMSTATS_CONTENT_DIR:-$HAMSTATS_ROOT}"
exec "${HAMSTATS_PYTHON:-/srv/ionis/.venv/bin/python}" \
     "$HAMSTATS_ROOT/publish.py" "$@"
EOF
cat > %{buildroot}%{_bindir}/hamstats-refresh <<'EOF'
#!/bin/bash
export HAMSTATS_ROOT="${HAMSTATS_ROOT:-/srv/ionis/repos/ionis-hamstats}"
exec "${HAMSTATS_PYTHON:-/srv/ionis/.venv/bin/python}" \
     "$HAMSTATS_ROOT/refresh.py" "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/hamstats-publish %{buildroot}%{_bindir}/hamstats-refresh

install -p -m 0644 systemd/hamstats-refresh@.service       %{buildroot}%{_unitdir}/
install -p -m 0644 systemd/hamstats-refresh@live.timer     %{buildroot}%{_unitdir}/
install -p -m 0644 systemd/hamstats-refresh@daily.timer    %{buildroot}%{_unitdir}/
install -p -m 0644 systemd/hamstats-refresh@weekly.timer   %{buildroot}%{_unitdir}/
install -p -m 0644 systemd/hamstats-publish.service        %{buildroot}%{_unitdir}/
install -p -m 0644 systemd/hamstats-publish.timer          %{buildroot}%{_unitdir}/

%post
%systemd_post hamstats-refresh@live.timer hamstats-refresh@daily.timer hamstats-refresh@weekly.timer hamstats-publish.timer
if [ $1 -eq 1 ]; then
cat <<'EOM'
------------------------------------------------------------
 ionis-hamstats installed.

 Before enabling the timers:
   - /etc/hamstats/db-rw.dsn and db-ro.dsn must exist (Vault Agent renders them)
   - /srv/ionis/repos/ionis-hamstats must be a checkout the service user can push
   - the service virtualenv needs: jinja2 psycopg[binary] clickhouse-connect pyyaml
     ionis-validate

 If /etc/systemd/system/hamstats-publish.service still exists it is the old hand-placed
 unit and SHADOWS the packaged one. Remove it, then: systemctl daemon-reload
------------------------------------------------------------
EOM
fi

%preun
%systemd_preun hamstats-refresh@live.timer hamstats-refresh@daily.timer hamstats-refresh@weekly.timer hamstats-publish.timer

%postun
%systemd_postun_with_restart hamstats-refresh@live.timer hamstats-refresh@daily.timer hamstats-refresh@weekly.timer hamstats-publish.timer

%files
%license LICENSE
%doc README.md
%{_bindir}/hamstats-publish
%{_bindir}/hamstats-refresh
%{_unitdir}/hamstats-refresh@.service
%{_unitdir}/hamstats-refresh@*.timer
%{_unitdir}/hamstats-publish.service
%{_unitdir}/hamstats-publish.timer
%dir %{_sysconfdir}/hamstats

%changelog
* Wed Sep 09 2026 Greg Beam <ki7mt@yahoo.com> - 1.1.1-1
- refresh.py defaulted CH_HOST to 10.60.1.1, the Thunderbolt DAC between the 9975 and the M3.
  That is correct only from those two machines; from publish-1 it is unroutable and every
  query dies on a 10-second connect timeout that names nothing. Defaults to the LAN address
  192.168.1.90 now, as publish.py always has.
- Units read an optional EnvironmentFile=-/etc/hamstats/env, so a host that IS on the DAC can
  set CH_HOST without editing code or the packaged unit.

* Wed Sep 09 2026 Greg Beam <ki7mt@yahoo.com> - 1.1.0-1
- Ship the units, not the code. 1.0.0 packaged publish.py, refresh.py, queries, SQL,
  templates and data into /usr/share/ionis-hamstats, which meant every edit on hamstats-1 --
  the host where ham-stats is developed as well as published -- cost a tag, a build and an
  install, and the installed copy silently shadowed the edited one.
- HAMSTATS_ROOT now defaults to the checkout (/srv/ionis/repos/ionis-hamstats). Each unit
  pulls before it runs, so what executes is what is committed to main and the host cannot
  drift from the branch.
- The units and launchers stay packaged. Hand-placed units owned by nothing was the actual
  problem being solved, and it still is.

* Wed Sep 09 2026 Greg Beam <ki7mt@yahoo.com> - 1.0.0-1
- First packaged release. The publish service was a hand-placed unit in
  /etc/systemd/system running scripts out of a git working tree, owned by no package and no
  playbook -- so upgrades never touched it and nothing recorded what was deployed. Same
  problem ionis-apps 4.0.5 fixed for its 15 hand-copied units.
- Adds the PostgreSQL serving layer: refresh.py materialises ClickHouse aggregates on a
  per-query cadence (live/daily/weekly) and publish.py reads Postgres instead of scanning
  123,962,343,315 ClickHouse rows on every 3-hourly run to publish 4,398 of them.
- Splits HAMSTATS_ROOT (packaged artifacts, /usr/share) from HAMSTATS_CONTENT_DIR (the git
  checkout pages are committed to). Both default to the script's own directory, so running
  from a clone is unchanged.
