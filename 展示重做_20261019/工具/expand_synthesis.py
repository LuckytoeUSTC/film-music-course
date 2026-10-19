from pathlib import Path
import json,re,shutil
R=Path(__file__).resolve().parents[1]; O=R/'交付'; B=R/'build/合成乐修订';B.mkdir(parents=True,exist_ok=True)
p=R/'工具/slides.json'; slides=json.loads(p.read_text(encoding='utf-8'))
assert len(slides)==28,'一次性修订脚本，勿重复执行'
shutil.copy2(p,B/'slides.before.json')
shutil.copy2(O/'听见末代皇帝_音乐赏析.pptx',B/'before.pptx')
prompts=[
'交代问题：音乐怎样连接不同年代中的人物处境。介绍由具体场面进入的路线。',
'简述跨国制作与主要创作者。配乐由三人署名，避免全部归给坂本龙一。',
'说明北美公映和票房口径，介绍九项奥斯卡。不以获奖代替音乐分析。',
'并列评论分歧：宏大景观怎样容纳个人经验。留下问题，结尾回应。',
'只交代后面片段需要的身份变化，避免完整复述剧情。',
'区分囚禁中的现在与回忆。把时间结构留给后面的连续转场验证。',
'用人物与宫门的比例说明行动受限。交接：段从创作者与声音材料继续。',
'介绍三位作曲者及署名边界。片头Main Title Theme与坂本的主题条目区分。',
'简述坂本的参与与录音背景。预告电子音色会在主题变奏之后专门展开，本页不重复设备知识。',
'播放片头。引导辨认声音层次与音色联想，不先替听众指定全部乐器。',
'区分文化联想与历史复原。此处只讲观看预期，合成与采样留到后面的专页。',
'播放Open the Door，建立材料印象。曲名不能直接证明电影中的使用位置。',
'播放连续转场，注意声音与新画面谁先出现。区分剪辑连接与远距离主题重现。',
'解释主题怎样建立记忆联系，变化可落在配器、音区和伴奏。交接：丁比较两次追赶。',
'播放Where Is Armo，先抓伴奏的行进感与上方旋律，不堆叠听辨任务。',
'播放追阿嬷。观察身体、宫门、剪辑和音乐推进的关系，不把所有追逐都称为动作同步。',
'播放追婉容。年龄身份变化与相似行动并置，旋律对应只说到已回听核实的位置。',
'比较两次追赶的节奏、力度与织体，避免把音符变密都叫加速。交接：段从离开者讲到声音的重新组织。',
'播放Rain，注意音乐自身的表达。创作意图与实际听觉效果分开。',
'播放雨中离开。联系主观评论：配乐怎样影响我们理解离开。此页不重复合成器介绍。',
'播放两段原声，先比较材料联系，再关注音色和伴奏。保留同一主题也能改变表达的判断，接到合成乐专页。',
'先解释合成、采样与编序的区别。Fairlight兼具这些功能，设备介绍只用于理解声音组织，不据此猜定本片每个音色。',
'回扣刚才两段摘录，不再整段重播。区分已有评论、制作名单与自己的听辨。讨论音色的起音、延音、叠置怎样影响空间感。交接：丁把声音比较带回结尾。',
'播放First Coronation，带着材料印象看结尾。原声标题不能独自证明结尾配乐版本。',
'播放重返龙椅。人物与空间的关系已改变，核对音乐怎样参与记忆。',
'区分故事内声源与画外声音，回看音乐、对白、环境声的前景关系。没有配乐不等于静音。',
'回应开头的评论分歧：用前面的具体案例说明音乐怎样贴近个人经验，保留历史评价的限度。邀请段共同进入互动。',
'共同主持互动。丁接人物与叙事的问题，段接音色与合成乐的问题；另一人按需要补充，最后共同回应。',
'按提问定位来源，不逐条朗读参考文献。创作访谈、学术研究和影评的证据用途分开。',
'共同答疑，按问题选择备用片段。音乐细节尚未核实的地方直接说明，不临场补造。'
]
new=[
 {'title':'合成乐：声音怎样被制作出来？','body':['合成：用电子方式生成、塑造声音','采样：录入已有声音，再触发和处理','编序：安排声音出现的次序与节奏','Fairlight CMI把这些功能结合在同一系统中'],'layout':'text','sources':['COURSE_NEW','T01'],'minutes':1.3,'prep':''},
 {'title':'管弦乐与电子音色：怎样一起表达？','body':['《Variation 2》提供主题与音色的比较入口','比较起音、延音、声部叠置与空间感','电子声音可延展质感，管弦乐也能持续、反复','“宏大与孤寂”要回到具体声音与画面解释'],'layout':'text','sources':['COURSE_NEW','R06','S05','T01'],'minutes':1.5,'prep':'R06为评论者听辨；S05为制作名单二手转录。Fairlight型号及每个声部的生成方式未核实，不由设备名单直接推出。'}
]
slides[21:21]=new
for i,d in enumerate(slides,1):
    who='丁' if i<=7 or 15<=i<=18 or 24<=i<=27 else '段' if i<=23 else '丁、段'
    d['speaker']=who;d['notes']=who+'，'+prompts[i-1]
    d['original_slide']=i if i<=21 else i-2 if i>=24 else None
