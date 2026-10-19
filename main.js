(() => {
'use strict';
const root = document.documentElement;
const reduced = matchMedia('(prefers-reduced-motion: reduce)');
const reveals = [...document.querySelectorAll('.reveal')];
window.__revealAll = () => {
  root.classList.add('show-all');
  document.querySelectorAll('img').forEach(img => img.loading = 'eager');
  reveals.forEach(el => el.classList.add('is-visible'));
};
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('is-visible'); observer.unobserve(e.target); }
  }), { threshold: .15 });
  reveals.forEach((el, i) => { el.style.setProperty('--delay', `${i % 3 * 80}ms`); observer.observe(el); });
} else window.__revealAll();
root.classList.add('js');
const masthead = document.querySelector('.masthead');
new IntersectionObserver(([e]) => masthead.classList.toggle('is-scrolled', !e.isIntersecting), {rootMargin:'-80px 0px 0px 0px'}).observe(document.querySelector('.hero'));
const sticky = document.querySelector('.sets__sticky');
const fitSticky = () => sticky.style.setProperty('--sticky-top', `${Math.min(115, innerHeight-sticky.offsetHeight-24)}px`);
new ResizeObserver(fitSticky).observe(sticky);
addEventListener('resize', fitSticky);
const deck = document.querySelector('.deck');
const tags = [...deck.querySelectorAll('.tag')];
const rows = [...document.querySelectorAll('.set')];
const info = document.querySelector('.deck-info');
const counter = document.querySelector('.deck-counter');
let current = 0, frame = 0, gesture = null, suppress = false, syncUntil = 0;
function paint(x = 0) {
  tags.forEach((tag, i) => {
    const depth = (i - current + 8) % 8;
    tag.style.zIndex = 8 - depth;
    tag.style.opacity = depth < 3 ? '1' : '0';
    tag.style.pointerEvents = depth === 0 ? 'auto' : 'none';
    tag.inert = depth !== 0;
    tag.style.transform = depth === 0 ? `translateX(${x}px) rotate(${x * .05}deg)` : `translate(${depth * 8}px,${depth * 6}px) rotate(${depth % 2 ? 2 * depth : -2 * depth}deg) scale(${1 - .04 * depth})`;
  });
}
function clean() {
  cancelAnimationFrame(frame); frame = 0;
  tags.forEach(t => t.style.removeProperty('will-change'));
  deck.classList.remove('is-dragging');
}
function select(index, manual = true) {
  clean(); current = (index + 8) % 8; paint();
  if (manual) syncUntil = performance.now() + 1000;
  rows.forEach((row, i) => {
    row.classList.toggle('is-active', i === current);
    if (i === current) row.setAttribute('aria-current', 'true'); else row.removeAttribute('aria-current');
  });
  counter.textContent = `${String(current + 1).padStart(2, '0')} / 08`;
  const row = rows[current];
  info.replaceChildren(...['.set__name', '.set__desc', '.set__count'].map(s => row.querySelector(s).cloneNode(true)));
  const buy = document.createElement('a'); buy.href = row.querySelector('a').href;
  buy.textContent = row.querySelector('.set__cta').textContent + ' · $7'; info.append(buy);
}
select(0, false);
document.querySelector('.deck-prev').onclick = () => select(current - 1);
document.querySelector('.deck-next').onclick = () => select(current + 1);
deck.addEventListener('keydown', e => {
  if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') { e.preventDefault(); select(current + (e.key === 'ArrowRight' ? 1 : -1)); }
});
rows.forEach((row, i) => {
  row.addEventListener('pointerenter', e => { if (e.pointerType === 'mouse') select(i); });
  row.addEventListener('focusin', () => select(i));
  row.addEventListener('click', () => select(i));
});
const rowObserver = new IntersectionObserver(entries => {
  if (performance.now() < syncUntil || gesture || frame) return;
  const visible = entries.filter(e => e.isIntersecting).sort((a,b) => Math.abs(a.boundingClientRect.top - innerHeight * .5) - Math.abs(b.boundingClientRect.top - innerHeight * .5));
  if (visible.length) select(Number(visible[0].target.dataset.index), false);
}, {rootMargin:'-35% 0px -35% 0px',threshold:0});
rows.forEach(r => rowObserver.observe(r));
deck.addEventListener('pointerdown', e => {
  if (!e.isPrimary || e.button !== 0) return;
  clean(); paint(); suppress = false;
  gesture = {id:e.pointerId,x:e.clientX,y:e.clientY,dx:0,lock:null,target:e.target,samples:[{x:e.clientX,t:performance.now()}]};
  deck.setPointerCapture(e.pointerId);
});
deck.addEventListener('pointermove', e => {
  const g = gesture; if (!g || g.id !== e.pointerId) return;
  g.dx = e.clientX - g.x;
  const dy = e.clientY - g.y;
  if (!g.lock && Math.max(Math.abs(g.dx),Math.abs(dy)) >= 8) g.lock = Math.abs(g.dx) > Math.abs(dy) ? 'x' : 'y';
  if (g.lock !== 'x') return;
  const now = performance.now(); g.samples.push({x:e.clientX,t:now});
  g.samples = g.samples.filter(p => now - p.t <= 100);
  deck.classList.add('is-dragging'); tags[current].style.willChange = 'transform';
  if (!frame) frame = requestAnimationFrame(() => { frame = 0; if (gesture) paint(gesture.dx); });
});
function finish(e, cancelled = false) {
  const g = gesture; if (!g || g.id !== e.pointerId) return;
  gesture = null; clean();
  if (deck.hasPointerCapture(e.pointerId)) deck.releasePointerCapture(e.pointerId);
  const distance = Math.hypot(e.clientX - g.x,e.clientY - g.y);
  suppress = distance >= 6 || cancelled;
  if (!cancelled && distance < 6) {
    const link = g.target.closest('a');
    if (link) { suppress = true; location.assign(link.href); }
    paint(); return;
  }
  if (g.lock !== 'x') { paint(); return; }
  const now = performance.now();
  const samples = g.samples.filter(p => now - p.t <= 100);
  const first = samples[0];
  const velocity = first ? (e.clientX - first.x) / Math.max(1,now - first.t) : 0;
  const fling = !cancelled && (Math.abs(g.dx) > deck.clientWidth * .3 || Math.abs(velocity) > .5);
  const direction = Math.abs(velocity) > .5 ? Math.sign(velocity) : Math.sign(g.dx);
  if (reduced.matches) { if (fling) select(current + (direction < 0 ? 1 : -1)); else paint(); return; }
  let x = g.dx, v = fling ? direction * Math.max(Math.abs(velocity) * 16.667, 25) : 0;
  const target = direction * deck.clientWidth * 1.4;
  tags[current].style.willChange = 'transform';
  function animate() {
    if (fling) {
      x += v; v *= .95;
      if (Math.abs(x) >= Math.abs(target) || Math.abs(v) < .1) { select(current + (direction < 0 ? 1 : -1)); return; }
    } else {
      v = (v - x * .12) * .78; x += v;
      if (Math.abs(x) < .5 && Math.abs(v) < .05) { clean(); paint(); return; }
    }
    paint(x); frame = requestAnimationFrame(animate);
  }
  frame = requestAnimationFrame(animate);
}
deck.addEventListener('pointerup', e => finish(e));
deck.addEventListener('pointercancel', e => finish(e,true));
deck.addEventListener('click', e => { if (suppress) { e.preventDefault(); suppress = false; } },true);
const fine = matchMedia('(hover:hover) and (pointer:fine)');
document.querySelectorAll('.tilt').forEach(el => {
  let x=0,y=0,tx=0,ty=0,alpha=0,goal=0,raf=0;
  const gloss=el.querySelector('.gloss');
  function tick() {
    x+=(tx-x)*.12; y+=(ty-y)*.12; alpha+=(goal-alpha)*.12;
    el.style.transform=`perspective(1000px) rotateX(${-y*6}deg) rotateY(${x*6}deg) rotate(${innerWidth<640?-1.5:-3}deg)`;
    gloss.style.transform=`translate(${x*30}%,${y*30}%)`; gloss.style.opacity=alpha;
    if (Math.abs(tx-x)+Math.abs(ty-y)+Math.abs(goal-alpha)>.001) raf=requestAnimationFrame(tick); else raf=0;
  }
  function move(e) {
    const r=el.getBoundingClientRect(); tx=Math.max(-.5,Math.min(.5,(e.clientX-r.left)/r.width-.5)); ty=Math.max(-.5,Math.min(.5,(e.clientY-r.top)/r.height-.5));goal=.35;if(!raf)raf=requestAnimationFrame(tick);
  }
  function leave(){tx=ty=goal=0;if(!raf)raf=requestAnimationFrame(tick);}
  function bind(){
    el.removeEventListener('pointermove',move);el.removeEventListener('pointerleave',leave);
    cancelAnimationFrame(raf);raf=0;el.style.removeProperty('transform');gloss.style.opacity=0;
    if(fine.matches&&!reduced.matches){el.addEventListener('pointermove',move);el.addEventListener('pointerleave',leave);}
  }
  bind();fine.addEventListener('change',bind);reduced.addEventListener('change',bind);
});
})();
