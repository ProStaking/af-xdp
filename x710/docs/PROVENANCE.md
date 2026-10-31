# Provenance and scope

The configurations, collector, summarizer, data and chart were copied from the reviewed, sanitized ProStaking X710 publication candidates. The runbook's long shell/Python/build/collection recipes are retained; only publication-status text and local package links were adjusted. The optional config editor is the same Python body extracted from that runbook with an explanatory docstring. The systemd fragment is extracted from the runbook; its example filename is new, its four directives are not.

Tested values and outcomes come from the experimental record. The published shell procedure is a reconstructed operator recipe, not a replay of private orchestration. Offline validation of snippets does not establish a successful live migration. Private handover/fencing/history validation helpers are intentionally absent.

Pinned upstream references (external, not vendored):

- https://github.com/firedancer-io/firedancer/tree/6286f99e400c1d5ac6f95b8cf36491555faa3726
- https://github.com/firedancer-io/firedancer/blob/6286f99e400c1d5ac6f95b8cf36491555faa3726/src/app/firedancer/config/default.toml
- https://github.com/firedancer-io/firedancer/blob/6286f99e400c1d5ac6f95b8cf36491555faa3726/src/app/shared/fd_auto_net.c

No upstream binaries, driver source, firmware, client code, private consensus files or native-path implementation work are distributed in this package. No Broadcom baseline is included. X710 A/B socket labels must not be reused for a separate generic-XDP-copy baseline.
