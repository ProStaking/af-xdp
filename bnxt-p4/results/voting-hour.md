# P4 voting AF_XDP zero-copy: completed-hour findings

The measured P4 hour passed, and P4 remains the selected sole voter. X710 remains stopped/fenced with its zero-copy configuration and resources preserved. Final live health and signed-history checks passed; private evidence is retained.

Measured window: **2026-11-01T16:48:04+00:00 through 2026-11-01T17:48:04+00:00**, 3600.000114 seconds and 361 whole-system endpoint samples. Startup and fresh snapshot restoration are excluded. CPU and memory cover the service plus the disjoint migrated-tile cgroup, including descendant processes. Full per-core counters and both NVMe devices are retained in the private comparison and raw evidence; the public candidate JSON includes aggregate CPU and the data NVMe summary.

Validator system CPU changed from **0.08518 to 0.06705 core equivalents**, a **21.29% reduction** (0.01813 fewer CPU cores of system time). This is process system time, not total host kernel/softirq time or a throughput improvement. Firedancer busy-polls, so total CPU and system CPU must be interpreted separately.

| Metric | Prior same-host baseline | P4 zero-copy hour |
|---|---:|---:|
| Validator total CPU, core equivalents | 37.021 | 35.969 |
| Validator user CPU, core equivalents | 36.936 | 35.902 |
| Validator system CPU, core equivalents | 0.08518 | 0.06705 |
| Host system CPU, core equivalents | 0.10945 | 0.09807 |
| Host softirq CPU, core equivalents | 0.09444 | 0.04303 |
| Host IRQ CPU, core equivalents | 0.00000 | 0.00000 |
| Both-cgroup memory.current median, GiB | 90.717 | 28.663 |
| Host MemAvailable median, GiB | 217.808 | 396.756 |
| Data interface RX, MiB/s | 7.234 | 7.559 |
| Data interface TX, MiB/s | 8.079 | 8.321 |
| Data interface RX, packets/s | 21,681.2 | 23,279.6 |
| Data interface TX, packets/s | 24,470.4 | 25,115.2 |
| Linux interface RX drops | 0 | 0 |
| Linux interface RX errors | 0 | 0 |
| Data NVMe write, MiB/s | 1.325 | 2.953 |
| Data NVMe write IOPS | 12.074 | 25.380 |
| Data NVMe mean write await, ms | 0.825 | 1.932 |
| Data NVMe busy time, % | 0.459 | 0.645 |

Voting/replay: 361/361 caught-up observations; own public votes advanced from 459359665 to 459376094. Independent finalized-head versus local-root absolute lag: {'min': 0, 'median': 2, 'p95': 2, 'max': 6}. This is a different lag definition from the prior baseline's native replay-root distance; it is not a direct latency comparison. No leader skip-rate or voting-credit gain is inferred.

Observed nonzero active-port driver error/drop-related deltas: `{}`.

Application counters include gossip validity/age rejection, expired transactions and QUIC connection/key rejection; their complete reason-by-reason deltas are retained in the retained private comparison. The TX-ring-empty counter records polling observations and must not be presented as packet loss. Linux interface drops, checksum counters and application reason counters describe different layers; none alone establishes end-to-end packet loss. The P4 driver RX/TX success/completion counters remain in the JSON report.

This is a same-host comparison with matching collection categories, not an isolated causal test. The baseline used kernel 6.8.0-117, stock Ubuntu bnxt_en, an active-backup bond and generic XDP COPY. This run uses kernel 6.8.0-138, modified Broadcom 239.1.170.0, a standalone port, native AF_XDP zero-copy, the reviewed Firedancer pre-bind initialization patch and a different voting layout. Traffic, epoch/leader duties and cache history also differ. The new layout uses one net tile instead of two. Network workload changes must be considered alongside CPU changes; this does not establish Mellanox parity.

RAM: process RSS is not summed because shared mappings can be counted multiple times. The reserved hugepage pools changed from 88 × 1 GiB + 2,687 × 2 MiB to 87 × 1 GiB + 2,747 × 2 MiB. Cgroup memory.current, hugepage reservations and host MemAvailable are separate views and must not be added as independent physical allocations. Higher available RAM after different reboot/snapshot/cache history is not proof of equivalent validator memory savings. Cgroup memory.stat supports that distinction: median file memory changed from 86.843 to 26.881 GiB, while anonymous memory was nearly unchanged at 1.117 versus 1.091 GiB. These components overlap other memory views and are not extra allocations.

Coverage: the old guard lasted 3601.15 seconds; its interior hardware samples span 3593.21 seconds. Current hardware endpoints themselves span the full scored hour. Rates use each actual interval. The new collector retains all raw FD metrics and process/cgroup counters; periodic BPF attachment identity was not sampled. Runtime physical zero-copy was proven at startup, with service generation stable through scoring. Disk await is a mean, not a latency percentile.

Operational state: the pinned experimental driver and kernel 138 boot image, standalone network, resources and service setup are installed. The boot image's module payload was inspected, but this persistent voter has not been reboot-tested. Restart=no and fresh peer-fence/signed-history gates intentionally require controlled restart/reconciliation. Exceptional firmware/DMA cleanup remains unproven; no forced reset/unload or new firmware was used. A future failback must stop P4 and transfer its newest verified signed history before any X710 start.


Sanitized numeric data: [firedancer-voting-hour.json](firedancer-voting-hour.json). The full operational evidence is retained privately.
