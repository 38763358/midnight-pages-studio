import numpy as np, sys, json
from PIL import Image, ImageFilter, ImageDraw
from scipy import ndimage as nd
IMG='/workspace/midnight-pages-site/img/'
def coeffs(dst,src):
    A=[];B=[]
    for (x,y),(u,v) in zip(dst,src):
        A+=[[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]];B+=[u,v]
    return np.linalg.solve(np.array(A,float),np.array(B,float))
def load_art(src,box,hole,rot=0):
    im=Image.open(IMG+src).convert('RGB')
    if hole:
        hx,hy,r=hole;d=ImageDraw.Draw(im)
        a=np.array(im);ring=[]
        for t in np.linspace(0,2*np.pi,48):
            x=int(hx+(r+6)*np.cos(t));y=int(hy+(r+6)*np.sin(t));ring.append(a[y,x])
        c=tuple(int(v) for v in np.median(ring,0));d.ellipse((hx-r-3,hy-r-3,hx+r+3,hy+r+3),fill=c)
    im=im.crop(box)
    if rot: im=im.rotate(rot,expand=True)
    return im.resize((im.width*4,im.height*4),Image.LANCZOS)
def tag_mask(a,seed,tol):
    f=a.astype(float);s=f[seed[1],seed[0]]
    near=np.sqrt(((f-s)**2).sum(2))<tol
    lab,_=nd.label(near);m=lab==lab[seed[1],seed[0]]
    m=nd.binary_opening(m,iterations=1)
    filled=nd.binary_fill_holes(m)
    return m,filled
def oriented_quad(filled):
    ys,xs=np.nonzero(filled);P=np.stack([xs,ys],1).astype(float);c=P.mean(0)
    u,s,vt=np.linalg.svd(P-c,full_matrices=False);ax=vt
    pr=(P-c)@ax.T;lo=pr.min(0);hi=pr.max(0)
    corners=[(lo[0],lo[1]),(hi[0],lo[1]),(hi[0],hi[1]),(lo[0],hi[1])]
    Q=np.array([c+np.array(k)@ax for k in corners])
    # order TL,TR,BR,BL by position
    o=np.argsort(np.arctan2(Q[:,1]-c[1],Q[:,0]-c[0]))  # starts at angle -pi (left)
    Q=Q[o];i=np.argmin(Q.sum(1));Q=np.roll(Q,-i,0)
    if Q[1][0]<Q[3][0]: Q=Q[[0,3,2,1]]
    return Q
def run(cfg):
    bg=Image.open(cfg['scene']).convert('RGB');a=np.array(bg)
    if cfg.get('disp'):
        k=bg.size[0]/1024.0
        for key in ('quad','mask_poly'):
            if key in cfg: cfg[key]=[[x*k,y*k] for x,y in cfg[key]]
        cfg['disp']=False
    if 'quad' in cfg:
        H0,W0=a.shape[:2];pm=Image.new('L',(W0,H0),0);ImageDraw.Draw(pm).polygon([tuple(p) for p in cfg['quad']],fill=255)
        poly=np.array(pm)>0;polyd=nd.binary_dilation(poly,iterations=cfg.get('pad',4))
        f=a.astype(float);ys,xs=np.nonzero(nd.binary_erosion(poly,iterations=12));med=np.median(f[ys,xs],0)
        near=(np.sqrt(((f-med)**2).sum(2))<cfg.get('tol',40))&polyd
        lab,_=nd.label(near);big=np.argmax(np.bincount(lab[poly].ravel())[1:])+1;m=lab==big
        m=nd.binary_opening(m,iterations=1);filled=nd.binary_fill_holes(m)&polyd
        if cfg.get('poly_mask'):
            pm2=Image.new('L',(W0,H0),0);ImageDraw.Draw(pm2).polygon([tuple(p) for p in cfg.get('mask_poly',cfg['quad'])],fill=255);filled=np.array(pm2)>0;m=m|(near&filled)
    else:
        m,filled=tag_mask(a,cfg['seed'],cfg.get('tol',38))
    if 'grow' in cfg: filled=nd.binary_dilation(filled,iterations=cfg['grow'])
    Q=np.array(cfg['quad'],float) if 'quad' in cfg else oriented_quad(filled)
    if cfg.get('portrait_fix') is not None:
        pass
    art=load_art(cfg['art'],cfg['box'],cfg.get('hole'),cfg.get('rot',0))
    if cfg.get('stretch'):
        art=art.resize((art.width,int(art.height*cfg['stretch'])),Image.LANCZOS)
    if cfg.get('pad_top'):
        arr=np.array(art);col=np.median(arr[4:14].reshape(-1,3),0).astype('uint8');n=int(arr.shape[0]*cfg['pad_top'])
        art=Image.fromarray(np.concatenate([np.tile(col,(n,arr.shape[1],1)),arr],0))
    if cfg.get('pad_bottom'):
        qw=(np.linalg.norm(Q[1]-Q[0])+np.linalg.norm(Q[2]-Q[3]))/2;qh=(np.linalg.norm(Q[3]-Q[0])+np.linalg.norm(Q[2]-Q[1]))/2
        aw,ah=art.size;nh=int(aw*qh/qw)
        if nh>ah:
            arr=np.array(art);col=np.median(arr[-12:-4].reshape(-1,3),0).astype('uint8')
            pad=np.tile(col,(nh-ah,aw,1));art=Image.fromarray(np.concatenate([arr[:-4],pad,arr[-4:]],0))
    W,H=bg.size;w,h=art.size
    # inset quad slightly so art bleeds to edge
    c=Q.mean(0);Q=c+(Q-c)*cfg.get('scale',1.02)
    k=coeffs([tuple(p) for p in Q],[(0,0),(w,0),(w,h),(0,h)])
    warped=np.array(art.transform((W,H),Image.PERSPECTIVE,tuple(k),Image.BICUBIC)).astype(float)
    # shading from blank tag luminance
    L=a.astype(float).mean(2);Ls=nd.gaussian_filter(L,cfg.get('shade_sigma',1.5))
    ref=np.percentile(L[m],cfg.get('ref_pct',92))
    sh=np.clip(Ls/ref,0.25,1.12)[...,None]
    tint=(a[m].astype(float).mean(0)/a[m].astype(float).mean())  # warm cast of light
    tint=1+(tint-1)*cfg.get('tint',0.8)
    out=warped*sh*tint
    # depth of field + grain
    blur=cfg.get('blur',0.6)
    if blur>0: out=nd.gaussian_filter(out,(blur,blur,0))
    hf=L-nd.gaussian_filter(L,1.0);g=hf[m].std()*cfg.get('grain',1.0)
    out=out+np.random.default_rng(3).normal(0,g,(H,W,1))
    out=np.clip(out,0,255)
    occl=(filled & ~m) if not cfg.get('no_occl') else np.zeros_like(m)  # twine, hole, etc stay from plate
    occl=nd.binary_dilation(occl,iterations=cfg.get('occl_grow',1))&filled
    keep=(filled & ~occl) if not cfg.get('no_occl') else nd.binary_fill_holes(filled)
    alpha=nd.gaussian_filter(keep.astype(float),cfg.get('feather',0.8))[...,None]
    res=a*(1-alpha)+out*alpha
    Image.fromarray(res.astype('uint8')).save(cfg['out'],quality=92)
    print(cfg['out'],'quad',Q.round(1).tolist(),'mask px',int(m.sum()),int(filled.sum()))
for c in json.load(open(sys.argv[1])): 
    if len(sys.argv)<3 or c['out'].find(sys.argv[2])>=0: run(c)
