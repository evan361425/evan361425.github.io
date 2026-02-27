window.MathJax = {
  tex: {
    inlineMath: [['\\(', '\\)']],
    displayMath: [['\\[', '\\]']],
    processEscapes: true,
    processEnvironments: true,
  },
  options: {
    ignoreHtmlClass: '.*|',
    processHtmlClass: 'arithmatex',
  },
  menuOptions: {
    settings: {
      assistiveMml: false,
    },
  },
};

document$.subscribe(() => {
  MathJax.typesetPromise();
  document.querySelectorAll('.md-content img:not(a > img)').forEach((img) => {
    const link = document.createElement('a');
    link.href = img.src;
    link.target = "_blank";
    link.classList.add('pswp-target-link');

    if (img.complete) {
      link.dataset.pswpWidth = img.naturalWidth;
      link.dataset.pswpHeight = img.naturalHeight;
    } else {
      img.onload = () => {
        link.dataset.pswpWidth = img.naturalWidth;
        link.dataset.pswpHeight = img.naturalHeight;
      };
    }

    img.parentNode.insertBefore(link, img);
    link.appendChild(img);
  });
  const lightbox = new PhotoSwipeLightbox({
    gallery: '.md-content',
    children: '.pswp-target-link',
    pswpModule: PhotoSwipe,
    secondaryZoomLevel: 2,
  });
  lightbox.on('uiRegister', function () {
    lightbox.pswp.ui.registerElement({
      name: 'focused-caption',
      order: 9,
      isButton: false,
      appendTo: 'root',
      html: '',
      onInit: (el, _pswp) => {
        lightbox.pswp.on('change', () => {
          const currSlideElement = lightbox.pswp.currSlide.data.element;
          let captionHTML;
          if (currSlideElement) {
            captionHTML = currSlideElement.querySelector('img').getAttribute('alt');
          }
          el.innerHTML = captionHTML || '';
        });
      }
    });
  });


  lightbox.init();
});
