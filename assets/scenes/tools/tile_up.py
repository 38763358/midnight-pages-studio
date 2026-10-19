import sys,subprocess,os,numpy as np
from PIL import Image
E='tools/esrgan/realesrgan-ncnn-vulkan';T=340;O=40;S=4
def starts(n):
    s=list(range(0,n-T,T-O))+[n-T];return sorted(set(s))
for name in sys.argv[1:]:
    src=Image.open(f'raw/{name}.jpg').convert('RGB');W,H=src.size
    acc=np.zeros((H*S,W*S,3));wt=np.zeros((H*S,W*S,1))
    r=np.minimum(np.arange(T*S)+1,np.arange(T*S)[::-1]+1);r=np.minimum(r/(O*S),1.0)
    win=(r[:,None]*r[None,:])[...,None]+1e-4
    for y in starts(H):
        for x in starts(W):
            src.crop((x,y,x+T,y+T)).save('/tmp/mps_t_in.png')
            subprocess.run([E,'-i','/tmp/mps_t_in.png','-o','/tmp/mps_t_out.png','-n','realesrgan-x4plus','-s','4','-t',str(T+20),'-m','tools/esrgan/models'],capture_output=True,check=True)
            t=np.array(Image.open('/tmp/mps_t_out.png').convert('RGB'),dtype=float)
            acc[y*S:(y+T)*S,x*S:(x+T)*S]+=t*win;wt[y*S:(y+T)*S,x*S:(x+T)*S]+=win
            print(name,x,y,flush=True)
    out=Image.fromarray(np.clip(acc/wt,0,255).astype('uint8')).resize((W*2,H*2),Image.LANCZOS)
    out.save(f'up/{name}.png');print(name,'done',flush=True)
