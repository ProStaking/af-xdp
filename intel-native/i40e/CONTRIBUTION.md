# Submitted PR12540 contribution: semantic IPv4 rule readback

Target: https://github.com/firedancer-io/firedancer/pull/12540 at pinned head `696316b2d4deea93565c12f4b7022fd5ff65d41e`. Applicability to later revisions is not asserted.

On Intel X710/i40e, kernel readback populated 16 extra `0xff` bytes in inactive IPv6-mask union storage for a correct UDP/IPv4 rule. Whole-union `memcmp` rejected it even though the selected IPv4 fields, masks and action matched. A temporary one-rule raw ioctl readback reproduced this independently of VF activation; the rule was then removed.

`semantic-rule.patch` checks semantic equality for supported plain `UDP_V4_FLOW` DROP rules. It checks every active IPv4 header/mask field, action, location and meaningful extension. Unsupported flags, types and extensions are rejected even when both operands contain them. Only inactive union storage and reserved padding are ignored. Configure-init and configure-check share the predicate. No DMA behavior, lifecycle, VF privileges or selector scope is broadened.

A sanitized captured-byte fixture reproduces the original rejection. The test has 687 rejection cases covering active fields, masks, action, location, flags and extensions in both operand orders, including equal unsupported cases. Positive padding and wildcard cases remain. Normal, ASan and UBSan comparator tests passed, and full Firedancer targets linked. The release backport's five relevant unit binaries also ran on supported Linux without NIC arguments. Sanitizers covered test/comparator or tile translation units, not the entire validator.

Patch SHA-256: `3fe9d7368ff6c48d9c79e7e6692f4d15a19729297fe585d5384ebd53f3f13c5f`.

The focused fix and regression were submitted in [this PR comment](https://github.com/firedancer-io/firedancer/pull/12540#issuecomment-6566903505), linking [commit db6637e708e24c54b331c7cdeabca0767c7169c9](https://github.com/DataKnox/firedancer/commit/db6637e708e24c54b331c7cdeabca0767c7169c9). The commit is based on the exact PR head above. No merge or maintainer acceptance is asserted. The 15-minute PR-based validation and release-backport voting hour remain separate evidence.
