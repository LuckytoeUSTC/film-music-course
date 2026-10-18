from pathlib import Path
import subprocess,json
ROOT=Path(__file__).resolve().parents[2]/'展示制作_20261018'
OUT=ROOT/'交付'/'媒体';OUT.mkdir(parents=True,exist_ok=True)
for src in sorted((ROOT/'媒体').glob('*.mp4')):
 dest=OUT/src.name
 if dest.exists() and dest.stat().st_size>100:continue
 sub=src.with_suffix('.srt')
 vf='pad=1280:720:0:88:black,setsar=1'
 if sub.stat().st_size>3:
  subrel=sub.relative_to(ROOT.parent).as_posix()
  vf+=f",subtitles=filename='{subrel}':force_style='Fontname=Microsoft YaHei,Fontsize=18,Outline=1.2,Shadow=0,MarginV=9'"
 p=subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-vf',vf,'-c:v','libx264','-crf','21','-preset','veryfast','-threads','4','-c:a','copy','-movflags','+faststart',str(dest)],capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr[-2000:])
 print(dest.name,flush=True)
import shutil
for src in (ROOT/'媒体').glob('*.m4a'):shutil.copy2(src,OUT/src.name)
