from pathlib import Path
import json,shutil,html
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'交付'
slides=json.loads((ROOT/'工具'/'slides.json').read_text(encoding='utf-8'))
sources=json.loads((ROOT/'工具'/'sources.json').read_text(encoding='utf-8'))
manifest=json.loads((ROOT/'交付/参考资料/片段清单.json').read_text(encoding='utf-8'))
imgs=OUT/'图片';imgs.mkdir(exist_ok=True)
for d in slides:
 for f in d.get('images',[]):shutil.copy2(ROOT/'截图'/f,imgs/f)
refs=OUT/'参考资料';refs.mkdir(exist_ok=True)
for f in []:
 shutil.copy2(ROOT/'研究'/f,refs/f)
md=['# 双人逐页讲稿\n','丁、段按完整主题交接，互动共同主持；具体分工见双人交接安排。\n','所有书签只用于检索。表中的视频区间不是音乐cue起止。声音与乐器的未决判断见《参考资料/证据与判断边界.md》，应在排练中实际回听后修订。\n']
for i,d in enumerate(slides,1):
 md += [f'## 第{i}页　{d["title"]}\n',d['notes']+'\n']
 if d.get('prep'):md.append('**排练备忘（不朗读）**：'+d['prep']+'\n')
 if d.get('media'):md.append('播放：'+d['media']+ ('；'+d['secondMedia'] if d.get('secondMedia') else '')+'\n')
 if d['sources']:md.append('来源：'+'；'.join(d['sources'])+'。完整链接见来源表。\n')
