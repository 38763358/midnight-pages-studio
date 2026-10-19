const {chromium}=require('/workspace/mps-tools-8df2/node_modules/playwright-core');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
const dir='/workspace/midnight-pages-site/screenshots/v3/';
for(const [n,w,h,m] of [['desktop',1440,900,false],['mobile',390,844,true]]){
 const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:m?2:1,isMobile:m,hasTouch:m});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',c=>{if(c.type()==='error')errs.push(c.text())});
 await p.goto('http://localhost:8765/index.html');await p.waitForTimeout(1500);
 await p.screenshot({path:dir+n+'-hero.png'});
 const H=await p.evaluate(()=>document.documentElement.scrollHeight);
 for(let y=0;y<H;y+=400){await p.evaluate(y=>scrollTo(0,y),y);await p.waitForTimeout(80);}
 await p.evaluate(()=>window.__revealAll&&window.__revealAll());await p.evaluate(()=>scrollTo(0,0));await p.waitForTimeout(1200);
 await p.screenshot({path:dir+n+'-full.png',fullPage:true});console.log(n,H,errs);}
await b.close();})();
