# Provenance

This repository packages the reviewed ProStaking experiment artifacts. Per-experiment provenance identifies source versions, artifact categories and verification limits. See [X710 provenance](x710/docs/PROVENANCE.md).

The X710 package contains experiment-specific helpers/configuration examples and experimental observations; upstream client implementations, drivers, firmware and binaries are not vendored. Upstream references remain pinned in the experiment documentation. No private host-handover, credential, fencing or signed-history material is included.

The reconstructed operator/build recipes must not be confused with private lab orchestration or a clean-room replay. Later experiments need their own evidence, review and provenance; they must not inherit another hardware result.

For X710, the originating experiment worker confirmed that the helpers, config-edit block, prose and measurement analysis were created for this project, without copied upstream implementation. Configuration examples use upstream option names and tested operator values; charts are generated outputs. This is a work-record/inspection confirmation, not an exhaustive similarity scan. Inherited base-service authorship has the qualification in LICENSE.md.

Pinned upstream Firedancer is Apache-2.0 unless otherwise noted; retain its [LICENSE](https://github.com/firedancer-io/firedancer/blob/6286f99e400c1d5ac6f95b8cf36491555faa3726/LICENSE) and [NOTICE](https://github.com/firedancer-io/firedancer/blob/6286f99e400c1d5ac6f95b8cf36491555faa3726/NOTICE) boundaries if adding upstream material. The X710 package links upstream and does not redistribute its implementation. The separately licensed P4 patch material does redistribute derivative source changes; its component notices and licenses are included.

## Broadcom P4 experiment

See [P4 provenance](bnxt-p4/PROVENANCE.md), [source reconstruction](bnxt-p4/results/source-reconstruction.json), and [bounded result](bnxt-p4/results/firedancer-unstaked.json). This addition includes verified source patches, not driver/validator binaries or a vendor installer. It establishes sustained advancing unstaked replay, not catch-up, voting readiness or performance improvement.
