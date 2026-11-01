#!/bin/sh
set -eu
# Run from reconstructed p4-experimental, with sibling research-driver baseline.
export PYTHONDONTWRITEBYTECODE=1 ASAN_OPTIONS=detect_leaks=1:halt_on_error=1 UBSAN_OPTIONS=halt_on_error=1
python3 tests/test_usr_fltr_restore.py
python3 tests/test_open_restore_unwind.py
python3 tests/test_reserve_rings_xsk.py
python3 tests/test_reserve_wrapper_xsk.py
python3 tests/test_xsk_steering_check.py
python3 tests/test_xsk_ring_reset.py
python3 tests/test_nq0_close_idempotent.py
python3 tests/test_p4_xsk_gate.py
python3 tests/test_p4_lifecycle.py
python3 tests/test_xsk_rx_ownership.py
python3 tests/test_xsk_pass_ownership.py
python3 tests/test_p4_steering.py
python3 tests/test_close_reopen_order.py
python3 tests/test_xsk_batch_events.py
python3 tests/test_p4_xsk_poll.py
python3 tests/test_netdev_lock_compat.py
python3 tests/test_p4_group_checked.py
python3 tests/test_p4_queue_transaction.py
python3 tests/test_p4_rx_unwind.py
python3 tests/test_p4_ring_groups.py
python3 tests/test_p4_initialization.py
python3 tests/test_p4_completion_routing.py
python3 tests/test_p4_topology_preservation.py
python3 tests/test_xsk_completion.py
python3 tests/test_normal_lifecycle.py
python3 tests/test_generation_gate.py
python3 tests/test_pool_lifecycle.py
