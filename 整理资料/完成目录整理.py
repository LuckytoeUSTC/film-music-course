from pathlib import Path
from html.parser import HTMLParser
import json,re,hashlib
R=Path(__file__).resolve().parents[1]; ref=R/'参考资料'
class Text(HTMLParser):
    def __init__(self): super().__init__();self.skip=0;self.parts=[]
    def handle_starttag(self,t,a):
        if t in ('script','style'):self.skip+=1
    def handle_endtag(self,t):
        if t in ('script','style'): self.skip=max(0,self.skip-1)
    def handle_data(self,d):
        if not self.skip and d.strip():self.parts.append(d.strip())
rows=json.loads((ref/'来源登记.json').read_text(encoding='utf-8'))
texts=ref/'网页提取';texts.mkdir(exist_ok=True)
for x in rows:
    if x.get('文件','').endswith('.html'):
        p=R/x['文件'];parser=Text();parser.feed(p.read_text(encoding='utf-8',errors='replace')); text='\n'.join(parser.parts)
        out=texts/(x['id']+'.txt');out.write_text(text,encoding='utf-8')
        x['提取文本']=str(out.relative_to(R)).replace('\\','/')
        blocked=any(w in text.lower() for w in ('sec.douban.com','异常请求','有异常请求','豆瓣安全验证','captcha')) and len(text)<3000
        x['状态']='已保存拦截页，未取得正文' if blocked else '已保存网页与文字提取；未据此新增全文阅读声明'
        print(x['id'],len(text),text[:110].replace('\n',' '))
    elif x.get('文件','').endswith('.pdf'):
        import fitz
        d=fitz.open(R/x['文件']);x['PDF页数']=len(d);out=texts/(x['id']+'.txt')
        out.write_text('\n\n'.join(f'--- PDF第{i+1}页 ---\n'+p.get_text() for i,p in enumerate(d)),encoding='utf-8')
        x['提取文本']=str(out.relative_to(R)).replace('\\','/')
        if x['id']=='S02':x['说明']='本轮已成功取得机构库PDF；此前403记录见阅读记录，下载成功不表示新增完成逐谱视读。'
(ref/'来源登记.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# 参考资料：原文、评论与阅读记录','', '更新：2026-10-19。30项来源统一登记；网页响应、正文、检索摘录和获取失败分别记录。新增下载不等于新增全文阅读。','', '先读[课堂定向文献阅读](阅读记录/课堂定向文献阅读.md)，再查[评论阅读与取舍](../展示重做_20261019/交付/参考资料/评论阅读与取舍.md)。课程讲义原件仍在[2021讲义目录](../归档/02_课堂讲义_2021)，老师提供的照片仍在[照片归档](../归档/05_老师展示照片_20261019/照片提取与批注整理.md)。','', '|编号|来源|本地留存|','|---|---|---|']
for x in rows:
    links=[]
    for key in ('文件','提取文本'):
        if key in x:links.append(f"[{key}](../{x[key]})")
    lines.append(f"|{x['id']}|{x['书目信息']}|{x['状态']} {' / '.join(links)}|")
