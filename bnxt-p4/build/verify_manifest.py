"""Read-only byte verification. Usage: manifest.json reconstructed-root."""
import hashlib,json,sys
from pathlib import Path
manifest=json.loads(Path(sys.argv[1]).read_text());root=Path(sys.argv[2]).resolve()
for name,want in manifest.items():
 p=(root/name).resolve()
 if root not in p.parents: raise SystemExit('unsafe manifest path')
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=want:raise SystemExit('mismatch: '+name)
print('verified',len(manifest),'files')
