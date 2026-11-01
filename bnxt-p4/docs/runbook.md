# Bounded unstaked operator procedure

This is a **source-and-manual reproduction package, not a drop-in deployment or complete portable activation kit**. The supplied service is a documentary template: private start/final-exec/fence helpers are **not included**. Supply reviewed equivalent safeguards before activation; do not remove the checks just to make the example start. A key-generating or voting handover script is deliberately not provided.

1. Reconstruct/verify source, build/pin default and opt-in driver and FD artifacts, confirm exact kernel/vermagic/PCI/firmware. Inspect Secure Boot/module trust through the site's normal policy; this guide does not disable it. Prepare independent management and console recovery. Remove the selected physical port from any bond/bridge under a separate approved topology plan. No voting instance may use this experimental host; source voter fence and retained-key exposure must be resolved by the operator.
2. Derive config from an existing working **unstaked** validator. Use the supplied TOML as measured layout reference, replace every placeholder, preserve current cluster/genesis/snapshot trust. Never set allow_any=true to bypass trust. `vote_account=""`, authorized voters empty, block production off. Use a distinct unfunded identity, no voting-key copy. Preserve snapshot loading despite snapshot production being disabled.
3. Create all configured directories as runtime-owned0700, including **vote_history even with voting disabled**, and verify writable parents in the actual service namespace. Files0600. Reuse content-hash-verified trusted snapshots/genesis in separate mutable data; never overwrite existing voting state. The first trial failed on the absent history directory even though physical zero-copy initialized.
4. Capture stock module/hash, all interface/routing/firewall/BPF/IRQ/cgroup/hugepage/offload/RSS/console state and exact inverse steps. Reserve a60-minute window, startup cutoff 30 minutes, stop cutoff 45 minutes and 15 minutes for recovery. Arm a root-owned independent normal-stop deadline before changing resources. No automatic retries. Any manual recovery/restart requires fresh safety, identity, resource and deadline checks within the approved window; the completed measured run used one service start.
5. Preview memory using the pinned experimental FD and final standalone config. Provision exactly the measured pool only if that config requires it; no blind configure-all or repeated compaction. Prepare NIC channels/offloads/loopback, IRQ balance/affinity/workqueue/cpuset using narrowly selected stock configure stages. Observe asynchronous irqbalance changes. Full configure check must pass, including console requirements. Preserve original values for inverse restoration.
6. Dedicated rules must direct only the configured UDP-port subset (tested approved maximum8001,8003,8004,8005,8701,8702,9001,9006,9007) to queue 0, ordinary RSS to remaining queues. Inspect rule masks/actions and both before/after bind. Redirected UDP bypasses ordinary firewall processing; SSH TCP is not redirected, RPC/metrics localhost. GRE selector behavior and downstream tunnel checks remain distinct; no DoubleZero claim.
7. Render the transient service with the candidate binary/config, existing privileged bootstrap and normal FD drop/sandbox. Restart=no; no boot enablement or inherited failure hooks. Consume a one-use launch token, validate current pins/fences after configure checks and immediately before exec. RuntimeMaxSec must be remaining time to the original stop cutoff. Launch `firedancer run --config CONFIG` with explicit complete TOML, as tested; no implicit cluster flags.
8. Verify runtime ZC/identity/replay and start a continuous15-minute healthy span only after those checks. A separate guard outside the FD cpuset collects health and can request ordinary stop. Keep raw metrics; stop for memory<16 GiB, diskfree<250 GiB, management loss, bad identity/fence, steering errors, relevant kernel/firmware/IOMMU faults or ambiguous ownership. Checksum-only counters are diagnostic. Ordinary testnet traffic only.
9. Normal stop and stock restoration are part of the result. Follow rollback guide, verify restored state, then retire deadline and preserve sanitized results. Do not promote to voting or begin benchmarks under this scope.

The test service starts privileged; FD later drops to config.user. InaccessiblePaths restricts the process namespace but does not protect retained keys from experimental kernel/root code. Current source gates and resource guards are essential operator prerequisites, not optional snippets.


