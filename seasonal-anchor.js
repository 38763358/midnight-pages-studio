// Seasonal deep links: /#seasonal, /#seasonal-jan … /#seasonal-dec, /#seasonal-bundle
// (also with a query string, e.g. ?utm_source=pinterest#seasonal-oct). Keeps the section title
// clear of the sticky masthead, scrolls the phone carousel so the target card is fully visible,
// and briefly tints the card. Only touches scroll positions and one class; never touches hrefs.
(() => {
  'use strict';
  try {
    const section = document.getElementById('seasonal');
    if (!section) return;
    const list = section.querySelector('.seasonals__list');
    const head = document.querySelector('.masthead');
    const reduced = matchMedia('(prefers-reduced-motion: reduce)');
    let timer = 0;

    const target = () => {
      const id = decodeURIComponent(location.hash.slice(1));
      if (!/^seasonal(-[a-z]+)?$/.test(id)) return null;
      const el = document.getElementById(id);
      return el && section.contains(el) ? el : null;
    };

    function go(smooth) {
      const el = target();
      if (!el) return;
      const behavior = smooth && !reduced.matches ? 'smooth' : 'auto';
      const headH = head ? head.getBoundingClientRect().height : 0;
      const viewH = innerHeight;

      // Horizontal: phone carousel (only when the list actually scrolls sideways).
      if (list && el.parentElement === list && list.scrollWidth > list.clientWidth + 1) {
        const pad = parseFloat(getComputedStyle(list).paddingLeft) || 0;
        const left = list.scrollLeft + el.getBoundingClientRect().left - list.getBoundingClientRect().left - pad;
        list.scrollTo({ left: Math.max(0, left), behavior });
      }

      // Vertical: stop at the section title (16px under the masthead). If the target card would
      // then fall below the fold, tighten the gap to 4px; if it still doesn't fit (e.g. the bundle on
      // a short desktop screen), scroll just enough to show the whole card instead.
      const y = scrollY;
      const titleTop = section.querySelector('.seasonals__head').getBoundingClientRect().top + y;
      let top = titleTop - headH - 16;
      if (el !== section) {
        const r = el.getBoundingClientRect();
        const cardTop = r.top + y, cardBottom = r.bottom + y;
        if (cardBottom - top > viewH - 8) {
          top = titleTop - headH - 4;
          if (cardBottom - top > viewH - 4) top = Math.min(cardTop - headH - 16, cardBottom - viewH + 16);
        }
      }
      window.scrollTo({ top: Math.max(0, top), behavior });

      if (el !== section) {
        section.querySelectorAll('.is-anchored').forEach(n => n.classList.remove('is-anchored'));
        clearTimeout(timer);
        el.classList.add('is-anchored');
        timer = setTimeout(() => el.classList.remove('is-anchored'), 1400);
      }
    }

    if (target()) {
      if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
      go(false);
      // Fonts/images can still shift layout a little after DOMContentLoaded: settle once more.
      let touched = false;
      const mark = () => { touched = true; };
      ['wheel', 'touchstart', 'keydown'].forEach(t => addEventListener(t, mark, { once: true, passive: true }));
      addEventListener('load', () => requestAnimationFrame(() => { if (!touched) go(false); }), { once: true });
    }
    addEventListener('hashchange', () => go(true));
  } catch (e) { /* never block the page */ }
})();
