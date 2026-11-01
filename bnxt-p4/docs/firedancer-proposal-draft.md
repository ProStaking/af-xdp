# Proposal draft: opt-in pre-bind AF_XDP receive-buffer publication

DESIGN DRAFT. No PR submitted; no new TOML option implemented.

## Problem and demonstrated result

Our experimental BCM57416 vendor239 driver requires available FILL entries when the AF_XDP pool is bound. The tested Firedancer26.10.5 path binds before its later receive-buffer bootstrap. A separately compiled userspace adaptation publishes a validated, disjoint receive span before bind, reserves the physical/loopback/TX ownership partitions consistently, and prevents a second bootstrap from republishing frames already available to the kernel. It retains explicit zero-copy verification and the normal supervisor/sandbox.

Separate userspace harnesses qualified bounded RX/TX behavior first. The opt-in Firedancer build then completed healthy unstaked replay and subsequently one caught-up testnet voting hour. This is evidence for the narrow integration, not general cross-NIC or exceptional teardown qualification. Existing source/build/license/tests are in the bnxt-p4 repository directory. No GPL driver implementation is copied into Firedancer.

## Current applicability check

Inspected official main at commit **300acc6fdcce505957d828bdcf9bc070b78cd9ce** on2026-11-01:

- [fd_xsk.c](https://github.com/firedancer-io/firedancer/blob/300acc6fdcce505957d828bdcf9bc070b78cd9ce/src/waltz/xdp/fd_xsk.c), setup/mmap then bind around lines306–329: no pre-bind FILL publication in the inspected path.
- [fd_xdp_tile.c](https://github.com/firedancer-io/firedancer/blob/300acc6fdcce505957d828bdcf9bc070b78cd9ce/src/disco/net/xdp/fd_xdp_tile.c): initialization calls near1200/1228, later bootstrap near1383. The upstream code has evolved beyond the tested release; the existing release patch is not claimed to apply cleanly.
- [default.toml](https://github.com/firedancer-io/firedancer/blob/300acc6fdcce505957d828bdcf9bc070b78cd9ce/src/app/firedancer/config/default.toml) contains neither our compile-time switch nor a supported bnxt_zero_copy option. Inspection does not exclude related open/unmerged work.

## Proposed interface

Discuss a default-false `[net.xdp] experimental_xsk_prebind_fill` boolean (name provisional) rather than `bnxt_zero_copy`. It controls initializer behavior, not driver support. Current shipped experiment remains **EXTRAS=p4-prebind**; do not put the proposed option in operational TOML yet.

Omitted/false must preserve the ordinary path. True initially requires explicit zero-copy, one qualified standalone physical queue0 and tested RX geometry; invalid COPY/auto/bond/multi-tile cases should fail before resources are activated. Propagate through defaults, parsing, validation, topology and both initialization stages. Maintain aligned bounded UMEM spans, overflow checks, release publication, disjoint loopback/TX ownership and no double publication. Runtime XDP_OPTIONS_ZEROCOPY proof remains mandatory; no silent COPY fallback after partial activation. Avoid auto-enabling by bnxt_en driver string or assuming all P4/P5 models share the contract.

A generic always-prebind improvement is an alternative only after supported-driver/kernel and topology regressions justify it. Capability detection alone does not prove the required lifetime or buffer-ownership semantics. Maintainer guidance should decide whether a temporary experimental option belongs upstream.

## Required work before a reviewable PR

Rebase the small userspace adaptation onto the chosen current commit; implement the option and parser/default/serialization tests; test disabled behavior, invalid configurations, zero-count legacy behavior, arithmetic/alignment/bounds, bind failure and unchanged loopback COPY; preserve tested disjoint ownership and runtime proof. Existing nine mocked initializer cases and sanitizer runs are useful but do not exercise a new TOML path. Full default/opt-in builds must pass on the rebased tree. Add supported cross-NIC/kernel runtime regression coverage, including the current ordinary X710 path, before any default change.

Do not replace normal supervision or loosen sandboxing to hide candidate driver cleanup uncertainty. Document which exceptional reset/device-loss paths remain unqualified. The measured CPU reductions are not justification for changing default semantics: topology/kernel/layout also changed. This draft requests design feedback; it is not a merge-ready implementation or an assertion of an upstream bug.
