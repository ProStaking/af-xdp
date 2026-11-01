# Fresh snapshots before catch-up or voting measurement

The completed unstaked trial used an older local snapshot pair and never reported caught up. Exact concurrent cluster slot was not sampled at the stop instant, so exact final lag is unknown.

A later metadata-only preparation at 2026-11-01 15:45:10 UTC found full slot 459289683 and incremental459342294 from an already-trusted peer, with expected genesis verified. No archive body was downloaded and no config was changed. Those slot numbers are historical observations, not current download recommendations.

Keep `snapshots.sources.servers=[]`, `snapshots.sources.gossip.allow_any=false`, and use only your already approved `TRUSTED_SNAPSHOT_IDENTITY` in allow_list. Do not replace this with a universal public peer recommendation. Refresh metadata/genesis before download. Prefer FD's trusted gossip discovery; keep archive/account-hash/age/consensus validation enabled.

The incremental's base must equal the full snapshot slot. The older458983809 full cannot pair with an incremental based on459289683. Stage complete verified transfers in isolated snapshot storage, preserve old originals and check disk headroom for both pairs. Filenames alone are not authentication. No inbound firewall/public RPC/snapshot hosting, identity change or validation relaxation is needed.

Before a separately scoped voting/performance interval, require replay_is_caught_up=1 and a contemporaneous trusted cluster-slot comparison. Metadata HEAD success does not predict ingest/catch-up time or establish that this gate has passed.
