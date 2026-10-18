from pathlib import Path
import json,shutil,hashlib
root=Path(__file__).resolve().parent
workspace=root.parent
tools=root/'工具';tools.mkdir(exist_ok=True)
names=['build_delivery.py','build_media.py','contact.py','embed_media.py','extra_frames.py','make_clips.py','prepare_portable.py','signal_match.py','slide_contact.py','verify_media.py','verify_powerpoint.ps1']
changes=[]
for name in names:
 src=workspace/'tmp'/name;dest=tools/name
 if not src.exists():continue
 raw=src.read_text(encoding='utf-8')
 if name=='build_media.py':raw=raw.replace('ROOT=Path(__file__).resolve().parents[1]','ROOT=Path(__file__).resolve().parents[2]')
 elif name.endswith('.py'):raw=raw.replace("Path(__file__).resolve().parents[1]/'展示制作_20261018'","Path(__file__).resolve().parents[2]/'展示制作_20261018'")
 else:raw=raw.replace("Join-Path $PSScriptRoot '..\\展示制作_20261018'","Join-Path $PSScriptRoot '..'")
 dest.write_text(raw,encoding='utf-8')
 changes.append({'from':str(src.relative_to(workspace)),'to':str(dest.relative_to(workspace)),'sha256_before':hashlib.sha256(src.read_bytes()).hexdigest(),'sha256_after':hashlib.sha256(dest.read_bytes()).hexdigest(),'change':'调整脚本位置并修正相对路径'})
 src.unlink() # only explicitly listed task-created scripts
for name in ['build_deck.mjs','finalize.mjs','slides.json','sources.json']:
 src=root/'build'/name
 shutil.copy2(src,tools/name)
(root/'制作记录'/'整理清单.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8')
progress=root/'制作记录'/'进度.md'
progress.write_text(progress.read_text(encoding='utf-8')+'''\n## 初稿交付检查完成（2026-10-18）\n\n- 23页PPT已用PowerPoint只读打开、导出23页并逐页目视检查；识别8个嵌入音视频。\n- PDF为PowerPoint导出，23页均含文本。\n- 13段视频、4段音频均完成全长解码，无报错。\n- 离线HTML静态资源链接检查通过；尚未实测浏览器播放与PPT放映中的点击播放。\n- 当前为可审阅初稿，不能宣称音频听辨和现场排练全部完成。\n- 用户明确授权保持GitHub公开，上传完整成果；邮件测控有效期2天，定时摘要关闭。\n''',encoding='utf-8')
readme=root/'交付'/'开始阅读.md'
text=readme.read_text(encoding='utf-8').replace('PPT媒体已嵌入并做文件结构检查；实际PowerPoint播放行为与课堂音箱效果需现场试播。','PPT已在本机PowerPoint只读打开并逐页检查导出图，8个嵌入媒体获识别；点击播放行为与课堂音箱效果仍需现场试播。')
text=text.replace('当前包无成员姓名，也未上传、发布或发群。','展示成品使用成员A/B，不含成员姓名。用户已授权公开上传GitHub；未向教师或课程群发送。')
readme.write_text(text,encoding='utf-8')
print('organized',len(changes),'scripts')
