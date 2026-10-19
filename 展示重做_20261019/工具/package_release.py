from pathlib import Path
import json,shutil,hashlib,zipfile
R=Path(__file__).resolve().parents[1];O=R/'交付';base=R.parent/'发布包';pkg=base/'末代皇帝_课堂展示_20261019';pkg.mkdir(parents=True,exist_ok=True)
shutil.copy2(O/'听见末代皇帝_音乐赏析.pptx',pkg/'末代皇帝.pptx')
shutil.copy2(O/'听见末代皇帝_静态备份.pdf',pkg/'末代皇帝.pdf')
media=pkg/'媒体';media.mkdir(exist_ok=True)
slides=json.loads((R/'工具/slides.json').read_text(encoding='utf-8'));names=sorted({d[k] for d in slides for k in ['media','secondMedia'] if d.get(k)})
for n in names:shutil.copy2(O/'媒体'/n,media/n)
(pkg/'使用说明.txt').write_text('''末代皇帝课堂展示包

解压整个ZIP到本地文件夹，推荐用Windows版Microsoft PowerPoint打开“末代皇帝.pptx”。
封面点击画面播放37秒开场片段并置，后续页面点击画面或封面播放相应音视频。音视频已内嵌PPT；媒体文件夹保留独立文件，遇到播放问题时可直接打开。
PDF是静态备用，不含可播放媒体。用PDF展示时，可按需打开媒体文件夹。
请拷贝整个文件夹，不从ZIP预览中直接运行。该包只含正式页面引用的媒体，其他备用片段及研究资料留在项目仓库。
开场是经过重新编排的片段，保留各段原声，无新增配乐；分析声画关系时回到后面的原片段。
备注以丁、段标明提示词，互动共同主持。当前内容保留供审核，尚未删去你们未决定舍弃的主题。
已核验：PowerPoint打开、PDF导出、开场完整解码、嵌入媒体与文件一致。尚需：实际听辨、点击播放、排练和课堂设备试播。
''',encoding='utf-8')
rows=[]
for p in sorted(pkg.rglob('*')):
 if p.is_file():rows.append({'文件':str(p.relative_to(pkg)).replace('\\','/'),'字节':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(pkg/'文件校验.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
archive=base/'TheLastEmperor-Classroom-20261019.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=3) as z:
 for p in pkg.rglob('*'):
  if p.is_file():z.write(p,str(p.relative_to(base)))
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 for row in rows:assert hashlib.sha256(z.read(pkg.name+'/'+row['文件'])).hexdigest()==row['sha256']
report={'发布包':str(archive.relative_to(R.parent)),'ZIP字节':archive.stat().st_size,'ZIP_SHA256':hashlib.sha256(archive.read_bytes()).hexdigest(),'媒体文件数':len(names),'文件逐项哈希核对':True,'ZIP完整性检查':True,'说明':'发布包已生成；实际播放与课堂设备仍需试播'}
(R/'制作记录/发布包核验.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(report)
