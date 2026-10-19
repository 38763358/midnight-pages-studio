import json,subprocess,sys,os
from PIL import Image
c=json.load(open('tools/scenes-v4.json'));out=[]
names={'prev-v4-hero.jpg':'v4-hero-porch','prev-v4-keys.jpg':'v4-use-keys','prev-v4-openhouse.jpg':'v4-use-openhouse'}
plates={'raw/v4-hero-porch.jpg':'up/v4-hero-porch.png','raw/v4-keys.jpg':'up/v4-keys.png','raw/v4-openhouse.jpg':'up/v4-openhouse.png'}
for s in c:
    p=plates[s['scene']]
    if not os.path.exists(p): continue
    s=dict(s,scene=p,out='final-'+names[s['out']]+'.png',blur=s.get('blur',0.6)*1.6);out.append(s)
json.dump(out,open('/tmp/mps_final.json','w'))
subprocess.run([sys.executable,'tools/composite.py','/tmp/mps_final.json'],check=True)
for s in out:
    n=s['out'][6:-4];im=Image.open(s['out']).convert('RGB')
    im.save(n+'.webp',quality=82,method=6);im.resize((1280,720),Image.LANCZOS).save(n+'-1280.webp',quality=82)
    if n=='v4-hero-porch':
        W,H=im.size;cw=int(H*0.75);x0=int(400/1024*W)-cw//2;im.crop((x0,0,x0+cw,H)).resize((810,1080),Image.LANCZOS).save('v4-hero-porch-mobile.webp',quality=82)
    os.remove(s['out']);print(n,im.size)
