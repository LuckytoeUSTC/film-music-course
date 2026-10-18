from pathlib import Path
import subprocess,json
import numpy as np
from scipy.signal import stft
ROOT=Path(__file__).resolve().parents[2]/'展示制作_20261018'
SRC=Path(r'D:\__Netdisk Download\The Last Emperor')
def feature(p):
 raw=subprocess.run(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar','11025','-f','f32le','-'],capture_output=True,check=True).stdout
 a=np.frombuffer(raw,dtype=np.float32)
 freq,t,z=stft(a,11025,nperseg=4096,noverlap=1891,boundary=None)
 mag=np.abs(z)
 notes=np.round(69+12*np.log2(np.maximum(freq,1)/440)).astype(int)
 feat=np.array([mag[notes==n].sum(axis=0) for n in range(36,108)])
 feat=np.log1p(feat*1000)
 feat-=np.mean(feat,axis=0,keepdims=True)
 feat/=np.linalg.norm(feat,axis=0,keepdims=True)+1e-8
 return feat
albums=[(p.name,feature(p)) for p in SRC.glob('*.opus')]
results=[]
for p in sorted((ROOT/'媒体').glob('*.mp4')):
 f=feature(p);r=[]
 for name,a in albums:
  sim=f.T@a
  win=40 # about 8s, no tempo correction
  best=(-2,0,0)
  for d in range(-sim.shape[0]+win,sim.shape[1]-win):
   vals=np.diagonal(sim,offset=d)
   if len(vals)<win:continue
   means=np.convolve(vals,np.ones(win)/win,mode='valid');k=int(np.argmax(means));v=float(means[k])
   if v>best[0]:best=(v,max(0,-d)+k,max(0,d)+k)
  r.append(dict(album=name,similarity=round(best[0],4),clip_offset=round(best[1]*.2,1),album_offset=round(best[2]*.2,1)))
 r.sort(key=lambda x:x['similarity'],reverse=True)
 results.append(dict(clip=p.name,candidates=r[:3]))
 print(p.name,r[:1],flush=True)
(ROOT/'研究'/'音频信号候选匹配.json').write_text(json.dumps(dict(method='72 semitone log spectrum, cosine diagonal mean over 8s; no tempo correction; computational candidates only, not listening verification',results=results),ensure_ascii=False,indent=2),encoding='utf-8')
