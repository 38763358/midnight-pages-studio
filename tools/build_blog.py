"""Builds /blog pages, sitemap.xml and robots.txt. Run: python3 tools/build_blog.py"""
import json,os,html
from posts import POSTS,FREE,L,S
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE="https://38763358.github.io/midnight-pages-studio"
DATE="2026-10-19"; DATE_H="October 19, 2026"
NAMES={"curb-appeal":"Curb Appeal","postmark-society":"Postmark Society","fair-isle-lodge":"Fair Isle Lodge","herbarium-market":"Herbarium Market","gilded-hush":"Gilded Hush","chalk-talk":"Chalk Talk","gingham-kitchen":"Gingham Kitchen","riso-papercut":"Riso Papercut"}
IMG={"curb-appeal":"curb-appeal","postmark-society":"postmark","fair-isle-lodge":"fair-isle","herbarium-market":"herbarium","gilded-hush":"gilded-hush","chalk-talk":"chalk-talk","gingham-kitchen":"gingham-kitchen","riso-papercut":"riso-papercut"}
ORG={"@type":"Organization","name":"Midnight Pages Studio","url":"https://midnightpagesstudio.gumroad.com"}
def ld(o): return '<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False,indent=1).replace("</","<\\/")+'</script>'
def head(title,desc,url,img,typ,r,extra):
  e=html.escape
  return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#111c33">
<link rel="icon" href="{r}favicon.svg" type="image/svg+xml">
<link rel="icon" href="{r}favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{r}apple-touch-icon.png">
<meta property="og:type" content="{typ}">
<meta property="og:site_name" content="Midnight Pages Studio">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{img}">
<link rel="preload" href="{r}fonts/InstrumentSerif-Regular.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="{r}blog.css">
{extra}
</head>
<body>
<a class="b-skip" href="#main">Skip to content</a>
<header class="b-mast">
 <div class="b-wrap b-mast__row">
  <a class="b-wordmark" href="{r}">MIDNIGHT PAGES STUDIO</a>
  <nav aria-label="Primary"><ul class="b-nav">
   <li><a href="{r}#sets">Gift tags</a></li>
   <li><a href="{r}blog/" aria-current="{'page' if typ=='website' else 'false'}">Journal</a></li>
   <li><a class="b-nav__buy" href="{L}">Library $39</a></li>
  </ul></nav>
 </div>
</header>
'''
def sample(r):
  return f'''<aside class="b-sample" aria-labelledby="sample-h">
 <div class="b-sample__img"><img src="{r}img/free-sample-480.webp" width="480" height="270" alt="Cover of the free sample: 10 AI prompts for real estate agents" loading="lazy" decoding="async"></div>
 <div><p class="b-eyebrow">Free</p><h2 id="sample-h" class="b-sample__h">Ten prompts, <em>on the house</em></h2>
 <p>A free sample of ten AI prompts for listing and follow-up writing. Enter your email on Gumroad and it&rsquo;s yours.</p>
 <a class="b-btn" href="{FREE}">Get the free sample</a></div>
</aside>'''
def foot(r):
  return f'''<footer class="b-foot"><div class="b-wrap b-foot__row">
 <p class="b-foot__mark">Midnight Pages Studio</p>
 <ul class="b-foot__links"><li><a href="{r}">Home</a></li><li><a href="{r}blog/">Journal</a></li><li><a href="{L}">Tag Library</a></li><li><a href="https://midnightpagesstudio.gumroad.com">Gumroad shop</a></li><li><a href="{FREE}">Free sample</a></li></ul>
 <p class="b-foot__fine">Digital downloads for US real estate agents. Nothing ships; everything prints.</p>
