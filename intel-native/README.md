# Native Intel networking experiments

Native Intel experiments are grouped by the Linux physical-function driver and hardware family.

- [`i40e/`](i40e/README.md): Intel X710, native iAVF, measured testnet voting experiment and filter-readback contribution.
- A future `ice/` experiment can cover E810. No ice results or qualification are included here.

The directory name identifies the PF driver. Firedancer's native provider for the tested virtual function is `iavf`. This differs from the earlier X710 AF_XDP experiment, which remains in `x710/` at repository root. These packages must not be combined or used interchangeably.
