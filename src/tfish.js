/* TAI SUD T-Fish explainer: dal palmare all'etichetta. Vanilla JS, no dependencies. */
(function () {
  "use strict";

  var SVGNS = "http://www.w3.org/2000/svg";
  var DURATION = [4400, 3600, 3800, 4200]; // ms per step during autoplay

  /* Illustrative QR pattern: deterministic, not a decodable code */
  function rng(seed) {
    var s = seed >>> 0;
    return function () {
      s = (s * 1664525 + 1013904223) >>> 0;
      return s / 4294967296;
    };
  }
  function qrPath(seed) {
    var N = 25, grid = [], reserved = [], x, y;
    for (y = 0; y < N; y++) { grid.push([]); reserved.push([]); for (x = 0; x < N; x++) { grid[y].push(0); reserved[y].push(0); } }
    function finder(ox, oy) {
      for (var j = -1; j <= 7; j++) for (var i = -1; i <= 7; i++) {
        var X = ox + i, Y = oy + j;
        if (X < 0 || Y < 0 || X >= N || Y >= N) continue;
        reserved[Y][X] = 1;
        var ring = i === 0 || i === 6 || j === 0 || j === 6;
        var core = i >= 2 && i <= 4 && j >= 2 && j <= 4;
        grid[Y][X] = (i >= 0 && i <= 6 && j >= 0 && j <= 6 && (ring || core)) ? 1 : 0;
      }
    }
    finder(0, 0); finder(N - 7, 0); finder(0, N - 7);
    for (var t = 8; t < N - 8; t++) {
      grid[6][t] = grid[t][6] = t % 2 === 0 ? 1 : 0;
      reserved[6][t] = reserved[t][6] = 1;
    }
    for (y = 16; y <= 20; y++) for (x = 16; x <= 20; x++) {
      reserved[y][x] = 1;
      grid[y][x] = (x === 16 || x === 20 || y === 16 || y === 20 || (x === 18 && y === 18)) ? 1 : 0;
    }
    var r = rng(seed);
    for (y = 0; y < N; y++) for (x = 0; x < N; x++) if (!reserved[y][x]) grid[y][x] = r() < 0.47 ? 1 : 0;
    var d = "";
    for (y = 0; y < N; y++) for (x = 0; x < N; x++) if (grid[y][x]) d += "M" + x + " " + y + "h1v1h-1z";
    return d;
  }
  function barRects(seed) {
    var r = rng(seed), x = 0, out = [], bar = true;
    var start = [2, 1, 1, 2, 3, 2];
    var stop = [2, 3, 3, 1, 1, 1, 2];
    var seq = start.slice();
    for (var i = 0; i < 54; i++) seq.push(1 + Math.floor(r() * 4));
    seq = seq.concat(stop);
    for (var k = 0; k < seq.length; k++) {
      if (bar) out.push([x, seq[k]]);
      x += seq[k];
      bar = !bar;
    }
    return { rects: out, width: x };
  }
  function paintCodes(root) {
    var qd = qrPath(428);
    var qrs = root.querySelectorAll("[data-tf-qr]");
    for (var i = 0; i < qrs.length; i++) {
      var s = qrs[i];
      s.setAttribute("viewBox", "-1 -1 27 27");
      s.setAttribute("shape-rendering", "crispEdges");
      var p = document.createElementNS(SVGNS, "path");
      p.setAttribute("d", qd);
      p.setAttribute("fill", s.getAttribute("data-tone") === "light" ? "#FFFFFF" : "#0B0B0B");
      s.appendChild(p);
    }
    var b = barRects(4280);
    var bars = root.querySelectorAll("[data-tf-bar]");
    for (var j = 0; j < bars.length; j++) {
      var svg = bars[j];
      svg.setAttribute("viewBox", "0 0 " + b.width + " 10");
      svg.setAttribute("shape-rendering", "crispEdges");
      var d = "";
      b.rects.forEach(function (rc) { d += "M" + rc[0] + " 0h" + rc[1] + "v10h-" + rc[1] + "z"; });
      var path = document.createElementNS(SVGNS, "path");
      path.setAttribute("d", d);
      path.setAttribute("fill", "#0B0B0B");
      svg.appendChild(path);
    }
  }

  function init(root) {
    if (root.__tfInit) return;
    root.__tfInit = true;

    var stage = root.querySelector(".tf__stage");
    var canvas = root.querySelector(".tf__canvas");
    var tabs = Array.prototype.slice.call(root.querySelectorAll('[role="tab"]'));
    var caption = root.querySelector(".tf__caption");
    var toggle = root.querySelector(".tf__toggle");
    var toggleTxt = root.querySelector(".tf__toggle-txt");
    var fields = Array.prototype.slice.call(root.querySelectorAll(".tf-fld__v"));
    var btn = root.querySelector(".tf-scr__btn");
    var reduce = window.matchMedia ? window.matchMedia("(prefers-reduced-motion: reduce)") : { matches: false };

    // Clone the label template into the printer feed so both stay identical
    var tpl = root.querySelector("[data-tf-label]");
    var feed = root.querySelector(".tf-label--feed");
    if (tpl && feed) feed.innerHTML = tpl.innerHTML;
    paintCodes(root);

    // Fit the fixed design canvas to the stage width
    function fit() {
      var w = stage.clientWidth;
      var cw = canvas.offsetWidth || 760;
      canvas.style.setProperty("--k", (w / cw).toFixed(4));
    }
    fit();
    if ("ResizeObserver" in window) new ResizeObserver(fit).observe(stage);
    else window.addEventListener("resize", fit);

    var step = 1;
    var playing = !reduce.matches;
    var inView = false, hovering = false, focused = false;
    var elapsed = 0, last = 0, raf = 0;
    var typeTimers = [];

    /* Typing effect for step 1 */
    function clearTyping() {
      typeTimers.forEach(clearTimeout);
      typeTimers = [];
      fields.forEach(function (f) { f.classList.remove("is-active"); });
      if (btn) btn.classList.remove("is-ready");
    }
    function fillAll() {
      fields.forEach(function (f) { f.textContent = f.getAttribute("data-value"); });
    }
    function type() {
      clearTyping();
      if (reduce.matches) { fillAll(); return; }
      fields.forEach(function (f) { f.textContent = ""; });
      var t = 350;
      fields.forEach(function (f) {
        var val = f.getAttribute("data-value");
        typeTimers.push(setTimeout(function () {
          fields.forEach(function (o) { o.classList.remove("is-active"); });
          f.classList.add("is-active");
        }, t));
        for (var c = 1; c <= val.length; c++) {
          (function (n) {
            typeTimers.push(setTimeout(function () { f.textContent = val.slice(0, n); }, t + 40 + n * 38));
          })(c);
        }
        t += 40 + val.length * 38 + 170;
      });
      typeTimers.push(setTimeout(function () {
        fields.forEach(function (o) { o.classList.remove("is-active"); });
        if (btn) btn.classList.add("is-ready");
      }, t));
    }

    function paintBars(p) {
      tabs.forEach(function (tab, i) {
        var n = i + 1;
        var v = n < step ? 1 : n === step ? p : 0;
        tab.style.setProperty("--p", v.toFixed(3));
        if (n < step) tab.setAttribute("data-done", ""); else tab.removeAttribute("data-done");
      });
    }

    function go(n, opts) {
      opts = opts || {};
      step = n;
      root.setAttribute("data-step", String(n));
      tabs.forEach(function (tab) {
        var on = +tab.getAttribute("data-step") === n;
        tab.setAttribute("aria-selected", on ? "true" : "false");
        tab.tabIndex = on ? 0 : -1;
        if (on) {
          stage.setAttribute("aria-labelledby", tab.id);
          if (caption) caption.textContent = tab.querySelector(".tf__desc").textContent;
          if (opts.focus) tab.focus();
        }
      });
      if (caption) caption.setAttribute("aria-live", opts.user ? "polite" : "off");
      elapsed = 0;
      paintBars(opts.user && !playing ? 1 : 0);
      if (n === 1) type(); else { clearTyping(); fillAll(); }
    }

    function setPlaying(v) {
      playing = v;
      toggle.setAttribute("aria-pressed", v ? "false" : "true");
      toggleTxt.textContent = v ? "Pausa" : "Riproduci";
      if (!v) paintBars(Math.min(1, elapsed / DURATION[step - 1]));
    }

    function active() {
      return playing && inView && !hovering && !focused && !document.hidden;
    }
    function frame(t) {
      var dt = last ? Math.min(100, t - last) : 0;
      last = t;
      if (active()) {
        elapsed += dt;
        var dur = DURATION[step - 1];
        if (elapsed >= dur) go(step % 4 + 1);
        else paintBars(elapsed / dur);
      }
      raf = requestAnimationFrame(frame);
    }

    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        setPlaying(false);
        go(+tab.getAttribute("data-step"), { user: true });
      });
      tab.addEventListener("keydown", function (ev) {
        var n = +tab.getAttribute("data-step"), next = 0;
        if (ev.key === "ArrowRight" || ev.key === "ArrowDown") next = n % 4 + 1;
        else if (ev.key === "ArrowLeft" || ev.key === "ArrowUp") next = (n + 2) % 4 + 1;
        else if (ev.key === "Home") next = 1;
        else if (ev.key === "End") next = 4;
        if (next) {
          ev.preventDefault();
          setPlaying(false);
          go(next, { user: true, focus: true });
        }
      });
    });
    toggle.addEventListener("click", function () {
      var resume = !playing;
      setPlaying(resume);
      if (resume && elapsed >= DURATION[step - 1]) elapsed = 0;
    });

    var hoverZone = root.querySelector(".tf__grid") || root;
    hoverZone.addEventListener("mouseenter", function () { hovering = true; });
    hoverZone.addEventListener("mouseleave", function () { hovering = false; });
    root.addEventListener("focusin", function () { focused = true; });
    root.addEventListener("focusout", function (ev) { if (!root.contains(ev.relatedTarget)) focused = false; });

    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        var was = inView;
        inView = entries[0].isIntersecting;
        if (inView && !was && step === 1 && elapsed === 0) type();
      }, { threshold: 0.35 }).observe(stage);
    } else {
      inView = true;
    }
    if (reduce.addEventListener) reduce.addEventListener("change", function () { if (reduce.matches) setPlaying(false); });

    setPlaying(playing);
    go(+(root.getAttribute("data-step") || 1));
    raf = requestAnimationFrame(frame);
  }

  function boot() {
    var roots = document.querySelectorAll("[data-tf]");
    for (var i = 0; i < roots.length; i++) init(roots[i]);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
