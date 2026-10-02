(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var G = typeof window.gsap !== 'undefined';
  if (G && window.ScrollTrigger) gsap.registerPlugin(ScrollTrigger);
  var mq = function (q) { return window.matchMedia && matchMedia(q).matches; };
  var now = new Date();
  function pad(n) { return (n < 10 ? '0' : '') + n; }

  /* photos: placeholder if missing */
  $$('.photo img').forEach(function (img) {
    function empty() { img.closest('.photo').classList.add('empty'); }
    if (img.complete && !img.naturalWidth) empty();
    img.addEventListener('error', empty);
  });

  /* smooth scroll */
  var lenis = null;
  if (!reduce && window.Lenis && !mq('(pointer: coarse)')) {
    lenis = new Lenis({ lerp: 0.1 });
    if (G) { lenis.on('scroll', function () { window.ScrollTrigger && ScrollTrigger.update(); }); gsap.ticker.add(function (t) { lenis.raf(t * 1000); }); gsap.ticker.lagSmoothing(0); }
    else (function raf(t) { lenis.raf(t); requestAnimationFrame(raf); })(0);
  }
  function lock(on) { if (lenis) { on ? lenis.stop() : lenis.start(); } document.documentElement.style.overflow = on ? 'hidden' : ''; }

  /* header */
  var hdr = $('#hdr'), lastY = 0;
  function onScroll() {
    var y = window.scrollY || 0, open = document.body.classList.contains('menu-open');
    hdr.classList.toggle('scrolled', y > 8);
    var mb = $('.mbar'); if (mb) mb.classList.toggle('on', y > 320);
    hdr.classList.toggle('compact', y > 60 && !open);
    if (y > 600 && y > lastY + 6 && !open) hdr.classList.add('hide');
    else if (y < lastY - 6 || y < 600) hdr.classList.remove('hide');
    lastY = y;
  }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  var burger = $('.burger');
  function setMenu(open) {
    document.body.classList.toggle('menu-open', open);
    burger.setAttribute('aria-expanded', String(open));
    $('.burger .lbl').textContent = open ? 'Chiudi' : 'Menu';
    $$('.mmenu nav a').forEach(function (a, i) { a.style.transitionDelay = open ? (0.18 + i * 0.04) + 's' : '0s'; });
    hdr.classList.remove('hide'); if (open) hdr.classList.remove('compact'); else onScroll();
    $$('main, footer, .mbar').forEach(function (el) { if (open) el.setAttribute('inert', ''); else el.removeAttribute('inert'); });
    if (open) setTimeout(function () { var f = $('.mmenu a'); if (f) f.focus({ preventScroll: true }); }, 350);
    lock(open);
  }
  burger.addEventListener('click', function () { setMenu(!document.body.classList.contains('menu-open')); });
  $$('.mmenu a').forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
  document.addEventListener('keydown', function (e) { if (e.key !== 'Escape') return; if (document.body.classList.contains('menu-open')) { setMenu(false); burger.focus(); } $$('.has-menu').forEach(function (m) { m.classList.remove('open'); m.querySelector('button').setAttribute('aria-expanded', 'false'); }); });
  $$('.has-menu > button').forEach(function (b) { b.addEventListener('click', function () { var m = b.parentNode, o = !m.classList.contains('open'); m.classList.toggle('open', o); b.setAttribute('aria-expanded', String(o)); }); });
  document.addEventListener('click', function (e) { $$('.has-menu').forEach(function (m) { if (!m.contains(e.target)) { m.classList.remove('open'); m.querySelector('button').setAttribute('aria-expanded', 'false'); } }); });
  window.addEventListener('resize', function () { if (window.innerWidth > 1040 && document.body.classList.contains('menu-open')) setMenu(false); });

  /* utc clock in util bar + readout */
  function tick() {
    var d = new Date(), t = pad(d.getUTCHours()) + ':' + pad(d.getUTCMinutes()) + ':' + pad(d.getUTCSeconds());
    $$('[data-utc]').forEach(function (el) { el.textContent = t.slice(0, 5) + ' UTC'; });
    var nx = $('#next-tx'); if (nx) { var s = 1800 - ((d.getUTCMinutes() % 30) * 60 + d.getUTCSeconds()); nx.textContent = pad(Math.floor(s / 60)) + ':' + pad(s % 60); }
  }
  tick(); setInterval(tick, 1000);
  var dl = Math.max(0, Math.ceil((new Date('2027-07-10T00:00:00') - now) / 864e5)); $$('[data-days]').forEach(function (el) { el.textContent = dl; });

  /* deadlines */
  var DL = [
    { d: '2026-01-10', label: '10 gen 2026', t: 'VMS obbligatorio dai 12 metri', p: 'VMS e giornale di pesca elettronico obbligatori per tutte le unità da pesca da 12 metri in su.' },
    { d: '2026-08-31', label: '31 ago 2026', t: 'Fine del periodo transitorio', p: 'Gli apparati devono rispettare le nuove specifiche: display integrato, IP67, memoria di almeno 200 posizioni.' },
    { d: '2027-07-10', label: '10 lug 2027', t: 'Posizione ogni 30 minuti', p: 'Diventa la frequenza standard. 60 minuti solo oltre le 12 miglia e lontano dalle zone di restrizione (FRA).' },
    { d: '2029-01-10', label: 'gennaio 2029', t: 'Tracciabilità digitale estesa', p: 'L\'obbligo di tracciabilità digitale si estende a preparati, conserve, crostacei e molluschi.' }
  ];
  var nextD = DL.filter(function (x) { return new Date(x.d + 'T00:00:00') > now; })[0];
  function st(x) { return new Date(x.d + 'T00:00:00') <= now ? 'past' : (nextD && nextD.d === x.d ? 'next' : 'future'); }
  var lab = { past: 'In vigore', next: 'Prossima scadenza', future: 'In arrivo' };
  var ht = $('#home-dl');
  if (ht) ht.innerHTML = DL.map(function (x) { var s = st(x), c = { past: 'in', next: 'next', future: 'future' }[s]; return '<div class="dl rv ' + s + '"><time>' + x.label + '</time><h3>' + x.t + '</h3><p>' + x.p + '</p><span class="chip ' + c + '"><i></i>' + lab[s] + '</span></div>'; }).join('');
  var nt = $('#norm-dl');
  if (nt) nt.innerHTML = DL.map(function (x) { var s = st(x), c = { past: 'l-in', next: 'l-next', future: 'l-future' }[s]; return '<div class="rv ' + s + '"><time>' + x.label + '</time><b>' + x.t + '</b><p>' + x.p + '</p><span class="chip ' + c + '"><i></i>' + lab[s] + '</span></div>'; }).join('');
  $$('[data-dl-bar]').forEach(function (b) { var s0 = new Date('2026-01-10'), e0 = new Date('2027-07-10'); b.style.width = Math.min(100, Math.max(0, (now - s0) / (e0 - s0) * 100)).toFixed(1) + '%'; });
  var cd = $('#cd-days');
  if (cd) { var days = Math.max(0, Math.ceil((new Date('2027-07-10T00:00:00') - now) / 864e5)); cd.textContent = days; cd.setAttribute('data-count', days); cd.setAttribute('data-from', days + 120); }

  /* faq */
  var FAQ = [
    { id: 'chi-deve', k: 'obbligo 12 metri lunghezza blue box', c: 'obbligo', q: 'Chi deve installare il VMS?', a: '<p>Tutte le unità da pesca da 12 metri in su, dal 10 gennaio 2026. Insieme al VMS è obbligatorio il giornale di pesca elettronico.</p>', home: 1 },
    { id: 'scadenza', k: 'transizione 31 agosto 2026 15 metri', c: 'obbligo', q: 'Entro quando bisognava mettersi in regola?', a: '<p>Il periodo transitorio si è chiuso il 31 agosto 2026. Da quella data gli apparati devono rispettare le nuove specifiche tecniche.</p>', home: 1 },
    { id: 'taibox-conforme', k: 'conformita modifiche blue box', c: 'taibox', q: 'La TaiBox è conforme alle nuove regole?', a: '<p>Sì. Chi ha già una TaiBox non deve modificarla né aggiungere nulla: è conforme alle regole attuali e alle nuove specifiche tecniche.</p>', home: 1 },
    { id: 'ip67', k: 'ip 67 embedded display schermo', c: 'taibox', q: 'Perché l\'apparato deve essere IP67 ed "embedded"?', a: '<p>Lo chiede il Regolamento di esecuzione (UE) 2025/2196. IP67 indica la tenuta ad acqua e polvere: la TaiBox è certificata da gennaio 2026.</p><p>Embedded vuol dire con display integrato. Sulla TaiBox è un touch screen da 7" che mostra stato, avvisi ed errori e permette di cambiare modalità.</p>' },
    { id: 'frequenza-oggi', k: 'ore minuti aree protette guardia costiera', c: 'frequenza', q: 'Ogni quanto si trasmette la posizione oggi?', a: '<p>Almeno ogni 2 ore. Ogni 30 minuti nelle aree protette e nelle 5 miglia che le precedono, o quando la guardia costiera lo chiede per controlli specifici.</p>' },
    { id: '2027', k: '30 minuti 60 fra 12 miglia luglio', c: 'frequenza', q: 'Cosa cambia dal 10 luglio 2027?', a: '<p>La posizione va trasmessa ogni 30 minuti. L\'intervallo può arrivare a 60 minuti solo oltre le 12 miglia dalla costa e ad almeno 5 miglia dalle zone di restrizione della pesca (FRA).</p>', home: 1 },
    { id: 'comandante', k: 'responsabilita obblighi bordo', c: 'bordo', q: 'Cosa deve garantire il comandante?', a: '<p>Che l\'apparato:</p><ul><li>sia acceso e trasmetta per tutta la navigazione</li><li>non venga manomesso</li><li>trasmetta dati corretti</li><li>sia alimentato quando la barca lascia il porto</li></ul>' },
    { id: 'spegnere', k: 'spegnere porto manutenzione standby 24 ore', c: 'bordo', q: 'Si può spegnere l\'apparato?', a: '<p>No, se non dopo averlo comunicato alle autorità competenti. In porto o in manutenzione la TaiBox va in modalità Porto o Manutenzione.</p><p>In queste modalità, senza corrente di bordo, entra in standby e si riattiva da sola ogni 24 ore per inviare la posizione.</p>' },
    { id: 'acm', k: 'rete mobile costiera locale aci acs copertura', c: 'obbligo', q: 'Chi può usare un ACM su rete mobile?', a: '<p>Solo chi fa pesca costiera locale entro le 12 miglia, e solo se la rete copre sia il porto sia la zona di pesca. Senza copertura serve un ACS satellitare o un ACI ibrido.</p>' },
    { id: 'segnale', k: 'guasto memoria 200 posizioni perdita', c: 'bordo', q: 'Cosa succede se si perde il segnale?', a: '<p>L\'apparato salva in memoria almeno 200 posizioni e le invia da solo appena il segnale torna.</p>' }
  ];
  function norm(t) { return (t || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]/g, ''); }
  function faqHTML(list) { return list.map(function (f) { return '<details id="faq-' + f.id + '" data-c="' + f.c + '" data-k="' + norm(f.k + f.q + f.a.replace(/<[^>]+>/g, '')) + '"><summary>' + f.q + '<span class="pm" aria-hidden="true"></span></summary><div class="ans">' + f.a + '</div></details>'; }).join(''); }
  var fh = $('[data-faq="home"]'); if (fh) fh.innerHTML = faqHTML(FAQ.filter(function (f) { return f.home; })).replace(/id="faq-/g, 'id="hfaq-');
  var fa = $('[data-faq="all"]');
  if (fa) {
    fa.innerHTML = faqHTML(FAQ);
    var cat = 'tutte', fq = $('#faq-q'), cnt = $('#faq-count');
    var filt = function () {
      var q = norm(fq.value), n = 0;
      $$('details', fa).forEach(function (d) { var hit = (cat === 'tutte' || d.getAttribute('data-c') === cat) && (!q || d.getAttribute('data-k').indexOf(q) > -1); d.hidden = !hit; if (hit) n++; if (q) d.open = hit; });
      $('#faq-empty').hidden = n > 0; cnt.textContent = n + (n === 1 ? ' risposta' : ' risposte');
    };
    fq.addEventListener('input', filt);
    $$('.fchips button').forEach(function (b) { b.addEventListener('click', function () { cat = b.getAttribute('data-c'); $$('.fchips button').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); }); filt(); }); });
    var all = $('#faq-all'); if (all) all.addEventListener('click', function () { cat = 'tutte'; fq.value = ''; $$('.fchips button').forEach(function (x) { x.setAttribute('aria-pressed', String(x.getAttribute('data-c') === 'tutte')); }); filt(); });
    filt();
    var hd = location.hash && $(location.hash); if (hd && hd.tagName === 'DETAILS') hd.open = true;
  }

  /* partners */
  var PARTNERS = ['Orbcomm', 'Sinlogic', 'Metatron', 'Teko', 'FIAMM', 'Assel', 'Cariati', 'Mengoni'];
  var pt = PARTNERS.map(function (p) { return '<span>' + p + '</span>'; }).join('');
  $$('[data-partners]').forEach(function (el) { el.innerHTML = pt + '<span aria-hidden="true" style="display:contents">' + pt + '</span>'; });
  var yr = $('#yr'); if (yr) yr.textContent = now.getFullYear();

  /* mobile scroller dots */
  $$('[data-dots]').forEach(function (sc) {
    var kids = sc.children, dots = document.createElement('div'); dots.className = 'hs-dots';
    for (var i = 0; i < kids.length; i++) dots.appendChild(document.createElement('i'));
    sc.parentNode.insertBefore(dots, sc.nextSibling);
    function upd() { var w = kids[0] ? kids[0].getBoundingClientRect().width + 14 : 1; var k = Math.round(sc.scrollLeft / w); $$('i', dots).forEach(function (d, j) { d.classList.toggle('on', j === k); }); }
    sc.addEventListener('scroll', upd, { passive: true }); upd();
  });

  /* nautical chart */
  function chart(cv, opt) {
    if (!cv) return;
    var ctx = cv.getContext('2d'), W, H, dpr, bg, boats = [], visible = true, last = 0;
    function rand(a, b) { return a + Math.random() * (b - a); }
    function build() {
      dpr = Math.min(window.devicePixelRatio || 1, 2); W = cv.clientWidth; H = cv.clientHeight;
      if (!W || !H) return;
      cv.width = W * dpr; cv.height = H * dpr;
      bg = document.createElement('canvas'); bg.width = W * dpr; bg.height = H * dpr;
      var b = bg.getContext('2d'); b.scale(dpr, dpr);
      var cs = [[W * .82, H * .25, 1.2], [W * .55, H * .9, .9], [W * .05, H * .1, .7]];
      cs.forEach(function (c, ci) {
        for (var k = 1; k < 14; k++) {
          var r0 = k * 34 * c[2]; b.beginPath();
          for (var a = 0; a <= Math.PI * 2 + .01; a += .04) { var r = r0 * (1 + .14 * Math.sin(3 * a + ci + k * .2) + .07 * Math.sin(5 * a + k * .5) + .04 * Math.sin(9 * a + ci)); var x = c[0] + Math.cos(a) * r * 1.25, y = c[1] + Math.sin(a) * r; a === 0 ? b.moveTo(x, y) : b.lineTo(x, y); }
          b.strokeStyle = 'rgba(25,61,136,' + (k % 4 === 0 ? .13 : .06) + ')'; b.lineWidth = 1; b.stroke();
        }
      });
      var step = 96; b.strokeStyle = 'rgba(25,61,136,.065)';
      for (var gx = step; gx < W; gx += step) { b.beginPath(); b.moveTo(gx + .5, 0); b.lineTo(gx + .5, H); b.stroke(); }
      for (var gy = step; gy < H; gy += step) { b.beginPath(); b.moveTo(0, gy + .5); b.lineTo(W, gy + .5); b.stroke(); }
      b.strokeStyle = 'rgba(25,61,136,.25)';
      for (gx = step; gx < W; gx += step) for (gy = step; gy < H; gy += step) { b.beginPath(); b.moveTo(gx - 3, gy + .5); b.lineTo(gx + 4, gy + .5); b.moveTo(gx + .5, gy - 3); b.lineTo(gx + .5, gy + 4); b.stroke(); }
      b.font = '500 10px "IBM Plex Mono", monospace'; b.fillStyle = 'rgba(25,61,136,.32)';
      for (gx = step; gx < W - 60; gx += step * 2) b.fillText('12°' + pad((gx / step * 7) % 60 | 0) + "'E", gx + 6, H - 10);
      boats = [];
      var n = opt.boats || (W < 700 ? 3 : 6);
      for (var i = 0; i < n; i++) boats.push({ x: rand(W * .1, W * .95), y: rand(H * .1, H * .9), a: rand(0, 6.28), v: rand(.12, .24), turn: 0, trail: [], t: rand(0, 1400) });
    }
    function draw(ts) {
      requestAnimationFrame(draw);
      if (!visible || !bg) return;
      var dt = Math.min(64, ts - (last || ts)); last = ts;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.clearRect(0, 0, W, H); ctx.drawImage(bg, 0, 0, W, H);
      boats.forEach(function (bt) {
        bt.turn = Math.max(-.004, Math.min(.004, bt.turn + rand(-.0004, .0004))); bt.a += bt.turn * dt * .06;
        bt.x += Math.cos(bt.a) * bt.v * dt * .06; bt.y += Math.sin(bt.a) * bt.v * dt * .06;
        if (bt.x < -20 || bt.x > W + 20 || bt.y < -20 || bt.y > H + 20) { bt.x = rand(W * .2, W * .8); bt.y = rand(H * .2, H * .8); bt.trail = []; }
        bt.t += dt; if (bt.t > 1500) { bt.t = 0; bt.trail.push({ x: bt.x, y: bt.y, age: 0 }); if (bt.trail.length > 12) bt.trail.shift(); }
        if (bt.trail.length) { ctx.beginPath(); ctx.moveTo(bt.trail[0].x, bt.trail[0].y); bt.trail.forEach(function (p) { ctx.lineTo(p.x, p.y); }); ctx.lineTo(bt.x, bt.y); ctx.strokeStyle = 'rgba(48,160,218,.45)'; ctx.setLineDash([2, 4]); ctx.lineWidth = 1; ctx.stroke(); ctx.setLineDash([]); }
        bt.trail.forEach(function (p, i) { p.age += dt; ctx.fillStyle = 'rgba(25,61,136,' + (.25 + .5 * i / bt.trail.length) + ')'; ctx.fillRect(p.x - 1.5, p.y - 1.5, 3, 3); if (p.age < 1200) { var k = p.age / 1200; ctx.beginPath(); ctx.arc(p.x, p.y, 3 + k * 18, 0, 7); ctx.strokeStyle = 'rgba(48,160,218,' + (.5 * (1 - k)) + ')'; ctx.stroke(); } });
        ctx.save(); ctx.translate(bt.x, bt.y); ctx.rotate(bt.a); ctx.beginPath(); ctx.moveTo(7, 0); ctx.lineTo(-5, 4.5); ctx.lineTo(-3, 0); ctx.lineTo(-5, -4.5); ctx.closePath(); ctx.fillStyle = '#193D88'; ctx.fill(); ctx.restore();
      });
    }
    build();
    if (reduce) { if (bg) { ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.drawImage(bg, 0, 0, W, H); } return; }
    requestAnimationFrame(draw);
    if ('IntersectionObserver' in window) new IntersectionObserver(function (e) { visible = e[0].isIntersecting; }).observe(cv);
    var tmo; window.addEventListener('resize', function () { clearTimeout(tmo); tmo = setTimeout(build, 160); });
  }
  $$('canvas.chart').forEach(function (c) { chart(c, { boats: c.getAttribute('data-boats') ? +c.getAttribute('data-boats') : 0 }); });

  /* radar */
  (function () {
    var cv = $('#radar'); if (!cv) return;
    var ctx = cv.getContext('2d'), dpr = Math.min(window.devicePixelRatio || 1, 2), S = 92; cv.width = S * dpr; cv.height = S * dpr;
    var blips = [[.55, .3], [.3, .62], [.72, .7]], a = 0;
    function draw() {
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.clearRect(0, 0, S, S);
      var c = S / 2, R = c - 2;
      ctx.fillStyle = '#0B2350'; ctx.beginPath(); ctx.arc(c, c, R, 0, 7); ctx.fill();
      ctx.strokeStyle = 'rgba(138,210,242,.25)'; ctx.lineWidth = 1;
      [R, R * .66, R * .33].forEach(function (r) { ctx.beginPath(); ctx.arc(c, c, r, 0, 7); ctx.stroke(); });
      ctx.beginPath(); ctx.moveTo(c - R, c); ctx.lineTo(c + R, c); ctx.moveTo(c, c - R); ctx.lineTo(c, c + R); ctx.stroke();
      var gr = ctx.createConicGradient ? ctx.createConicGradient(a - 1.2, c, c) : null;
      if (gr) { gr.addColorStop(0, 'rgba(138,210,242,0)'); gr.addColorStop(.19, 'rgba(138,210,242,.45)'); gr.addColorStop(.19, 'rgba(138,210,242,0)'); ctx.fillStyle = gr; ctx.beginPath(); ctx.arc(c, c, R, 0, 7); ctx.fill(); }
      ctx.strokeStyle = '#8AD2F2'; ctx.beginPath(); ctx.moveTo(c, c); ctx.lineTo(c + Math.cos(a) * R, c + Math.sin(a) * R); ctx.stroke();
      blips.forEach(function (b) {
        var bx = b[0] * S, by = b[1] * S, ang = Math.atan2(by - c, bx - c); var d = ((a - ang) % 6.283 + 6.283) % 6.283;
        var al = Math.max(0, 1 - d / 3.5); ctx.fillStyle = 'rgba(255,255,255,' + (.15 + .85 * al) + ')'; ctx.beginPath(); ctx.arc(bx, by, 2.2, 0, 7); ctx.fill();
      });
      a += .025; if (!reduce) requestAnimationFrame(draw);
    }
    draw();
  })();

  /* how it works */
  (function () {
    var hw = $('[data-hw]'); if (!hw) return;
    var items = $$('.hw-it', hw), cap = $('.hw-cap-n', hw), capk = $('.hw-cap-k', hw);
    var reduce = mq('(prefers-reduced-motion: reduce)');
    var cur = 1, timer = 0, inView = false, hover = false, DUR = 5500;
    function set(n) {
      cur = n;
      items.forEach(function (it) { var on = +it.getAttribute('data-s') === n; it.classList.toggle('on', on); $('.hw-btn', it).setAttribute('aria-expanded', on ? 'true' : 'false'); });
      $$('.node', hw).forEach(function (g) { var k = +g.getAttribute('data-n'); g.classList.toggle('on', k <= n); g.classList.toggle('cur', k === n); });
      $$('.flow', hw).forEach(function (f) { f.classList.toggle('on', +f.getAttribute('data-f') <= n); });
      var p = $('.pulse', hw); if (p) p.classList.toggle('on', n >= 2);
      if (cap) cap.textContent = '0' + n + ' / 04';
      if (capk) capk.textContent = $('.hw-k', items[n - 1]).textContent;
      restart();
    }
    function restart() {
      clearTimeout(timer);
      var bar = $('.hw-it.on .hw-bar i', hw);
      if (bar) { bar.style.animation = 'none'; void bar.offsetWidth; bar.style.animation = ''; }
      if (reduce || !inView || hover) { hw.classList.toggle('play', !reduce && inView); return; }
      hw.classList.add('play');
      timer = setTimeout(function () { set(cur % items.length + 1); }, DUR);
    }
    items.forEach(function (it) {
      $('.hw-btn', it).addEventListener('click', function () { set(+it.getAttribute('data-s')); });
    });
    var list = $('.hw-list', hw);
    if (mq('(hover: hover)')) {
      list.addEventListener('mouseenter', function () { hover = true; hw.classList.add('paused'); clearTimeout(timer); });
      list.addEventListener('mouseleave', function () { hover = false; hw.classList.remove('paused'); restart(); });
    }
    new IntersectionObserver(function (es) { es.forEach(function (e) { var was = inView; inView = e.isIntersecting; if (inView && !was) set(cur); if (!inView) { clearTimeout(timer); hw.classList.remove('play'); } }); }, { threshold: .35 }).observe(hw);
    hw.style.setProperty('--hw-dur', DUR + 'ms');
    set(1);
  })();

  /* display mock: modes */
  var MODES = {
    nav: ['Navigazione', 'Trasmette la posizione alla frequenza prevista dal regolamento. Anomalie e infrazioni arrivano al centro di controllo a terra.'],
    porto: ['Porto', 'Con la barca in porto. Senza corrente di bordo la TaiBox va in standby e si riattiva ogni 24 ore per inviare la posizione.'],
    man: ['Manutenzione', 'Durante gli interventi tecnici. Anche qui, in standby, la TaiBox si riattiva ogni 24 ore.'],
    sos: ['SOS', 'Un tasto invia al centro di controllo a terra dati di navigazione, stato della barca e ora.']
  };
  $$('[data-mode]').forEach(function (b) {
    b.addEventListener('click', function () {
      var m = b.getAttribute('data-mode');
      $$('[data-mode]').forEach(function (x) { if (!x.classList.contains('sos')) x.setAttribute('aria-pressed', String(x === b)); });
      $('#mode-lbl').textContent = MODES[m][0].toUpperCase(); $('#mode-t').textContent = MODES[m][0]; $('#mode-d').textContent = MODES[m][1];
      $('#mode-lbl').style.background = m === 'sos' ? '#b3261e' : '';
    });
  });

  /* mini maps */
  function miniMap(cv, o) {
    if (!cv) return;
    var ctx = cv.getContext('2d'), dpr = Math.min(window.devicePixelRatio || 1, 2), W = 0, H = 0, pts = [], t = 0;
    function size() { W = cv.clientWidth; H = cv.clientHeight; cv.width = W * dpr; cv.height = H * dpr; }
    function draw() {
      if (!W) size();
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.clearRect(0, 0, W, H);
      ctx.strokeStyle = o.grid; ctx.lineWidth = 1;
      for (var x = 0; x < W; x += 24) { ctx.beginPath(); ctx.moveTo(x + .5, 0); ctx.lineTo(x + .5, H); ctx.stroke(); }
      for (var y = 0; y < H; y += 24) { ctx.beginPath(); ctx.moveTo(0, y + .5); ctx.lineTo(W, y + .5); ctx.stroke(); }
      ctx.strokeStyle = o.coast; ctx.lineWidth = 1.3; ctx.beginPath();
      for (var i = 0; i <= 40; i++) { var yy = i / 40 * H, xx = W * .2 + Math.sin(i * .5) * 8 + Math.sin(i * .17) * 14; i ? ctx.lineTo(xx, yy) : ctx.moveTo(xx, yy); }
      ctx.stroke();
      if (o.track) {
        t += .006; var px = W * (.5 + .25 * Math.sin(t)), py = H * (.5 + .3 * Math.sin(t * 1.7));
        if (!pts.length || Math.hypot(px - pts[pts.length - 1][0], py - pts[pts.length - 1][1]) > 10) { pts.push([px, py]); if (pts.length > 18) pts.shift(); }
        ctx.setLineDash([2, 3]); ctx.strokeStyle = 'rgba(138,210,242,.8)'; ctx.beginPath(); pts.forEach(function (p, k) { k ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); }); ctx.stroke(); ctx.setLineDash([]);
        ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(px, py, 3, 0, 7); ctx.fill();
        if (!reduce) requestAnimationFrame(draw);
      } else {
        var cx = W * .56, cy = H * .5; ctx.strokeStyle = '#193D88'; ctx.lineWidth = 1.3;
        ctx.beginPath(); ctx.arc(cx, cy, 10, 0, 7); ctx.stroke(); ctx.globalAlpha = .35; ctx.beginPath(); ctx.arc(cx, cy, 26, 0, 7); ctx.stroke(); ctx.globalAlpha = 1;
        ctx.beginPath(); ctx.moveTo(cx - 40, cy); ctx.lineTo(cx + 40, cy); ctx.moveTo(cx, cy - 40); ctx.lineTo(cx, cy + 40); ctx.stroke();
        ctx.fillStyle = '#193D88'; ctx.font = '500 12px "IBM Plex Mono", monospace'; ctx.fillText('TAI SUD · ROMA', cx + 18, cy - 16);
      }
    }
    draw(); window.addEventListener('resize', function () { size(); if (!o.track) draw(); });
  }
  miniMap($('#mini-map'), { grid: 'rgba(138,210,242,.12)', coast: 'rgba(138,210,242,.55)', track: true });
  miniMap($('#map-card'), { grid: 'rgba(25,61,136,.08)', coast: 'rgba(25,61,136,.3)' });

  /* form */
  var form = $('#cform');
  if (form) (function () {
    var LABELS = { taibox: 'Preventivo TaiBox', tfish: 'Preventivo T-Fish', assistenza: 'Assistenza tecnica', moduli: 'Invio moduli', candidatura: 'Candidatura', altro: 'Altro' };
    var MSG = { taibox: 'Quante barche e per quando?', tfish: 'Come gestisci oggi le etichette?', assistenza: 'Cosa segnala l\'apparato?', moduli: 'Note sui moduli inviati', candidatura: 'Presentati in poche righe', altro: 'Il tuo messaggio' };
    function cur() { return form.querySelector('input[name="motivo"]:checked').value; }
    function apply() {
      var m = cur();
      $$('[data-for]', form).forEach(function (el) {
        var on = el.getAttribute('data-for').split(' ').indexOf(m) > -1; el.hidden = !on;
        $$('input, select, textarea', el).forEach(function (i) { i.disabled = !on; });
      });
      $('#msg-label').textContent = MSG[m];
      $('#drop-hint').textContent = m === 'candidatura' ? 'CV in PDF, max 10 MB' : m === 'assistenza' ? 'Foto del display o PDF, max 10 MB per file' : 'PDF, JPG o PNG, max 10 MB per file';
      $('#tel-hint').textContent = m === 'assistenza' ? 'Obbligatorio per l\'assistenza: ti richiama un tecnico.' : 'Per essere richiamato. Serve almeno telefono o email.';
      if ($('#drop').closest('[hidden]')) { files = []; render(); }
    }
    function fromHash() {
      var h = (location.hash || '').replace('#', ''), q = new URLSearchParams(location.search);
      if (LABELS[h]) { var r = form.querySelector('input[value="' + h + '"]'); if (r) r.checked = true; }
      if (q.get('lft')) $('#f-lft').value = q.get('lft');
      if (q.get('zona')) { var z = $('#f-pesca'); if (q.get('zona') === 'costiera') z.value = 'Pesca costiera locale (entro 12 miglia)'; }
      apply();
    }
    window.addEventListener('hashchange', function () { fromHash(); form.scrollIntoView({ behavior: 'smooth', block: 'start' }); });
    $$('input[name="motivo"]', form).forEach(function (r) { r.addEventListener('change', apply); });
    var files = [];
    function render() { $('#files').innerHTML = files.map(function (f, i) { return '<div><span>' + f.name.replace(/</g, '&lt;') + '</span><em>' + (f.size / 1048576).toFixed(1) + ' MB</em><button type="button" data-i="' + i + '">Rimuovi</button></div>'; }).join(''); }
    function add(list) {
      var rej = [];
      Array.prototype.forEach.call(list, function (f) { if (f.size <= 10485760) files.push(f); else rej.push(f.name); });
      render(); $('#file-err').textContent = rej.length ? rej.join(', ') + ': il file supera 10 MB e non è stato aggiunto.' : '';
    }
    fromHash();
    $('#f-files').addEventListener('change', function (e) { add(e.target.files); e.target.value = ''; });
    $('#files').addEventListener('click', function (e) { var i = e.target.getAttribute('data-i'); if (i !== null) { files.splice(+i, 1); render(); } });
    var drop = $('#drop');
    ['dragenter', 'dragover'].forEach(function (ev) { drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.add('over'); }); });
    ['dragleave', 'drop'].forEach(function (ev) { drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.remove('over'); }); });
    drop.addEventListener('drop', function (e) { if (e.dataTransfer) add(e.dataTransfer.files); });
    function mark(id, ok) { var el = document.getElementById(id), f = el.closest('.f'); f.classList.toggle('invalid', !ok); el.setAttribute('aria-invalid', String(!ok)); return ok; }
    function check(id) {
      var m = cur(), nome = $('#f-nome').value.trim(), em = $('#f-email').value.trim(), tel = $('#f-tel').value.replace(/\s/g, '');
      var emOk = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(em), telOk = /^\+?\d{6,}$/.test(tel);
      var r = {
        'f-nome': nome.length > 1,
        'f-email': em ? emOk : (m !== 'assistenza' && telOk),
        'f-tel': tel ? telOk : (m !== 'assistenza' && emOk)
      };
      if (id) return mark(id, r[id]);
      return ['f-nome', 'f-tel', 'f-email'].map(function (k) { return mark(k, r[k]); }).every(Boolean);
    }
    ['f-nome', 'f-email', 'f-tel'].forEach(function (id) {
      var el = document.getElementById(id);
      el.addEventListener('blur', function () { if (el.value) check(id); });
      el.addEventListener('input', function () { if (el.closest('.f').classList.contains('invalid')) check(id); });
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = check(), priv = $('#f-priv').checked;
      $('#consent').classList.toggle('invalid', !priv); $('#consent-err').hidden = priv;
      if (!ok || !priv) { var bad = form.querySelector('.invalid input, .consent.invalid input'); if (bad) { bad.focus(); bad.scrollIntoView({ block: 'center', behavior: 'smooth' }); } return; }
      var m = cur(), rows = [['Motivo', LABELS[m]], ['Nome', $('#f-nome').value]];
      if ($('#f-tel').value) rows.push(['Telefono', $('#f-tel').value]);
      if ($('#f-email').value) rows.push(['Email', $('#f-email').value]);
      if (files.length && !$('#drop').closest('[hidden]')) rows.push(['Allegati', files.length + ' file']);
      $('#sent-sum').innerHTML = rows.map(function (r) { return '<dt>' + r[0] + '</dt><dd>' + String(r[1]).replace(/</g, '&lt;') + '</dd>'; }).join('');
      $('#urgent').hidden = m !== 'assistenza';
      $('#form-body').hidden = true; $('#sent').hidden = false; $('#sent h3').focus();
    });
    $('#again').addEventListener('click', function () { form.reset(); files = []; render(); $('#sent').hidden = true; $('#form-body').hidden = false; apply(); });
  })();

  /* self check: does my boat need VMS */
  $$('[data-check]').forEach(function (box) {
    var st = { lft: null, zona: null };
    var R = {
      none: null,
      small: { t: 'Verifichiamo il tuo caso.', p: 'L\'obbligo VMS in vigore dal 10 gennaio 2026 riguarda le unità da pesca da 12 metri in su. Per barche più corte un tecnico verifica le regole che valgono per te.', c: [['Chiedi la verifica', 'contatti.html#taibox']], tag: 'Da verificare' },
      sat: { t: 'Ti serve un apparato satellitare o ibrido.', p: 'VMS e giornale di pesca elettronico sono obbligatori. Oltre le 12 miglia o senza copertura di rete serve un ACS o un ACI. TaiBox è un ACS autorizzato dal Masaf.', c: [['Preventivo TaiBox', 'contatti.html?lft={l}#taibox'], ['Scarica il questionario', 'modulistica.html#questionario']], tag: 'Obbligo in vigore' },
      coast: { t: 'Il VMS è obbligatorio. Puoi scegliere l\'apparato.', p: 'Per la pesca costiera locale entro 12 miglia, con copertura di rete in porto e in mare, è ammesso anche un ACM. Un ACS come TaiBox trasmette anche dove la rete non arriva.', c: [['Preventivo TaiBox', 'contatti.html?lft={l}&zona=costiera#taibox'], ['Parla con un tecnico', 'tel:+390697840077']], tag: 'Obbligo in vigore' }
    };
    var q2 = $('[data-q="zona"]', box), out = $('.chk-out', box);
    function show() {
      var k = st.lft === 'lt' ? 'small' : (st.lft === 'ge' && st.zona) ? (st.zona === 'costa' ? 'coast' : 'sat') : null;
      q2.classList.toggle('dim', st.lft !== 'ge');
      $$('button', q2).forEach(function (b) { b.disabled = st.lft !== 'ge'; });
      if (!k) { out.innerHTML = '<span class="chk-step">' + (st.lft ? '1' : '0') + ' di 2 risposte</span><h3 class="chk-ph">Il risultato apparirà qui.</h3><p>Ti diciamo se il VMS è obbligatorio per la tua barca e quale apparato serve.</p>'; return; }
      var r = R[k], l = st.lft === 'ge' ? 12 : '';
      out.innerHTML = '<span class="chip ' + (k === 'small' ? 'l-future' : 'l-next') + '"><i></i>' + r.tag + '</span><h3>' + r.t + '</h3><p>' + r.p + '</p>' + (k !== 'small' ? '<p class="chk-note"><b>10 luglio 2027</b> la posizione va trasmessa ogni 30 minuti.</p>' : '') + '<div class="ctas">' + r.c.map(function (c, i) { return '<a class="btn ' + (i ? 'ghost' : '') + ' sm" href="' + c[1].replace('{l}', l) + '">' + c[0] + '</a>'; }).join('') + '</div>';
      if (G && !reduce) gsap.from(out.children, { opacity: 0, y: 12, duration: .5, stagger: .05, ease: 'power2.out' });
    }
    $$('[data-q] button', box).forEach(function (b) {
      b.addEventListener('click', function () {
        var q = b.closest('[data-q]').getAttribute('data-q'); st[q] = b.getAttribute('data-v');
        if (q === 'lft' && st.lft === 'lt') st.zona = null;
        $$('button', b.closest('[data-q]')).forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
        if (q === 'lft' && st.lft === 'lt') $$('button', q2).forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
        show();
      });
    });
    show();
  });

  /* live fleet hero */
  (function () {
    var cv = $('#fleet'); if (!cv || typeof window.TaiFleet !== 'function') return;
    var copy = $('.hero .copy'), hero = $('.hero');
    var ro = $('#ping'), sp = ro ? ro.querySelector('span') : null, tmo;
    TaiFleet(cv, {
      focusRight: true, fadeLeft: true, narrowDim: false,
      avoidRect: function () { if (!copy) return null; var a = copy.getBoundingClientRect(), b = cv.getBoundingClientRect(); if (a.bottom < b.top + 4 || a.top > b.bottom - 4) return null; return { x: a.left - b.left - 24, y: a.top - b.top - 24, w: a.width + 48, h: a.height + 48 }; },
      onPing: function (e) { if (!sp) return; sp.textContent = e.label + ' · trasmissione ricevuta'; ro.classList.add('flash'); clearTimeout(tmo); tmo = setTimeout(function () { ro.classList.remove('flash'); }, 500); }
    }).start();
  })();

  /* motion */
  function reveals() {
    if (!G || reduce || !window.ScrollTrigger) return;
    var items = $$('.rv');
    gsap.set(items, { opacity: 0, y: 26 });
    ScrollTrigger.batch(items, { start: 'top 92%', once: true, onEnter: function (b) { gsap.to(b, { opacity: 1, y: 0, duration: .9, ease: 'power3.out', stagger: .07, overwrite: true }); } });
    document.addEventListener('focusin', function (e) { var r = e.target.closest && e.target.closest('.rv'); if (r) gsap.to(r, { opacity: 1, y: 0, duration: .3, overwrite: true }); });
    $$('[data-count]').forEach(function (el) {
      var to = +el.getAttribute('data-count'), o = { v: +(el.getAttribute('data-from') || 0) };
      ScrollTrigger.create({ trigger: el, start: 'top 92%', once: true, onEnter: function () { gsap.to(o, { v: to, duration: 1.6, ease: 'power2.out', onUpdate: function () { el.textContent = Math.round(o.v); } }); } });
    });
    $$('.mosaic:not(.hero-mosaic)').forEach(function (m) {
      var t = $$('i:not(.e)', m); gsap.set(t, { opacity: 0, scale: .7 });
      ScrollTrigger.create({ trigger: m, start: 'top 85%', once: true, onEnter: function () { gsap.to(t, { opacity: 1, scale: 1, duration: .7, ease: 'back.out(1.6)', stagger: { each: .035, from: 'random' } }); } });
    });
    $$('.band .photo, .cta-photo .photo').forEach(function (p) { gsap.fromTo(p, { yPercent: -5 }, { yPercent: 5, ease: 'none', scrollTrigger: { trigger: p.parentNode, start: 'top bottom', end: 'bottom top', scrub: true } }); });
  }
  function heroIn() {
    if (!G || reduce) return;
    var lines = $$('.hero h1 .ln > span, .page-hero h1 .ln > span');
    if (lines.length) gsap.from(lines, { yPercent: 108, duration: 1.1, ease: 'power4.out', stagger: .08 });
    gsap.from($$('.hero .hin, .page-hero .hin'), { opacity: 0, y: 22, duration: 1, ease: 'power3.out', stagger: .08, delay: .2 });
    var hm = $$('.hero-mosaic i:not(.e)');
    if (hm.length) gsap.from(hm, { opacity: 0, scale: .6, duration: .8, ease: 'back.out(1.5)', stagger: { each: .03, from: 'random' }, delay: .1 });
    var ro = $('.readout'); if (ro) gsap.from(ro, { opacity: 0, y: 24, duration: .9, ease: 'power3.out', delay: .7 });
  }

  /* intro */
  function seen() { try { return sessionStorage.getItem('ts-intro') === '1'; } catch (e) { return false; } }
  function mark() { try { sessionStorage.setItem('ts-intro', '1'); } catch (e) {} }
  function intro(done) {
    var ov = $('#intro');
    if (!ov) return done();
    if (reduce || seen() || typeof window.TaiSudLogo !== 'function') { ov.parentNode.removeChild(ov); return done(); }
    document.body.classList.add('intro-on'); lock(true);
    var svg = ov.querySelector('svg'), flown = false;
    TaiSudLogo(svg).play(); svg.style.visibility = 'visible';
    function fly() {
      if (flown) return; flown = true;
      ov.querySelector('.skip').style.visibility = 'hidden';
      var target = $('.brand svg').getBoundingClientRect(), tiles = svg.querySelector('.tiles').getBoundingClientRect(), box = svg.getBoundingClientRect();
      var s = target.width / tiles.width, tx = target.left - box.left - (tiles.left - box.left) * s, ty = target.top - box.top - (tiles.top - box.top) * s, D = 1250;
      svg.querySelector('.tagline').animate([{ opacity: 1, transform: 'translateY(0)' }, { opacity: 0, transform: 'translateY(10px)' }], { duration: 380, easing: 'ease-in', fill: 'forwards' });
      svg.querySelector('.marks').animate([{ opacity: 1 }, { opacity: 0 }], { duration: 200, fill: 'forwards' });
      var mv = svg.animate([{ transform: 'translate(0px,0px) scale(1)' }, { transform: 'translate(' + tx + 'px,' + ty + 'px) scale(' + s + ')' }], { duration: D, delay: 160, easing: 'cubic-bezier(.76,0,.18,1)', fill: 'forwards' });
      ov.animate([{ backgroundColor: 'rgba(255,255,255,1)' }, { backgroundColor: 'rgba(255,255,255,0)' }], { duration: 900, delay: 160 + D * .45, easing: 'ease-out', fill: 'forwards' });
      setTimeout(done, 160 + D * .5);
      mv.onfinish = function () { document.body.classList.remove('intro-on'); requestAnimationFrame(function () { if (ov.parentNode) ov.parentNode.removeChild(ov); }); lock(false); mark(); };
    }
    setTimeout(fly, 4250);
    ov.querySelector('.skip').addEventListener('click', fly);
  }
  var rp = $('#replay-intro'); if (rp) rp.addEventListener('click', function () { try { sessionStorage.removeItem('ts-intro'); } catch (e) {} location.href = 'home.html'; });

  intro(heroIn);
  reveals();
})();
