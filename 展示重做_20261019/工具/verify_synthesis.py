from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as E
import json,re,hashlib,posixpath
R=Path(__file__).resolve().parents[1];O=R/'交付';root=R.parent
slides=json.loads((R/'工具/slides.json').read_text(encoding='utf-8'))
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def contents(z):
    rels=E.fromstring(z.read('ppt/_rels/presentation.xml.rels'));mapping={e.get('Id'):e.get('Target') for e in rels}
    pres=E.fromstring(z.read('ppt/presentation.xml'))
    for node in pres.findall('p:sldIdLst/p:sldId',ns):
        target=mapping[node.get('{'+ns['r']+'}id')];name=posixpath.normpath(posixpath.join('ppt',target)) if not target.startswith('/') else target[1:]
        yield name,E.fromstring(z.read(name))
with ZipFile(O/'听见末代皇帝_音乐赏析.pptx') as z,ZipFile(R/'build/合成乐修订/before.pptx') as before:
    pages=list(contents(z));assert len(pages)==30
    for i,(name,doc) in enumerate(pages):
        text=''.join(t.text or '' for t in doc.findall('.//a:t',ns)); assert slides[i]['title'] in text,(i,text)
        relpath=posixpath.join(posixpath.dirname(name),'_rels',posixpath.basename(name)+'.rels');rel=E.fromstring(z.read(relpath))
        note=next(e.get('Target') for e in rel if e.get('Type').endswith('/notesSlide'))
        note=posixpath.normpath(posixpath.join(posixpath.dirname(name),note)) if not note.startswith('/') else note[1:]
        doc=E.fromstring(z.read(note));body=next(s for s in doc.findall('.//p:sp',ns) if any(ph.get('type')=='body' for ph in s.findall('.//p:ph',ns)))
        text=''.join(t.text or '' for t in body.findall('.//a:t',ns))
        assert text==slides[i]['notes'],(i,text)
        assert not re.search(r'预算|分钟|讲者[AB]',text),i
    def mediahash(zz):return sorted(hashlib.sha256(zz.read(n)).hexdigest() for n in zz.namelist() if n.startswith('ppt/media/') and n.lower().endswith(('.mp4','.m4a','.mp3','.wav','.aac')))
    old=mediahash(before);new=mediahash(z);assert all(new.count(h)>=old.count(h) for h in old),(len(old),len(new))
    assert hashlib.sha256((O/'媒体/00_开场_追赶离开重访.mp4').read_bytes()).hexdigest() in new
import fitz
assert len(fitz.open(O/'听见末代皇帝_静态备份.pdf'))==30
html=(O/'离线展示.html').read_text(encoding='utf-8');assert "预算 '+s.minutes" not in html
bad=[]
for p in [root/'README.md',root/'README_资料导航.md',*O.glob('*.md')]:
    for u in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
        if not u.startswith(('http:','https:','#')) and not (p.parent/u).exists():bad.append([str(p),u])
assert not bad,bad
result={'PPT页数':30,'PDF页数':30,'备注与源文件一致':True,'备注无时间估计':True,'嵌入音视频文件数':len(new),'既有音视频哈希未改变，新增开场已嵌入':True,'链接异常':bad,'视觉检查':'新增22、23页及修改9页已通过PowerPoint导出目视检查；其余沿用原版式并更新页码','未验证':'本地实际听辨、点击播放、每轮实际时长和课堂设备'}
(R/'制作记录/合成乐与双人分工核验.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(result)
