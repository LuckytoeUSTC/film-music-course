from pathlib import Path
import hashlib,json,shutil,csv
R=Path.cwd(); records=[]
def move(src,dst):
 s=R/src;d=R/dst
 if not s.exists():return
 assert not d.exists(),str(d)
 h=hashlib.sha256(s.read_bytes()).hexdigest();d.parent.mkdir(parents=True,exist_ok=True);shutil.move(s,d)
 assert hashlib.sha256(d.read_bytes()).hexdigest()==h
 records.append({'原路径':src,'新路径':dst,'SHA256':h,'核验':'一致'})
titles=['论文要求_字数与结构','论文要求_内容与考勤','论文考核片单_01至05','论文考核片单_06至10','论文考核片单_汇总','PPT展示要求_报名时限与互动','PPT推荐片单_说明','PPT配乐片单_01至05_含末代皇帝','PPT配乐片单_06至10','PPT配乐片单_汇总']
for p,t in zip(sorted(R.glob('Weixin*.png')),titles):move(p.name,'归档/01_最新要求_20261014/'+t+'.png')
for p in list(R.glob('电影*.pdf')):
 name=p.name.replace('(1)','');move(p.name,'归档/02_课堂讲义_2021/2021_'+name)
for p in list(R.glob('爱情*.pdf')):move(p.name,'归档/03_参考展示与论文/参考论文_爱乐之城_电影音乐创作运用浅析.pdf')
move('《千与千寻》电影音乐鉴赏论文.md','归档/03_参考展示与论文/参考论文_千与千寻_电影音乐鉴赏.md')
move('关于制作思路、准备经验与现场细节.md','归档/04_评论与展示经验/同学经验_制作思路与现场细节.md')
move('46DDD5E4C7624E03EC8F8FCCD976DBE9.png','归档/05_历史作业/历史作业_喜爱影片与配乐作用.png')
move('QQ捞人.png','归档/07_其他历史图片/历史截图_QQ联系人.png')
for n in ['电影艺术与音乐_图片资料整理.md','weixin_ocr.json']:move(n,'归档/06_历史整理_20260921/'+n)
for n in ['ocr_weixin.py','整理weixin资料.py','organize_album.py']:move(n,'归档/08_历史工具/'+n)
# Existing 42-image archive keeps its paths; index joins it with current sources.
for p in sorted((R/'归档/Weixin图片').glob('*.png')):
 records.append({'原路径':str(p.relative_to(R)).replace('\\','/'),'新路径':str(p.relative_to(R)).replace('\\','/'),'SHA256':hashlib.sha256(p.read_bytes()).hexdigest(),'核验':'原位保留'})
(R/'整理资料/文件变更清单.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
with (R/'整理资料/文件变更清单.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['原路径','新路径','SHA256','核验']);w.writeheader();w.writerows(records)
old=(R/'归档/06_历史整理_20260921/电影艺术与音乐_图片资料整理.md').read_text(encoding='utf-8')
(R/'整理资料/历史截图整理_整合阅读版.md').write_text('> 历史资料：2026-09-21 整理的42张截图。考核信息请以本次10张最新截图及《最新要求核对》为准；原文单独保存。\n\n'+old.replace('](归档/','](../归档/'),encoding='utf-8')
ocr=json.loads((R/'整理资料/文字提取/新增截图_OCR.json').read_text(encoding='utf-8'))
mp={x['原路径']:x['新路径'] for x in records}
text=['# 新增截图逐图文字\n\n自动OCR原文，保留错字；标题和考核摘要另经原图核对。QQ联系人截图涉及个人信息，仅保留本地JSON，不编入学习阅读版。\n']
for p in ocr:
 p['current_path']=mp[p['original']]
 if p['original']=='QQ捞人.png':continue
 text.append('\n## ['+Path(p['current_path']).stem+'](../../'+p['current_path'].replace(' ','%20')+')\n\n原文件名：'+p['original']+'\n\n'+'\n\n'.join(x['text'] for x in p['lines']))
(R/'整理资料/文字提取/新增截图逐图文字.md').write_text('\n'.join(text),encoding='utf-8')
(R/'整理资料/文字提取/新增截图_OCR.json').write_text(json.dumps(ocr,ensure_ascii=False,indent=2),encoding='utf-8')
# Source labels for extracted PDFs.
for p in (R/'整理资料/文字提取').glob('电影*.md'):
 t=p.read_text(encoding='utf-8');p.write_text('> 2021年旧讲义：仅作课程知识参考，不能据此确定本次考核要求。\n\n'+t,encoding='utf-8')
print('verified records',len(records),'historical images',len(list((R/'归档/Weixin图片').glob('*.png'))))
