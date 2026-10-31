# SPDX-License-Identifier: MIT
# Copyright (c) 2026 ProStaking contributors
"""Summarize a selected steady-state window from collect_system.py JSONL."""
import argparse,json,statistics
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('samples');p.add_argument('--interface',required=True);p.add_argument('--disk',required=True)
p.add_argument('--start',type=float,default=float('-inf'),help='Inclusive Unix UTC seconds')
p.add_argument('--end',type=float,default=float('inf'),help='Inclusive Unix UTC seconds')
a=p.parse_args();r=[json.loads(l) for l in open(a.samples)];r=[x for x in r if a.start<=x['time']<=a.end]
assert len(r)>=2,'At least two in-window samples required'
f,z=r[0],r[-1];dt=z['time']-f['time'];assert dt>0

def cpu(x):return {k:int(v) for k,v in (s.split() for s in x['cgroup']['cpu.stat'].splitlines())}
def cpus(x):return {s.split()[0]:list(map(int,s.split()[1:9])) for s in x['proc_stat'].splitlines() if s.startswith('cpu')}
def net(x):return list(map(int,next(s.split(':')[1] for s in x['net_dev'].splitlines() if s.split(':')[0].strip()==a.interface).split()))
def disk(x):return list(map(int,next(s.split()[3:] for s in x['diskstats'].splitlines() if s.split()[2]==a.disk)))
def delta(x,y):
 d=[v-u for u,v in zip(x,y)];assert all(v>=0 for v in d),'Counter reset: split the window at restart';return d
def q(v):
 v=sorted(v);return {'min':v[0],'median':statistics.median(v),'p95':v[min(len(v)-1,int(.95*len(v)))],'max':v[-1]}
generations=[(x.get('boot_id'),x.get('service_generation')) for x in r]
continuity='External uninterrupted-service proof required: generation metadata unavailable'
if all(all(v is not None for v in g) for g in generations):
 assert len(set(generations))==1,'Boot or service generation changed'
 continuity='Sampled boot and service generation unchanged; sub-sample events are not independently excluded'
for old,new in zip(r,r[1:]):
 assert new['time']>old['time'],'Non-increasing timestamps'
 u,v=cpu(old),cpu(new)
 assert all(v[k]>=u[k] for k in ['usage_usec','user_usec','system_usec']),'Cgroup counter decreased'
 delta(net(old),net(new))
 d=[v-u for u,v in zip(disk(old),disk(new))]
 assert all(v>=0 for i,v in enumerate(d) if i!=8),'Disk counter decreased'
 for name,values in cpus(old).items():
  assert all(y>=x for x,y in zip(values,cpus(new)[name])), 'CPU accounting decreased; iowait can decrease without a reset, so this CPU window needs review'
cf,cz=cpu(f),cpu(z);assert cz['usage_usec']>=cf['usage_usec'],'Cgroup counter decreased'
o={'continuity':continuity,'samples':len(r),'start':f['time'],'end':z['time'],'seconds':dt,'max_sample_gap_seconds':max(y['time']-x['time'] for x,y in zip(r,r[1:])),'validator_cpu_cores':(cz['usage_usec']-cf['usage_usec'])/dt/1e6,'validator_system_cpu_cores':(cz['system_usec']-cf['system_usec'])/dt/1e6,'cpu':{}}
for name,old in cpus(f).items():
 d=delta(old,cpus(z)[name]);total=sum(d)
 if total:o['cpu'][name]={'busy_excluding_iowait_pct':100*(total-d[3]-d[4])/total,'system_pct':100*d[2]/total,'softirq_pct':100*d[6]/total,'iowait_pct':100*d[4]/total}
o['available_RAM_GiB']=q([int(next(s.split()[1] for s in x['meminfo'].splitlines() if s.startswith('MemAvailable:')))/1048576 for x in r]);o['cgroup_memory_GiB']=q([int(x['cgroup']['memory.current'])/2**30 for x in r])
n=delta(net(f),net(z));o['network']={'rx_MiB_s':n[0]/dt/2**20,'rx_pps':n[1]/dt,'rx_errors':n[2],'rx_drops':n[3],'tx_MiB_s':n[8]/dt/2**20,'tx_pps':n[9]/dt,'tx_errors':n[10],'tx_drops':n[11]}
d=[v-u for u,v in zip(disk(f),disk(z))];assert all(v>=0 for i,v in enumerate(d) if i!=8),'Disk counter reset';o['disk']={'read_MiB_s':d[2]*512/dt/2**20,'write_MiB_s':d[6]*512/dt/2**20,'read_IOPS':d[0]/dt,'write_IOPS':d[4]/dt,'read_await_ms':d[3]/d[0] if d[0] else None,'write_await_ms':d[7]/d[4] if d[4] else None,'avg_queue_depth':d[10]/dt/1000,'busy_time_pct':100*d[9]/dt/1000}
for field in ['memory.events','memory.stat','cpu.pressure','memory.pressure','io.pressure']:
 o[field]={'first':f['cgroup'].get(field),'last':z['cgroup'].get(field)}
o['hugepages']={'first':f['hugepages'],'last':z['hugepages']}
print(json.dumps(o,indent=2))
