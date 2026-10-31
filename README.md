# AF_XDP experiments by ProStaking

Operator-facing configurations, measurement data and runbooks for bounded AF_XDP experiments. Each hardware experiment keeps its versions, prerequisites, scripts, runtime verification and limitations together.

## Experiments

- [Intel X710](x710/README.md): Firedancer 26.10.5 on the documented testnet configuration; final TOML/resource settings, scoped backend swap and rollback, sanitized measurements and optional helpers.

No other hardware experiment is included yet. Results from one configuration do not establish support or performance on another device, client release or cluster.

## Read before running

Start with the experiment README and `experiment.json`. Examples are reference material, not authority to operate a host. Distinguish read-only inspection, local candidate generation and host-mutating steps. There is no unattended installer. Host migration, bond conversion, signing-history validation, NIC preparation and recovery are site-specific prerequisites.

The human article explains the result; the experiment package provides exact settings and evidence boundaries. After publication, citations should use the actual full commit permalink rather than a moving branch.

## Licenses and provenance

Original code/configuration examples use MIT; original prose/data/figures use CC BY 4.0. See [the license map](LICENSE.md) and [provenance](PROVENANCE.md). Upstream Firedancer/driver source and binaries are not vendored. No private consensus history, keys or management endpoints are included.
