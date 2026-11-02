#!/usr/bin/env python3
"""Reconstruct local sources only. No builds, devices, downloads or deployment."""
import hashlib
import io
import json
import pathlib
import subprocess
import sys
import tarfile

BASE = "6286f99e400c1d5ac6f95b8cf36491555faa3726"
HERE = pathlib.Path(__file__).resolve().parent
if len(sys.argv) != 3:
    raise SystemExit("usage: reconstruct.py UPSTREAM_GIT_CHECKOUT NEW_OUTPUT_DIRECTORY")
checkout = pathlib.Path(sys.argv[1]).resolve()
out = pathlib.Path(sys.argv[2]).resolve()
if out.exists():
    raise SystemExit("Refusing to overwrite existing output directory")
actual = subprocess.check_output(["git", "-C", str(checkout), "rev-parse", BASE + "^{commit}"], text=True).strip()
assert actual == BASE
archive = subprocess.check_output(["git", "-C", str(checkout), "archive", BASE])
with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
    for member in tar.getmembers():
        path = pathlib.PurePosixPath(member.name)
        assert not path.is_absolute() and ".." not in path.parts
        assert member.isfile() or member.isdir() or member.issym()
        if member.issym():
            link = pathlib.PurePosixPath(member.linkname)
            assert not link.is_absolute() and ".." not in link.parts
    out.mkdir()
    # Members come from the pinned official Git tree and were checked above.
    tar.extractall(out)
for line in (HERE / "series").read_text().splitlines():
    patch = HERE / line
    subprocess.run(["git", "apply", "--check", str(patch)], cwd=out, check=True)
    subprocess.run(["git", "apply", str(patch)], cwd=out, check=True)
manifest = json.loads((HERE / "full-source-sha256.json").read_text())
actual_files = {str(p.relative_to(out)) for p in out.rglob("*") if p.is_file() and not p.is_symlink()}
assert actual_files == set(manifest), "Source path set differs"
for name, expected in manifest.items():
    assert hashlib.sha256((out / name).read_bytes()).hexdigest() == expected, name
print(f"Verified {len(manifest)} manifested source files from {BASE}")
