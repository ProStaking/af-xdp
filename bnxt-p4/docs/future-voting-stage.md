# Historical voting plan, now followed by a completed trial

The voting hour subsequently completed on2026-11-01; see [results](../results/voting-hour.md) and [voting runbook](voting-runbook.md). The plan below is retained as historical scope, not an instruction to perform another handover. P4 was left voting and X710 stopped with zero-copy preserved.

# Conditional P4 voting/performance stage — not executed

Conditional sequence: completed unstaked trial and stock restoration; documentation/package plus upstream assessment; then a separately coordinated single-voter handover and full one-hour whole-system/voting capture. If that hour passes, leave P4 as the voting node and use the existing voter as the IntelPR12540 lab. This is a plan, not evidence those later stages occurred.

## Before moving voting

- Use a fresh trusted testnet snapshot and prove cluster catch-up on the separate unstaked P4 identity. The completed 902.9-second test showed advancing replay, not catch-up. Preserve the existing voter as sole voter during preparation.
- Freeze exact driver/FD source and binary pins, topology and service configuration. Recalculate the *voting* topology's memory and CPU requirements with the actual opt-in binary; do not reuse unstaked80/2083 counts by assumption. Preserve normal seccomp/no-new-privileges, source-key exclusion for the nonvoter, localhostRPC/metrics and independent management.
- Specify persistent standalone addressing, driver availability for exact kernel, boot ordering, bnxt_re exclusion, queue/RSS/offload/IRQ settings and required loopback sysctls before treating the node as long-lived. The current experiment installed no persistent driver and all transient units were removed. A persistent voting service needs its own reviewed config/pins and single-voter start gate, not the expired experiment token.
- Retain a recoverable stock driver/network configuration. No forced unload/reset after uncertain DMA. An ordinary reboot/on-site recovery may still be required on exceptional failures; a fifteen-minute ordinary run does not qualify these paths.

## Serialized handover

Stop and fence the existing voter voting first, prevent unexpected restart and verify its processes are gone. Stop the P4 nonvoter before activating its voter. Transfer only the latest final signed Alpenglow vote-history state by the existing pinned encrypted path; verify identity, signature, monotonic/current state and any required wait boundary before activation. Resolve the target signing-key custody explicitly; any old target history is stale and must not be used. Do not print keys or copy withdrawal/mainnet identities. Revalidate same cluster/protocol/build compatibility and sole-owner state immediately before start. If ownership or history is uncertain, keep both voters stopped.

Failback is the same serialized operation in reverse, carrying the newest signed history back. Never automatically restart the existing voter on its stale history. The temporary trial's unconditional stop timer is not an appropriate unattended failback mechanism for a voting identity.

## Measurement and success criteria

Begin the scored sixty minutes only after correct identity, ongoing own-vote activity and cluster catch-up are verified. Keep startup/snapshot catch-up outside the scored interval. Reuse ten-second CPU/per-core/system/softirq, RAM/cgroup/hugepage/pressure, NIC/application/error and diskIOPS/throughput/latency/utilization sampling, plus voting/replay/participation/skips, with exact metric availability recorded. Record network load, cluster/epoch context, software and configuration differences.

Compare against the prior same-host Broadcom bonded generic-XDP COPY baseline, explicitly noting standalone topology, FD initializer, layout/resource and workload differences. If those differ materially, label the comparison observational and schedule a matched same-host control rather than attributing every change to zero-copy. Cross-host the existing voter/Broadcom comparisons remain hardware-confounded. Busy polling can keep total CPU high even when system time falls; report absolute system/softirq costs and useful work, not a percentage headline alone.

On success preserve P4 as sole voter, retire only the measurement/recovery controls whose expiry would wrongly stop it, and verify persistent boot/recovery behavior separately. Keep the existing voter voting fenced while it becomes the IntelPR12540 lab. Do not begin Intel hardware changes until that role transition is verified. No external upstream submission is part of this handover.

## Exact ordinary stop and measurement accounting

The completed run received SIGTERM at **2026-11-01 15:38:28.020624 UTC**. Systemd recorded successful deactivation at **15:38:28.043563 UTC** and stopped at **15:38:28.043924 UTC**. The guard’s continuous healthy span was **902.902646894 seconds**; stock restoration completed later at **15:40:57.926541 UTC**. These are distinct events.

Systemd reported **16 minutes 42.379 seconds of service CPU time**, but fixed Firedancer tiles migrate into a sibling cpuset cgroup. That figure and the service’s MemoryCurrent are **not total Firedancer CPU or RAM**. A later performance comparison must collect host/per-core counters, every Firedancer process and both the service and migrated-tile cgroups, accounting for overlap rather than summing duplicate counters. The migrated cpuset’s separate **104 GiB memory cap** was verified. This functional trial does not supply a matched performance result.
