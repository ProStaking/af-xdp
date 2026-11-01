# Historical measured-source reconstruction

This page reproduces the original compile-time-prebind voting-hour checkpoint. For the subsequent stable-initial-fill correction and runtime-option candidate, follow [corrected-source instructions](corrected-source.md). Preserve both checkpoints; do not attribute the original performance hour to corrected code.

## Reconstruct and build; never install automatically

Obtain the exact vendor source archive identified in PROVENANCE through the official vendor download process. Verify its SHA256 before safe extraction (reject absolute/traversal members). Work in a new directory, not a live module/source tree. Let PACKAGE be this package's absolute path.

```sh
cp -a bnxt_en-1.10.3-239.1.170.0 research-driver
cd research-driver
patch -p1 --batch < "$PACKAGE/driver/patches/0001-vendor-to-research.patch"
python3 "$PACKAGE/build/verify_manifest.py" "$PACKAGE/driver/BASELINE-SHA256.json" .
cd ..
cp -a research-driver p4-experimental
cd p4-experimental
patch -p1 --batch < "$PACKAGE/driver/patches/0002-p4-initialization.patch"
python3 "$PACKAGE/build/verify_manifest.py" "$PACKAGE/driver/SOURCE-SHA256.json" .
```

Keep `research-driver` beside `p4-experimental`: regression tests need the baseline. These commands reconstruct the source tested; they do not alter live hardware. Compile separate temporary copies with exact target headers, config and Module.symvers, GCC12 and make/binutils:

```sh
make -j2 CC=x86_64-linux-gnu-gcc-12 KVER=6.8.0-138-generic
# In a separate clean copy:
make -j2 CC=x86_64-linux-gnu-gcc-12 KVER=6.8.0-138-generic p4_xsk_experimental=1
```

The opt-in flag must be a make command-line assignment, not an environment variable. Verify version, vermagic and SHA256 of both outputs. No modprobe/install command belongs in the build step. Actual build used read-only/network-disabled nonroot containers, no capabilities/devices and scratch copies. Provision dependencies before entering that sandbox. Public image reconstruction is not yet independently reproduced; hashes and exact toolchain/header inputs are in PROVENANCE. Do not treat kernel 6.8 generally as equivalent to ABI 138.

Firedancer source and build:

```sh
git clone https://github.com/firedancer-io/firedancer.git firedancer-p4
cd firedancer-p4
git checkout --detach 6286f99e400c1d5ac6f95b8cf36491555faa3726
git apply "$PACKAGE/firedancer/patches/0001-prebind-primitives.patch"
git apply "$PACKAGE/firedancer/patches/0002-opt-in-prebind.patch"
python3 "$PACKAGE/build/verify_manifest.py" "$PACKAGE/firedancer/SOURCE-SHA256.json" .
```

Use the pinned upstream dependency instructions (`deps.sh`), reviewing their build-host effects first. The original offline image already held prepared dependencies, so clean dependency provisioning is a separate prerequisite. Do not execute the validator during build.

```sh
make -j4 MACHINE=linux_gcc_x86_64 CC=gcc-12 CXX=g++-12 LD=gcc-12 \
  BUILDDIR=p4-default build/p4-default/bin/firedancer
make -j4 MACHINE=linux_gcc_x86_64 CC=gcc-12 CXX=g++-12 LD=gcc-12 \
  EXTRAS=p4-prebind BUILDDIR=p4-wired build/p4-wired/bin/firedancer
sha256sum build/p4-default/bin/firedancer build/p4-wired/bin/firedancer
```

The built path is verified by the retained build scripts/logs. The opt-in macro selects pre-bind publication and partitioning. The patch also adds an unconditional UMEM-size validation and include outside that macro; do not claim the default path is byte-for-byte unchanged. Default binary equality with an unmodified upstream build is not claimed. This package's patch replay has been checked, but its portable instructions have not been run as a fresh full build on an operator's machine.
