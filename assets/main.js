/** Progressive enhancement: every artwork remains an ordinary image link without JS. */
(() => {
  const modal = document.querySelector('#artwork-dialog');
  if (!modal || typeof modal.showModal !== 'function') return;
  const img = modal.querySelector('#lightbox-img');
  const title = modal.querySelector('#lightbox-title');
  const details = modal.querySelector('#lightbox-details');
  const number = modal.querySelector('#lightbox-number');
  const close = modal.querySelector('.lightbox-close');
  let lastFocus = null;
  document.querySelectorAll('[data-artwork]').forEach((link) => {
    link.addEventListener('click', (event) => {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button !== 0) return;
      event.preventDefault();
      lastFocus = document.activeElement;
      img.src = link.href;
      img.alt = link.dataset.title + ', obra de Nohemi Palencia Cisneros';
      title.textContent = link.dataset.title;
      details.textContent = link.dataset.details;
      number.textContent = link.dataset.number;
      modal.showModal();
      close.focus();
    });
  });
  close.addEventListener('click', () => modal.close());
  modal.addEventListener('click', (event) => { if (event.target === modal) modal.close(); });
  modal.addEventListener('close', () => {
    img.removeAttribute('src');
    if (lastFocus && typeof lastFocus.focus === 'function') lastFocus.focus();
  });
})();
