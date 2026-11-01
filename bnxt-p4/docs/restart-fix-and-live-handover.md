# P4 follow-up: confirmed startup race, correction and live handover

Recorded follow-up, 2026-11-01. The completed one-hour performance measurements remain unchanged and belong to the earlier compile-time-prebind binary/driver combination. No repeat performance hour is claimed for the later correction.

## Confirmed failure and fix

Subsequent restarts failed AF_XDP bind with ENOBUFS, including the earlier known-good build. Failure-branch tracing observed the post-open RX producer at 525 while the ring size was 511. The candidate was comparing a moving producer counter after NAPI/interrupt processing had already started. A normal producer advance could therefore be mistaken for incomplete initial allocation.

The correction records full initial RX allocation before packet processing can change the producer, then checks that stable result after open. It does not delete the allocation check: regressions still reject genuine partial fills, including a partial-fill producer later advancing to 511. Original evidence and module remain preserved. This change does not qualify all exceptional DMA/reset/unwind paths.

Corrected experimental module SHA256:
`e7440f76994f394bc21d714ea8254386231ba8aaf8ea6c795ba28d6e8aaa4968`

All 27 existing suites plus new allocator/rejection regressions and sanitizer cases passed. Exact kernel 6.8.0-138 builds linked. Independent review passed. Three ordinary unstaked start/traffic/stop cycles passed with physical zero-copy and clean observed teardown, without ENOBUFS or observed kernel faults. These were short qualification cycles, not production certification.

## Firedancer runtime option

The earlier performance hour used the compile-time opt-in. The subsequent same-base v26.10.5 candidate uses default-off `net.xdp.experimental_prebind_fill = true`, with explicit physical zero-copy and disjoint buffer ownership preserved. Its SHA256 is `c6234c9d903a94cf832b8a8e80ccd8490abdbe66bdfc9faddbd684f7ba63c137`. Keep this validation separate from the newer-upstream proposal branch; same-base hardware evidence does not automatically qualify a different upstream base.

## Persistence and handover

The corrected module was installed and the rebuilt boot image extracted to verify the exact payload. No reboot was performed for that persistence step: boot payload verified, not boot-tested.

A separate unstaked P4 standby restored a trusted cluster snapshot, caught up and passed independent lag checks. A public vote-account setting was then populated while retaining the unstaked identity, block-production topology and key-directory isolation. After it caught up again, supported live identity transitions moved voting from X710 to P4. X710 demoted first, its final signed Alpenglow history was verified and transferred, and P4 promoted using its already-existing local key through the protected admin path. Neither live process stopped during that identity transition.

Final verification showed P4 caught up, its vote account current and lastVote advancing across independent observations. X710 remained caught up on its separate unstaked identity with zero-copy intact. Current history paths and restart roles were aligned. No private-key transfer or directory-permission widening was used.

## Operator limits

This remains experimental. Repeated-start evidence now includes the targeted correction and three successful cycles, but does not establish firmware/reset/abnormal-DMA recovery safety. Keep independent management and a known-good recovery path. Live identity switching does not change static topology or public vote-account configuration: prepare those before promotion. Preserve newest signed history in both directions, verify exclusive signing, and commit restart roles coherently.

Our private P4 startup guard still requires fresh peer-role confirmation; without it startup fails closed. Do not describe this as unattended failover or a portable turnkey service package. No new performance hour or upstream submission is claimed.
