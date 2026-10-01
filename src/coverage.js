/* TAI SUD coverage explainer: ACS, ACI o ACM. Vanilla JS, no dependencies. */
(function () {
  "use strict";

  var SVGNS = "http://www.w3.org/2000/svg";

  var MODES = {
    acs: {
      kicker: "Apparato di controllo satellitare",
      text: "Trasmette la posizione via satellite: è valido anche oltre le 12 miglia e dove la rete mobile non arriva.",
      note: "TaiBox è un ACS.",
      zones: [
        ["ok", "Via satellite"],
        ["ok", "Via satellite"],
        ["ok", "Via satellite"]
      ],
      links: ["sat-b1", "sat-b2", "sat-b3"]
    },
    aci: {
      kicker: "Apparato ibrido",
      text: "Abbina la rete mobile a un modulo satellitare: dove la rete mobile non arriva, la posizione viaggia via satellite.",
      note: "",
      zones: [
        ["ok", "Rete mobile o satellite"],
        ["ok", "Rete mobile o satellite"],
        ["ok", "Via satellite"]
      ],
      links: ["mob-b1", "mob-b2", "sat-b3"]
    },
    acm: {
      kicker: "Apparato su rete mobile",
      text: "Ammesso solo per la pesca costiera locale entro le 12 miglia e solo con copertura di rete garantita in porto e in mare. Senza copertura serve un ACS o un ACI.",
      note: "",
      zones: [
        ["cond", "Solo con copertura garantita"],
        ["cond", "Solo con copertura garantita"],
        ["no", "Non ammesso"]
      ],
      links: ["mob-b1", "mob-b2"]
    }
  };
  var ORDER = ["acs", "aci", "acm"];

  function init(root) {
    if (root.__covInit) return;
    root.__covInit = true;

    var tabs = Array.prototype.slice.call(root.querySelectorAll('[role="tab"]'));
    var panel = root.querySelector('[role="tabpanel"]');
    var live = root.querySelector(".cov__live");
    var zoneItems = root.querySelectorAll(".cov__zones li");
    var dotsLayer = root.querySelector(".cov-dots");
    var reduce = window.matchMedia ? window.matchMedia("(prefers-reduced-motion: reduce)") : { matches: false };

    var dots = [];
    var visible = true;
    var raf = 0;

    function linkGeom(id) {
      var l = root.querySelector('[data-link="' + id + '"]');
      if (!l) return null;
      return {
        // dots travel from the boat (x2,y2) up to the receiver (x1,y1): the boat reports its position
        x0: +l.getAttribute("x2"), y0: +l.getAttribute("y2"),
        x1: +l.getAttribute("x1"), y1: +l.getAttribute("y1"),
        kind: id.indexOf("sat") === 0 ? "sat" : "mob"
      };
    }

    function buildDots(mode) {
      while (dotsLayer.firstChild) dotsLayer.removeChild(dotsLayer.firstChild);
      dots = [];
      MODES[mode].links.forEach(function (id, i) {
        var g = linkGeom(id);
        if (!g) return;
        for (var k = 0; k < 2; k++) {
          var c = document.createElementNS(SVGNS, "circle");
          c.setAttribute("r", "5");
          c.setAttribute("class", "cov-dot cov-dot--" + g.kind);
          dotsLayer.appendChild(c);
          dots.push({ el: c, g: g, phase: k * 0.5 + i * 0.17 });
        }
      });
      place(performance.now());
    }

    function place(t) {
      var still = reduce.matches;
      for (var i = 0; i < dots.length; i++) {
        var d = dots[i];
        var p = still ? 0.5 + (d.phase % 1 - 0.25) * 0.4 : ((t / 2600) + d.phase) % 1;
        var e = p < 0.5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
        var x = d.g.x0 + (d.g.x1 - d.g.x0) * e;
        var y = d.g.y0 + (d.g.y1 - d.g.y0) * e;
        d.el.setAttribute("cx", x.toFixed(1));
        d.el.setAttribute("cy", y.toFixed(1));
        var o = still ? 1 : Math.min(1, Math.sin(Math.PI * p) * 1.6);
        d.el.setAttribute("opacity", o.toFixed(2));
      }
    }

    function loop(t) {
      place(t);
      raf = requestAnimationFrame(loop);
    }
    function start() {
      if (raf || reduce.matches || !visible) return;
      raf = requestAnimationFrame(loop);
    }
    function stop() {
      if (raf) cancelAnimationFrame(raf);
      raf = 0;
    }

    function render(mode) {
      var m = MODES[mode];
      var html =
        '<p class="cov__kicker"></p><p class="cov__text"></p>' +
        (m.note ? '<p class="cov__note"><span class="cov__badge">TaiBox</span> <span></span></p>' : "");
      live.innerHTML = html;
      live.querySelector(".cov__kicker").textContent = m.kicker;
      live.querySelector(".cov__text").textContent = m.text;
      if (m.note) live.querySelector(".cov__note span:last-child").textContent = m.note;
      for (var i = 0; i < zoneItems.length; i++) {
        zoneItems[i].setAttribute("data-state", m.zones[i][0]);
        zoneItems[i].querySelector(".cov__zval").textContent = m.zones[i][1];
      }
      live.classList.remove("is-swap");
      void live.offsetWidth;
      live.classList.add("is-swap");
    }

    function select(mode, focus) {
      if (!MODES[mode]) return;
      root.setAttribute("data-mode", mode);
      tabs.forEach(function (tab) {
        var on = tab.getAttribute("data-mode") === mode;
        tab.setAttribute("aria-selected", on ? "true" : "false");
        tab.tabIndex = on ? 0 : -1;
        if (on) {
          panel.setAttribute("aria-labelledby", tab.id);
          if (focus) tab.focus();
        }
      });
      render(mode);
      buildDots(mode);
    }

    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () { select(tab.getAttribute("data-mode"), false); });
      tab.addEventListener("keydown", function (ev) {
        var idx = ORDER.indexOf(tab.getAttribute("data-mode"));
        var next = null;
        if (ev.key === "ArrowRight" || ev.key === "ArrowDown") next = ORDER[(idx + 1) % 3];
        else if (ev.key === "ArrowLeft" || ev.key === "ArrowUp") next = ORDER[(idx + 2) % 3];
        else if (ev.key === "Home") next = ORDER[0];
        else if (ev.key === "End") next = ORDER[2];
        if (next) { ev.preventDefault(); select(next, true); }
      });
    });

    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        visible = entries[0].isIntersecting;
        if (visible) start(); else stop();
      }, { threshold: 0.05 }).observe(root);
    }
    var onMotion = function () { if (reduce.matches) { stop(); place(0); } else start(); };
    if (reduce.addEventListener) reduce.addEventListener("change", onMotion);

    var initial = root.getAttribute("data-mode") || "acs";
    root.setAttribute("data-mode", initial);
    buildDots(initial);
    start();
  }

  function boot() {
    var roots = document.querySelectorAll("[data-cov]");
    for (var i = 0; i < roots.length; i++) init(roots[i]);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