</div></footer>
</body>
</html>
'''
def write(p,s):
  os.makedirs(os.path.dirname(p),exist_ok=True); open(p,"w").write(s)
cards=""
for p in POSTS:
  url=f"{BASE}/blog/{p['slug']}/"; r="../../"; og=f"{BASE}/img/blog/og-{p['img']}.jpg"
  data={"@context":"https://schema.org","@type":"BlogPosting","headline":p["title"],"description":p["desc"],"image":[og],"datePublished":DATE,"dateModified":DATE,"author":ORG,"publisher":{**ORG,"logo":{"@type":"ImageObject","url":f"{BASE}/apple-touch-icon.png"}},"mainEntityOfPage":{"@type":"WebPage","@id":url},"url":url,"inLanguage":"en-US","isPartOf":{"@type":"Blog","@id":f"{BASE}/blog/"}}
  crumbs={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Journal","item":f"{BASE}/blog/"},{"@type":"ListItem","position":2,"name":p["title"],"item":url}]}
  rel="".join(f'''<li><a href="{S[k]}"><img src="{r}img/{IMG[k]}-480.webp" width="480" height="480" alt="{NAMES[k]} gift tag set" loading="lazy" decoding="async"><span class="b-rel__name">{NAMES[k]}</span><span class="b-rel__price">$12 · Buy on Gumroad</span></a></li>''' for k in p["tags"])
  body=f'''<main id="main" class="b-article">
 <header class="b-wrap b-art__head">
  <p class="b-crumb"><a href="../">Journal</a> <span aria-hidden="true">/</span> Pop-by guides</p>
  <h1 class="b-display">{p["title"]}</h1>
  <p class="b-dek">{p["dek"]}</p>
  <p class="b-byline">Midnight Pages Studio · <time datetime="{DATE}">{DATE_H}</time></p>
 </header>
 <figure class="b-wrap b-hero"><img src="{r}img/blog/{p['img']}-1280.webp" srcset="{r}img/blog/{p['img']}-800.webp 800w, {r}img/blog/{p['img']}-1280.webp 1280w" sizes="(min-width: 72rem) 68rem, 100vw" width="1280" height="720" alt="Printable pop-by gift tags from Midnight Pages Studio" fetchpriority="high"></figure>
 <div class="b-wrap b-prose">{p["body"]}
  {sample(r)}
  <section class="b-rel" aria-labelledby="rel-h"><h2 id="rel-h">Tag sets for this season</h2><ul>{rel}</ul>
  <div class="b-rel__all"><p>Or get all eight collections, 109 designs and The Home Letter 2027 in the Pop-By Tag Library.</p><a class="b-btn b-btn--ink" href="{L}">Buy the Library <span class="b-btn__price">$39</span></a><p class="b-save">Save $57 vs. buying all 8 sets separately ($96)</p></div></section>
 </div>
</main>
'''
  write(f"{ROOT}/blog/{p['slug']}/index.html",head(p["seo"]+" · Midnight Pages Studio",p["desc"],url,og,"article",r,ld(data)+"\n"+ld(crumbs))+body+foot(r))
  cards+=f'''<li class="b-card"><a href="{p['slug']}/"><img src="../img/blog/{p['img']}-800.webp" width="800" height="450" alt="" loading="lazy" decoding="async"><span class="b-card__date"><time datetime="{DATE}">{DATE_H}</time></span><h2 class="b-card__h">{p["title"]}</h2><p>{p["desc"]}</p><span class="b-card__more">Read the guide <span aria-hidden="true">&rarr;</span></span></a></li>'''
url=f"{BASE}/blog/"; desc="Practical guides for US real estate agents: pop-by gift ideas, tag wording, and a year-round client touch calendar."
blog={"@context":"https://schema.org","@type":"Blog","@id":url,"url":url,"name":"The Journal · Midnight Pages Studio","description":desc,"inLanguage":"en-US","publisher":ORG,"blogPost":[{"@type":"BlogPosting","headline":p["title"],"url":f"{BASE}/blog/{p['slug']}/","datePublished":DATE,"image":f"{BASE}/img/blog/og-{p['img']}.jpg","author":ORG} for p in POSTS]}
write(f"{ROOT}/blog/index.html",head("Pop-By Ideas and Client Touch Guides for Realtors · Midnight Pages Studio Journal",desc,url,f"{BASE}/img/blog/og-calendar.jpg","website","../",ld(blog))+f'''<main id="main">
 <header class="b-wrap b-list__head"><p class="b-eyebrow">The Journal</p><h1 class="b-display">Notes on <em>staying in touch</em></h1><p class="b-dek">Pop-by ideas, tag wording and a calendar for the year. Short, practical guides for agents.</p></header>
 <ul class="b-wrap b-cards" role="list">{cards}</ul>
 <div class="b-wrap b-list__sample">{sample("../")}</div>
</main>
'''+foot("../"))
urls=[f"{BASE}/",f"{BASE}/blog/"]+[f"{BASE}/blog/{p['slug']}/" for p in POSTS]
write(f"{ROOT}/sitemap.xml",'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"  <url><loc>{u}</loc><lastmod>{DATE}</lastmod></url>\n" for u in urls)+"</urlset>\n")
write(f"{ROOT}/robots.txt",f"""User-agent: *
Allow: /

Sitemap: {BASE}/sitemap.xml
""")
print("built",len(POSTS))
