# Evidence needed

Require actual `XDP_OPTIONS_ZEROCOPY` on physical queue 0, explicit zero-copy config, native attachment,1024 FILL entries published before bind, separate loopback COPY and correct unfunded identity with empty vote account. A service-active flag or config value alone is insufficient. The opt-in FD emits runtime confirmation after getsockopt; correlate it with the current invocation, binary hash and socket/interface.

Record steady replay progress, packet activity, resources/driver/kernel health and continuous health duration. Catch-up is separate: this run progressed but was not caught up. Use final pre-stop live counters and their timestamps. Post-detach driver counters reset; zero afterward is not proof of zero traffic or errors. FD metrics and driver samples have different timings/coverage and must not be subtracted as a packet-loss estimate.

Completed result is 902.902646894 seconds healthy replay plus verified stock restoration. Last FD counters: RX 42,634,070; TX submitted 58,915,953; invalid descriptors/ring-full/FILL-stall 0; TX no_neighbor 1. Last driver sample: RXsuccess 19,101,217; TXsent 27,556,950; TXcompleted 27,556,948; alloc/no-room/redirect/ring-full 0. Two outstanding submissions in that earlier sample are not by themselves proof of loss or failed completion. The later normal-stop receipt establishes ordinary cleanup, not all exceptional DMA paths.

## Exact ordinary stop and measurement accounting

The completed run received SIGTERM at **2026-11-01 15:38:28.020624 UTC**. Systemd recorded successful deactivation at **15:38:28.043563 UTC** and stopped at **15:38:28.043924 UTC**. The guard’s continuous healthy span was **902.902646894 seconds**; stock restoration completed later at **15:40:57.926541 UTC**. These are distinct events.

Systemd reported **16 minutes 42.379 seconds of service CPU time**, but fixed Firedancer tiles migrate into a sibling cpuset cgroup. That figure and the service’s MemoryCurrent are **not total Firedancer CPU or RAM**. A later performance comparison must collect host/per-core counters, every Firedancer process and both the service and migrated-tile cgroups, accounting for overlap rather than summing duplicate counters. The migrated cpuset’s separate **104 GiB memory cap** was verified. This functional trial does not supply a matched performance result.
