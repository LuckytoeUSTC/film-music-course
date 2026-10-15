"""Batch OCR for Weixin screenshots; keep ordered per-image results in JSON.

Install dependency into a local directory first:
  python -m pip install rapidocr_onnxruntime --target .ocrdeps
Then set PYTHONPATH=.ocrdeps when running this script.
"""
import json
import re
from pathlib import Path

from rapidocr_onnxruntime import RapidOCR

ROOT = Path(__file__).resolve().parent
IMAGES = list(ROOT.glob("Weixin*.png")) or list((ROOT / "归档" / "Weixin图片").glob("Weixin*.png"))
IMAGES.sort(key=lambda p: int(re.search(r"_(\d+)_366\.png$", p.name).group(1)))
ocr = RapidOCR()
pages = []
for i, path in enumerate(IMAGES, 1):
    result, _ = ocr(str(path))
    lines = [{"text": x[1], "confidence": round(float(x[2]), 3)} for x in (result or [])]
    pages.append({"file": path.name, "lines": lines})
    print(f"{i}/{len(IMAGES)} {path.name}: {len(lines)} lines", flush=True)
(ROOT / "weixin_ocr.json").write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding="utf-8")
