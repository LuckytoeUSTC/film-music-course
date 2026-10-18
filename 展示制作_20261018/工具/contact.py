from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[2]/'展示制作_20261018'
files=sorted((root/'截图').glob('*.jpg'))
sheet=Image.new('RGB',(1280,210* ((len(files)+2)//3)), '#eeeeee')
draw=ImageDraw.Draw(sheet)
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',16)
for i,f in enumerate(files):
 im=Image.open(f);im.thumbnail((420,178));x=(i%3)*426;y=(i//3)*210
 sheet.paste(im,(x,y));draw.text((x+5,y+180),f.stem,fill='black',font=font)
sheet.save(root/'build'/'frames_contact.jpg')
