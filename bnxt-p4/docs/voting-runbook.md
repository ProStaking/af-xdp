# Voting checkpoint and reproduction procedure

Historical measured-hour procedure, prepared 1 November 2026. For the subsequent corrected driver and runtime-option source, use [corrected-source instructions](../build/corrected-source.md) and [the restart/live-handover follow-up](restart-fix-and-live-handover.md). The stop/start handover below documents the original hour, not the later live identity transition. This supplements the earlier bounded unstaked procedure. The trial controller is not a voting deployment tool.

Start with the [source reconstruction and build instructions](../build/README.md). Operators must supply reviewed fencing, signed-history verification, resource preparation and supervisor helpers. Those site-specific components are not distributed as portable executables.

## Tested hardware and software

- **NIC:** BCM57416, PCI `14e4:16d8`, revision 01. Firmware `220.0.59.0`, package `220.0.83.0`.
- **Server:** AMD EPYC 9254, 48 logical CPUs, approximately 503 GiB usable RAM.
- **Kernel:** Ubuntu `6.8.0-138-generic`.
- **Driver:** experimental `bnxt_en` version `1.10.3-p4xsk-239.1.170.0`.
- **Firedancer:** version 26.10.5, base commit `6286f99e400c1d5ac6f95b8cf36491555faa3726`, plus the initializer patches published in repository commit `cc41e8bfa24cf05d1ee306790da807165ec01744`.

Build with the documented `EXTRAS=p4-prebind` opt-in. There is no runtime `bnxt_zero_copy` TOML flag.

## Configuration and resources

The [complete measured TOML](../config/voting.example.toml) replaces private identifiers with `SITE` placeholders. It enables voting and block production, with one net tile, four shred tiles, a 200 million account limit and a 12 GiB account cache. Snapshot production is disabled; snapshot loading remains enabled. Keep an explicit snapshot allowlist and `allow_any=false`.

Reconcile the historical genesis, shred and checkpoint values with the current cluster before use. Do not copy them blindly.

The physical port used the following layout:

| Setting | Measured value |
|---|---|
| Topology | Standalone port |
| MTU | 1500 |
| AF_XDP physical queue | 0 |
| Combined channels | 48 |
| Ordinary RSS queues | 1–47 |
| Additional RSS contexts | None |
| Steering | n-tuple enabled; no TruFlow |
| Hardware RX/TX ring sizes | 511 |
| AF_XDP software queue depths | 1024 |
| Physical mode | Explicit `drv` and zero-copy |
| Loopback mode | Separate COPY path |

Hardware rings and AF_XDP software queues are different resources. The tested offload and IRQ preparation remains required. If resource admission fails, stop and investigate rather than disabling checks or silently selecting another layout.

The voting topology had **52 startup tiles**, with fixed tile CPUs **1–23, 25–28 and 30–40**. It used:

- **87 × 1 GiB and 2,747 × 2 MiB hugepages**, on dedicated hugetlbfs mounts with the corresponding page-size and `min_size` reservations.
- **104 GiB memlock**.
- **112 GiB MemoryMax** on both the service and the disjoint cgroup containing migrated tiles.
- A calculated locked-memory requirement of **99,240,873,984 bytes**.

Calculate requirements again with the final pinned binary and configuration. These values describe this experiment, not universal defaults. Keep independent management outside the experimental Broadcom path.

## 1. Verify the builds and recovery plan

Reconstruct both source trees using the manifest and build procedure. Pin the resulting artifacts and verify the exact kernel, vermagic, firmware, card and queue restrictions. Preserve the stock modules and boot image. Never substitute a different build under a recorded hash.

Source reconstruction has been verified. A fresh build of the dependency image and a portable deployment procedure have not been independently qualified.

Plan the site's standalone addressing, MAC and gateway changes and their inverse. Save the original bond, routes, RSS, offloads, IRQs, resources and recovery state. Replacing the module affects all Broadcom functions bound to it. Independent Intel management cannot recover a whole-kernel hang, and retained signing keys remain exposed to experimental kernel code.

