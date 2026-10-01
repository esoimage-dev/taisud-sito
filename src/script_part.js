
(function () {
  // Tai Sud logo reveal. Rest state = the static logo, so if this never runs nothing is lost.
  var EASE = 'cubic-bezier(.22,.61,.36,1)';
  window.TaiSudLogo = function (svg, opts) {
    opts = opts || {};
    var rate = opts.rate || 1, anims = [];
    var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    function A(el, kf, o) { if (!el.animate) return; o.fill = 'both'; o.easing = o.easing || EASE; var a = el.animate(kf, o); a.playbackRate = rate; anims.push(a); }
    function play() {
      anims.forEach(function (a) { a.cancel(); }); anims = [];
      if (reduce) return;
      var vb = svg.viewBox.baseVal, W = vb.width + vb.x * 2;           // logo width
      var T0 = 250, SCAN = 1500;                                          // beam start, sweep time (ms)
      var at = function (x) { return T0 + (x / W) * SCAN; };

      // 1. plotter grid
      svg.querySelectorAll('.mk').forEach(function (m) {
        var t = at(+m.dataset.x) - 380;
        A(m, [{ opacity: 0 }, { opacity: .45 }], { duration: 360, delay: Math.max(0, t) });
        A(m, [{ opacity: .45 }, { opacity: 0 }], { duration: 700, delay: 2700, fill: 'forwards' });
      });

      // 2. scan beam, linear like an instrument sweep
      var beam = svg.querySelector('.beam');
      A(beam, [{ transform: 'translateX(-4px)' }, { transform: 'translateX(' + (W + 4) + 'px)' }], { duration: SCAN + 160, delay: T0 - 80, easing: 'linear' });
      A(beam, [{ opacity: 0 }, { opacity: 1, offset: .06 }, { opacity: 1, offset: .9 }, { opacity: 0 }], { duration: SCAN + 160, delay: T0 - 80, easing: 'linear' });

      // 3. tiles lock on as the beam crosses: outline traces, then facets light dark to light
      svg.querySelectorAll('.tile').forEach(function (g) {
        var t = at(+g.dataset.x + 4);
        A(g.querySelector('.o'), [{ strokeDashoffset: 1, strokeDasharray: 1 }, { strokeDashoffset: 0, strokeDasharray: 1 }], { duration: 520, delay: t });
        [['d', 140], ['m', 230], ['l', 320]].forEach(function (p) {
          g.querySelectorAll('.' + p[0]).forEach(function (f) {
            A(f, [{ opacity: 0 }, { opacity: 1 }], { duration: 420, delay: t + p[1] });
          });
        });
      });

      // 4. tagline settles in, left to right
      var gl = svg.querySelectorAll('.gl'), TT = 1650;
      gl.forEach(function (p, i) {
        A(p, [{ opacity: 0, transform: 'translateY(5px)' }, { opacity: 1, transform: 'translateY(0)' }], { duration: 560, delay: TT + i * 22 });
      });
      // 5. the three initials take the brand blue, T then A then I
      svg.querySelectorAll('.acc').forEach(function (p, i) {
        var navy = '#193D88', blue = p.getAttribute('fill');
        A(p, [{ fill: navy }, { fill: blue }], { duration: 650, delay: 2750 + i * 160, easing: 'ease-in-out' });
      });

      // 6. one light pass across the facets
      A(svg.querySelector('.sheen'), [{ transform: 'skewX(-18deg) translateX(0)', opacity: 1 }, { transform: 'skewX(-18deg) translateX(' + (W + 140) + 'px)', opacity: 1 }],
        { duration: 1100, delay: 3000, easing: 'cubic-bezier(.45,0,.25,1)', fill: 'none' });
      return anims;
    }
    return { play: play, setRate: function (r) { rate = r; anims.forEach(function (a) { a.playbackRate = r; }); } };
  };
})();
