from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
r=Path(__file__).resolve().parents[2]/'展示制作_20261018'/'build'
fs=sorted((r/'renders').glob('*.png'))
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',16)
for base in range(0,len(fs),12):
 subset=fs[base:base+12];sheet=Image.new('RGB',(1280,265*((len(subset)+2)//3)),'#ddd');dr=ImageDraw.Draw(sheet)
 for i,p in enumerate(subset):
  im=Image.open(p);im.thumbnail((420,236));x=i%3*426;y=i//3*265;sheet.paste(im,(x,y));dr.text((x+5,y+238),p.stem,fill='black',font=font)
 sheet.save(r/f'slides_contact_{base//12+1}.jpg')
