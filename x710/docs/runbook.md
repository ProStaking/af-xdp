# Enable AF_XDP zero-copy on an existing standalone-port Firedancer validator

Prepared for publication. The voting comparison and restored-voter checks are complete. See [the article](VOTING-BLOG-DRAFT.md) for the measured results and [the numeric summary](voting-summary.json) for the full resource data. The executable procedure below changes the backend on an already-working validator with a dedicated standalone X710 port. Host migration, bond conversion, NIC preparation and initial resource provisioning are separate prerequisites.

## What is being tested

Stock Linux i40e, stock Firedancer 26.10.5 commit 6286f99e400c1d5ac6f95b8cf36491555faa3726, Intel X710 (PCI ID 8086:1572), Ubuntu 26.04.1, kernel 7.0.0-42-generic, Ryzen 7950X / 128 GB machine, one 10 Gbps link, MTU 1500. No custom driver, firmware update, or Firedancer code patch. This is a tested tuple, not a claim that every X710/firmware/kernel combination behaves identically.

The existing two-port active-backup bond cannot be used for this pinned native-XDP path. The controlled test uses the connected physical port directly, preserves the existing public address/MAC/gateway, and keeps independent management on another NIC. Do not silently convert an active-backup bond to LACP. Validate upstream MAC/port policy and recovery before any topology change.

## Scope and prerequisites

Start with a healthy **sole voting instance on this same host**, already using sockets on a dedicated standalone X710 port. Its public address, MAC, routes, consensus-state files and identity stay in place throughout this procedure. Confirm its existing restart/history checks and independent management work before proceeding. Pause any external service-start automation for the maintenance interval. Keep the existing sandbox, trusted snapshot policy and localhost-only RPC/metrics.

The following are site-specific preparations, not supplied migration automation:

- If moving from another host, complete your client/version-specific identity and authoritative consensus-state handover first. Stop and fence the previous voter before this host starts. This guide neither transfers keys nor implements a signed-history verifier.
- If starting on an active-backup bond, complete and test a separately reviewed standalone-port migration and its restoration procedure first. Resolve switch MAC policy, routes and independent management. No bond/IP/MAC changes appear in the commands below.
- Provision enough hugepages, hugetlbfs reservations, memlock and service memory for both backends before the maintenance window. Retain that common pool across restarts. The measured layout and sizing are below; boot provisioning is host-specific.
- Prepare the dedicated NIC and loopback offloads for this exact XDP configuration, with a saved NIC state and reviewed site restoration commands. For one net tile, our preparation selected one combined queue, queue-zero RSS and UDP4 four-tuple hashing; RX/TX rings stayed 512/512. The targeted stages were `ethtool-channels`, `ethtool-offloads` and `ethtool-loopback`. Their **check** must pass before the backend swap. The scoped procedure does not mutate these settings.
- Verify a site recovery path that can stop this service through independent management if startup or connectivity fails. If a timer is used, it must fail closed rather than start a second voter. The lab's private fencing/history/recovery helpers are not part of this downloadable runbook.

DoubleZero is optional and was not validated. Existing healthy connectivity and a separate compatibility test are required before claiming support for that integration.

## Reversible backend configuration

These commands are a published operator recipe, not a clean-room replay of the lab's private orchestration. Use Bash as root on the prepared Linux host. Replace the service, config and interface values with your verified existing values. The service must already read `CONFIG` directly and run the pinned binary; do not change its ExecStart or security settings here. Python 3.11+ is used only to parse and minimally edit TOML. The example configuration files are reference layouts, not substitutes for your working configuration.

```bash
sudo -i
set -euo pipefail
FD=/opt/firedancer/v26.10.5/bin/firedancer
SERVICE=firedancer.service
CONFIG=/etc/firedancer/testnet.toml
IFACE=ens1f0
STATE=$(mktemp -d /var/tmp/firedancer-x710.XXXXXXXX)
chmod 700 "$STATE"
export CONFIG IFACE STATE

test -f "$CONFIG" && test ! -L "$CONFIG"
test -d "/sys/class/net/$IFACE/device"
test ! -e "/sys/class/net/$IFACE/master"
"$FD" --version
sha256sum "$FD"
systemctl show "$SERVICE" -p ExecStart -p ControlGroup -p MainPID
ip -details link show dev "$IFACE"
ethtool -i "$IFACE"
cp --preserve=all "$CONFIG" "$STATE/socket.toml"
sysctl -n net.ipv4.conf.lo.accept_local > "$STATE/lo.accept_local"
sysctl -n net.ipv4.conf.lo.route_localnet > "$STATE/lo.route_localnet"
```

