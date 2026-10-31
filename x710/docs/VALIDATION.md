# Validation record

- Both TOML reference files parse successfully.
- Python scripts parse successfully.
- All corrected Bash recipe blocks pass bash -n (syntax only).
- Extracted config editor passed two offline sanitized cases: omitted listen_gre and an existing explicit false value. The editor's structural-equality assertion enforces only intended network changes.
- Collector and summarizer bodies match the reviewed source; publication adds only MIT attribution headers. They were not run against a validator during packaging.
- No live service, NIC, sysctl, consensus-state or baseline changes were performed.
- No credentials, credential locators, private keys/history, private management endpoints or user workspace paths were found by the scoped text review. Explicit IPv4 addresses in configs are loopback and RFC 5737 documentation addresses; version/firmware values are not endpoints.
- Packaging validation did not change any live host. Repository publication is a separate operation.

Limits: reconstructed build recipe and host-changing shell workflow have not been clean-room executed. The collector's earlier experimental smoke test is documented in the runbook, not repeated here. Runtime forced-zero-copy and voting proof are reported from the experiment record, not independently rerun by this packaging review.


## Collector coverage prerequisite

The portable collector reads one selected service cgroup. Before measuring, confirm ALL validator tiles are in that cgroup. Tiles moved into another cgroup will be omitted and the CPU/resource totals will be incomplete. The measured X710 layout satisfied this prerequisite. Multi-cgroup layouts need a separately reviewed collector.
