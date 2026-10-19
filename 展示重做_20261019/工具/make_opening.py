from pathlib import Path
import subprocess,json,shutil
R=Path(__file__).resolve().parents[1];B=R/'build/开场剪辑';B.mkdir(exist_ok=True)
M=R/'交付/媒体';ff=r'D:\ffmpeg\bin\ffmpeg.exe'
shutil.copy2(r'C:\Windows\Fonts\msyh.ttc',B/'font.ttc')
def run(args):subprocess.run([ff,'-hide_banner','-loglevel','error','-y',*args],cwd=B,check=True)
base=['-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-movflags','+faststart']
items=[]
def card(name,text,seconds):
 (B/(name+'.txt')).write_bytes(text.encode('utf-8'))
 run(['-f','lavfi','-i','color=c=0x171714:s=1280x720:r=25','-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-t',str(seconds),'-vf',f'drawtext=fontfile=font.ttc:textfile={name}.txt:fontcolor=0xF1E7D3:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2:line_spacing=22',*base,name+'.mp4']);items.append(name+'.mp4')
card('intro','追赶，离开，重访\n《末代皇帝》片段并置',2)
cuts=[('05_追阿嬷.mp4',20,8,'童年：追赶'),('10_追婉容.mp4',40,8,'成年：追赶'),('09_雨中离开.mp4',41,8,'雨中：离开'),('12_重访紫禁城.mp4',19,8,'晚年：重访')]
for i,(file,start,dur,label) in enumerate(cuts,1):
 name=f'cut{i}';(B/(name+'.txt')).write_text(label,encoding='utf-8')
 vf=f"fps=25,scale=1280:720,setsar=1,drawtext=fontfile=font.ttc:textfile={name}.txt:fontcolor=0xF1E7D3:fontsize=34:x=46:y=24,fade=t=in:st=0:d=0.12,fade=t=out:st={dur-.12}:d=0.12"
 run(['-ss',str(start),'-i',str(M/file),'-t',str(dur),'-vf',vf,'-af',f'afade=t=in:st=0:d=0.08,afade=t=out:st={dur-.08}:d=0.08',*base,name+'.mp4']);items.append(name+'.mp4')
card('end','音乐怎样连接这些时刻？',3)
(B/'concat.txt').write_text('\n'.join("file '"+x+"'" for x in items),encoding='utf-8')
out=M/'00_开场_追赶离开重访.mp4'
run(['-f','concat','-safe','0','-i','concat.txt','-c','copy','-movflags','+faststart',str(out)])
run(['-i',str(out),'-f','null','-'])
receipt={'文件':str(out.relative_to(R)),'预期秒数':37,'素材':[{'文件':f,'相对切片起点':s,'长度':d,'标注':l} for f,s,d,l in cuts],'声音处理':'保留各段原声；分段边缘80毫秒淡入淡出，不新增配乐，不作响度标准化','画面处理':'保留完整画幅和既有字幕，段落标注置于上方黑边；分段120毫秒淡入淡出','用途':'开场提出问题，重组后的声画不作为原片连续性证据','检查':'已完整解码；未声称实际回听'}
(R/'制作记录/开场剪辑记录.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8');print(out)
