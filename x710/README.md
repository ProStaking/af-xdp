# ProStaking: Intel X710 AF_XDP zero-copy experiment

Companion package for the ProStaking X710 experiment. The article will cite a fixed repository revision.

This package documents a stock Intel X710 with Firedancer 26.10.5, commit `6286f99e400c1d5ac6f95b8cf36491555faa3726`, on Ubuntu 26.04.1 / kernel 7.0.0-42-generic, using a Ryzen 7950X and 128 GB RAM. It is one testnet observation, not a universal setup or performance guarantee.

## Start with the final settings

- [XDP reference TOML](configs/voting-xdp.example.toml): complete sanitized reference layout, with placeholders; omitted keys use pinned defaults. Preserve extra settings in your working config.
- [Socket reference TOML](configs/voting-socket.example.toml): the original bonded baseline. A standalone control must use the already-verified standalone interface instead of bond0.
- [systemd resource drop-in example](configs/60-x710-resources.conf.example): tested resource values, not a full service. The filename is an operator example. Preserve existing ExecStart, history gates and sandbox.
- [Loopback runtime values](configs/loopback-runtime-values.txt): temporary settings, not a persistent sysctl file.
- [Full runbook and rollback](docs/runbook.md): preserves the longer config-editing, stop/apply/restore, collection, summarization and reconstructed build snippets.

The executable recipe starts from an already-working sole voter on a dedicated standalone port, with independent management and sufficient reserved resources. Identity migration, bond conversion, NIC queue/RSS/offload preparation, resource boot provisioning and recovery services are site-specific prerequisites. It changes config and loopback values only, then restores those same settings. Never restore stale vote history when reverting a backend.

## For agents and automated readers

[experiment.json](experiment.json) records the tested configuration, prerequisites, operation effects, runtime proof, rollback boundaries and limitations. Read [the agent reading guide](docs/AGENT-READING-GUIDE.md) before treating any example as a proposed action. There is no unattended installer.

## Full measured configuration record

[Measured TOML, effective service and preparation dependencies](docs/MEASURED-CONFIG-AND-SERVICE.md) distinguish root bootstrap from Firedancer runtime isolation, and exclude the history prestart helper added only after C completed. [Measured service example](configs/measured-service.service.example) and [exact voting drop-in](configs/measured-voting-drop-in.conf.example) include non-operational site dependencies, not runnable replacements. [Measured TOML](configs/measured-xdp.toml) preserves non-site values. The earlier resource fragment remains a selected-settings example.

## Optional helpers

`python3 scripts/make_xdp_config.py` creates a candidate only. Set STATE to a private directory containing a protected copy named socket.toml, and IFACE to that config's existing standalone interface. The helper rejects another provider/interface and asserts the parsed candidate has only the intended network changes. Review the diff; it does not install, stop, start or configure any service.

`collect_system.py` and `summarize_system.py` are retained verbatim from the reviewed public source. Run the examples in docs/runbook.md from scripts/. The collector reads Linux procfs/sysfs/systemd/ethtool and creates a new private output directory; it is not a safety watchdog. It does not prove own voting or zero-copy. Inspect new captures before sharing; labels and host metadata can require redaction.

The multi-step shell recipe remains in the runbook with its decision points. It is not bundled into an unattended install script.

## What the measurements mean

- A: bonded sockets, about 60 minutes.
- B: standalone sockets, about 15 minutes.
- C: standalone explicit AF_XDP zero-copy, about 60 minutes.
- Validator system CPU A/C: 0.3550799087 / 0.0261025539 core equivalents, a 92.65% reduction (about 0.329 core).
- B/C reduction: 92.42%. Total validator CPU stayed near 28 cores.

These sequential observations combine topology/backend/queue differences; ordinary testnet traffic is not a controlled capacity benchmark. Linux drops increased in both standalone phases and their cause remains unverified. No mainnet, maximum-throughput, latency-percentile, energy, losslessness or native-mlx5-parity claim is made.

[Aggregate data](data/voting-summary.json), [chart data](data/voting-timeseries.json), and [chart](figures/voting-resources.png) are sanitized artifacts. `kernel_cpu_cores` denotes validator system CPU, not total CPU. The chart retains the early disk-write burst. Raw private machine logs, keys, histories, identity mappings, management endpoints and fencing/transfer helpers are excluded.

## Verification and provenance

See [validation](docs/VALIDATION.md), [provenance](docs/PROVENANCE.md) and [license map](../LICENSE.md). SHA256SUMS identifies this staged package's files. The clean-build recipe is reconstructed and untested; no executable build-output path is asserted.

After publication, replace the article's pending source link with the actual full-commit permalink to this README and the runbook. Link downloads to that same commit/release. Do not substitute a mutable branch link for the cited experimental revision.


## Collector coverage prerequisite

The portable collector reads one selected service cgroup. Before measuring, confirm ALL validator tiles are in that cgroup. Tiles moved into another cgroup will be omitted and the CPU/resource totals will be incomplete. The measured X710 layout satisfied this prerequisite. Multi-cgroup layouts need a separately reviewed collector.