lines+=['','原始文件与文字提取均保留在本目录。HTML提取包含导航等杂项，不冒称精校正文。访问失败的来源保留地址、错误与此前阅读范围，不用转述补造全文。大小、哈希、页数及获取时间见[来源登记](来源登记.json)。','', '本地已有课程论文、展示稿和经验材料继续保留在归档/03_参考展示与论文及归档/04_评论与展示经验；此次没有移动或删去原件。']
(ref/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
mapping=[]
for name in ('课堂定向文献阅读.md','重做依据与资料口径.md'):
    p=ref/'阅读记录'/name;mapping.append({'原路径':'展示重做_20261019/研究/'+name,'现路径':'参考资料/阅读记录/'+name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(ref/'目录调整记录.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2),encoding='utf-8')
pointer=ref/'阅读记录/阅读记录已迁移.md'
if pointer.exists():pointer.unlink()
note=ref/'阅读记录/课堂定向文献阅读.md'
s=note.read_text(encoding='utf-8');s=s.replace('已读网络工具返回的PDF相关正文：PDF第32—44页，对应印刷p.32—44，注意该PDF封面后标页有偏移，引用以页面显示的印刷页码为准。谱例截图请求及本地下载403，未声称完成逐音视读。','此前已读网络工具返回的§3.1.1相关正文；页序与印刷页码不混用。早先谱例截图请求及下载403，本轮原文归档成功保存了机构库PDF，但尚未新增完成逐音视读。')
s=s.replace('谱例页尚未取得','谱例尚待逐音核对');note.write_text(s,encoding='utf-8')
(R/'README.md').write_text('''# 《末代皇帝》电影音乐展示

更新：2026-10-19。当前使用《听见末代皇帝》28页新版。本轮补入课堂理论与片段的论证文稿，统一保存参考论文、访谈和评论，并将旧版与当前阅读入口分开。

## 最新内容，先读这里

1. [课堂要点与片段论证](展示重做_20261019/交付/课堂要点与片段论证.md)：从两次追赶、雨中离开与晚年重访，解释主题、声画关系、心理功能与声音剪辑；末尾对照全部页面与讲义。
2. [展示设计与证据说明](展示重做_20261019/交付/展示设计与证据说明.md)：为什么这样选片段、怎样组织音频和画面、评论参与什么论证。
3. [参考资料总目录](参考资料/README.md)：研究、访谈、影评的原始响应、文字提取、阅读范围及获取失败记录。
4. [新版展示包说明](展示重做_20261019/交付/开始阅读.md)、[PPT](展示重做_20261019/交付/听见末代皇帝_音乐赏析.pptx)、[静态PDF](展示重做_20261019/交付/听见末代皇帝_静态备份.pdf)。

文稿采用从具体场面进入、逐层限定判断的表达。没有补造组员的观影感受。双人逐页讲稿保留为排练材料，阅读以两篇新文稿为主。

## 目录怎么用

|目录|用途|
|---|---|
|展示重做_20261019/交付|当前28页PPT、PDF、阅读文稿、音视频与离线页面|
|参考资料|来源总登记、原文留存、网页提取、研究阅读记录|
|展示重做_20261019/工具、制作记录|可复现制作文件与核验结果|
|展示制作_20261018|此前23页版本，供历史比较|
|归档|考核要求、讲义、参考展示、经验与老师提供的照片原件|
|整理资料|文字提取、索引、文件调整与核验记录|

当前PPT共28页，13段独立视频、8段音频；主讲预算约36分钟。文件结构、页面和解码检查已完成，音乐精确起止、旋律与乐器辨认及课堂设备播放仍需实际回听、试播。初稿上传不代表整项目已经结束。

更多资料见[完整导航](README_资料导航.md)。D盘原始电影、字幕、书签与原声未改动。观影书签仅作定位，不能作为严格音乐起点。第三方材料权利归原权利人。
''',encoding='utf-8')
nav=R/'README_资料导航.md';old=nav.read_text(encoding='utf-8');tail=old[old.index('## 统一资料目录'):]
tail=tail.replace('## 来源与文件安全','## 既有归档说明（历史记录）')
nav.write_text('''# 电影音乐艺术课资料导航

更新：2026-10-19。新版内容在前，历史资料在后。

## 当前展示与阅读

- [课堂要点与片段论证](展示重做_20261019/交付/课堂要点与片段论证.md)
- [展示设计与证据说明](展示重做_20261019/交付/展示设计与证据说明.md)
- [28页新版展示包](展示重做_20261019/交付/开始阅读.md)
- [统一参考资料目录](参考资料/README.md)、[课堂定向阅读](参考资料/阅读记录/课堂定向文献阅读.md)、[重做依据](参考资料/阅读记录/重做依据与资料口径.md)
- [老师提供照片的提取与批注](归档/05_老师展示照片_20261019/照片提取与批注整理.md)
- [旧23页展示包](展示制作_20261018/交付/开始阅读.md)：历史版本，不作为当前交付入口。

## 要求与准备资料

- [最新考核要求核对](整理资料/最新要求核对.md)
- [课堂内容与参考分析索引](整理资料/课堂内容与参考分析索引.md)
- [观影记录模板](整理资料/观影记录模板.md)、[早期双人准备计划](整理资料/末代皇帝_双人准备计划.md)

'''+tail,encoding='utf-8')
start=R/'展示重做_20261019/交付/开始阅读.md';s=start.read_text(encoding='utf-8');s=s.replace('## 从这里开始','''## 先读论证，再排练

本轮新增[课堂要点与片段论证](课堂要点与片段论证.md)与[展示设计与证据说明](展示设计与证据说明.md)。前者详细对应课堂理论，后者解释选材和组织。逐页讲稿仍供双人分工使用。

研究阅读记录与下载原文统一见[参考资料总目录](../../参考资料/README.md)。

## 打开展示''');start.write_text(s,encoding='utf-8')
# 修复已迁移正文的已知旧链接；历史归档原件不作全局替换。
for p in [R/'README.md',nav,start,*list((R/'展示重做_20261019/交付').glob('*.md'))]:
    s=p.read_text(encoding='utf-8')
    s=s.replace('../研究/重做依据与资料口径.md','../../参考资料/阅读记录/重做依据与资料口径.md')
    p.write_text(s,encoding='utf-8')
print('完成：目录、来源登记、导航、两篇阅读文稿')
