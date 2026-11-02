# Completed voting results

These are sequential testnet observations on the same X710/7950X. The native interval ran from 2026-11-01 23:48:04.394801 to 2026-11-02 00:48:04.394811 UTC: 361 clean samples over 3,600 seconds, all caught up. Public votes advanced 16,484 slots. Independent slot lag was median/p95 two slots, maximum six.

| Metric | AF_XDP zero-copy | Native Intel |
|---|---:|---:|
| Total validator CPU, cores | 28.006571 | 28.008631 |
| Validator system CPU, cores | 0.026103 | 0.003480 |
| Whole-host softirq CPU, cores | 0.016433 | 0.001000 |
| Hardware RX packets/sec | 21,691 | 23,297 |
| Hardware TX packets/sec | 24,484 | 25,079 |
| Median cgroup RAM, GiB | 97.737 | 101.375 |
| Disk writes, MiB/sec | 2.027 | 1.759 |
| Disk write await, ms | 15.989 | 1.164 |

Validator system time was 86.67% lower, saving 0.02262 cores. Total CPU was essentially unchanged. Whole-host softirq time was 93.91% lower; this is a different accounting scope and must not be added to process system time.

Native counters recorded 83,844,400 received packets and 90,266,276 TX completions. IAVF drop counters and hardware error/discard counters did not increase. Linux interface drop counters did increase, so this is not a zero-packet-loss claim. Linux PF counters exclude most VF traffic; use hardware port and application counters together. Protocol rejection counters are also distinct from NIC loss.

Observed replay work was 13.37% higher and wire RX packet rate 7.40% higher. Different epochs, packet mix, cache state, build/compiler and 39-versus-38 configured tiles prevent isolating causality. Native adds an idle socket tile alongside iavf in place of net; netlnk exists in both. Lower disk await is an observation, not a demonstrated NIC effect. Network latency, end-to-end transaction latency and maximum capacity were not measured. There is no Mellanox parity or DoubleZero claim.

RAM included 82.598 GiB of hugepage charge and growing file cache; do not add hugepages twice. Peak charge reached 103.230 GiB against a 104 GiB limit without limit/OOM events. It warrants monitoring, not an automatic limit increase. This hour does not qualify automatic boot/recovery. Subsequent CVE mitigation at 00:50:48.350309949 UTC is outside the scored data.
