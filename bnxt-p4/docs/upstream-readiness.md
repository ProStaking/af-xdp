# Upstream readiness assessment

Prepared 2026-11-01. Sanitized assessment based on the retained review. No publication, maintainer contact, submission, driver modification, or new experiment is authorized by this document.

The result supports a narrowly described engineering report and preparation of separate proposals. It does **not** make the vendor driver patch ready for upstream merge. The recorded trial sustained approximately 902.9 seconds of healthy unstaked replay and completed verified ordinary restoration. It did not establish catch-up, voting readiness, performance, or exceptional firmware/reset/device-loss DMA safety. Those limits belong in any eventual cover letter.

## Upstream applicability

On this review date, the browsed upstream `bnxt` [Makefile](https://raw.githubusercontent.com/torvalds/linux/master/drivers/net/ethernet/broadcom/bnxt/Makefile) lists `bnxt_xdp.o` but no `bnxt_xsk.o`. The corresponding `bnxt_xsk.c` URL returns 404. The inspected [bnxt_xdp.c](https://raw.githubusercontent.com/torvalds/linux/master/drivers/net/ethernet/broadcom/bnxt/bnxt_xdp.c), lines 433–445 in that response, dispatches `XDP_SETUP_PROG` and rejects other commands. Its XDP transmit path uses `xdp_frame` objects; that is not the vendor AF_XDP UMEM TX/completion implementation. These findings mean the vendor P4 change cannot be presented as a small upstream switch enabling an otherwise identical implementation.

This is a dated source comparison, not an immutable upstream baseline or a complete net-next audit. The web results expose moving `master` URLs, and the attempt to acquire an exact revision through the local network environment failed DNS resolution. Before preparing patches, obtain an exact net/net-next commit, inspect pending netdev work, and repeat the comparison against that revision. No claim is made that upstream maintainers have no unpublished or pending AF_XDP work.

| Component | Classification and route | Remaining work |
| --- | --- | --- |
| Vendor P4 AF_XDP pool activation, RX/TX/completion and steering | Feature work needing an upstream design/port, normally net-next | Establish the missing upstream foundation, review queue/resource/ownership design with maintainers, then port and test against an exact tree |
| Pool validation, failure unwind, TX reclamation, reopen ordering | Potential generally useful correctness ideas, not yet established upstream bugs | Demonstrate an equivalent defect on current upstream before claiming a fix or adding a `Fixes:` tag |
| `bnxt_compat.h` API alias | Vendor compatibility maintenance | Keep out of an upstream feature series unless a separate in-tree defect is demonstrated |
| Firedancer pre-bind FILL and disjoint UMEM partition | Independent userspace initialization change | Separate Firedancer proposal with configuration, ownership and regression tests |
| Site restoration, deadline, identity fences and hugepage allocation scripts | Lab operating procedure | Keep out of a general kernel/FD patch and do not export site defaults |

Local source comparison found changed common C/H files `bnxt.c`, `bnxt.h`, `bnxt_compat.h`, `bnxt_xdp.c`, `bnxt_xsk.c`, and `bnxt_xsk.h` between pristine vendor239 and `official-239/p4-experimental`. This list is not a complete release-manifest diff.

Concrete local anchors, relative to the retained vendor source root:

- `p4-experimental/bnxt_xsk.c:81–110`: P4 nTUPLE requirement, TruFlow refusal, additional-RSS-context refusal and exclusion of the AF_XDP queue from default RSS.
- `p4-experimental/bnxt_xsk.c:166–192`: running/XDP/state/ring checks, single-pool restriction, prefilled allocation requirement and DMA mapping.
- `p4-experimental/bnxt_xsk.c:194–205`: whole-device close/reopen and resulting pool/mode checks.
- `p4-experimental/bnxt_xsk.c:226–250`: ordinary disable closes before clearing/unmapping; exceptional reset/device loss is explicitly unqualified. Successful ordinary runs do not establish firmware drain on every failure path.
- `p4-experimental/bnxt_xsk.c:278–285`: chip/bitmap gate precedes setup. Removing only this gate is not a complete port.
- `p4-experimental/bnxt_compat.h:3313`: alias for the renamed network-lock compatibility assertion; a vendor portability concern rather than a new upstream AF_XDP facility.

Before a driver RFC, produce an upstream-native patch decomposition, a minimal AF_XDP reproducer independent of Firedancer, exact build/config/firmware identifiers, and a clearly bounded test matrix. Cover ordinary RX/TX/completion recycling, starvation/refill, bind failure/unwind, detach/reopen, resource exhaustion, steering changes, and regression behavior on already supported generations. Exceptional teardown needs a documented contract and evidence; an absence of observed faults is not proof. Do not combine speculative cleanup changes with feature enablement or describe source concerns as reproduced corruption.

## Vendor239 provenance and licensing evidence

The retained `official-239/PROVENANCE.md:3–17` records the [Broadcom P425G distribution page](https://www.broadcom.com/products/ethernet-connectivity/network-adapters/p425g), the [239 installer landing page](https://docs.broadcom.com/docs/NXE_Linux_Installer-239.1.170.0), source acquisition history, extraction precautions, and lack of a verified detached signature. This review read that record and independently recomputed all three following hashes:

| Retained artifact | SHA-256 |
| --- | --- |
| `bcm_239.1.170.0a.tar.gz` | `9e3d40259889e24ea3bbfa4f3ab2bd9e0dfc7df02fd38b3bd548385cf444f258` |
| `bnxt_en-1.10.3-239.1.170.0.tar.gz` | `87c51c315d783b19c7fe67e1326d7cd78500b88ad37a3bbfcfe3c9ceff728f53` |
| source `COPYING` | `8177f97513213526df2cf6184d8ff986c675afb514d4e68a404010521b880643` |

The source archive is the recorded bundle member `bcm_239.1.170.0a/drivers_linux/bnxt_en/bnxt_en-1.10.3-239.1.170.0.tar.gz`. Pristine `bnxt.c:1–10` retains Broadcom copyright and GPL redistribution/modification notices; `bnxt.c:178` declares `MODULE_LICENSE("GPL")`; `COPYING` contains GPL version 2. These are source provenance facts, not a blanket license determination for the complete installer, firmware, or unrelated bundled files. Preserve original notices and audit every contributed file. Do not assign a new SPDX identifier solely from a module-license string. No GPL implementation should be copied into Firedancer; its proposal must remain independently written userspace work under the project's applicable licensing rules.

## Submission route and human responsibility

Current [MAINTAINERS](https://raw.githubusercontent.com/torvalds/linux/master/MAINTAINERS), BNXT_EN entry, lists Michael Chan (`michael.chan@broadcom.com`), Pavan Chebbi (`pavan.chebbi@broadcom.com`), and `netdev@vger.kernel.org`. Re-run `scripts/get_maintainer.pl` on the eventual exact patch to collect all relevant reviewers and AF_XDP/core recipients. No messages were sent.

The current [networking process](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/process/maintainer-netdev.rst) routes networking development through netdev email. Use a reviewable emailed RFC series for the feature/design, not a generic PR to the Linux GitHub mirror. Existing upstream bug fixes belong in the appropriate `net` workflow; new features normally target `net-next`. Check tree status before sending and keep independently justified fixes separate. The [submission guide](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/process/submitting-patches.rst) requires a comprehensible problem statement and focused changes; prepare reproducible evidence and exact base identifiers before outreach.

**AI policy correction:** the current upstream [coding-assistants source](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/process/coding-assistants.rst) says AI agents must not add `Signed-off-by`; human contributors review the work, take responsibility, and certify the DCO themselves. Its current text no longer prescribes an `Assisted-by` tag. An older rendered kernel.org “latest” page retrieved during this review still included that prescription, so it must not be treated as current policy. Current [generated-content guidance](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/process/generated-content.rst) calls for transparent origin/tool-use information in cover letters and changelogs, and understanding and defending the submission. Disclose the substantial AI assistance here, including review and test generation, and recheck policy on the pinned submission tree. Do not manufacture human sign-offs or claim a mandatory current `Assisted-by` format.

## Separate Firedancer proposal and a possible TOML option

The present switch is **compile-time** `EXTRAS=p4-prebind`, defined by `p4-fd-integration/config/extra/with-p4-prebind.mk`. There is no implemented `bnxt_zero_copy=true` TOML option. In `src/disco/net/xdp/fd_xdp_tile.c:1190–1208`, the experimental build requires one standalone physical queue 0, explicit zero-copy and RX depth 1024, then reserves disjoint TX-free/cache/physical/loopback spans. Lines 1416–1435 skip a second physical bootstrap because the kernel may already have consumed the published entries. `src/waltz/xdp/fd_xsk.c:318–357` publishes before bind and checks `XDP_OPTIONS_ZEROCOPY` afterwards. Loopback remains separately provisioned COPY.

A default-false runtime option is feasible, but it is new implementation work. Prefer a mechanism-specific experimental name, such as `experimental_xsk_prebind_fill`, over `bnxt_zero_copy`: the latter suggests the option supplies driver zero-copy support and obscures the existing zero-copy mode setting. The exact section/name should follow FD maintainer conventions. It must propagate through TOML parsing, defaults, validation, topology and privileged/unprivileged initialization; replacing the preprocessor condition alone is insufficient.

Required semantics for an initial narrow option:

- Omission or false preserves the existing path and startup behavior. True requires explicit zero-copy and the currently qualified topology/geometry; incompatible COPY/auto/bond/multiple-tile configurations fail with a useful diagnostic before activation.
- Validate alignment, arithmetic, FILL capacity, UMEM bounds and disjoint ownership; reserve the same spans in both initialization stages and prohibit double publication.
- Capability advertisement or a driver name is preliminary information, not runtime proof. Require successful explicit zero-copy bind and the returned socket option; do not silently downgrade to COPY or retry another bind mode after partial activation.
- Do not auto-enable every `bnxt_en` device or infer P4 qualification from a generic driver string. A whitelist can express an experimental tested scope, but it cannot replace kernel validation.
- General pre-bind FILL may ultimately be preferable to a permanent vendor quirk. That requires testing other supported NICs and kernels, multiple queue/topology layouts, COPY, loopback, initial failure paths and shared-UMEM assumptions before changing the default.

Existing evidence includes default and opt-in full builds; primitive boundary tests; nine optimized and ASan/UBSan mocked actual-`fd_xsk_init` cases, including zero-count legacy behavior and loopback COPY (`p4-fd-integration-evidence/wiring/test_init.c`, `final-tests.log`); and the bounded P4 runtime trial. These do not cover a TOML parser/serialization path, cross-NIC runtime regressions, broad topology combinations, exceptional teardown, catch-up or voting. An earlier existing `test_xsk` runtime attempt was blocked by missing container NUMA sysfs, not a pass.

Recommendation: preserve this checkpoint and the exact tested artifacts. Prepare a separate, default-off Firedancer PR proposal with the existing tests plus the configuration/backward-compatibility matrix above. Prepare a vendor/upstream driver design report independently, then an upstream-native RFC only after pinning the target and filling its portability/ownership gaps. No additional live test, option implementation, submission, or publication is part of this checkpoint.