## 2. Prepare state and the persistent service

Create every configured state directory under the intended runtime user, including `vote_history`. The earlier missing-directory startup failure is part of the test record. Reuse accounts, shreds or snapshot data only after the previous owner has stopped and is fenced. Keep vote history separate and current.

Install the reviewed persistent preparation, module/initrd and service configuration. The [service example](../config/voting.service.example) is documentary: its prepare unit and gate/checkpoint helpers must be supplied and reviewed. Do not remove missing helpers merely to make the template launch.

Keep Firedancer's normal privilege drop, sandbox and supervisor behavior. `Restart=no`, `SendSIGKILL=no` and controlled reconciliation are deliberate parts of this setup.

## 3. Prepare networking and access controls

Persist only the tested network, offload, IRQ and resource settings, including loopback `accept_local=1` and `route_localnet=1`. Preserve management connectivity and existing access restrictions.

Redirected validator UDP bypasses ordinary firewall processing. Stock GRE selection and downstream tunnel validation are separate mechanisms. Keep RPC port **8899** and metrics port **7999** bound to localhost. DoubleZero was neither configured nor validated.

## 4. Transfer voting authority without overlap

Verify the other validator's identity and voting role. Stop it normally, prevent automatic or external restart, and establish that no other replica can vote. Preserve its zero-copy-ready configuration for a possible controlled failback.

If the target already holds the correct identity, transfer only the latest signed Alpenglow history over an authenticated encrypted channel. Verify the canonical signature, identity, freshness and minimum wait boundary before activation. This package does not provide key migration or a universal consensus-history verifier.

Start P4 only after the exclusivity, history, configuration and artifact-pin checks pass.

## 5. Establish catch-up and runtime proof

Obtain a fresh, matching full and incremental snapshot pair from explicitly trusted sources on the compatible cluster. Preserve genesis and integrity validation.

Before measuring, verify all of the following:

- Physical `XDP_OPTIONS_ZEROCOPY` runtime proof.
- The expected local identity.
- Independently observed advancement of the validator's own public votes.
- Cluster catch-up.

An active service alone does not establish these conditions.

## 6. Measure a full stable hour

Keep startup and snapshot loading outside the scored interval. This run required **five consecutive observations at 10-second intervals** with caught-up status, absolute independent finalized-head/local-root lag of **at most 32 slots**, advancing own votes, stable process/boot/configuration generation and no collection errors. Only then did the full **3,600-second** interval begin.

Capture both disjoint cgroup roots and all tile processes. Service-only accounting misses migrated tiles. Record:

- Per-core CPU, system and softirq time.
- Memory, pressure and hugepage usage.
- NIC and application counters.
- Both disks' throughput, IOPS, mean await and busy time.
- Public votes and replay progress.

Retain immutable endpoints, hashes and sampling gaps. A checksum-only diagnostic increase is not, by itself, proof of lost validator traffic. A genuine kernel, identity or resource fault requires normal stop and fencing. Ambiguous DMA ownership does not authorize forced termination or module unloading.

## 7. Preserve the selected voter and safe failback

After a successful hour, leave the selected P4 voter running, the previous voter fenced and monitoring active.

A later failback must first stop P4 and transfer its newest verified history back. Never restart the previous node with stale history.

The persistent module and initrd contents were inspected, but this voting deployment has **not undergone a reboot test**. It is not qualified for unattended high availability.

## Observed outcome and limits

The hour from **16:48:04 to 17:48:04 UTC** passed with **361 caught-up observations**, no collection errors and advancing votes. See the [measured results](../results/voting-hour.md).

Earlier ordinary unstaked restoration and attach/detach qualification also succeeded. Those results do not prove exceptional reset, device-loss or firmware cleanup. They establish neither throughput gains, leader skip-rate improvement, mainnet readiness nor Mellanox parity. Kernel, layout, topology, workload and cache differences limit causal interpretation of the CPU comparison.
