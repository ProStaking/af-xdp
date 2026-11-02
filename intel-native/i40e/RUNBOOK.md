# Reproduction and recovery draft

This is a reviewed workflow outline, not an unattended installer. Keep independent management and a known-good fallback. VFIO and hardware steering need a host-specific activation plan.

1. **Pin the build (local source changes).** Follow BUILD.md to select the PR-based or release-based track. For the tested release derivative, the supplied ordered series reconstructs all 3,661 manifested files and the container wrapper builds from clean output. Do not apply the separate root semantic patch again to this series. Preserve source, patch, toolchain and binary hashes. Run the five listed unit binaries on supported Linux; the documented Docker NUMA limitation prevents four from reaching their cases locally. Byte-identical binary reproduction is not claimed.
2. **Inventory and preserve recovery (read-only inspection).** Record kernel, i40e, firmware/NVM, PCI IDs, IOMMU groups, interfaces, filters, queues, offloads, addressing and routes. Verify management uses a separate NIC. The tested X710 had NVM 6.01/API 1.7 and kernel 7.0.0-42-generic. No firmware update or custom Intel kernel driver was needed.
3. **Prepare an unstaked configuration.** Use a separate identity and state directory. Merge `config.example.toml` into the required configuration for the selected release. Replace every placeholder. Preserve genesis, trusted snapshot sources, sandboxing and localhost RPC/metrics. Do not expose voting keys to the nonvoter.
4. **Calculate resources with the actual binary.** The release voting layout required 39 tiles, 78 × 1 GiB and 2,354 × 2 MiB pages. We reserved 79 × 1 GiB and 2,354 × 2 MiB, with 96 GiB memlock, 104 GiB MemoryMax and swap disabled for the service. These are hardware-specific values. The PR-based unstaked build had different requirements. Check migrated tile cgroups as well as the systemd supervisor when applicable.
5. **Configure the native path within the maintenance scope (mutating, maintenance required).** Stop only the target nonvoter normally and verify resources have been released. Create one VF on the selected PF. Require an exclusive IOMMU group; bind only that VF to vfio-pci, without bypassing IOMMU protection. Disable spoof checking only on that VF and keep trust disabled. Preserve PF addressing, MAC, routes and management. Use the candidate's configure-init/check path for exact destination UDP selectors; never bypass failed readback validation. The PR-based trial used ports 8001, 8003, 8004, 8005, 8701, 8702, 9001 and 9007. The release backport additionally enumerates 9006. Verify destination scope and port ownership before activation.
6. **Qualify unstaked first.** Verify that the iavf process owns VFIO descriptors, the physical NIC has no XDP attachment, native RX/TX completion counters advance, and the expected unstaked identity catches up against an independent RPC. Observe 15 healthy minutes. Perform an ordinary stop/restart with ownership checks. Service-active status and configuration text are insufficient proof.
7. **Coordinate voting separately (mutating, changes the active voter).** Keep the fallback synced on its unstaked identity. Demote the current voter before promoting the candidate, transfer and verify its latest signed Alpenglow history, and keep restart roles coherent. Private-key transfer is not part of this public workflow. Begin measurement only after own votes advance and replay is caught up.
8. **Measure a complete interval (read-only observation).** Sample CPU across all processes and disjoint cgroups, RAM/hugepages/pressure, NIC hardware and application counters, disk activity, voting and replay every ten seconds. Require a completion record and uninterrupted coverage. Preserve raw data and hashes. Exclude later configuration changes from the scored interval.
9. **Use ordinary rollback (mutating).** Before fallback voting, demote or fence the candidate and obtain its latest history. Never restore stale history. Stop native processes normally, verify VFIO ownership is gone, remove only owned filters/VF through normal configure-fini, restore saved PF settings and AF_XDP configuration, then verify a fresh bind and catch-up. Ambiguous DMA ownership requires reviewed recovery, not forced unload or reset.
10. **Close the release gaps.** Persistent VF/filter/resource ordering, boot identity guards, reboot recovery, failback and bounded log retention need separate implementation and testing. The tested native service remains runtime-only, with `Restart=no` and a fail-closed start gate. A successful hour does not establish production readiness.

## Service requirements

The tested resource settings were:

```ini
[Service]
LimitMEMLOCK=96G
MemoryMax=104G
MemorySwapMax=0
Restart=no
```

This is a resource fragment, not a complete unit. Preserve the existing Firedancer privilege-drop, sandbox/seccomp, identity checks and startup prerequisites. The host-specific guard and admin helpers are intentionally absent from this public draft. Do not treat it as a turnkey package or replace those controls with a stripped-down service.