md += ['## 来源表\n']+[f'- {k}　{v}\n' for k,v in sources.items()]
(OUT/'双人逐页讲稿.md').write_text('\n'.join(md),encoding='utf-8')
timeline=['# 片段与现场顺序\n','以下是视频截取区间，不是配乐开始/结束时间。观影期间书签可能滞后，后期批注也只作检索。\n','| 文件 | 原片起点 | 原片终点 | 秒数 | 用途 |\n|---|---|---|---:|---|']
def ts(s):return f'{int(s)//3600:02}:{int(s)//60%60:02}:{int(s)%60:02}'
for m in manifest:timeline.append(f'| {m["id"]} | {ts(m["start"])} | {ts(m["end"])} | {m["duration"]} | {m["description"]} |')
timeline+=['\n主讲媒体：片头35秒、Open the Door30秒、回忆转场45秒、Where Is Armo30秒、追阿嬷90秒、追婉容70秒、Rain30秒、雨中离开65秒、主题变奏30+35秒、First Coronation35秒、结尾92秒；合计687秒，约11分27秒。其余片段备用。','\n字幕为用户提供ASS中对应时段的简化转换并烧录，原片与字幕源均保留不变。外置ASS文件标题虽含Extended Cut，本次以162分54秒原片与已检查的对话对应为依据。','\n视频：1280×720画布，原画幅居中，H.264/AAC立体声，英语音轨，HDR到SDR。没有进行AI补帧、改色或音效重制。原声音频摘录另为AAC/M4A。']
(OUT/'片段与现场顺序.md').write_text('\n'.join(timeline),encoding='utf-8')
(OUT/'课程群标题与大纲.md').write_text('''# 课程群标题与大纲草稿

标题：听见《末代皇帝》——音乐主题、人物与时代

本次展示以音乐为主体，简述影片与评论背景，结合原声摘录和电影选段，讨论音乐如何表现人物并连接不同时空。主要内容包括影片资料、上映票房与奖项、评论分歧、创作背景，以及Open the Door、Where Is Armo、Rain、主题变奏和结尾的音乐分析。展示设置片头听辨和片段讨论，并参考中外影评及创作者访谈，保留对人物责任与影片视角的追问。

预计约36分钟，含音视频和互动。展示小组两人，具体分工以排练调整。

提交前：确认展示日期、老师的新通知，完成声音回听和现场试播；按课程要求提前一周交内容与标题，并提前发布大纲。此文件未发送到任何群或外部账户。
''',encoding='utf-8')
readme='''# 《末代皇帝》展示包

## 从这里开始

1. 打开“听见末代皇帝_音乐赏析.pptx”，28页，可编辑文字与讲者备注。放映时点击媒体画面/封面播放。本包同时保留独立媒体。
2. 或直接用Chrome/Edge打开“离线展示.html”，左右方向键翻页，F全屏，N显示/隐藏讲稿。媒体不需要联网。
3. “媒体回放.html”列出所有13段视频和8段原声，可按片段逐项查看。“图片”保留正文使用的真实原片静帧。
4. PDF是静态备份，不含音视频，配合媒体回放页使用。双人讲稿、大纲和片段清单均可编辑。

## 仍需两位讲者完成的核验

本稿已完成资料研究、结构、讲稿、画面与媒体制作，但当前模型接口不能直接听取本地音频。因此，音乐具体进入/退出、个别乐器与旋律重现仍须人工实际回听。相关句子保留为现场聆听问题，没有声称完成逐声部听觉分析。请先读“参考资料/证据与判断边界.md”。

PPT媒体已嵌入并做文件结构检查；实际PowerPoint播放行为与课堂音箱效果需现场试播。离线HTML可作为备用播放方式，也需在实际浏览器中试播。HDR转SDR截图用于展示，不能作为精确色值或原片发行色彩的测量。

## 资料与原件

研究覆盖豆瓣、Ebert、Criterion、Washington Post、ReelViews、配乐专栏和一手访谈。每条来源的阅读范围、不同意见和未采用材料见“参考资料/评论阅读与取舍.md”。

D盘电影、原声、字幕和书签原件未改动。原有思路文件、课程资料和截图未改动。当前生成的展示正文不使用成员姓名。成果已按用户授权上传公开GitHub仓库；未代发课程群。

主讲预算约36分钟，另留答疑与机动。不是自动计时的保证，必须至少完整排练一次。备用片段不必全部播放。
'''
# 操作说明由人工维护，不覆盖。(OUT/'开始阅读.md')
# self-contained viewer, only local media/images are referenced
payload=json.dumps(slides,ensure_ascii=False).replace('</','<\\/')
page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>听见《末代皇帝》</title>
<style>*{box-sizing:border-box}body{margin:0;background:#171714;color:#f1e7d3;font-family:"Microsoft YaHei",sans-serif}main{max-width:1280px;margin:auto;min-height:90vh;padding:3.2vh 4vw}h1{font-size:clamp(28px,3.4vw,46px);margin:0 0 3vh}.visuals{display:flex;gap:2vw;align-items:center;justify-content:center}.visuals figure{margin:0;flex:1;min-width:0}.visuals img{width:100%;max-height:54vh;object-fit:contain}figcaption{font-size:18px;color:#d5b16b;margin-top:14px}video{display:block;width:100%;max-height:65vh;background:black}audio{width:min(580px,90%);margin:14px 0}.body{font-size:clamp(20px,2.2vw,31px);line-height:1.5}.body p{margin:.65em 0}.cover h1{font-size:clamp(36px,4.5vw,62px);margin-top:2vh}.cover .visuals img{max-height:58vh}.sub{color:#d5b16b;font-size:28px}.video .body{font-size:24px}nav{position:fixed;bottom:0;width:100%;display:flex;align-items:center;gap:14px;padding:10px 24px;background:#171714ee;font-size:14px}button,select{background:#292820;color:#f1e7d3;border:1px solid #74634b;padding:8px 12px;font-size:14px}#notes{white-space:pre-wrap;background:#292820;padding:22px;font-size:19px;line-height:1.8;margin-bottom:70px}#notes[hidden]{display:none}a{color:#d5b16b}main{padding-bottom:70px}</style>
<main id="stage"></main><aside id="notes" hidden></aside><nav><button id="prev">上一页</button><select id="choose"></select><button id="next">下一页</button><button id="full">全屏</button><button id="note">讲稿</button><span id="counter"></span><a href="媒体回放.html" target="_blank">全部媒体</a></nav>
<script>const slides=PAYLOAD;let index=0;const stage=document.getElementById('stage'),notes=document.getElementById('notes'),choose=document.getElementById('choose');const esc=s=>s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));slides.forEach((s,i)=>choose.add(new Option((i+1)+' '+s.title,i)));function media(f){return f.endsWith('.mp4')?'<video controls preload="metadata" src="媒体/'+encodeURIComponent(f)+'"></video>':'<audio controls preload="metadata" src="媒体/'+encodeURIComponent(f)+'"></audio>'}function show(i){document.querySelectorAll('video,audio').forEach(m=>m.pause());index=Math.max(0,Math.min(slides.length-1,i));let s=slides[index];stage.className=s.layout;let imgs=(s.images||[]).map((f,k)=>'<figure><img src="图片/'+encodeURIComponent(f)+'" alt="'+esc(f)+'">'+(s.captions?'<figcaption>'+esc(s.captions[k])+'</figcaption>':'')+'</figure>').join('');let visual=(s.layout==='video'||s.layout==='cover'&&s.media)?media(s.media):'<div class="visuals">'+imgs+'</div>';stage.innerHTML='<h1>'+esc(s.title)+'</h1>'+visual+(s.subtitle?'<div class="sub">'+esc(s.subtitle)+'</div>':'')+'<div class="body">'+s.body.map(t=>'<p>'+esc(t)+'</p>').join('')+'</div>'+(s.media&&s.layout!=='video'&&s.layout!=='cover'?media(s.media):'')+(s.secondMedia?media(s.secondMedia):'');notes.textContent=s.notes;choose.value=index;document.getElementById('counter').textContent=(index+1)+' / '+slides.length;location.hash='s'+(index+1)}document.getElementById('prev').onclick=()=>show(index-1);document.getElementById('next').onclick=()=>show(index+1);choose.onchange=()=>show(+choose.value);function full(){if(document.fullscreenElement)document.exitFullscreen();else document.documentElement.requestFullscreen()}document.getElementById('full').onclick=full;function note(){notes.hidden=!notes.hidden}document.getElementById('note').onclick=note;document.addEventListener('keydown',e=>{if(['VIDEO','AUDIO','SELECT'].includes(e.target.tagName))return;if(e.key==='ArrowRight'||e.key==='PageDown')show(index+1);if(e.key==='ArrowLeft'||e.key==='PageUp')show(index-1);if(e.key==='Home')show(0);if(e.key==='End')show(slides.length-1);if(e.key.toLowerCase()==='f')full();if(e.key.toLowerCase()==='n')note()});show(Math.max(0,parseInt(location.hash.slice(2)||'1')-1));</script></html>'''.replace('PAYLOAD',payload)
(OUT/'离线展示.html').write_text(page,encoding='utf-8')
blocks=['<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>媒体回放</title><style>body{max-width:1000px;margin:30px auto;background:#171714;color:#f1e7d3;font:20px/1.6 "Microsoft YaHei";padding:20px}video{width:100%;background:black}audio{width:90%}a{color:#d5b16b}section{margin:45px 0}small{color:#b5ad9d}</style><h1>媒体回放</h1><a href="离线展示.html">进入展示</a><p>以下为截取区间，不是音乐起止点。字幕已烧录。视频保留前后余量，可拖动复查。</p>']
for m in manifest:blocks.append(f'<section id="v{m["id"][:2]}"><h2>{html.escape(m["id"])}</h2><p>{ts(m["start"])}—{ts(m["end"])}，{m["duration"]}秒</p><video controls preload="metadata" src="媒体/{m["id"]}.mp4"></video><small>{html.escape(m["description"])}</small></section>')
for f in sorted((OUT/'媒体').glob('*.m4a')):blocks.append(f'<section><h2>{f.stem}</h2><audio controls src="媒体/{f.name}"></audio></section>')
blocks.append('</html>');(OUT/'媒体回放.html').write_text('\n'.join(blocks),encoding='utf-8')
print('delivery text and offline viewer complete')
