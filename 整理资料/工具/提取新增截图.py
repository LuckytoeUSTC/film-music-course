import sys,json
from pathlib import Path
root=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root/'.ocrdeps'))
from rapidocr_onnxruntime import RapidOCR
ocr=RapidOCR();results=[]
manifest=json.loads((root/'整理资料/文件变更清单.json').read_text(encoding='utf-8'))
inputs=[x for x in manifest if x['原路径'].endswith('.png') and '/' not in x['原路径']]
for item in inputs:
 p=root/item['新路径']
 r,_=ocr(str(p));lines=[{'text':a[1],'confidence':round(float(a[2]),3),'box':a[0]} for a in (r or [])]
 results.append({'original':item['原路径'],'current_path':item['新路径'],'lines':lines});print(p.name,len(lines),flush=True)
 (root/'整理资料/文字提取/新增截图_OCR.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
