// Pass utm_* query parameters from the landing URL through to Gumroad links (for attribution).
// Shared by the home page and the blog. Covers links present at load, links added later
// (MutationObserver), and re-checks on click/auxclick/contextmenu in the capture phase so the
// href is final before gads.js (bubble phase) reads it. Existing params are preserved except
// on data-utm-default links: incoming UTMs replace all five default UTM keys. Without
// incoming UTMs, defaults stay unchanged. Values are capped at 100 characters.
(() => {
  'use strict';
  try {
    const keys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
    const incoming = new URLSearchParams(location.search);
    const utm = keys.filter(k => incoming.get(k)).map(k => [k, incoming.get(k).slice(0, 100)]);
    if (!utm.length) return;
    const decorate = a => {
      try {
        if (!a || a.tagName !== 'A' || !a.hasAttribute('href')) return;
        const url = new URL(a.getAttribute('href'), location.href);
        if (url.protocol !== 'https:' || !/(^|\.)gumroad\.com$/.test(url.hostname)) return;
        if (a.hasAttribute('data-utm-default')) {
          const original = url.toString();
          keys.forEach(k => url.searchParams.delete(k));
          utm.forEach(([k, v]) => url.searchParams.set(k, v));
          if (url.toString() !== original) a.href = url.toString();
          return;
        }
        let changed = false;
        utm.forEach(([k, v]) => { if (!url.searchParams.has(k)) { url.searchParams.set(k, v); changed = true; } });
        if (changed) a.href = url.toString();
      } catch (e) { /* ignore this link */ }
    };
    const scan = root => {
      if (root.nodeType !== 1) return;
      if (root.tagName === 'A') decorate(root);
      root.querySelectorAll('a[href]').forEach(decorate);
    };
    scan(document.documentElement);
    const onEvent = e => { const a = e.target && e.target.closest ? e.target.closest('a[href]') : null; if (a) decorate(a); };
    ['click', 'auxclick', 'contextmenu'].forEach(t => document.addEventListener(t, onEvent, true));
    if ('MutationObserver' in window) {
      new MutationObserver(list => list.forEach(m => {
        if (m.type === 'attributes') decorate(m.target);
        else m.addedNodes.forEach(scan);
      })).observe(document.documentElement, { childList: true, subtree: true, attributes: true, attributeFilter: ['href'] });
    }
  } catch (e) { /* never block the page */ }
})();
