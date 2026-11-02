# AF_XDP experiments by ProStaking

Operator-facing configurations, measurement data and runbooks for bounded AF_XDP and native-networking experiments. Each hardware experiment keeps its versions, prerequisites, scripts, runtime verification and limitations together.

## Experiments

- [Native Intel X710 / i40e](intel-native/i40e/README.md): native iAVF versus AF_XDP zero-copy, final configuration, voting measurements, submitted filter-readback fix and a verified source/build recipe. Total validator CPU stayed near 28 cores; kernel CPU fell by 0.02262 core. Native Intel experiments are grouped by PF driver under `intel-native/`.

- [Intel X710](x710/README.md): Firedancer 26.10.5 on the documented testnet configuration; final TOML/resource settings, scoped backend swap and rollback, sanitized measurements and optional helpers.

- [Broadcom BCM57416 P4](bnxt-p4/README.md): experimental driver and Firedancer initialization patches, verified source reconstruction, final configuration examples, ordered runbooks and a completed caught-up voting hour. The complete configuration used 1.052 fewer CPU cores while reducing net tiles from two to one; see the measured results and recovery limits.

Results from one configuration do not establish support or performance on another device, client release or cluster.

## Read before running

Start with the experiment README and `experiment.json`. Examples are reference material, not authority to operate a host. Distinguish read-only inspection, local candidate generation and host-mutating steps. There is no unattended installer. Host migration, bond conversion, signing-history validation, NIC preparation and recovery are site-specific prerequisites.

The human article explains the result; the experiment package provides exact settings and evidence boundaries. After publication, citations should use the actual full commit permalink rather than a moving branch.

## Licenses and provenance

Original code/configuration examples use MIT; original prose/data/figures use CC BY 4.0. See [the license map](LICENSE.md) and [provenance](PROVENANCE.md). The X710 package contains no upstream source or binaries. The bnxt-p4 package contains separately licensed driver and Firedancer patch material and required notices; it contains no binaries, firmware or vendor installer. No private consensus history, keys or management endpoints are included.

The native Intel package retains Apache-2.0 source-patch notices; see [its provenance](intel-native/i40e/PROVENANCE.md). It includes no binary payloads or private host logs.
