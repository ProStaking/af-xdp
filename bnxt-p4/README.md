# Experimental Broadcom P4 AF_XDP support

An opt-in bnxt_en driver candidate and a separate Firedancer pre-bind initialization patch ran **902.903 seconds of healthy unstaked replay** on BCM57416. Physical queue 0 used runtime-confirmed zero-copy; loopback used COPY. The host was restored to its stock driver/network on 2026-11-01 at 15:40:57 UTC.

The node **did not catch up** to the cluster. This is not voting validation, a performance comparison or exceptional DMA-recovery qualification. This is a **source-and-manual reproduction package**, with verified code reconstruction and reference configuration. It is not a drop-in deployment kit: the measured site launch/guard/deadline/restoration helpers are not supplied. The original private build images also had pre-provisioned dependencies; clean dependency/image provisioning has not been independently reproduced. See the precise deployment gaps in the runbook before any activation.

1. Read [provenance](PROVENANCE.md) and [license map](LICENSE-MAP.md).
2. Reconstruct source using [build instructions](build/README.md). Driver patches and Firedancer patches are separate components; both are required for this experiment.
3. Review the [configuration](config/unstaked.example.toml), [layout](config/layout.md), [service record](config/service.example) and [operator procedure](docs/runbook.md).
4. Review [fresh snapshot preparation](docs/snapshot-preparation.md) before a later catch-up/voting stage.
5. Read [verification](docs/verification.md), [rollback](docs/rollback.md), [limits](docs/limitations.md) and [results](results/README.md) before considering hardware work.

Test tuple: BCM57416 PCI 14e4:16d8 revision 01, firmware 220.0.59.0/pkg 220.0.83.0, Ubuntu kernel 6.8.0-138-generic, AMD EPYC 9254/48 logical CPUs/~503 GiB usable RAM, MTU 1500, hardware RX/TX rings 511. Experimental driver 1.10.3-p4xsk-239.1.170.0. Firedancer v26.10.5 plus the supplied patches.

No firmware, vendor installer, credentials, host-specific handover helpers or executable binaries are distributed here. `SITE_*`, `/SITE/...`, and 192.0.2.10 are placeholders. Cluster checkpoint/shred values are historical as-run values and must be reconciled with the operator's current cluster. Nothing here should start a second voter.

Future work: [upstream assessment](docs/upstream-readiness.md) separates the vendor driver feature port from the independent FD initializer proposal; [conditional voting plan](docs/future-voting-stage.md) is not an executed result. No runtime TOML prebind option has been implemented; current opt-in remains compile-time.
