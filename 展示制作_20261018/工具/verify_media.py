from pathlib import Path
import subprocess,json,hashlib,re,zipfile
ROOT=Path(__file__).resolve().parents[2]/'展示制作_20261018'
OUT=ROOT/'交付'
reports=[]
for f in sorted((OUT/'媒体').iterdir()):
 if f.suffix not in ['.mp4','.m4a']:continue
 probe=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,codec_type,width,height','-of','json',str(f)],capture_output=True,check=True)
 p=subprocess.run(['ffmpeg','-v','error','-i',str(f),'-f','null','-'],capture_output=True)
 reports.append(dict(file=f.name,bytes=f.stat().st_size,probe=json.loads(probe.stdout),decode_ok=p.returncode==0,error=p.stderr.decode(errors='replace')[:1000],sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
 print(f.name,'decode',p.returncode,flush=True)
htmls=[]
for p in OUT.glob('*.html'):
 text=p.read_text(encoding='utf-8');bad=[]
 for a in re.findall(r'(?:src|href)="([^"]+)"',text):
  if '${' in a or 'encodeURIComponent' in a or a.endswith("'+") or a.startswith(('http','#')):continue
  if "'+" in a:continue
  if not (OUT/a).exists():bad.append(a)
 htmls.append(dict(file=p.name,missing_static_targets=bad))
(ROOT/'制作记录'/'media.validation.json').write_text(json.dumps(dict(media=reports,html=htmls),ensure_ascii=False,indent=2),encoding='utf-8')
