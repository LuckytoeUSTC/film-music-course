exec(open(__file__.replace('extra_frames.py','build_media.py'),encoding='utf-8').read().split('points=')[0])
points=[(35,'片头题字'),(378,'割腕'),(399,'回忆宫门'),(560,'初见全景'),(1640,'童年奔跑全景'),(2185,'追阿嬷奔跑'),(2205,'追阿嬷远景'),(2238,'追逐结束'),(2484,'庄士敦到来'),(3205,'自行车宫门'),(4860,'离宫全景'),(5840,'雨中出门'),(5870,'雨中独行'),(8185,'追婉容奔跑'),(8218,'追婉容门'),(9338,'重访背影'),(9385,'重返龙椅'),(9590,'配乐字幕')]
for sec,label in points:
 p=OUT/'截图'/f'{sec:05d}_{label}.jpg'
 if not p.exists():run(['-ss',str(sec),'-i',str(video),'-vf',f'scale=1280:-2,{tone}','-frames:v','1','-q:v','2',str(p)])
 print(sec,label,flush=True)