## Concrete operator preflight on an already-isolated host

The following commands are a portable manual reference, **not a replay-tested replacement for the measured private controller**. They intentionally stop before mutation of network/modules or service activation. Begin only after the operator has provided a dedicated standalone port, existing distinct unstaked identity, stock recovery/console plan, prepared resource pool/NIC scheduling and the site gate/deadline implementation. No key transfer or generation occurs here.

```bash
# Bash, Linux; replace every SITE value before use.
set -euo pipefail
FD=/SITE/bin/firedancer-p4-prebind
CONFIG=/SITE/config/p4-unstaked.toml
IFACE=SITE_P4_INTERFACE
DATA=/SITE/data
RUNTIME_USER=sol
IDENTITY=/SITE/keys/unstaked-identity.json

test -f "$FD" && test -f "$CONFIG" && test -f "$IDENTITY"
test -d "/sys/class/net/$IFACE/device"
test ! -e "/sys/class/net/$IFACE/master"
uname -r
sha256sum "$FD"
ethtool -i "$IFACE"
ethtool -l "$IFACE"
ethtool -g "$IFACE"
ethtool -k "$IFACE"
ethtool -x "$IFACE"
ethtool -n "$IFACE"
ip -details link show dev "$IFACE"
ip route show
```

Compare these with the pinned kernel/module/binary and 48-channel/queue 0 layout. Reject unexpected bond membership, another XDP owner, extra RSS contexts or missing independent management. Check actual configured ports/rules, not merely the maximum port list in the article.

Directory preparation (only new dedicated trial paths, never an existing voter data directory):

```bash
sudo install -d -o "$RUNTIME_USER" -g "$RUNTIME_USER" -m 0700 \
  "$DATA" "$DATA/snapshots" "$DATA/vote-history"
sudo -u "$RUNTIME_USER" test -w "$DATA/vote-history"
"$FD" mem --json --config "$CONFIG"
cat /sys/devices/system/node/node0/hugepages/hugepages-1048576kB/nr_hugepages
cat /sys/devices/system/node/node0/hugepages/hugepages-2048kB/nr_hugepages
findmnt -t hugetlbfs
sudo "$FD" configure check all --config "$CONFIG"
```

Verify exact80/2083 preview, both dedicated mount minima/ownership,96 GiB memlock and 104 GiB service **and migrated-cpuset** ceilings. Failure means preparation remains incomplete. These checks do not allocate pages, run configure-all init, change IRQ masks or authorize alternate channel counts.

The measured launch used a60-minute lease from first mutation, a45-minute stop cutoff and a30-minute startup cutoff. Its one-use token, final pin/deadline check, independent guard, normal-stop timer, RuntimeMaxSec remaining to the original cutoff, migrated-cgroup checks and restoration ownership were supplied by private reviewed code. They are not replaced by `sleep`, a service-active check or a bare `systemd-run --on-active` timer in this package.

## Precise deployment gaps

Before activating from this package, an operator must supply and review:

- `start_gate.py` and `final_exec.py` equivalents or an explicitly reviewed manual launch gate, enforcing pins, identity/fence, clock/boot lease and final check after configure.
- Independent root guard outside the FD cpuset, runtime-proof capture and a fixed absolute normal-stop deadline; no automatic force-kill/unload/reboot.
- Resource allocation/mount preparation and owner-aware inverse; exact saved IRQ/irqbalance/workqueue/console/sysctl restoration, including recreated IRQ identities.
- Candidate module/standalone address transition and stock restoration for that site's interfaces, without affecting management or silently changing boot state.
- A durable terminal/cleanup receipt and final stock-state verification before timer retirement, plus exceptional incident/console recovery.

The documentary service references those missing site components and is **not runnable unchanged**. Do not delete its gates or invent their success. Source patch reconstruction is complete and verified; a universal activation controller and a fresh full clean-environment build remain outside the validation delivered here.
