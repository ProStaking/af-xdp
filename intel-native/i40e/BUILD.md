# Reconstructing and building the tested release derivative

This package contains the complete source change used for the voting-hour derivative, not just the narrow filter fix. Source reconstruction is verified. Byte-identical binary reproducibility is **not** claimed.

## Release source: exact, verified reconstruction

Run from the root of a checkout containing this `intel-native/i40e/` package. These commands download official source and create local build directories; they do not activate hardware:

```sh
package=$(pwd)/intel-native/i40e
work=$(pwd)/iavf-reproduction
mkdir "$work"
git clone https://github.com/firedancer-io/firedancer.git "$work/upstream"
git -C "$work/upstream" cat-file -e 6286f99e400c1d5ac6f95b8cf36491555faa3726^{commit}
python3 "$package/source/release/reconstruct.py" "$work/upstream" "$work/source"
```

`reconstruct.py` archives the exact pristine v26.10.5 commit, then applies `source/release/series` in order using **git apply**, not git am. It refuses an existing output directory and verifies the complete 3,661-file manifest. Submodules are not needed for the native C Firedancer targets built here; this recipe does not build Agave/Frankendancer or Rust targets.

The first resolved patch contains eight Intel PR12540 commits plus the release-specific adaptations. The second contains the semantic IPv4 rule comparison fix. Original author-bearing patches in `upstream-inputs/` document provenance; they are **not** a directly applicable release series. The aggregate `complete-release-backport.patch` is an alternative representation of both steps, not an additional third patch. Do not apply it on top of the series.

All 65 modified files match the original tested source manifest. Independently reconstructing both patches reproduces all 3,661 manifested files. Those files also match the retained compiler input. The old build directory had extra generated files, duplicates and reject remnants outside this manifest; complete directory identity is not claimed. The clean-output build succeeded without those leftovers.

## Build environment and exact target command

The recorded environment was Linux/amd64, Ubuntu22.04, GCC12.3.0-1ubuntu1~22.04.3, GNU make4.3 and binutils2.38. `source/release/build-packages.tsv` records the full image package inventory. Native C dependencies such as zstd/blst are vendored in the pinned tree. The source uses Linux userspace headers; it does not need the validator kernel's Module.symvers or an out-of-tree Intel kernel driver build.

The exact make invocation is:

```sh
make -j4 MACHINE=linux_gcc_x86_64 CC=gcc-12 CXX=g++-12 LD=gcc-12 \
  BUILDDIR=iavf-release firedancer test_iavf_rule test_iavf_tile \
  test_auto_net test_config_parse test_config_json
```

The machine file selects Haswell ISA, Skylake tuning and the tree's optimization/security/debug flags. No extra feature flags were added. `CXX=g++-12` was retained in the recorded command, but this target set used C/assembly; the original image did not have g++-12 installed. The public environment recipe installs it explicitly.

Build the supplied public environment, then compile with networking disabled, no devices, no capabilities and read-only source/root:

```sh
docker build --platform=linux/amd64 -t firedancer-i40e-reproduction:review \
  "$package/source/release"
mkdir "$work/output"
sh "$package/source/release/build-in-container.sh" \
  firedancer-i40e-reproduction:review "$work/source" "$work/output"
```

Output is `$work/output/firedancer`, with `build.log` and `binary.sha256`. The wrapper refuses a nonempty output directory. Package installation happens only while constructing the build image; review that step before running it. Ubuntu package availability and versions can change. Record the resulting image digest/package versions; this is not a frozen public package repository snapshot.

The original local image was `sha256:ee7a49bda04d636097b995dd7c7874d34ac5957c2ea8b870c0972c4a0a56e046`. It is an evidence pin, **not a publicly pullable image**. The public Dockerfile's validation outcome is recorded separately in `VALIDATION.md`.

## Tests and the NUMA limitation

Run the five built unit executables from `output/tree/build/iavf-release/unit-test/` on a supported Linux environment, **without hardware arguments**. Inspect the test source first. The tile test uses mock queues/socketpairs when invoked this way; these tests are not NIC activation or a validator launch.

The recorded deployment build passed all five on supported Linux. The clean reconstruction's comparator passed in Docker; four other binaries exited in common initialization because Docker Desktop did not expose `/sys/devices/system/node` (`numa_cnt=0`). They did not reach their cases and are not reported as passes. Do not work around this by granting privileged access or binding host devices. Sanitizer coverage is limited to comparator/tile translation units, not the full validator.

## Why the binary hashes differ

- Voting artifact: `c28f3a3150d22bb7f4655a2123bd8754b62b9ea224f132c9288225a3f77f5531`.
- Clean-output rebuild in the same original image: `65804ae99802f3dda1ab516e4923681738f44bf9c237091510265021338ba2f8`.

Of 656 common object files, 654 match byte-for-byte. The two differing objects are `fd_log.o` and `firedancer.buildinfo.o`, which import generated build metadata. The make rules embed build/link dates, build user/hostname/path and Git availability. In the final ELF, `.text` and every compared section except `.rodata` and `.note.gnu.build-id` match. `source/release/BINARY-COMPARISON.json` records section hashes. This strongly explains the observed difference as build metadata, but it is not a claim that the complete binaries are byte-identical or that the rebuilt binary has been hardware-qualified. No timestamps or artifacts were rewritten to manufacture a matching hash.

## Separate PR-based track

The narrow semantic fix was submitted as commit `db6637e708e24c54b331c7cdeabca0767c7169c9`, on PR head `696316b2d4deea93565c12f4b7022fd5ff65d41e`, with discussion at https://github.com/firedancer-io/firedancer/pull/12540#issuecomment-6566903505. That track had a 15-minute unstaked hardware qualification; the release derivative above had the voting hour. Do not label one build's evidence as the other's or apply `semantic-rule.patch` twice to the submitted fix commit.
