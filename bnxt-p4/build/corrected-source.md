# Corrected source: stable initial fill and runtime opt-in

This is the later experimental candidate, not the binary/driver used for the original performance hour. It passed three short unstaked restart cycles and a subsequent recorded live voting handover. Boot payload was verified, not reboot-tested. Exceptional reset/device-loss/DMA recovery and P5+ hardware remain unqualified.

Work only in new build directories. PACKAGE is the absolute path to bnxt-p4 in this repository. No commands below install modules or start a validator. Preserve vendor acquisition requirements, upstream notices and the recovery prerequisites in the voting runbook.

## Driver: append the correction

First follow the driver portion of [historical reconstruction](README.md), through both patches and its SOURCE-SHA256.json verification. Keep the research-driver baseline beside the experimental tree for tests. Then, in the reconstructed p4-experimental directory:

```sh
patch -p1 --batch < "$PACKAGE/driver/patches/0003-stable-initial-fill.patch"
python3 "$PACKAGE/build/verify_manifest.py" "$PACKAGE/driver/CORRECTED-SOURCE-SHA256.json" .
```

The patch records completed initial RX allocation before NAPI/interrupt processing can advance the producer. It replaces a mutable post-open equality check; genuine partial fills still reject. Reconstruction independently matched all 307 corrected source entries. The original 306-entry source checkpoint is retained separately.

Build with the exact target headers/config/Module.symvers and the documented GCC12 toolchain. The existing make command-line opt-in `p4_xsk_experimental=1` remains required. A coherent full rebuild is necessary because the RX-ring structure changes. Recorded experimental module SHA256: `e7440f76994f394bc21d714ea8254386231ba8aaf8ea6c795ba28d6e8aaa4968`.

## Firedancer: replace the historical patch sequence

Use a new pristine checkout. Do not apply the two historical Firedancer patches first.

```sh
git clone https://github.com/firedancer-io/firedancer.git firedancer-p4-runtime
cd firedancer-p4-runtime
git checkout --detach 6286f99e400c1d5ac6f95b8cf36491555faa3726
git apply "$PACKAGE/firedancer/patches/runtime-option-v26.patch"
```

The complete patch changes 19 files. Independent replay reproduced all 19 retained candidate files from local archive-import commit 9bcbd17b0a0de118e82c0c3b96c55e8b78c94d53, representing that upstream base. This is not a claim of a fresh authenticated upstream download or clean dependency provisioning.

With reviewed dependencies already provisioned, the retained build used:

```sh
make -j4 MACHINE=linux_gcc_x86_64 CC=gcc-12 CXX=g++-12 LD=gcc-12 \
  BUILDDIR=prebind-v26 firedancer test_config_parse test_config_json \
  test_auto_net test_xdp_tile test_xsk_prebind test_xsk_init_prebind
```

The resulting executable was `build/prebind-v26/bin/firedancer`. Recorded binary SHA256: `c6234c9d903a94cf832b8a8e80ccd8490abdbe66bdfc9faddbd684f7ba63c137`. Do not assert deterministic binary reproduction from source alone. The original build used prepared dependencies; independent clean dependency-image reproduction remains outstanding.

## Final configuration difference

Start from the sanitized historical [voting TOML](../config/voting.example.toml), replacing SITE placeholders and reconciling current cluster checkpoints. In its existing `[net.xdp]` section add:

```toml
experimental_prebind_fill = true
```

This is a boolean, default false; there is no EXTRAS compile-time gate in this candidate. Keep explicit xdp/drv/zero-copy, standalone physical port, native_bond="false", dedicated RSS, one net tile and RX depth 1024. There is no bnxt_zero_copy option. Physical RX/TX and loopback ownership remain disjoint; loopback remains COPY.

The runtime candidate retained 52 startup tiles, 87 one-GiB and 2747 two-MiB pages. Calculated locked bytes increased by 4096 to 99,240,878,080 versus the historical binary. Recompute from the exact binary/config before activation; existing numeric limits are measured-host examples.

Use the [voting runbook](../docs/voting-runbook.md) for prerequisite gates and [follow-up](../docs/restart-fix-and-live-handover.md) for the later transition. Private preparation, peer-role, signed-history and restart gates are not portable helpers in this package. Never bypass missing gates. The new runtime path does not automatically provision resources or switch voting ownership.
