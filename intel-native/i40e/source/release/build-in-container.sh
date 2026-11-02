#!/bin/sh
# Build only: no devices, networking changes or validator activation.
set -eu
[ "$#" -eq 3 ] || { echo "usage: $0 IMAGE SOURCE_DIR EMPTY_OUTPUT_DIR" >&2; exit 2; }
image=$1
source_dir=$(CDPATH= cd -- "$2" && pwd)
output_dir=$(CDPATH= cd -- "$3" && pwd)
[ -z "$(ls -A "$output_dir")" ] || { echo 'Output directory must be empty' >&2; exit 2; }
mkdir "$output_dir/tree"
docker run --rm --pull=never --platform=linux/amd64 --network=none --read-only \
 --cap-drop=ALL --security-opt=no-new-privileges --user "$(id -u):$(id -g)" \
 --pids-limit 256 --memory 4g --cpus 4 --tmpfs /tmp:rw,exec,nosuid,nodev,size=512m \
 --mount "type=bind,src=$source_dir,dst=/source,readonly" \
 --mount "type=bind,src=$output_dir,dst=/out" \
 --entrypoint sh "$image" -c '
set -eu
tar -C /source --exclude=.git -cf - . | tar -C /out/tree -xf -
cd /out/tree
make -j4 MACHINE=linux_gcc_x86_64 CC=gcc-12 CXX=g++-12 LD=gcc-12 BUILDDIR=iavf-release firedancer test_iavf_rule test_iavf_tile test_auto_net test_config_parse test_config_json > /out/build.log 2>&1
cp build/iavf-release/bin/firedancer /out/firedancer
sha256sum /out/firedancer > /out/binary.sha256
'
