# Measured X710 configuration and systemd settings

This is the configuration record for the completed one-hour **C: standalone X710 / AF_XDP zero-copy** voting run. It accompanies the results article (publication link pending) and [scoped backend runbook](runbook.md). No Firedancer or i40e code changes were made.

`SITE_*` and `/SITE/...` are deliberately non-operational placeholders for the original private names, paths, interface, public vote account and trusted snapshot provider. `192.0.2.10` is a documentation address replacing the tested public address. The tested runtime account was `sol`, UID 1000. The cluster genesis value and localhost listeners are unchanged. Replace placeholders through your existing working-validator setup, not by copying this document into a service blindly.

## Full measured TOML, with site values redacted

All non-site values below retain the measured configuration's types and values. The original file had a stale analysis-only comment; it is omitted because this configuration did run with the voting identity.

```toml
user = "sol"
name = "SITE_VALIDATOR_NAME"
telemetry = false
[paths]
base = "/SITE/validator/data"
identity_key = "/SITE/validator/keys/identity.json"
vote_account = "SITE_PUBLIC_VOTE_ACCOUNT"
vote_history = "/SITE/validator/vote-history"
[accounts]
max_accounts = 200000000
cache_size_gib = 12
[layout]
affinity = "auto"
enable_block_production = true
enable_snapshot_production = false
net_tile_count = 1
execrp_tile_count = 4
snapdc_tile_count = 1
snapin_tile_count = 1
shred_tile_count = 2
[tiles.gui]
enabled = false
[tiles.rpc]
enabled = true
rpc_listen_address = "127.0.0.1"
rpc_listen_port = 8899

[net]
provider = "xdp"
interface = "SITE_STANDALONE_X710_INTERFACE"
bind_address = "192.0.2.10"
[hugetlbfs]
mount_path = "/SITE/hugetlbfs"
[snapshots.server]
enabled = false
[tiles.metric]
prometheus_listen_address = "127.0.0.1"

[log]
path = "/SITE/validator/data/logs/firedancer.log"
[development]
sandbox = true
core_dump = "disabled"

[consensus]
expected_genesis_hash = "4uhcVJyU9pJkvQyS88uRDiswHXSCkY3zQawwpjk2NsNY"
alpenglow = true
[snapshots.sources]
servers = []
[snapshots.sources.gossip]
allow_any = false
allow_list = ["SITE_TRUSTED_SNAPSHOT_PROVIDER"]

[net.xdp]
xdp_mode = "drv"
native_bond = "false"
xdp_zero_copy = "true"
poll_mode = "softirq"
rss_queue_mode = "simple"
```

`listen_gre` was **absent in the measured C TOML**. Its pinned default is the string `"auto"`; in `rss_queue_mode = "simple"`, that field is ignored. Omitting it does not disable GRE. Snapshot **production** was disabled; snapshot loading/restoration remained part of startup. The trusted-provider allowlist was populated with an actual approved provider during the test.

## Effective measured validator service

This is a consolidated representation of the base unit plus the measured voting drop-in, not a replacement service recommendation. The Description in the original base unit still said “non-voting” from the earlier lab phase; the TOML vote account and runtime evidence establish that C was voting. The description below is labeled for readability. Site helper names and dependencies are placeholders for private infrastructure, not supplied runnable helpers.

```ini
[Unit]
Description=SITE validator (description label sanitized)
Requires=site-validator-prepare.service
Wants=network-online.target site-resource-guard.timer
After=network-online.target site-validator-prepare.service
StartLimitIntervalSec=600
StartLimitBurst=3
ConditionPathExists=!/SITE/experiment/hold
ConditionPathExists=!/SITE/experiment/fenced

[Service]
Type=simple
User=root
WorkingDirectory=/SITE/validator
ExecStartPre=/SITE/libexec/resource-check
ExecStart=/opt/firedancer/v26.10.5/bin/firedancer run --testnet --config /SITE/config/validator.toml
Restart=no
RestartSec=30
TimeoutStopSec=60
KillMode=control-group
LimitMEMLOCK=96G
LimitNOFILE=1024000
LimitNICE=40
LimitCORE=0
TasksMax=128
MemoryMax=104G
MemorySwapMax=0
CPUAffinity=1-15 17-31
UMask=0077
ProtectSystem=strict
ReadWritePaths=/SITE/validator /SITE/hugetlbfs
PrivateTmp=yes

[Install]
WantedBy=multi-user.target
```

The base unit specified `LimitMEMLOCK=80G`, `MemoryMax=96G` and `Restart=on-failure`. The measured voting drop-in overrode those three values. `RestartSec=30` remained in the base but was inactive with `Restart=no`.

### Exact measured voting drop-in, with site paths redacted

```ini
[Unit]
ConditionPathExists=!/SITE/experiment/hold
ConditionPathExists=!/SITE/experiment/fenced
[Service]
LimitMEMLOCK=96G
MemoryMax=104G
Restart=no
```