slides[8]['body'][-1]='录音与电子制作共同参与；稍后结合主题变奏展开'
sources=json.loads((R/'工具/sources.json').read_text(encoding='utf-8'))
sources.update({'COURSE_NEW':'老师最新PPT配乐片单：《末代皇帝》条目“东方管弦与电子合成器碰撞”。归档/01_最新要求_20261014/PPT配乐片单_01至05.png。', 'T01':'Science Museum Group, Fairlight CMI Series 3 Mainframe：综合合成、采样和编序功能；设备通史材料，不证明本片使用具体型号。https://collection.sciencemuseumgroup.org.uk/objects/co8607596/fairlight-cmi-series-3-mainframe'})
(R/'工具/sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2),encoding='utf-8');p.write_text(json.dumps(slides,ensure_ascii=False,indent=2),encoding='utf-8')
md=['# 双人讲稿提示词','', '与30页PPT讲者备注一致。只作提示，不是逐字稿；页面内不列时间估计。丁、段按完整主题交接，互动共同主持。','']
for i,d in enumerate(slides,1):
    md += [f'## 第{i}页　{d["title"]}','',d['notes'],'']
    if d.get('media'):md += ['播放文件：'+d['media']+('；'+d['secondMedia'] if d.get('secondMedia') else ''),'']
(O/'双人逐页讲稿.md').write_text('\n'.join(md),encoding='utf-8')
plan='''# 双人交接安排

按完整主题轮换，姓名与PPT备注一致。目标是每人每轮连同音视频不超过10分钟；页数与文字只能帮助分段，达标仍须实际排练。备注不写时间估计。

|轮次|主讲|页码|内容与交接|
|---|---|---|---|
|一|丁|1—7|问题、背景、评论与空间，交给段从创作与声音切入|
|二|段|8—14|作曲、片头、材料与转场，交给丁比较追赶|
|三|丁|15—18|两次追赶，交给段讨论离开者与音乐表达|
|四|段|19—23|雨中离开、主题变奏、合成与采样、电子与管弦乐的结合|
|五|丁|24—27|结尾、声音结构与评价，邀请段共同互动|
|互动|丁、段|28|共同主持，按提问互相补充|
|资料与备用|丁、段|29—30|按需查来源、回放与答疑|

第四轮将合成乐作为中心：第19—20页保留场景，第21页提供试听材料，第22—23页集中解释，避免各处重复介绍电子制作。暂未删去其他主题。审核时可决定哪些页略讲、哪些媒体改作备用；如排练超时，再按内容价值缩减，不能只靠加快语速。
'''
(O/'双人交接安排.md').write_text(plan,encoding='utf-8')
# 保留原离线页面的播放器，仅同步源数据与提示词格式。
page=O/'离线展示.html';h=page.read_text(encoding='utf-8');a=h.index('const slides=')+len('const slides=');b=h.index(';let index=',a)
h=h[:a]+json.dumps(slides,ensure_ascii=False).replace('</','<\\/')+h[b:]
h=h.replace("notes.textContent='讲者 '+s.speaker+'　预算 '+s.minutes+'分钟\\n\\n'+s.notes",'notes.textContent=s.notes')
page.write_text(h,encoding='utf-8')
# 修改未来构建入口，防止重新引入A/B与时间预算、覆盖新的首页。
builder=R/'工具/build_deck.mjs';h=builder.read_text(encoding='utf-8');start=h.index(' s.speakerNotes.text=');end=h.index(';',start)+1;h=h[:start]+' s.speakerNotes.text=d.notes;'+h[end:];builder.write_text(h,encoding='utf-8')
b=R/'工具/build_delivery.py';h=b.read_text(encoding='utf-8');h=h.replace("f'讲者：{d[\"speaker\"]}。时间预算：{d[\"minutes\"]}分钟（含本页媒体与互动）。\\n',",'')
h=h.replace("notes.textContent='讲者 '+s.speaker+'　预算 '+s.minutes+'分钟\\\\n\\\\n'+s.notes",'notes.textContent=s.notes')
h=h.replace("(OUT/'开始阅读.md').write_text(readme,encoding='utf-8')", "# 操作说明由人工维护，不覆盖。(OUT/'开始阅读.md')")
h=h.replace('沿用约36分钟的排练预算，含主讲媒体和互动；语言修订后的实际时长尚待排练，勿为凑时长刻意放慢。末页为备用。讲者A/B可互换，文件不使用成员姓名。','丁、段按完整主题交接，互动共同主持；具体分工见双人交接安排。')
b.write_text(h,encoding='utf-8')
print('源文件、提示词、分工与离线页面已更新：30页')
