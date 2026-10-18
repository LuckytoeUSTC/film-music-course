from pathlib import Path
import subprocess,json,re,datetime
ROOT=Path(__file__).resolve().parents[2]
SRC=Path(r'D:\__Netdisk Download\The Last Emperor')
OUT=ROOT/'展示制作_20261018'
for d in ['研究','媒体','截图','制作记录','交付','build']:(OUT/d).mkdir(parents=True,exist_ok=True)
video=next(SRC.glob('*.mkv'))
def run(args):
 p=subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',*args],capture_output=True,text=True,encoding='utf-8',errors='replace')
 if p.returncode:raise RuntimeError(p.stderr[-3000:])
 return p
bookmarks=[]
for f in SRC.glob('*.pbf'):
 raw=f.read_bytes()
 for line in raw.decode('utf-16' if raw.startswith(b'\xff\xfe') else 'utf-8-sig').splitlines():
  m=re.match(r'(\d+)=(\d+)\*([^*]*)',line)
  if m:bookmarks.append(dict(file=f.name,index=int(m[1]),seconds=int(m[2])/1000,title=m[3]))
(OUT/'研究'/'书签提取.json').write_text(json.dumps(bookmarks,ensure_ascii=False,indent=2),encoding='utf-8')
tone='zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=mobius:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p'
points=[(0,'片头'),(390,'首次转场'),(554,'紫禁城初见'),(1392,'鼓声转场'),(1633,'奔跑'),(2175,'追阿嬷'),(2219,'呼喊'),(2480,'紫禁城众人'),(3196,'自行车'),(4844,'紫禁城离开'),(5860,'雨'),(8170,'追婉容'),(8448,'枪声转场'),(9328,'重访紫禁城'),(9547,'片尾')]
for sec,label in points:
 p=OUT/'截图'/f'{sec:05d}_{label}.jpg'
 if not p.exists():run(['-ss',str(sec),'-i',str(video),'-vf',f'scale=1280:-2,{tone}','-frames:v','1','-q:v','2',str(p)])
 print('frame',sec,label,flush=True)
(OUT/'制作记录'/'素材信息.json').write_text(json.dumps(dict(source=str(video),duration=9774.223,audio='0:1 English DTS',tone_map=tone,bookmarks=len(bookmarks),start='2026-10-18 20:27 Asia/Shanghai'),ensure_ascii=False,indent=2),encoding='utf-8')
