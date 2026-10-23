// Keep Template Kit details open above the phone breakpoint and collapsed on phones.
(() => {
  'use strict';
  try {
    const phones = window.matchMedia('(max-width:600px)');
    const update = () => {
      document.querySelectorAll('.kit-module__details').forEach(details => {
        details.open = !phones.matches;
      });
    };
    update();
    if (phones.addEventListener) phones.addEventListener('change', update);
    else phones.addListener(update);
  } catch (e) { /* keep the HTML details open if setup fails */ }
})();
