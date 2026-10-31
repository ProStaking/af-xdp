# SPDX-License-Identifier: MIT
# Copyright (c) 2026 ProStaking contributors
"""Read-only 10-second whole-system performance samples; no active benchmark."""
import pathlib,time,json,os,subprocess,argparse,re
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--service',required=True);p.add_argument('--interface',required=True);p.add_argument('--output-dir',required=True)
p.add_argument('--label',default='measurement');p.add_argument('--duration',type=int,default=3600);p.add_argument('--interval',type=float,default=10)
a=p.parse_args();assert re.fullmatch(r'[A-Za-z0-9_][A-Za-z0-9_.@-]*\.service',a.service)
assert re.fullmatch(r'[A-Za-z0-9_.:-]+',a.interface) and a.duration>0 and a.interval>=1
os.umask(0o077);B=pathlib.Path(a.output_dir);B.mkdir(mode=0o700,parents=False,exist_ok=False)
control=subprocess.check_output(['systemctl','show',a.service,'-p','ControlGroup','--value'],text=True).strip()
assert control.startswith('/') and control != '/' and '..' not in control.split('/'), 'Service must have a dedicated cgroup'
cg=pathlib.Path('/sys/fs/cgroup'+control);P=pathlib.Path('/proc');deadline=time.monotonic()+a.duration

def read(p):
 try:return pathlib.Path(p).read_text()
 except OSError:return None
while True:
 start=time.monotonic();r={'time':time.time(),'clock_ticks':os.sysconf('SC_CLK_TCK'),'schema_version':2}
 r['boot_id']=read('/proc/sys/kernel/random/boot_id')
 r['service_generation']=subprocess.check_output(['systemctl','show',a.service,'-p','MainPID','-p','ExecMainStartTimestampMonotonic'],text=True,timeout=5)
 assert 'MainPID=0' not in r['service_generation'].splitlines(), 'Service is stopped'
 r['proc_stat']=read('/proc/stat');r['meminfo']=read('/proc/meminfo');r['diskstats']=read('/proc/diskstats');r['net_dev']=read('/proc/net/dev');r['softirqs']=read('/proc/softirqs')
 r['pressure']={k:read('/proc/pressure/'+k) for k in ['cpu','memory','io']}
 r['cgroup']={k:read(cg/k) for k in ['cpu.stat','memory.current','memory.stat','memory.events','memory.swap.current','io.stat','cpu.pressure','memory.pressure','io.pressure']}
 r['hugepages']={z:{k:read('/sys/kernel/mm/hugepages/hugepages-'+z+'kB/'+k) for k in ['nr_hugepages','free_hugepages','resv_hugepages','surplus_hugepages']} for z in ['2048','1048576']}
 r['processes']=[]
 for pid in (read(cg/'cgroup.procs') or '').split():
  raw=read(P/pid/'stat');status=read(P/pid/'status')
  if raw and status:r['processes'].append({'pid':int(pid),'stat':raw,'status_fields':[l for l in status.splitlines() if l.startswith(('Name:','VmRSS:','RssAnon:','RssFile:','RssShmem:','VmSwap:','Threads:','voluntary_ctxt_switches:','nonvoluntary_ctxt_switches:'))],'io':read(P/pid/'io')})
 try:
  r['label']=a.label;r['interface']=a.interface;r['service']=a.service
  r['driver']=subprocess.check_output(['ethtool','-S',a.interface],text=True,timeout=5)
 except Exception as e:r['collection_error']=str(e)
 r['collection_seconds']=time.monotonic()-start
 with (B/'system.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
 if time.monotonic()>=deadline:break
 time.sleep(max(.1,min(a.interval-(time.monotonic()-start),deadline-time.monotonic())))
