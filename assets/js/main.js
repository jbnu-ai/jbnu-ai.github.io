/* JBNU 영상정보신기술연구센터 - Main JavaScript */

document.addEventListener('DOMContentLoaded', function () {

  // Active nav highlight
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href && href !== '/' && currentPath.startsWith(href)) {
      link.classList.add('active');
    }
  });

  // Per-paper BibTeX download
  document.querySelectorAll('.bibtex-download-btn').forEach(btn => {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const bibtex = this.getAttribute('data-bibtex');
      const filename = this.getAttribute('download') || 'reference.bib';
      const blob = new Blob([bibtex], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      a.click();
      URL.revokeObjectURL(url);
    });
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // Gallery lightbox (basic)
  const galleryItems = document.querySelectorAll('.gallery-item img');
  galleryItems.forEach(img => {
    img.style.cursor = 'pointer';
    img.addEventListener('click', function () {
      const modal = document.createElement('div');
      modal.style.cssText = `
        position:fixed; top:0; left:0; width:100%; height:100%;
        background:rgba(0,0,0,0.85); z-index:9999;
        display:flex; align-items:center; justify-content:center; cursor:pointer;
      `;
      const image = document.createElement('img');
      image.src = this.src;
      image.style.cssText = 'max-width:90%; max-height:90vh; border-radius:8px;';
      modal.appendChild(image);
      modal.addEventListener('click', () => document.body.removeChild(modal));
      document.body.appendChild(modal);
    });
  });

});
