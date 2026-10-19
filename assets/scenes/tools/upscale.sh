#!/bin/bash
cd /workspace/midnight-pages-site/assets/scenes
for f in v4-hero-porch v4-keys v4-openhouse hero-porch; do
  [ -f up/$f.png ] && continue
  SECONDS=0; tools/esrgan/realesrgan-ncnn-vulkan -i raw/$f.jpg -o up/$f.tmp.png -n realesrgan-x4plus -s 2 -t 400 -m tools/esrgan/models >/dev/null 2>&1 && mv up/$f.tmp.png up/$f.png; echo "$f done ${SECONDS}s"
done
