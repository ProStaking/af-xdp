# Local reproducibility validation

Validated on November 2, 2026. No validator hosts were accessed for this packaging check.

- **Source reconstruction passed.** The packaged `reconstruct.py` applied the ordered series to pristine commit `6286f99e400c1d5ac6f95b8cf36491555faa3726` and verified the exact 3,661-file manifest. An independent reviewer also applied the series and verified it. The 65 changed files match the retained voting-build source manifest.
- **Clean build in the original environment passed.** All requested targets linked from reconstructed source and empty output. The rule comparator passed. Four other tests stopped before their cases because Docker Desktop lacks the required NUMA sysfs topology; these are not passes.
- **Public environment recipe built successfully.** The supplied Ubuntu 22.04 Dockerfile built a fresh Linux/amd64 image. The packaged wrapper then built Firedancer and all five requested unit binaries successfully from the reconstructed source and empty output, with networking disabled and no devices/capabilities. The fresh-image rule comparator passed (687 rejection cases). Fresh-image binary SHA-256: `6417cd905247b630f5135012ef8a7842af5f94935085e64f31edfd306190c2cf`. The other four tests were not rerun; the original-image NUMA limitation above remains.
- **Binary identity is not claimed.** The original-image rebuild matched 654 of 656 objects and the final executable `.text`; the two changed objects embed generated build metadata. Only `.rodata` and `.note.gnu.build-id` differed among compared ELF sections. See `source/release/BINARY-COMPARISON.json` and BUILD.md.

This validates a source/build recipe, not new hardware qualification, boot recovery or validator throughput. The original voting-hour measurements remain specific to the original artifact in README.md.
