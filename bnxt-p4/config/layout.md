# Exact measured layout and host-specific controls

48 logical CPUs, fixed tiles1-18,25-36; housekeeping0,19-24,37-47.42 tiles. One physical AF_XDP queue 0;48 combined channels, RSS1..47, no extra RSS contexts, ntuple on, no TruFlow, MTU 1500, RX/TX hardware rings 511. Candidate channels follow min(maximum,48), not the superseded12-channel proposal.48 channels may require144 TX rings,96 CP/stat contexts and 49 vNICs; failed firmware admission is a stop, not permission to reduce channels behind configure checks.

Node0 pools80×1 GiB and 2083×2 MiB; locked90, 327,339,008 bytes. Dedicated hugetlbfs `.gigantic` pagesize1073741824/min_size 85899345920 and `.huge` pagesize2097152/min_size 4368367616, runtime owner0700. Memlock96 GiB, MemoryMax104 GiB, LimitNOFILE1048576. Owned cpuset memory.max104 GiB also required because fixed tiles leave the systemd cgroup. Restore saved original pools/masks after normal cleanup.

Physical LRO/rx-gro-hw/GRE segmentation/checksum segmentation off; loopback tx-udp-segmentation off. Loopback accept_local/route_localnet temporary1, original 0; rp_filter2 unchanged. Global max_map_count1000000/nr_open1048576 already sufficient. Console blink inherited1 was temporarily disabled and restored; printk3 unchanged. Values are measured host inputs, not universal recommendations.

No IP/MAC/route or real host names are embedded here. The experiment temporarily moved a public address/MAC/gateway from an active-backup bond to a standalone function. This requires an operator-specific reviewed migration and inverse, independent management and a stock boot recovery path. Module unload affects every Broadcom function, not just the selected port.
