(() => {
  document.getElementById('yr').textContent = new Date().getFullYear();
  const grid = document.getElementById('grid');
  const lb = document.getElementById('lightbox');
  const lbImg = document.getElementById('lb-img');
  let photos = [];
  let current = 0;

  fetch('photos.json', { cache: 'no-cache' })
    .then(r => r.json())
    .then(data => {
      photos = data.photos || [];
      if (!photos.length) { document.getElementById('empty').hidden = false; return; }
      photos.forEach((p, i) => {
        const btn = document.createElement('button');
        btn.className = 'tile';
        btn.setAttribute('aria-label', 'View photo ' + (i + 1));
        const img = document.createElement('img');
        img.src = p.thumb;
        img.alt = p.alt || '';
        if (p.w && p.h) { img.width = p.w; img.height = p.h; }
        img.loading = 'lazy';
        img.decoding = 'async';
        img.onload = () => img.classList.add('loaded');
        btn.appendChild(img);
        btn.addEventListener('click', () => open(i));
        grid.appendChild(btn);
      });
    })
    .catch(() => { document.getElementById('empty').hidden = false; });

  function show(i) {
    current = (i + photos.length) % photos.length;
    lbImg.src = photos[current].full;
    lbImg.alt = photos[current].alt || '';
    // preload neighbor
    new Image().src = photos[(current + 1) % photos.length].full;
  }
  function open(i) { show(i); lb.hidden = false; document.body.style.overflow = 'hidden'; }
  function close() { lb.hidden = true; lbImg.src = ''; document.body.style.overflow = ''; }

  lb.querySelector('.lb-close').addEventListener('click', close);
  lb.querySelector('.lb-prev').addEventListener('click', e => { e.stopPropagation(); show(current - 1); });
  lb.querySelector('.lb-next').addEventListener('click', e => { e.stopPropagation(); show(current + 1); });
  lb.addEventListener('click', e => { if (e.target === lb) close(); });
  document.addEventListener('keydown', e => {
    if (lb.hidden) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') show(current - 1);
    if (e.key === 'ArrowRight') show(current + 1);
  });

  // swipe on phones
  let x0 = null;
  lb.addEventListener('touchstart', e => { x0 = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener('touchend', e => {
    if (x0 === null) return;
    const dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 40) show(current + (dx < 0 ? 1 : -1));
    x0 = null;
  });
})();