Review the printed binary, service and interface before proceeding. Keep `STATE` recorded in your private maintenance notes; do not lose the backup path across shell sessions. The next block rejects a non-socket or different-interface baseline and changes only the backend fields. All identity, history, trust, resource and application settings are retained.

```bash
python3 - <<'PYCONFIG'
import os, pathlib, re, tomllib
state = pathlib.Path(os.environ['STATE'])
text = (state/'socket.toml').read_text()
original = tomllib.loads(text)
assert original['net']['provider'] == 'socket', 'Require explicit socket baseline'
assert original['net']['interface'] == os.environ['IFACE'], 'Require same standalone port'
updates = {'net': {'provider': 'xdp'}, 'net.xdp': {
    'xdp_mode': 'drv', 'native_bond': 'false', 'xdp_zero_copy': 'true',
    'poll_mode': 'softirq', 'rss_queue_mode': 'simple'}}
for section, values in updates.items():
    pattern = r'(?m)^[ \t]*\[' + re.escape(section) + r'\][ \t]*(?:#.*)?$'
    matches = list(re.finditer(pattern, text))
    assert len(matches) <= 1
    if not matches:
        text += '\n[' + section + ']\n'
        matches = list(re.finditer(pattern, text))
    start = matches[0].end()
    following = re.search(r'(?m)^[ \t]*\[', text[start:])
    end = start + following.start() if following else len(text)
    body = text[start:end]
    for key, value in values.items():
        line = f'{key} = "{value}"'
        key_pattern = r'(?m)^[ \t]*' + re.escape(key) + r'[ \t]*=.*$'
        if re.search(key_pattern, body):
            body = re.sub(key_pattern, line, body)
        else:
            body += '\n' + line + '\n'
    text = text[:start] + body + text[end:]
candidate = tomllib.loads(text)
expected = tomllib.loads((state/'socket.toml').read_text())
expected['net']['provider'] = 'xdp'
expected['net'].setdefault('xdp', {}).update(updates['net.xdp'])
assert candidate == expected, 'Unexpected config change'
path = state/'xdp.toml'
path.write_text(text)
path.chmod(0o600)
PYCONFIG
diff -u "$STATE/socket.toml" "$STATE/xdp.toml" || test "$?" -eq 1
"$FD" mem --json --testnet --config "$STATE/xdp.toml"
```

