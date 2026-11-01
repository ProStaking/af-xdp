# Proposal draft: BCM57416 AF_XDP zero-copy design and upstream port

DESIGN DRAFT. No email, RFC series, maintainer outreach or PR submitted.

## Result worth discussing

An experimental derivative of Broadcom bnxt_en239.1.170.0 on BCM57416 successfully completed bounded receive recycling, transmit completion/reuse, ordinary attach/detach and a caught-up Firedancer testnet voting hour. The deployed tuple and limitations are recorded in the voting runbook/results. This is a vendor-based feature prototype, not a Linux-mainline patch series or proof of exceptional DMA recovery.

The independently adapted Firedancer initializer supplies FILL buffers before bind. Its ownership/configuration work belongs in a separate userspace proposal. Do not combine it with the kernel submission or treat a userspace startup workaround as proof that the driver API contract is ideal.

## Current upstream applicability

Inspected Linux master **cbbddb6b08cc9900a87cccaa9b22bbe06aa4f50a** on2026-11-01. The [bnxt Makefile](https://github.com/torvalds/linux/blob/cbbddb6b08cc9900a87cccaa9b22bbe06aa4f50a/drivers/net/ethernet/broadcom/bnxt/Makefile) includes bnxt_xdp.o but not the vendor bnxt_xsk.o. In the inspected [bnxt_xdp dispatcher](https://github.com/torvalds/linux/blob/cbbddb6b08cc9900a87cccaa9b22bbe06aa4f50a/drivers/net/ethernet/broadcom/bnxt/bnxt_xdp.c#L462), XDP_SETUP_PROG is handled and other commands return EINVAL. This is not the vendor pool-setup/TX-completion implementation. Consequently the prototype is not a small chip-guard patch applicable to this upstream tree.

The net-next source endpoint could not be retrieved in this review; pending netdev series and unpublished vendor work were not exhaustively checked. Pin and inspect the actual target net-next revision and current mailing-list work before proposing code or claiming upstream lacks all related work. Mainline evidence is exact and retained; net-next applicability remains an explicit gate.

## Proposed discussion and eventual decomposition

Ask maintainers about the intended upstream AF_XDP foundation and P4 resource/firmware constraints first. If appropriate, prepare focused upstream-native commits covering pool validation and queue resource admission, DMA mapping/unwind ownership, RX allocation/refill and redirect, AF_XDP TX/completion recycling, dedicated steering/RSS interaction, and ordinary detach/reopen. Keep each demonstrated general bug fix separate from feature enablement; do not invent Fixes tags for vendor-only concerns or port compatibility aliases without an in-tree need.

Retain constraints from the prototype: one qualified P4 pool, no TruFlow or extra RSS contexts, dedicated selected queue excluded from ordinary RSS, explicit firmware resource rejection, and correctly staged prefilled buffers. These are design inputs, not an instruction to transplant vendor implementation blindly. NIC close/reopen operates on the selected netdev/function; unloading the module affects all bound functions. Exceptional reset/device-loss teardown remains unresolved. A successful hour cannot establish firmware DMA drain under every failure.

## Evidence and readiness gaps

Retain the minimal userspace RX/TX reproducer independent of Firedancer, exact firmware/kernel/compiler/build pins, default rejection control and packet/completion ownership counts. Complete starvation/refill, resource exhaustion, bind failure/unwind, outstanding RX/TX ordinary cleanup, steering changes, reset/device loss and already-supported-generation regression coverage. Separate observed faults from conservative lifetime concerns and do not infer safety from absence of corruption. Review build warnings and run upstream checkpatch on the actual port, not on the vendor patch archive.

The original Broadcom source component has GPL COPYING and file notices; preserve them. Public package includes source patches/tests and a license map, not firmware, installer bundle or vendor tools. Source reconstruction/provenance is verified; a detached vendor signature was not verified. No new authorship, SPDX provenance or human DCO certification should be invented.

## Submission route

Pinned [MAINTAINERS](https://github.com/torvalds/linux/blob/cbbddb6b08cc9900a87cccaa9b22bbe06aa4f50a/MAINTAINERS) lists Michael Chan, Pavan Chebbi and netdev@vger.kernel.org for BNXT_EN. Re-run get_maintainer.pl on the eventual patch. A networking feature normally goes through a reviewable emailed RFC/series toward net-next; independently established fixes follow the appropriate net process. This is not a generic GitHub pull request to the Linux mirror.

Review the current [networking process](https://docs.kernel.org/process/maintainer-netdev.html), [submission guide](https://docs.kernel.org/process/submitting-patches.html) and [AI guidance](https://github.com/torvalds/linux/blob/master/Documentation/process/coding-assistants.rst) on the submission tree. Disclose substantial AI assistance and its verification limits. A human reviewer/submitting author must take responsibility and provide any DCO sign-off; no sign-off is added by this draft. Author identity, send destination and exact series remain decisions for a later authorized submission.
