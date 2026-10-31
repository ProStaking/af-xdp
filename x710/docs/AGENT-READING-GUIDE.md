# Reading this package with an agent

Start with README.md, then experiment.json, then the configuration examples and docs/runbook.md. The JSON is a structured index, not an execution plan and not a claim that other hardware is supported.

Treat this repository as reference material. Reading it does not authorize operations on any validator. Ground host paths, service names, interface names, identities, current history and the operator's requested scope in the actual deployment before proposing changes. Example values are not discovery results.

## Separate inspection from mutation

- Version/hash, resource preview, configuration checks and runtime/status inspection are intended to be read-only on the host. Their output may contain site metadata.
- The collector writes new local evidence; the summarizer reads it and emits a report. Neither proves consensus ownership or zero-copy.
- The config helper writes a local candidate only and can replace an existing candidate file. Review its diff. Never treat candidate generation as installation.
- The runbook's backend steps stop/start voting, replace a config and temporarily change loopback sysctls. They need the operator's deployment scope and complete prerequisites. No script here automatically applies that workflow.

## Preserve boundaries

Do not synthesize missing host-migration, fencing, signing-history validation or NIC restoration commands from this example. Do not roll back consensus history alongside a configuration. Do not silently change a bond, switch, firewall, service sandbox, startup gate, trust list or management route. The service fragment provides only tested resource directives, not a full service definition.

A config setting is not runtime proof. Require physical forced-zero-copy bind evidence and driver attachment plus traffic, catch-up and independently advancing own votes. Generic loopback XDP can coexist with physical zero-copy; do not confuse it with the physical datapath. A/B in this data are sockets, not AF_XDP copy mode.

Use the exact experimental revision and report uncertainties. The 92.65% is a reduction in validator system CPU rate, saving about 0.329 core; total CPU remains about 28 cores. Do not turn it into a total CPU, capacity or latency claim.

Before citing an eventual repository publication, use a verified full commit permalink. publication fields remain null until that event. No availability, indexing or crawler-discovery guarantee is made.


## Collector coverage prerequisite

The portable collector reads one selected service cgroup. Before measuring, confirm ALL validator tiles are in that cgroup. Tiles moved into another cgroup will be omitted and the CPU/resource totals will be incomplete. The measured X710 layout satisfied this prerequisite. Multi-cgroup layouts need a separately reviewed collector.