Confirm the preview fits the **already reserved** pool and service limits. If `listen_gre` was absent, it remains absent: the pinned default is the string `"auto"`. In simple RSS mode that field is ignored; it is not a GRE-disable switch. If your working config explicitly sets it, this minimal edit preserves it. The [pinned schema](https://github.com/firedancer-io/firedancer/blob/6286f99e400c1d5ac6f95b8cf36491555faa3726/src/app/firedancer/config/default.toml#L1270-L1310) documents the distinction.

The following helper stops the service and checks every remaining process list in its cgroup. Keep the service stopped if this check or any preparation check fails. The config backup contains no backup of vote history: **never roll history back when restoring a backend**.

```bash
stop_validator() {
  local cg
  cg=$(systemctl show "$SERVICE" -p ControlGroup --value)
  systemctl stop "$SERVICE"
  test "$(systemctl show "$SERVICE" -p MainPID --value)" = 0
  if [ -n "$cg" ] && [ -d "/sys/fs/cgroup$cg" ]; then
    while IFS= read -r procs; do
      test -z "$(cat "$procs")" || return 1
    done < <(find "/sys/fs/cgroup$cg" -name cgroup.procs -type f)
  fi
}
stop_validator
sysctl -w net.ipv4.conf.lo.accept_local=1
sysctl -w net.ipv4.conf.lo.route_localnet=1
"$FD" configure check hugetlbfs sysctl ethtool-channels ethtool-offloads ethtool-loopback \
  --testnet --config "$STATE/xdp.toml"
cp --preserve=all "$STATE/socket.toml" "$STATE/install.toml"
cat "$STATE/xdp.toml" > "$STATE/install.toml"
cp --preserve=all "$STATE/install.toml" "$CONFIG"
systemctl start "$SERVICE"
systemctl is-active "$SERVICE"
journalctl -u "$SERVICE" --since '5 minutes ago' --no-pager
ip -details link show dev "$IFACE"
```

Do not measure until runtime proof and own-vote/catch-up checks below pass. If initialization reports insufficient workspace capacity, do not delete arbitrary hugetlbfs files: stop and use your pre-reviewed, manifest-scoped workspace maintenance procedure. A failed command leaves the maintenance sequence stopped; use the rollback below rather than continuing from a partial state.

To return to the original standalone/socket configuration, use the same shell variables (or restore their recorded values), keep external start automation paused, and run:

```bash
stop_validator
cp --preserve=all "$STATE/socket.toml" "$CONFIG"
sysctl -w "net.ipv4.conf.lo.accept_local=$(cat "$STATE/lo.accept_local")"
sysctl -w "net.ipv4.conf.lo.route_localnet=$(cat "$STATE/lo.route_localnet")"
cmp "$STATE/socket.toml" "$CONFIG"
test "$(sysctl -n net.ipv4.conf.lo.accept_local)" = "$(cat "$STATE/lo.accept_local")"
test "$(sysctl -n net.ipv4.conf.lo.route_localnet)" = "$(cat "$STATE/lo.route_localnet")"
ip -details link show dev "$IFACE"
ip -details link show dev lo
```

Confirm the experiment's XDP attachments have gone after graceful shutdown. If an attachment remains, keep the service stopped and investigate ownership; this guide does not blindly detach another program. After your existing consensus-state restart check passes, restart and verify:

```bash
systemctl start "$SERVICE"
systemctl is-active "$SERVICE"
journalctl -u "$SERVICE" --since '5 minutes ago' --no-pager
```

Verify correct identity/cluster, catch-up, independently advancing own votes, protected endpoints and unchanged management reachability before resuming external automation or retiring recovery. This rollback restores every setting changed by the scoped commands. It leaves the prerequisite NIC preparation and resource pool in place; reversing those separate preparations requires their saved site procedure.

## Resource layout

Compute the actual candidate footprint using the installed binary's `firedancer mem --json --testnet --config CONFIG`. This is a configuration footprint preview, not proof of runtime readiness. Block production materially changes requirements.

The tested voting candidate keeps one net tile, four replay-execution tiles, two shred tiles, one snapshot-decompression tile and one snapshot-ingestion tile, enables block production, disables snapshot production and uses generated automatic affinity within a fixed 30-logical-CPU budget. Preview:

| Backend | Tiles | 1 GiB pages | 2 MiB pages | Locked memory |
|---|---:|---:|---:|---:|
| Sockets |37|78|2305|88,642,129,920 bytes|
| Native XDP |38|79|2222|89,545,990,144 bytes|

For comparison, reserve the maximum 79×1 GiB plus 2305×2 MiB pool once and retain it across phases. The approved host limits are 96 GiB memlock and 104 GiB cgroup memory; these are not universal defaults. This host has approximately 122.69 GiB usable memory. Guard MemAvailable>=16 GiB and disk free>=250 GiB. Inspect cgroup memory events and pressure as well as available RAM; page cache and hugepages complicate RSS-only comparisons.

Provision gigantic pages before beginning this backend-only procedure, potentially early in a separately planned controlled reboot. Verify the resulting pool and restart behavior before measuring.

Workspace files on the two dedicated hugetlbfs mounts are disposable RAM state. Pinned Firedancer startup replaces current topology files but can leave obsolete backend workspaces. When switching topology, hold service startup, gracefully stop and verify an empty cgroup, then clear only manifest-verified regular workspace/stack files from those mounts while retaining the page pool. Never confuse these RAM files with disk vote history, keys, snapshots or account storage.

## Matched measurement

Run the same read-only 10-second collector throughout, separating startup/snapshot loading from steady state:

- A: 60 stable minutes, original active-backup bond/socket.
- B: 15 stable minutes, standalone X710/socket topology control.
- C: 60 stable minutes, standalone X710/native explicit zero-copy.

Keep binary, identity, functional layout, CPU budget, cache/accounts settings and MTU fixed. Record unavoidable backend and NIC differences. A→C measures the combined operational changes, not pure zero-copy. B→C controls topology more closely; an equal-settings native-XDP copy arm would further isolate copy cost.

Collect per-core user/system/softirq/iowait and host context switches; actual process/cgroup CPU time; process RSS and cgroup/cache/hugepage/pressure data; per-interface bytes/packets/errors/drops plus hardware/application counters; physical disk throughput/IOPS/average wait/queue/busy-time counters; voting, replay, epoch/load and assigned/produced leadership slots. Do not add partition and whole-disk totals together. Linux disk busy time is not a general NVMe saturation percentage; average I/O wait is not a latency distribution. RSS totals may double-count shared mappings and omit hugepage accounting.

Use ordinary cluster traffic, never active stress against peers. Normalize and disclose workload differences. No assigned leader slots means leadership performance remains untested. One hour is initial evidence, not long-term reliability proof. Missing baseline metrics cannot be backfilled: begin a new matched window.

## XDP configuration and runtime proof

The candidate uses native `drv`, explicit zero-copy, simple RSS and softirq polling. Exact schema/types must match the installed release. The native physical interface and loopback are involved; only required loopback `accept_local`/`route_localnet` values were changed in this test. Preserve originals and restore them on return to sockets.

Voting adds UDP 9001 and 9007 to the existing validator port set 8001/8003/8004/8005/8701/8702. Inspect the loaded selector and configured address/ports. Redirected XDP UDP bypasses ordinary netfilter, including applicable anti-spoof filters. The stock filter also selects matching inner GRE; downstream Alpenglow networking requires configured GRE remotes and rejects unconfigured GRE. This is a deliberate bounded filtering exception, not equivalent source filtering. SSH TCP must not be redirected; keep RPC/metrics bound to localhost.

Require runtime evidence of the physical AF_XDP forced-zero-copy bind (observed flags 0xc), driver-mode attachment, stable process/program identity and advancing receive/transmit activity. A config flag or successful service start alone is insufficient. Separate initial buffer warnings/counters from stable deltas. Report Linux interface drops, driver errors and application drops separately; none alone measures end-to-end packet loss.

## Finish and persistence

The scoped recipe finishes on the same standalone port with sockets, original loopback values and current consensus history. The lab additionally restored its original bond through a separately reviewed host-specific procedure. Mainnet, host migration and another consensus protocol each require their own operational plan.

### Read-only whole-system collector

Run the collector and summarizer examples from the repository `scripts/` directory.

`collect_system.py` was smoke-tested on the lab: two samples, valid CPU/disk/network fields,0700 output directory and 0600 JSONL file. It requires Linux procfs/sysfs/cgroupv2, systemd and existing ethtool; it installs nothing. Run with permission to read the validator processes' I/O counters. It does not stop/reconfigure the validator and is NOT the experiment's safety watchdog.

Example (replace the service, physical interface and fresh output directory):

```sh
sudo python3 collect_system.py \
  --service firedancer.service \
  --interface ens1f0 \
  --output-dir /var/tmp/firedancer-run-A \
  --label bonded-socket \
  --duration 3600 --interval 10
```

Capture voting/application metrics separately at the same cadence and retain actual common start/end timestamps. Record the exact config/topology and public cluster context for each labeled phase. The collector deliberately avoids key files, process command lines and environment variables. Inspect artifacts before publication; operator-provided labels and process names may still need redaction.

### Pinned build recipe

The tested source checkout is clean at commit `6286f99e400c1d5ac6f95b8cf36491555faa3726`. Binary compiler metadata identifies **GCC 13.4.0, Ubuntu 13.4.0-10ubuntu1**; existing build artifacts are under `build/native/gcc-13/13.4.0`. The pinned native machine configuration uses `-march=native -mtune=native`, so build for the target CPU rather than distributing that binary blindly to another architecture.

The following **untested clean-build recipe** is reconstructed from the pinned README/build configuration. Neither its clean-room success nor the output executable path was verified in this experiment:

```sh
git clone https://github.com/firedancer-io/firedancer.git
cd firedancer
git checkout --detach 6286f99e400c1d5ac6f95b8cf36491555faa3726
git submodule update --init --recursive
./deps.sh
make -j"$(nproc)" MACHINE=native CC=gcc-13 LD=gcc-13

```

Locate the actual native `firedancer` executable in the build output and verify its version/hash before installation; no output path is asserted here. The tested installed executable was `/opt/firedancer/v26.10.5/bin/firedancer`.

Install the appropriate GCC 13 toolchain through the operator's normal package process before building. The dependency script may install/build dependencies; review the pinned script for the build host. The historical shell invocation was not retained, so this is a recipe reconstructed from pinned build definitions and observed artifacts, not a claim that the current experiment reran or validated a clean-room build. Record dependency/toolchain versions and the resulting hash. The tested installed hash is listed in the compatibility table; differing toolchains can produce different binaries. Use the native `firedancer` binary, not an unreviewed development command that automatically creates keys or configures the host.


### Reference configuration and NIC preparation

[voting-socket.example.toml](../configs/voting-socket.example.toml) and [voting-xdp.example.toml](../configs/voting-xdp.example.toml) preserve the tested functional layout with operator placeholders. They are reference configurations, not drop-in service configs. Use the minimal edit above on your working standalone/socket configuration.

For the lab, NIC preparation used `configure init ethtool-channels ethtool-offloads ethtool-loopback`. This changes queue/RSS and offload state, and is deliberately outside the reversible backend-only commands above. Before a separate preparation window, save `ethtool -l/-g/-k/-c/-x/-n`, UDP4 flow-hash settings and loopback offloads; prepare explicit restore commands for the features and RSS key/table the driver actually supports. A reboot does not guarantee restoration of the RSS key. The loopback sysctls are restored directly by the scoped recipe; the physical interface required no corresponding relaxation.

### Calculate resource rates

Use `summarize_system.py` on a steady window from the collector. Specify the physical data disk, not both a disk and its partition. For a continuously collected file, pass the actual phase boundaries as Unix UTC seconds:

```sh
python3 summarize_system.py /var/tmp/firedancer-run-A/system.jsonl \
  --interface ens1f0 --disk nvme0n1 \
  --start START_UNIX_SECONDS --end END_UNIX_SECONDS > summary-A.json
```

The script uses the first and last samples inside the selected bounds, reports their actual duration and maximum sample gap, rejects observed per-sample counter decreases, checks sampled boot/service-generation metadata when available, and reports per-core CPU as well as validator cgroup CPU. CPU core equivalents are delta CPU microseconds divided by elapsed microseconds. NIC rates use counter deltas; disk bytes use Linux diskstats' 512-byte sectors. Average disk wait is cumulative request time divided by completed I/Os, and average queue depth is weighted I/O time divided by elapsed time. Instantaneous in-flight I/O is a gauge and is not treated as a monotonic counter. This analyzer reproduced the baseline CPU result from the private experimental data; it does not establish voting or runtime zero-copy proof.


Observed collection limits: cgroup `io.stat` was unavailable in this service configuration and is recorded as null. Whole-disk diskstats, per-process I/O counters and host/cgroup I/O pressure were available. Do not claim per-service physical I/O attribution from the missing cgroup counter. A large early C write burst is retained in the primary full-window result; a fixed first-five-minute exclusion applied to every phase is a sensitivity analysis, not a replacement for the original observations.


### Exact resource values used here

The shared page pool was reserved with two dedicated hugetlbfs mounts under the configured mount root. Their tested effective options were:

```text
.gigantic: rw,relatime,pagesize=1024M,min_size=84825604096
.huge:     rw,relatime,pagesize=2M,min_size=4833935360
```

Both mount roots were owned by the runtime account with mode 0700. `min_size` reserves the specified hugepage capacity; it does not create contiguous physical pages. The pools in `/sys/kernel/mm/hugepages/hugepages-1048576kB/nr_hugepages` and `hugepages-2048kB/nr_hugepages` must already reach 79 and 2305 respectively. Dynamic allocation did not reliably produce enough contiguous 1 GiB pages, so this lab provisioned them early in an approved controlled reboot, with persistent recovery and an independent management path already tested. Do not repeatedly churn allocations or drop caches on an active voter.

The systemd resource values were:

```ini
[Service]
LimitMEMLOCK=103079215104
MemoryMax=111669149696
CPUAffinity=1-15 17-31
Restart=no
```

This is a resource fragment, not a complete service unit. The CPU list is host-specific and must be replaced for another topology. Preserve the existing startup checks and sandbox; this experiment launched preparation as root, then verified the relevant runtime tiles at the unprivileged runtime UID, zero effective capabilities, NoNewPrivileges=1 and seccomp=2. The lab used an additional private startup-history check and persistent source fencing for its host handover. Those helpers are not supplied here. The scoped recipe preserves your existing restart protections and assumes this host already owns the sole voting instance.

The portable collector now records boot ID and systemd service generation. The experiment's older capture schema used the independent phase guard to enforce unchanged process/attachment identity. The analyzer explicitly reports missing generation metadata; do not treat endpoint deltas as proof of uninterrupted service. Events entirely between samples still require external continuity checks. A decreasing CPU iowait counter can be a Linux accounting artifact; the portable analyzer stops for review rather than labeling every such decrease a reboot.


## Observed completion

The zero-copy guard completed 3,605.011 seconds with 359/359 caught-up samples and maximum root distance 1. Both network backends kept the same functional layout and maximum page pool. Afterward, the bond/socket configuration, NIC snapshot, loopback values, routes, binary hash, protected endpoints and runtime isolation were checked. Own votes advanced across three public samples. The startup-history gate passed under the service restrictions, and the experiment timer was retired. A separately requested reverse handover is outside these measurement windows.


## Collector coverage prerequisite

The portable collector reads one selected service cgroup. Before measuring, confirm ALL validator tiles are in that cgroup. Tiles moved into another cgroup will be omitted and the CPU/resource totals will be incomplete. The measured X710 layout satisfied this prerequisite. Multi-cgroup layouts need a separately reviewed collector.
