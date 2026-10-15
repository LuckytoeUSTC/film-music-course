import pathlib, subprocess, json, base64, struct, hashlib

src = pathlib.Path(r'C:\Users\lucky\Downloads')
dst = pathlib.Path(r'D:\__Netdisk Download\The Last Emperor')
cover = dst / 'The Last Emperor (square).jpg'
names = ['First Coronation','Open The Door','Where Is Armo？','Picking Up Brides','The Last Emperor： Theme Variation 1','Rain (I Want A Divorce)','The Baby (Was Born Dead)','The Last Emperor： Theme Variation 2','The Last Emperor (Theme)','The Last Emperor (Main Title Theme)','Picking A Bride','Bed','Wind Rain And Water','Paper Emperor','Lunch','Red Guard',"The Emperor's Waltz",'Red Guard Dance']
titles = ['First Coronation','Open the Door','Where Is Armo?','Picking Up Brides','The Last Emperor – Theme Variation 1','Rain (I Want a Divorce)','The Baby (Was Born Dead)','The Last Emperor – Theme Variation 2','The Last Emperor – Theme','Main Title Theme (The Last Emperor)','Picking a Bride','Bed','Wind, Rain, and Water','Paper Emperor','Lunch','Red Guard (Sailing the Seas Depends on the Helmsman)',"The Emperor’s Waltz",'The Red Guard Dance']
def run(args):
    return subprocess.check_output(args, stderr=subprocess.PIPE).decode('utf-8')
def probe(p):
    return json.loads(run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(p)]))
def audio_hash(p):
    return run(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','streamhash','-hash','sha256','-']).strip()
data = cover.read_bytes()
pic = struct.pack('>I',3)+struct.pack('>I',10)+b'image/jpeg'+struct.pack('>I',0)+struct.pack('>IIIII',640,640,24,0,len(data))+data
picture = base64.b64encode(pic).decode()
report=[]
for i,(name,title) in enumerate(zip(names,titles),1):
    source=src/(name+'.webm')
    target=dst/(f'{i:02d} - '+name+'.opus')
    tags={'title':title,'album':'The Last Emperor','artist':'Ryuichi Sakamoto','album_artist':'Ryuichi Sakamoto','date':'1987','genre':'Film Soundtracks','tracknumber':str(i),'tracktotal':'18','discnumber':'1','disctotal':'1','metadata_block_picture':picture}
    if i<=9: tags['composer']='Ryuichi Sakamoto'
    elif i<=14: tags['composer']='David Byrne'
    elif i==15: tags['composer']='Cong Su'
    if i==16: tags['performer']='The Red Guard Accordion Band'
    if i==17:
        tags['composer']='Johann Strauss II'
        tags['performer']='Berliner Philharmoniker; Herbert von Karajan'
    if i==18: tags['performer']='The Girls Red Guard Dancers'
    metadata=pathlib.Path(__file__).with_name('album-tags.ffmetadata')
    def escape(value): return value.replace('\\','\\\\').replace('=','\\=').replace(';','\\;').replace('#','\\#')
    metadata.write_text(';FFMETADATA1\n'+''.join(key+'='+escape(value)+'\n' for key,value in tags.items()),encoding='utf-8')
    args=['ffmpeg','-v','error','-n','-i',str(source),'-f','ffmetadata','-i',str(metadata),'-map','0:a:0','-c:a','copy','-map_metadata','1']
    if not target.exists(): run(args+[str(target)])
    result=probe(target)
    actual=result['streams'][0]['tags']
    normalized={k.lower():v for k,v in actual.items()}
    normalized['tracknumber']=normalized.get('tracknumber',normalized.get('track'))
    normalized['discnumber']=normalized.get('discnumber',normalized.get('disc'))
    for key,value in tags.items():
        if key=='metadata_block_picture': continue
        if normalized.get(key)!=value: raise RuntimeError('Tag verification failed: '+key)
    embedded=subprocess.check_output(['ffmpeg','-v','error','-i',str(target),'-map','0:v:0','-c','copy','-f','image2pipe','-'],stderr=subprocess.PIPE)
    if embedded!=data: raise RuntimeError('Cover verification failed')
    original_hash=audio_hash(source)
    if original_hash!=audio_hash(target): raise RuntimeError('Audio mismatch')
    run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'])
    report.append({'track':i,'source':str(source),'target':str(target),'tags':{k:v for k,v in tags.items() if k!='metadata_block_picture'},'audio_packet_sha256':original_hash,'verified':True})
    print(f'Verified {i}/18: {title}',flush=True)
(dst/'metadata-verification.json').write_text(json.dumps({'playlist':'https://www.youtube.com/playlist?list=PL7wv1Ns4VJAmPRx8tWP-gtHPbhhmhscaO','cover_sha256':hashlib.sha256(data).hexdigest(),'tracks':report},ensure_ascii=False,indent=2),encoding='utf-8')
for item in report:
    pathlib.Path(item['source']).unlink()
print('Completed; all 18 corresponding sources deleted.')
