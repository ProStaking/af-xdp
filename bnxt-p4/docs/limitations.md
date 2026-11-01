# Limits

R13 remains documented rather than fixed: MAC changes or ntuple-off can remove steering rules unseen by the backstop. Do neither with an attached pool; use UDP4 ntuple rather than ether rules. Some NIC changes apply then fail reopen, leaving the interface down. Normal attached-pool transitions must stay within the reviewed tested scope.

Only one pool,2 KiB frames/compatible256-byte offset, MTU 1500, queue 0/one-net-tile and dedicated mode were exercised in this FD trial. No other P4 chip, multiple pools, GRE/DoubleZero, bonding, voting, maximum throughput, tail latency, energy efficiency or mlx5 parity was qualified. Firmware timeout/reset/device-loss teardown remains unqualified. Earlier source/mock tests are not silicon guarantees.

The node was not caught up. Successful advancing replay and ordinary restoration is useful functional evidence, not voting readiness. A future sole-voter handover and matched one-hour comparison require separate scope; any persistent P4-voter/X710-lab role swap is conditional on that later evidence.