The private `ExecStartPre` history-validation helper visible in the later service audit was appended **after C completed**, during final restoration. It is excluded from both measured-C excerpts above. The existing resource-check `ExecStartPre` was present during measurement. Host handover, authoritative-history validation and sole-voter fencing were handled separately by private orchestration; these excerpts do not implement them.

### Startup privilege and runtime isolation

The systemd service bootstrapped as **root**. The unit did not restrict `CapabilityBoundingSet`, set ambient capabilities, or enable unit-level `NoNewPrivileges`. The effective audit reported:

```text
User=root
Group=
NoNewPrivileges=no
AmbientCapabilities=
CapabilityBoundingSet=cap_chown cap_dac_override cap_dac_read_search cap_fowner cap_fsetid cap_kill cap_setgid cap_setuid cap_setpcap cap_linux_immutable cap_net_bind_service cap_net_broadcast cap_net_admin cap_net_raw cap_ipc_lock cap_ipc_owner cap_sys_module cap_sys_rawio cap_sys_chroot cap_sys_ptrace cap_sys_pacct cap_sys_admin cap_sys_boot cap_sys_nice cap_sys_resource cap_sys_time cap_sys_tty_config cap_mknod cap_lease cap_audit_write cap_audit_control cap_setfcap cap_mac_override cap_mac_admin cap_syslog cap_wake_alarm cap_block_suspend cap_audit_read cap_perfmon cap_bpf cap_checkpoint_restore
```

This is the full default capability bounding set reported by this host, not a tested least-privilege unit profile. Setting unit-level `NoNewPrivileges=yes` or stripping bootstrap capabilities would be a different, untested configuration.

Firedancer's own `sandbox = true` and privilege-drop path then applied to runtime tiles. The checked critical runtime tiles were UID 1000, `CapEff=0`, `NoNewPrivileges=1`, and `Seccomp=2`. Those process observations do not mean the systemd bootstrap unit itself was unprivileged, or that every ancillary service shared the same restrictions.

## Measured preparation dependency

The original prepare unit was `Type=oneshot`, `RemainAfterExit=yes`, with a 180-second start timeout and network/local-filesystem ordering. Its original command included `hugetlbfs sysctl snapshots`. During voting, a drop-in moved memory preparation to a separate private memory unit and replaced that command with `sysctl snapshots`:

```ini
# Base prepare unit, sanitized
[Unit]
Description=SITE validator resource preparation
After=local-fs.target network-online.target
Wants=network-online.target
[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/opt/firedancer/v26.10.5/bin/firedancer configure init hugetlbfs sysctl snapshots --testnet --config /SITE/config/validator.toml
TimeoutStartSec=180

# Measured prepare-unit drop-in, sanitized
[Unit]
Requires=site-voting-memory.service
After=site-voting-memory.service
ConditionPathExists=!/SITE/experiment/hold
[Service]
ExecStart=
ExecStart=/opt/firedancer/v26.10.5/bin/firedancer configure init sysctl snapshots --testnet --config /SITE/config/validator.toml
```

The memory helper, resource guard, resource check, hold/fence files and deadline/recovery infrastructure are site-specific prerequisites. Their names above explain the measured service dependencies; the public package does not provide their implementations. NIC queue/offload preparation was also performed separately. The scoped runbook starts after these prerequisites are ready and does not run a broad host `configure init` automatically.

## Which values to carry forward

**Hardware/layout-specific values:** `CPUAffinity=1-15 17-31` used a 30-logical-CPU budget on the Ryzen 7950X. Tile counts, the 200M account bound, 12 GiB cache, page pool and service limits were sized for this measured layout. The common pool was 79 × 1 GiB and 2,305 × 2 MiB pages; effective memlock was 103,079,215,104 bytes and MemoryMax was 111,669,149,696 bytes. Preview both backends on your own binary/config before provisioning. One net tile used one combined queue with simple RSS; this also changes the queueing available to ordinary socket traffic.

**Settings retained from the working validator:** identity/history paths, vote authorization, genesis, snapshot trust, localhost RPC/metrics, service resource checks and runtime isolation need to remain aligned with your existing deployment. Preserve their actual values rather than replacing them with this document's placeholders. `User=root` bootstrap and Firedancer's later privilege drop are distinct parts of the tested setup.

**Backend settings that identify this experiment:** `provider="xdp"`, `xdp_mode="drv"`, `native_bond="false"`, `xdp_zero_copy="true"`, `poll_mode="softirq"`, and `rss_queue_mode="simple"`. The interface was already standalone for C. No bond/IP/MAC/identity migration is encoded in this TOML.

The measured executable was `/opt/firedancer/v26.10.5/bin/firedancer`, version 26.10.5 at commit `6286f99e400c1d5ac6f95b8cf36491555faa3726`, SHA256 `e3db72439537f48b587e36782a6d0e1630833b22e1d976c0a7b83655f020bf46`. The current public build recipe remains a reconstructed, untested clean-build recipe.
