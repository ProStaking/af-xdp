# Experimental Broadcom P4 AF_XDP support

An experimental BCM57416 driver and a separate Firedancer initialization patch completed a **full caught-up voting hour** on Solana testnet on 1 November 2026. P4 remained the sole voter afterward. The complete configuration used **1.052 fewer CPU cores on average**, from37.021 to35.969, while changing from two net tiles to one. This is a measured configuration result, not an isolated zero-copy efficiency claim.

The original performance hour and later corrected restart/live-handover validation are separate checkpoints. The driver correction fixes the observed 525-versus-511 startup rejection; it does not establish exceptional DMA recovery. See [the follow-up](docs/restart-fix-and-live-handover.md).

## Operator configuration

Start with the [final voting TOML](config/voting.example.toml), [service record](config/voting.service.example) and [ordered voting runbook](docs/voting-runbook.md). The examples replace site identifiers with placeholders. The service requires operator-supplied preparation, fencing and signed-history helpers; it is not a turnkey installation kit.

The earlier [unstaked configuration](config/unstaked.example.toml), [layout](config/layout.md) and [bounded procedure](docs/runbook.md) remain historical records of the preceding902.903-second trial. That trial advanced replay without catching up; the later voting hour is separate evidence with fresh trusted snapshots.

## Source, builds and evidence

1. Review [provenance](PROVENANCE.md) and the [license map](LICENSE-MAP.md).
2. Reconstruct both source components using [build instructions](build/README.md). The driver and Firedancer patches are both required. The measured hour used compile-time `EXTRAS=p4-prebind`. The corrected candidate instead uses the default-off runtime option `net.xdp.experimental_prebind_fill = true`; see [corrected-source instructions](build/corrected-source.md). Do not combine these alternative Firedancer patch sequences.
3. Read the [voting results](results/voting-hour.md), [sanitized data](results/firedancer-voting-hour.json), [verification](docs/verification.md), [rollback](docs/rollback.md) and [limits](docs/limitations.md).
4. Review [snapshot preparation](docs/snapshot-preparation.md) and the voting runbook's single-voter handover requirements before activation.

Tested tuple: BCM57416 PCI14e4:16d8 revision01, firmware220.0.59.0/pkg220.0.83.0, kernel6.8.0-138-generic, EPYC9254/48logical CPUs/~503GiB usable RAM, MTU1500, hardwareRX/TXrings511. Driver1.10.3-p4xsk-239.1.170.0. Firedancer26.10.5 plus the supplied patches. Voting resources differ from unstaked resources; see the final runbook.

No binaries, firmware, vendor installer, credentials or private host-control helpers are distributed. Source reconstruction is verified; clean dependency-image provisioning and portable deployment are not independently qualified. Historical cluster checkpoints must be reconciled with the operator's current cluster.

## Remaining limits and proposals

Persistent voter reboot and exceptional firmware/reset/device-loss DMA cleanup remain unqualified. The known MAC/ntuple steering limitation remains. DoubleZero was not validated. Do not force teardown of ambiguous DMA ownership or restart a previous voter with stale history.

[Upstream assessment](docs/upstream-readiness.md) separates a proposed [default-off Firedancer option](docs/firedancer-proposal-draft.md) from the [Broadcom/netdev feature port](docs/broadcom-netdev-proposal-draft.md). These are design drafts, not submitted or merge-ready patches. Publishing this evidence does not establish general hardware support, mainnet readiness or Mellanox parity.
