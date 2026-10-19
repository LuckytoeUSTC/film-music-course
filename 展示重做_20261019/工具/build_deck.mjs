import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Presentation,PresentationFile} from 'file:///C:/Users/lucky/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const sourceDir=path.dirname(fileURLToPath(import.meta.url));
const root=path.dirname(sourceDir);const here=path.join(root,'build');const out=path.join(root,'交付');
const data=JSON.parse(await fs.readFile(path.join(sourceDir,'slides.json'),'utf8'));
const sources=JSON.parse(await fs.readFile(path.join(sourceDir,'sources.json'),'utf8'));
const deck=Presentation.create({slideSize:{width:1280,height:720}});
const paper='#F1E7D3',muted='#B5AD9D',gold='#D5B16B';
await fs.mkdir(path.join(here,'renders'),{recursive:true});
let media=[];
function text(slide,str,x,y,w,h,size=30,color=paper,bold=false,name=''){
 const sh=slide.shapes.add({name,geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 sh.text=str;sh.text.style={fontSize:size,typeface:'Microsoft YaHei',color,bold,autoFit:'none',insets:0,verticalAlignment:'top'};return sh;
}
async function image(slide,file,x,y,w,h,name=''){
 const buf=await fs.readFile(file);
 return slide.images.add({name,blob:buf.buffer.slice(buf.byteOffset,buf.byteOffset+buf.byteLength),contentType:'image/jpeg',alt:name||path.basename(file),fit:'contain',position:{left:x,top:y,width:w,height:h}});
}
for(let i=0;i<data.length;i++){
 const d=data[i],s=deck.slides.add();s.background.fill='#171714';
 const images=(d.images||[]).map(f=>path.join(root,'截图',f));
 if(d.layout==='cover'){
  await image(s,images[0],0,0,1280,495);
  if(d.media)media.push({slide:i+1,name:'MEDIA_'+i,file:d.media,kind:'video'});
  text(s,d.title,60,535,1160,75,56,paper,true);
  text(s,d.subtitle,62,625,1160,50,32,gold);
 }else{
  text(s,d.title,60,42,1160,72,44,paper,true);
  if(d.layout==='video'){
   const nm='MEDIA_'+i;await image(s,images[0],60,145,800,450,nm);
   d.body.forEach((a,k)=>text(s,a,910,180+k*165,300,140,30));
   text(s,'点击画面播放　'+d.media.replace('.mp4',''),60,626,1100,40,24,gold);
   media.push({slide:i+1,name:nm,file:d.media,kind:'video'});
  }else if(d.layout==='hero'){
   const nm=d.media?'MEDIA_'+i:'';await image(s,images[0],60,125,1160,430,nm);
   d.body.forEach((a,k)=>text(s,a,70,575+k*47,1140,45,30));
   if(d.media)media.push({slide:i+1,name:nm,file:d.media,kind:'audio'});
  }else if(d.layout==='audio'){
   await image(s,images[0],60,135,700,390,'MEDIA_'+i);
   d.body.forEach((a,k)=>text(s,a,810,170+k*145,400,125,29));
   text(s,'点击画面播放原声摘录',60,605,1160,45,24,gold);
   media.push({slide:i+1,name:'MEDIA_'+i,file:d.media,kind:'audio'});
  }else if(d.layout==='triple'){
   for(let k=0;k<3;k++){
    await image(s,images[k],60+k*395,160,370,210);
    text(s,d.captions[k],60+k*395,393,370,70,22,gold);
   }
   text(s,d.body[0],60,510,1160,105,34);
  }else if(d.layout==='pair'){
   for(let k=0;k<2;k++){
    await image(s,images[k],60+k*590,155,550,255);
    text(s,d.captions[k],60+k*590,438,550,55,25,gold);
   }
   d.body.forEach((a,k)=>text(s,a,60,520+k*65,1160,60,31));
  }else if(d.layout==='split'){
   await image(s,images[0],60,145,650,430);
   d.body.forEach((a,k)=>text(s,a,760,155+k*92,450,80,29));
  }else if(d.layout==='audioPair'){
   d.body.forEach((a,k)=>text(s,a,60,140+k*64,1160,60,30));
   const cover='D:/__Netdisk Download/The Last Emperor/The Last Emperor (square).jpg';
   await image(s,cover,80,370,230,230,'MEDIA_'+i);
   await image(s,cover,680,370,230,230,'MEDIA_'+i+'_b');
   text(s,'A　Theme Variation 2',340,410,310,110,28,gold);
   text(s,'B　Theme',940,410,270,110,28,gold);
   text(s,'点击封面播放对应原声摘录',60,630,1160,40,24,muted);
   media.push({slide:i+1,name:'MEDIA_'+i,file:d.media,kind:'audio'},{slide:i+1,name:'MEDIA_'+i+'_b',file:d.secondMedia,kind:'audio'});
  }else{
   const n=d.body.length;const gap=n>4?90:110;const font=d.layout==='refs'?28:33;
   d.body.forEach((a,k)=>text(s,a,65,160+k*gap,1145,gap-10,font,k===n-1&&d.layout!=='refs'?gold:paper));
  }
  text(s,String(i+1).padStart(2,'0'),1170,680,60,25,16,muted);
 }
 const imageNotes=(d.images||[]).map(f=>'原片静帧：'+f+'；本地资源D:/__Netdisk Download/The Last Emperor，HDR转SDR展示截图。').join('\n');
 s.speakerNotes.text=d.notes;
 console.log('build',i+1,d.title);
}
await (await PresentationFile.exportPptx(deck)).save(path.join(here,'candidate.pptx'));
await fs.writeFile(path.join(here,'media_map.json'),JSON.stringify(media,null,2));
for(let i=0;i<deck.slides.items.length;i++){
 const png=await deck.export({slide:deck.slides.items[i],format:'png',scale:1.5});
 await fs.writeFile(path.join(here,'renders',`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
 console.log('render',i+1);
}
await fs.writeFile(path.join(here,'deck_inspection.ndjson'),(await deck.inspect({kind:'slide,textbox,image,notes',maxChars:300000})).ndjson);
console.log('deck ready');
