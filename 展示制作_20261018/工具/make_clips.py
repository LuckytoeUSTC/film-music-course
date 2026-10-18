exec(open(__file__.replace('make_clips.py','build_media.py'),encoding='utf-8').read().split('points=')[0])
clips=[
('01_片头音色',10,65,'核心','片头音色与署名'),
('02_首次回忆转场',370,415,'核心','1950年与童年之间的剪辑'),
('03_紫禁城初见',548,575,'核心','夜色、宫门与进宫队伍'),
('04_童年奔跑',1625,1685,'备选','奔跑与追随的队列'),
('05_追阿嬷',2165,2255,'核心','奔跑、呼喊与空间距离'),
('06_紫禁城与人群',2472,2505,'核心','同一空间中的群体秩序'),
('07_自行车',3185,3245,'备选','运动的愉悦与宫墙边界'),
('08_离开紫禁城',4835,4885,'核心','离开时的空间与人物关系'),
('09_雨中离开',5815,5880,'核心','文绣与雨中的离开'),
('10_追婉容',8155,8225,'核心','成年奔跑与再次受阻'),
('11_枪声转场',8435,8465,'备选','声音与场景衔接'),
('12_重访紫禁城',9315,9365,'核心','重返时的空间身份'),
('13_龙椅与蝈蝈',9388,9480,'核心','身份对话与记忆物件'),
]
manifest=[]
for name,start,end,role,desc in clips:
 target=OUT/'媒体'/(name+'.mp4')
 if not target.exists():
  run(['-ss',str(start),'-i',str(video),'-t',str(end-start),'-map','0:0','-map','0:1','-vf',f'scale=1280:-2,{tone}','-c:v','libx264','-preset','veryfast','-crf','22','-threads','4','-c:a','aac','-b:a','192k','-ac','2','-movflags','+faststart','-map_metadata','-1',str(target)])
 print('clip',name,flush=True)
 # External ASS is provided separately. Make portable simplified Chinese/English SRT per clip.
 def sec(t):
  h,m,s=map(float,t.split(':'));return h*3600+m*60+s
 def ts(t):
  ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
 subs=[]
 for line in (SRC/'The Last Emperor.4K.ass').read_text(encoding='utf-8-sig').splitlines():
  if not line.startswith('Dialogue:'):continue
  fields=line.split(',',9)
  a,b=sec(fields[1]),sec(fields[2])
  if b<=start or a>=end:continue
  txt=re.sub(r'\{[^}]*\}','',fields[9]).replace('\\N','\n').replace('\\n','\n')
  if start<70:continue # omit animated title artwork as dialogue subtitles
  subs.append(f'{len(subs)+1}\n{ts(max(a,start)-start)} --> {ts(min(b,end)-start)}\n{txt}\n')
 target.with_suffix('.srt').write_text('\n'.join(subs),encoding='utf-8-sig')
 manifest.append(dict(id=name,start=start,end=end,duration=end-start,role=role,description=desc,file='媒体/'+target.name))
(OUT/'研究'/'片段清单.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
for prefix,start,duration in [('10',0,35),('05',0,25),('08',0,30),('09',0,35)]:
 source=next(SRC.glob(prefix+' - *.opus'))
 dest=OUT/'媒体'/('音频_'+prefix+'.m4a')
 if not dest.exists() or dest.stat().st_size<100:run(['-ss',str(start),'-i',str(source),'-t',str(duration),'-vn','-map','0:a:0','-c:a','aac','-b:a','192k',str(dest)])
