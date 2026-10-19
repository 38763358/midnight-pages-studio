#!/bin/bash
# Full-page screenshots via headless Chrome; trims trailing blank canvas.
cd "$(dirname "$0")"
for w in 1440 390; do
  google-chrome --headless=new --no-sandbox --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
    --window-size=$w,14000 --virtual-time-budget=4000 --screenshot=screens/home-$w.png "file://$PWD/index.html" 2>/dev/null
  python3 - "$w" <<'PY'
import sys;from PIL import Image
f=f"screens/home-{sys.argv[1]}.png";im=Image.open(f).convert('RGB');W,H=im.size;px=im.load()
y=H-1
while y>0 and all(px[x,y]==px[0,H-1] for x in range(0,W,7)): y-=1
im.crop((0,0,W,y+2)).save(f);print(f,W,y+2)
PY
done
