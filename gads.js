// Google Ads conversion for Gumroad checkout clicks (AW-18521268865/1V0ICI6vzKMdEIHF0P9E).
// Based on the Google event snippet; adds a 1 s fallback, a navigate-once flag, a no-gtag fallback,
// and reads the link's final href at navigation time (main.js may have added utm_* to it).
function gtag_report_conversion(url) {
  var done = false;
  var callback = function () {
    if (done) return;
    done = true;
    var dest = (typeof url === 'function') ? url() : url;
    if (typeof(dest) != 'undefined') {
      window.location = dest;
    }
  };
  if (typeof window.gtag !== 'function') {
    callback();
    return false;
  }
  try {
    gtag('event', 'conversion', {
        'send_to': 'AW-18521268865/1V0ICI6vzKMdEIHF0P9E',
        'event_callback': callback
    });
  } catch (e) {
    callback();
    return false;
  }
  if (typeof(url) != 'undefined') setTimeout(callback, 1000);
  return false;
}
(function () {
  'use strict';
  function gumroadLink(target) {
    var a = target && target.closest ? target.closest('a[href]') : null;
    if (!a) return null;
    try {
      var u = new URL(a.href, location.href);
      return /^https?:$/.test(u.protocol) && /(^|\.)gumroad\.com$/i.test(u.hostname) ? a : null;
    } catch (e) { return null; }
  }
  function track() {
    try { gtag_report_conversion(); } catch (e) { /* never block the click */ }
  }
  document.addEventListener('click', function (e) {
    var a = gumroadLink(e.target);
    if (!a || e.defaultPrevented) return;
    var t = (a.getAttribute('target') || '').toLowerCase();
    var newTab = t !== '' && t !== '_self';
    var modified = e.button !== 0 || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey;
    if (newTab || modified || a.hasAttribute('download')) { track(); return; }
    e.preventDefault();
    gtag_report_conversion(function () { return a.href; });
  });
  // Middle-click opens a new tab and fires auxclick, not click: count it, don't intercept.
  document.addEventListener('auxclick', function (e) {
    if (e.button === 1 && gumroadLink(e.target)) track();
  });
})();
