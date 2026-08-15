(() => {
  const images = [...document.querySelectorAll('.char-card img[src*="personajes/verne/"]')];
  if (!images.length) return;

  const overlay = document.createElement('div');
  overlay.className = 'verne-zoom';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-label', 'Retrato ampliado');
  overlay.innerHTML = `
    <button class="verne-zoom-close" type="button" aria-label="Cerrar">&times;</button>
    <figure>
      <img alt="">
      <figcaption></figcaption>
    </figure>`;
  document.body.appendChild(overlay);

  const enlarged = overlay.querySelector('img');
  const caption = overlay.querySelector('figcaption');
  const closeButton = overlay.querySelector('.verne-zoom-close');
  let lastFocus = null;

  function openZoom(source) {
    lastFocus = source;
    enlarged.src = source.currentSrc || source.src;
    enlarged.alt = source.alt || '';
    caption.textContent = source.alt || '';
    overlay.classList.add('is-open');
    document.body.classList.add('verne-zoom-open');
    closeButton.focus();
  }

  function closeZoom() {
    overlay.classList.remove('is-open');
    document.body.classList.remove('verne-zoom-open');
    enlarged.removeAttribute('src');
    if (lastFocus) lastFocus.focus();
  }

  images.forEach(image => {
    image.classList.add('verne-zoomable');
    image.tabIndex = 0;
    image.setAttribute('title', 'Doble clic para ampliar');
    image.setAttribute('aria-label', `${image.alt || 'Retrato'}. Doble clic para ampliar.`);
    image.addEventListener('dblclick', () => openZoom(image));
    image.addEventListener('keydown', event => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        openZoom(image);
      }
    });

    let lastTap = 0;
    image.addEventListener('touchend', event => {
      const now = Date.now();
      if (now - lastTap < 420) {
        event.preventDefault();
        openZoom(image);
        lastTap = 0;
      } else {
        lastTap = now;
      }
    }, {passive: false});
  });

  closeButton.addEventListener('click', closeZoom);
  overlay.addEventListener('click', event => {
    if (event.target === overlay) closeZoom();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && overlay.classList.contains('is-open')) closeZoom();
  });
})();
