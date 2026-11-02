# Native Intel X710: i40e experiment

Configuration, source, results and runbook for the native Intel experiment. The narrow fix has been submitted in the [PR discussion](https://github.com/firedancer-io/firedancer/pull/12540#issuecomment-6566903505) with [commit db6637e](https://github.com/DataKnox/firedancer/commit/db6637e708e24c54b331c7cdeabca0767c7169c9). Submission does not mean acceptance or merge. This is an experimental validation record, not a turnkey production package.

Two distinct builds were tested:

| Build | Evidence |
|---|---|
| PR12540 head `696316b2d4deea93565c12f4b7022fd5ff65d41e` plus semantic rule fix; binary `f08335e0a1dd9f20931ced20868f6cf83c8a287a5d2747727c2b44126a83a165` | 901.722 seconds caught-up unstaked native traffic; ordinary shutdown and AF_XDP restoration passed |
| v26.10.5 base `6286f99e400c1d5ac6f95b8cf36491555faa3726` plus eight Intel commits and semantic fix; binary `c28f3a3150d22bb7f4655a2123bd8754b62b9ea224f132c9288225a3f77f5531` | Exact build unstaked qualification and ordinary restart, then live promotion and 361-sample voting hour |

The voting hour does not qualify the unmodified upstream PR head. The PR-based build was not tested voting. DoubleZero and automatic boot/recovery remain unqualified.

See CONTRIBUTION.md, RESULTS.md, RUNBOOK.md and config.example.toml. The narrow submitted fix and complete experimental release backport are both included, with distinct provenance. See BUILD.md for the verified source reconstruction and local build recipe. Upstream-derived code retains Apache 2.0 licensing and notices; see LICENSE.upstream and NOTICE.upstream. Do not invent a human DCO/sign-off or claim maintainer acceptance.

## Package map

- `config.example.toml`: relevant tested release-layout settings with placeholders; not a complete portable deployment.
- `RUNBOOK.md`: ordered preparation, qualification and recovery outline, with mutating steps identified.
- `BUILD.md`: verified source reconstruction, build recipe and recorded limits.
- `RESULTS.md` and `experiment.json`: aggregate observations and machine-readable scope.
- `CONTRIBUTION.md` and `semantic-rule.patch`: submitted narrow correction and regression evidence.
- `PROVENANCE.md`, upstream notices and `MANIFEST.json`: source/licensing boundaries and checksums.

No automatic activation script, private logs, keys, addresses or host-specific identity guard is included. Read BUILD.md before attempting reconstruction of either measured binary.
