from pathlib import Path
import json, re, hashlib, shutil, urllib.request, concurrent.futures, datetime

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / '参考资料'
REF.mkdir(exist_ok=True)
records=[]
for name, dest in [('展示重做_20261019/研究','参考资料/阅读记录')]:
    src=ROOT/name; target=ROOT/dest; target.mkdir(parents=True,exist_ok=True)
    if src.exists():
        for p in src.glob('*.md'):
            if p.name == '阅读记录已迁移.md': continue
            out=target/p.name
            if out.exists(): raise RuntimeError(str(out))
            digest=hashlib.sha256(p.read_bytes()).hexdigest()
            shutil.move(str(p),str(out))
            assert hashlib.sha256(out.read_bytes()).hexdigest()==digest
            records.append({'原路径':str(p.relative_to(ROOT)),'现路径':str(out.relative_to(ROOT)),'sha256':digest})
        (src/'阅读记录已迁移.md').write_text('# 阅读记录\n\n统一移至[参考资料／阅读记录](../../参考资料/阅读记录/课堂定向文献阅读.md)。\n',encoding='utf-8')
if records:
    (REF/'目录调整记录.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
sources=json.loads((ROOT/'展示重做_20261019/工具/sources.json').read_text(encoding='utf-8-sig'))
sources.update({
'D02':'交织事实与想象的历史隐喻；此前仅检索摘录 https://movie.douban.com/review/2994478/',
'S01':'Ni 2021 https://www.atlantis-press.com/article/125957625.pdf',
'S02':'Venzheha 2023/2024 https://thesis.unipd.it/retrieve/3d2a7d4e-78cf-4df5-b6b2-fc438ca9f4c7/Venzheha_Oksana.pdf',
'S03':'Yu and Ahn 2025 https://dergipark.org.tr/en/download/article-file/4740203',
'S04':'Chattah Film Music Cognition to Interpretation；此前仅可见局部 https://www.researchgate.net/publication/376362840_Film_Music_Cognition_to_Interpretation',
'S05':'制作名单二手转录 https://hans-zimmer.com/product/the-last-emperor/',
'X01':'Los Angeles Times；此前只见条目信息 https://www.latimes.com/archives/la-xpm-1987-11-20-ca-15017-story.html',
'X02':'Guardian Bradshaw https://www.theguardian.com/film/2018/nov/26/bernardo-bertolucci-last-tango-paris-brilliant-last-emperor-of-highbrow-cinema',
'X03':'Rotten Tomatoes；检索入口 https://www.rottentomatoes.com/m/last_emperor',
'X04':'Mix；此前403及检索摘录 https://www.mixonline.com/recording/ryuichi-sakamoto-374280'})
raw=REF/'原文留存'; raw.mkdir(exist_ok=True)
for old, ident in [('Ni2021.pdf','S01'),('YuAhn2025.pdf','S03')]:
    p=ROOT/'展示重做_20261019/build/literature'/old
    if p.exists(): shutil.copy2(p,raw/(ident+'.pdf'))
def fetch(pair):
    ident, description=pair
    match=re.search(r'https?://\S+',description)
    row={'id':ident,'书目信息':description,'本次保存时间':datetime.datetime.now().astimezone().isoformat()}
    if not match:
        row['状态']='本地资料，保留原归档'; return row
    url=match.group(); row['url']=url
    existing=raw/(ident+'.pdf')
    try:
        if existing.exists():
            data=existing.read_bytes(); p=existing; row['状态']='已保存PDF原件'
        else:
            req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req,timeout=18) as r:
                data=r.read(); content_type=r.headers.get('Content-Type',''); row['最终URL']=r.url
            suffix='.pdf' if data.startswith(b'%PDF') else '.html'
            p=raw/(ident+suffix); p.write_bytes(data)
            row['状态']='已保存响应；网页正文与拦截页需区分' if suffix=='.html' else '已保存PDF原件'
            row['Content-Type']=content_type
        row.update({'文件':str(p.relative_to(ROOT)).replace('\\','/'),'字节':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    except Exception as e: row['状态']='本次获取失败'; row['错误']=str(e)
    return row
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool: rows=list(pool.map(fetch,sources.items()))
(REF/'来源登记.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# 文献、访谈与评论留存','', '2026-10-19整理。来源编号与展示 sources.json 对应，新增研究为S01—S05，补充检索入口为X01—X04。下载成功只表示取得响应；网页是否为正文另见下方核验。此前仅读检索摘录的来源，不因保存网页而改记成全文阅读。','', '论文与评论的阅读范围及取舍见[课堂定向文献阅读](阅读记录/课堂定向文献阅读.md)及[评论阅读与取舍](../展示重做_20261019/交付/参考资料/评论阅读与取舍.md)。','', '|编号|来源与地址|保存状态|','|---|---|---|']
for r in rows:
    location=f"[本地响应](../{r['文件']})" if '文件' in r else r.get('错误','原位置保留')
    lines.append(f"|{r['id']}|{r['书目信息']}|{r['状态']}；{location}|")
lines+=['','原始响应及PDF保存在本目录的“原文留存”。文件大小、SHA-256及失败原因保存在来源登记.json。没有正文的来源保留入口与获取记录，不用二手转述补造原文。']
(REF/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'移动文档':len(records),'登记来源':len(rows),'保存响应':sum('文件' in x for x in rows)},ensure_ascii=False))
