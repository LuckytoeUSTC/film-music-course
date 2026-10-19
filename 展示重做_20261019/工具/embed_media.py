from pathlib import Path
import zipfile,json,re,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1]
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships','p14':'http://schemas.microsoft.com/office/powerpoint/2010/main'}
for a,b in NS.items():E.register_namespace(a,b)
def el(n,attrs={}):return E.Element('{'+NS[n.split(':')[0]]+'}'+n.split(':')[1],attrs)
z=zipfile.ZipFile(ROOT/'build'/'candidate.pptx')
files={n:z.read(n) for n in z.namelist()}
relsns='http://schemas.openxmlformats.org/package/2006/relationships'
ctns='http://schemas.openxmlformats.org/package/2006/content-types'
ct=E.fromstring(files['[Content_Types].xml'])
for ext,typ in [('mp4','video/mp4'),('m4a','audio/mp4')]:
 if not any(x.get('Extension')==ext for x in ct):E.SubElement(ct,'{'+ctns+'}Default',Extension=ext,ContentType=typ)
for n,m in enumerate(json.loads((ROOT/'build'/'media_map.json').read_text(encoding='utf-8')),1):
 slidepath=f'ppt/slides/slide{m["slide"]}.xml';relpath=f'ppt/slides/_rels/slide{m["slide"]}.xml.rels'
 s=E.fromstring(files[slidepath]);rr=E.fromstring(files[relpath]);kind=m['kind'];src=ROOT/'交付'/'媒体'/m['file']
 if not src.exists():raise FileNotFoundError(src)
 media_name=f'embedded{n}{src.suffix}';files['ppt/media/'+media_name]=src.read_bytes()
 rid='rIdMediaFile'+str(n);rid2='rIdOfficeMedia'+str(n)
 E.SubElement(rr,'{'+relsns+'}Relationship',Id=rid,Type=NS['r']+'/'+kind,Target='../media/'+media_name)
 E.SubElement(rr,'{'+relsns+'}Relationship',Id=rid2,Type='http://schemas.microsoft.com/office/2007/relationships/media',Target='../media/'+media_name)
 pics=s.findall('.//p:pic',NS)
 # Artifact Tool exports image names as empty; map by known authored image order.
 matches=[pics[1 if m['name'].endswith('_b') else 0]] if pics else []
 if len(matches)!=1:raise RuntimeError((m,len(matches),[p.find('p:nvPicPr/p:cNvPr',NS).attrib for p in s.findall('.//p:pic',NS)]))
 pic=matches[0];cn=pic.find('p:nvPicPr/p:cNvPr',NS);spid=cn.get('id');cn.set('name',m['name'])
 cn.append(el('a:hlinkClick',{'action':'ppaction://media'}))
 nv=pic.find('p:nvPicPr/p:nvPr',NS)
 nv.append(el('a:'+kind+'File',{'{'+NS['r']+'}link':rid}))
 extlst=el('p:extLst');ext=el('p:ext',{'uri':'{DAA4B4D4-5B9D-4661-A4F6-83A2F4AD3B91}'});ext.append(el('p14:media',{'{'+NS['r']+'}embed':rid2}));extlst.append(ext);nv.append(extlst)
 timing=s.find('p:timing',NS)
 if timing is None:
  timing=el('p:timing');s.append(timing);lst=el('p:tnLst');timing.append(lst);par=el('p:par');lst.append(par);root=el('p:cTn',{'id':'1','dur':'indefinite','restart':'never','nodeType':'tmRoot'});par.append(root);root.append(el('p:childTnLst'))
 ch=timing.find('.//p:childTnLst',NS);node=el('p:'+kind);cm=el('p:cMediaNode',{'vol':'80000'});node.append(cm);tn=el('p:cTn',{'id':str(n+1),'fill':'hold','display':'0'});cm.append(tn);condlist=el('p:stCondLst');condlist.append(el('p:cond',{'delay':'indefinite'}));tn.append(condlist);tgt=el('p:tgtEl');tgt.append(el('p:spTgt',{'spid':spid}));cm.append(tgt);ch.append(node)
 files[slidepath]=E.tostring(s,encoding='utf-8',xml_declaration=True);files[relpath]=E.tostring(rr,encoding='utf-8',xml_declaration=True)
 print(m['slide'],m['file'],len(files['ppt/media/'+media_name]),flush=True)
E.register_namespace('',ctns)
files['[Content_Types].xml']=E.tostring(ct,encoding='utf-8',xml_declaration=True)
with zipfile.ZipFile(ROOT/'build'/'candidate_media.pptx','w',zipfile.ZIP_DEFLATED) as out:
 for n,b in files.items():out.writestr(n,b)
