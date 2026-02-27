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
  mediumZoom('.md-content img:not(a > img)', { background: '#EEEEEEA0' });
});
