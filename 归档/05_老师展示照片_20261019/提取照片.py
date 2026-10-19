import sys,json
from pathlib import Path
sys.path.insert(0,str(Path('.ocrdeps').resolve()))
from rapidocr_onnxruntime import RapidOCR
ocr=RapidOCR();r=Path('归档/05_老师展示照片_20261019');rows=[]
files=list((r/'原件/末代皇帝').glob('*.jpg'))+list((r/'阅读图').glob('*.jpg'))
for p in sorted(files):
 result,_=ocr(str(p));rows.append({'file':p.name,'lines':[{'text':x[1],'confidence':round(float(x[2]),3),'box':x[0]} for x in result or []]});print(p.name,len(result or []),flush=True)
(r/'照片OCR原始.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
