# Public build-environment recipe; availability depends on Ubuntu mirrors.
# This is not the private image used for the recorded voting artifact.
FROM ubuntu:22.04
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ca-certificates gcc-12 g++-12 make python3 libc6-dev linux-libc-dev \
    pkg-config libssl-dev zlib1g-dev libelf-dev libbpf-dev clang-14 llvm-14 \
    && rm -rf /var/lib/apt/lists/*
USER 65534:65534
