(() => {
  'use strict';
  const root = document.documentElement;
  const images = [...document.images];
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const hero = document.querySelector('.hero__photo img');
  let observer;
  let frame = 0;
  let showAll = false;

  function stop() {
    observer?.disconnect();
    cancelAnimationFrame(frame);
    frame = 0;
    removeEventListener('scroll', schedule);
    removeEventListener('resize', schedule);
    hero.style.removeProperty('transform');
  }
  window.__revealAll = () => {
    showAll = true;
    stop();
    root.classList.add('show-all');
    images.forEach(img => {
      img.loading = 'eager';
      img.classList.add('is-visible');
    });
  };
  function paint() {
    frame = 0;
    const top = document.querySelector('.hero').getBoundingClientRect().top;
    hero.style.transform = `translateY(${Math.min(40, Math.max(0, -top * 0.06))}px)`;
  }
  function schedule() {
    if (!frame) frame = requestAnimationFrame(paint);
  }
  function configure() {
    stop();
    if (showAll || reduced.matches) {
      images.forEach(img => img.classList.add('is-visible'));
      return;
    }
    if ('IntersectionObserver' in window) {
      observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.05 });
      images.forEach(img => observer.observe(img));
      root.classList.add('js');
    }
    addEventListener('scroll', schedule, { passive: true });
    addEventListener('resize', schedule);
    schedule();
  }
  reduced.addEventListener('change', configure);
  configure();
})();
