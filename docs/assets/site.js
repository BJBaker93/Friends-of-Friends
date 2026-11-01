const video = document.querySelector('[data-background-video]');
const toggle = document.querySelector('[data-motion-toggle]');
if (video && toggle) {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const mobile = window.matchMedia('(max-width: 760px)');
  let pausedByUser = false;
  function sync() {
    const pause = pausedByUser || reduced.matches || mobile.matches;
    if (pause) video.pause();
    else {
      if (!video.src) video.src = video.dataset.src;
      video.play().catch(() => { pausedByUser = true; update(); });
    }
    update();
  }
  function update() {
    toggle.textContent = video.paused ? 'Play background' : 'Pause background';
    toggle.setAttribute('aria-label', toggle.textContent + ' animation');
  }
  toggle.hidden = false;
  toggle.addEventListener('click', () => { pausedByUser = !video.paused; sync(); });
  video.addEventListener('play', update);
  video.addEventListener('pause', update);
  reduced.addEventListener('change', sync);
  mobile.addEventListener('change', sync);
  sync();
}
