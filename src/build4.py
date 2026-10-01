import re, os, shutil
D = '/home/claude/site4/'
svgsrc = open('/home/claude/svg_part.html').read()
css = open(D + 'styles.css').read() + open(D + 'v4.css').read()
appjs = open(D + 'app.js').read()
logojs = open('/home/claude/script_part.js').read()
sprite = open('/home/claude/site2/sprite.svg').read()

def variant(svg, pfx, keep_tagline, cls, vb, negative=False):
    v = svg.replace('id="tc', f'id="{pfx}c').replace('url(#tc', f'url(#{pfx}c')
    for a in ('ts-all', 'ts-beam', 'ts-sheen'):
        v = v.replace(a, a.replace('ts', pfx))
    v = v.replace('taisud-t', pfx + '-t')
    v = re.sub(r'<g class="marks".*?</g>', '', v, flags=re.S)
    v = re.sub(r'<g clip-path="url\(#[a-z]+-all\)"><rect class="sheen".*?</g>', '', v, flags=re.S)
    v = re.sub(r'<g class="beam">.*?</g>', '', v, flags=re.S)
    v = re.sub(r'<linearGradient.*?</linearGradient>', '', v, flags=re.S)
    if not keep_tagline:
        v = re.sub(r'<g class="tagline">.*?</g>', '', v, flags=re.S)
    if negative:
        v = v.replace('stroke="#193D88"', 'stroke="#EEF3FA"')
        v = re.sub(r'class="gl" d="([^"]+)" fill="#193D88"', r'class="gl" d="\1" fill="#EEF3FA"', v)
        v = re.sub(r'class="gl acc" d="([^"]+)" fill="#30A0DA"', r'class="gl acc" d="\1" fill="#8AD2F2"', v)
    v = v.replace('class="taisud-logo"', f'class="{cls}"')
    v = re.sub(r'viewBox="[^"]+"', f'viewBox="{vb}"', v, count=1)
    return v
m = re.search(r'viewBox="([-\d. ]+)"', svgsrc).group(1).split()
LW = float(m[2]) - 12; LH = float(m[3]) - 12
HDR_LOGO = variant(svgsrc, 'h', False, 'brand-mark', f"0 0 {LW:.2f} 111")
FTR_LOGO = variant(svgsrc, 'f', True, 'foot-mark', f"-1 -1 {LW+2:.2f} {LH+2:.2f}", negative=True)
MARK = variant(svgsrc, 'k', False, 'f-mark', f"0 0 {LW:.2f} 111", negative=True)
INTRO_LOGO = svgsrc.replace('role="img"', 'role="img" aria-hidden="true"')

A = '<svg><use href="#i-arrow"/></svg>'
TI = '<i class="tile-ico"></i>'
def ti(r=''): return f'<i class="tile-ico {r}"></i>'
def eb(t, r=''): return f'<span class="eyebrow hin rv">{ti(r)}{t}</span>'

def mosaic(img, layout, cls=''):
    rows = [r.split() for r in layout]
    R, C = len(rows), len(rows[0])
    out = []
    for r, row in enumerate(rows):
        for c, tok in enumerate(row):
            if tok == '.':
                out.append('<i class="e"></i>'); continue
            k = tok.lower()
            shape = '' if k in ('s', 'f') else k.replace('f', '')
            if k.startswith('f'):
                out.append(f'<i class="f {shape}"></i>'); continue
            px = c / (C - 1) * 100 if C > 1 else 50
            py = r / (R - 1) * 100 if R > 1 else 50
            out.append(f'<i class="{shape}" style="background-image:url(img/{img});background-position:{px:.1f}% {py:.1f}%"></i>')
    return f'<div class="mosaic {cls}" style="--cols:{C};--rows:{R}" aria-hidden="true">{"".join(out)}</div>'

def photo(src, alt, cls=''):
    return f'<figure class="photo {cls}"><img src="img/{src}" alt="{alt}" loading="lazy"><span class="ph">{src}</span></figure>'

NAV = [('chi-siamo', 'Chi siamo'), ('prodotti', 'Prodotti e servizi'), ('normativa', 'Normativa'), ('assistenza', 'Assistenza'), ('modulistica', 'Modulistica'), ('contatti', 'Contatti')]
PROD = {'prodotti', 'taibox', 't-fish'}

def header(active):
    items = []
    for slug, label in NAV:
        if slug == 'prodotti':
            act = ' active' if active in PROD else ''
            items.append(f'''<div class="has-menu{act}"><button type="button" aria-expanded="false" aria-haspopup="true">Prodotti e servizi <svg class="chev"><use href="#i-chev"/></svg></button>
<div class="mega">
<a class="card" href="taibox.html"><i class="thumb" style="background-image:url(img/taibox-kit-wide.jpg)"></i><div><b>{TI}TaiBox</b><span>Blue box VMS per pescherecci, autorizzata Masaf</span></div></a>
<a class="card" href="t-fish.html"><i class="thumb" style="background-image:url(img/mercato.jpg)"></i><div><b>{ti("r-bl")}T-Fish</b><span>Etichette e tracciabilità del pescato</span></div></a>
<div class="clock"><small>Prossima scadenza VMS</small><b data-days>--</b><span>giorni al 10 luglio 2027, quando la posizione andrà trasmessa ogni 30 minuti.</span><a href="normativa.html">Cosa cambia {A}</a></div>
<a class="all" href="prodotti.html">Panoramica prodotti e servizi {A}</a>
</div></div>''')
        else:
            cur = ' aria-current="page"' if active == slug else ''
            items.append(f'<a href="{slug}.html"{cur}>{label}</a>')
    mm = [('taibox', 'TaiBox', 'Blue box VMS'), ('t-fish', 'T-Fish', 'Etichette del pescato'), ('prodotti', 'Prodotti e servizi', 'Satellite e manutenzione'), ('normativa', 'Normativa', 'Scadenze, obblighi, FAQ'), ('assistenza', 'Assistenza', 'Guasti e segnalazioni'), ('modulistica', 'Modulistica', 'Questionario e installazione'), ('chi-siamo', 'Chi siamo', 'Dal 1988 a Roma'), ('contatti', 'Contatti', 'Preventivi e richieste')]
    mmh = ''.join(f'<a href="{s}.html"{" aria-current=\"page\"" if s==active else ""}><small>{i+1:02d}</small>{l}<em>{d}</em></a>' for i, (s, l, d) in enumerate(mm))
    return f'''<header class="site-header" id="hdr">
<div class="util"><div class="wrap"><div class="l"><span class="lbl">Assistenza TaiBox</span><a href="tel:+390697840077">06 97840077</a><a class="hide-s" href="mailto:info@taisud.com">info@taisud.com</a></div><div class="r"><a class="dl-chip" href="normativa.html"><i></i>Trasmissione ogni 30 min dal 10.07.2027 · <b><span data-days>--</span> giorni</b></a><span data-utc>--:-- UTC</span></div></div></div>
<div class="mainbar"><div class="wrap bar">
<a class="brand" href="home.html" aria-label="Tai Sud, home">{HDR_LOGO}</a>
<nav class="nav" aria-label="Principale">{''.join(items)}</nav>
<div class="hdr-cta"><a class="hdr-phone" href="tel:+390697840077"><svg><use href="#i-phone"/></svg><span><small>Assistenza</small>06 97840077</span></a><a class="btn sm" href="contatti.html#taibox">Preventivo TaiBox</a></div>
<button class="burger" type="button" aria-expanded="false" aria-controls="mmenu"><span class="lbl">Menu</span><span class="bx"><span></span><span></span></span></button>
</div></div></header>
<div class="mmenu" id="mmenu"><nav aria-label="Menu">{mmh}</nav>
<div class="mm-quick"><a href="tel:+390697840077"><span>Assistenza tecnica</span><b>Chiama<br>06 97840077</b></a><a href="contatti.html#taibox"><span>Preventivo TaiBox</span><b>Compila<br>la richiesta</b></a></div>
<div class="mm-foot"><span>TAI SUD s.r.l.<br>Viale G. Bonelli 341, Roma</span><div class="tile-strip"><i></i><i style="--o:.7"></i><i style="--o:.45"></i><i style="--o:.25"></i></div></div></div>'''

FOOTER = f'''<footer class="site-footer">
<div class="wrap f-top">
<div class="brandcol"><a href="home.html" aria-label="Tai Sud, home">{FTR_LOGO}</a><p>Apparati di controllo satellitare per la pesca professionale. Fornitura, installazione, traffico satellitare e manutenzione, dal 1988.</p><div class="phone-big"><small>Assistenza tecnica</small><a href="tel:+390697840077">06 97840077</a></div><div class="certs"><img src="img/imq.png" alt="IMQ, ISO 9001:2015"><img src="img/accredia.png" alt="ACCREDIA"></div></div>
<div><p class="fh">Prodotti</p><ul><li><a href="taibox.html">TaiBox</a></li><li><a href="t-fish.html">T-Fish</a></li><li><a href="prodotti.html#servizi">Servizi</a></li><li><a href="normativa.html">Normativa VMS</a></li><li><a href="normativa.html#faq">FAQ</a></li></ul></div>
<div><p class="fh">Azienda</p><ul><li><a href="chi-siamo.html">Chi siamo</a></li><li><a href="qualita.html">Qualità</a></li><li><a href="lavora-con-noi.html">Lavora con noi</a></li><li><a href="modulistica.html">Modulistica</a></li><li><a href="assistenza.html">Assistenza</a></li><li><a href="contatti.html">Contatti</a></li></ul></div>
<div class="addr"><p class="fh">Sede</p><address><span>Viale Gianluigi Bonelli, 341<br>00127 Roma (RM)</span><a href="tel:+390697840077" style="margin-top:10px">(+39) 06 97840077</a><a href="tel:+390697040156">(+39) 06 97040156</a><a href="mailto:info@taisud.com">info@taisud.com</a></address></div>
</div>
<div class="wrap f-bot"><span>© <span id="yr">2026</span> TAI SUD s.r.l. · P.IVA 03786241004</span><nav><a href="https://www.iubenda.com/privacy-policy/67795620" target="_blank" rel="noopener">Privacy</a><a href="https://www.iubenda.com/privacy-policy/67795620/cookie-policy" target="_blank" rel="noopener">Cookie</a><a href="qualita.html">Politica della qualità</a></nav></div>
</footer>
<nav class="mbar" aria-label="Azioni rapide"><a href="tel:+390697840077"><svg><use href="#i-phone"/></svg>Assistenza</a><a href="contatti.html#taibox">Preventivo TaiBox</a></nav>'''

def crumbs(*parts):
    out = ['<a href="home.html">Home</a>']
    for p in parts:
        out.append('<i></i>')
        out.append(f'<a href="{p[1]}">{p[0]}</a>' if len(p) > 1 else f'<span>{p[0]}</span>')
    return '<nav class="crumbs hin" aria-label="Percorso">' + ''.join(out) + '</nav>'

def h1(lines, extra=''):
    return f'<h1 class="h-xl"{extra}>' + ''.join(f'<span class="ln"><span>{l}</span></span>' for l in lines) + '</h1>'

def cta(title, text, primary=('Richiedi preventivo', 'contatti.html#taibox'), secondary=('06 97840077', 'tel:+390697840077'), img='faro.jpg'):
    return f'''<section class="sec" style="padding-top:clamp(40px,5vw,72px)"><div class="wrap"><div class="cta-photo rv">{photo(img, '')}<div class="in"><div><h2 class="h-l">{title}</h2><p>{text}</p></div><div class="ctas"><a class="btn white" href="{primary[1]}">{primary[0]} {A}</a><a class="btn line-w" href="{secondary[1]}">{secondary[0]}</a></div></div></div></div></section>'''

def page_hero(crumb, eyebrow, lines, lead, side='', extra='', chart=True):
    cls = '' if side else ' text-only'
    ch = '<canvas class="chart" data-boats="3" aria-hidden="true"></canvas>' if chart else ''
    sidehtml = f'<div class="side">{side}</div>' if side else ''
    return f'''<section class="page-hero{cls}">{ch}<div class="wrap"><div class="stack">{crumb}{eb(eyebrow)}{h1(lines)}<p class="lead hin">{lead}</p>{extra}</div>{sidehtml}</div></section>'''

FAQ_SEC = '''<section class="sec mist"><div class="wrap two">
<div class="stack sticky">{eb}<h2 class="h-l rv">Le domande degli armatori.</h2><p class="lead rv">Risposte brevi sulle regole VMS e sulla TaiBox.</p><a class="btn ghost rv" href="normativa.html#faq" style="justify-self:start">Tutte le FAQ {A}</a></div>
<div class="faq" data-faq="home"></div></div></section>'''.replace('{eb}', eb('FAQ')).replace('{A}', A)

PARTNERS = '<section class="sec tight" style="padding-bottom:16px"><div class="wrap">' + eb('Partner e fornitori') + '</div><div class="marquee" style="margin-top:30px"><div class="track" data-partners></div></div></section>'

P = {}

# ================= HOME =================
P['home'] = ('Blue box VMS per la pesca professionale', f'''
<section class="hero"><canvas class="chart" aria-hidden="true"></canvas><div class="wrap">
<div>
<span class="eyebrow hin">{TI}Produttore autorizzato Masaf · dal 1988</span>
{h1(['Il tuo peschereccio,', '<em>sempre in regola.</em>'])}
<p class="lead hin">TaiBox è la blue box che progettiamo e produciamo a Roma. La installiamo a bordo, gestiamo il traffico satellitare e ti seguiamo nel tempo.</p>
<div class="ctas hin"><a class="btn" href="contatti.html#taibox">Richiedi un preventivo {A}</a><a class="btn ghost" href="taibox.html">Scopri la TaiBox</a></div>
</div>
<div class="hero-media">{mosaic('hero.jpg', ['. tl s s s', 'tl s s s s', 's s s s br', 'ftr s s br .'], 'hero-mosaic')}
<aside class="readout" aria-label="Stato apparato"><div class="rh"><span>TaiBox · VMS</span><span class="live"><i></i>Online</span></div><div class="rb"><canvas id="radar" width="92" height="92"></canvas><dl><dt>Prossima tx</dt><dd id="next-tx">--:--</dd><dt>Frequenza</dt><dd>30 min</dd><dt>Protezione</dt><dd>IP67</dd><dt>Modalità</dt><dd>Navig.</dd></dl></div></aside>
</div></div></section>

<div class="trust"><div class="wrap">
<div class="t rv">{TI}<b>Produttore autorizzato</b><span>TaiBox è nell'elenco ufficiale del Masaf. <a href="https://www.controllopesca.politicheagricole.it/flex/cm/pages/ServeBLOB.php/L/IT/IDPagina/153" target="_blank" rel="noopener">Verifica ↗</a></span></div>
<div class="t rv"><div class="badges"><img src="img/imq.png" alt="IMQ, ISO 9001:2015"><img src="img/accredia.png" alt="ACCREDIA"></div><span>Qualità certificata ISO 9001:2015</span></div>
<div class="t rv">{ti("r-tl")}<b>Dal 1988</b><span>Tecnologia per l'industria, a Roma</span></div>
<div class="t rv">{ti("r-br")}<b>Un solo fornitore</b><span>Apparato, satellite, installazione e assistenza</span></div>
</div></div>

<section class="sec dark"><div class="wrap">
<div class="sec-head split"><div class="stack">{eb('Normativa VMS')}<h2 class="h-l rv">Le date che contano.</h2><p class="lead rv">Dal 2026 il VMS è obbligatorio per tutte le barche da 12 metri in su. La prossima tappa è la frequenza di trasmissione.</p></div>
<div class="countdown rv"><b id="cd-days">--</b><span>giorni al<br>10 luglio 2027</span></div></div>
<div class="tl hs-m" id="home-dl" data-dots></div>
<div style="margin-top:44px" class="rv"><a class="link-arrow" href="normativa.html">Normativa completa e FAQ {A}</a></div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head split"><div class="stack">{eb('Prodotti e servizi')}<h2 class="h-l rv">Due prodotti. Un unico interlocutore.</h2></div><p class="lead rv">Dalla plancia al banco del pesce, con un'assistenza che risponde.</p></div>
<div class="sol-grid">
<a class="sol rv" href="taibox.html"><span class="beam-border"></span><div class="ph"><img src="img/taibox-kit-wide.jpg" alt="Kit TaiBox con antenna satellitare" loading="lazy"><span class="chip l-in"><i></i>Conforme 2026</span></div>
<div class="body"><span class="eyebrow">{TI}Blue box · ACS</span><h3 class="h-m">TaiBox</h3><ul class="blist"><li>{TI}Posizione e rotta al centro di controllo, via satellite</li><li>{TI}Display touch 7", certificata IP67</li><li>{TI}SOS, avvisi di anomalia e di manomissione</li></ul><span class="link-arrow">Scopri la TaiBox {A}</span></div></a>
<a class="sol rv" href="t-fish.html"><span class="beam-border"></span><div class="ph"><img src="img/mercato.jpg" alt="Pescato su ghiaccio" loading="lazy"></div>
<div class="body"><span class="eyebrow">{ti("r-bl")}Tracciabilità</span><h3 class="h-m">T-Fish</h3><ul class="blist"><li>{TI}Palmare con app e stampante Zebra</li><li>{TI}Etichette con codice a barre e QR code</li></ul><span class="link-arrow">Scopri T-Fish {A}</span></div></a>
</div>
<div class="svc-row rv" id="servizi-home">
<div class="svc"><svg><use href="#i-install"/></svg><b>Installazione</b><span>Montaggio a bordo e collaudo.</span></div>
<div class="svc"><svg><use href="#i-sat"/></svg><b>Traffico satellitare</b><span>Fornitore autorizzato del servizio.</span></div>
<div class="svc"><svg><use href="#i-wrench"/></svg><b>Manutenzione</b><span>Interventi e aggiornamenti.</span></div>
<div class="svc"><svg><use href="#i-phone"/></svg><b>Assistenza</b><span>Un tecnico al telefono.</span></div>
</div></div></section>

<section class="sec dark"><div class="wrap">
<div class="sec-head">{eb('Come funziona')}<h2 class="h-l rv">Dalla barca al centro di controllo.</h2></div>
<div class="how">
<div class="how-steps">
<div class="how-step" data-s="1"><span class="n">01 · BORDO</span><h3>La TaiBox calcola la posizione</h3><p>Il GPS rileva posizione, rotta e velocità. Il comandante vede tutto sul display.</p></div>
<div class="how-step" data-s="2"><span class="n">02 · SATELLITE</span><h3>Trasmette via satellite</h3><p>Alla frequenza prevista dalla legge, anche dove il telefono non prende.</p></div>
<div class="how-step" data-s="3"><span class="n">03 · TERRA</span><h3>Il centro di controllo riceve</h3><p>La posizione arriva a terra. Da lì l'apparato si può anche riprogrammare.</p></div>
<div class="how-step" data-s="4"><span class="n">04 · AVVISI</span><h3>Anomalie e SOS in automatico</h3><p>Guasti, manomissioni e uscite dai limiti generano un report. L'SOS parte con un tasto.</p></div>
</div>
<div class="how-stage" aria-hidden="true"><svg viewBox="0 0 520 520">
<g class="rings"><circle cx="260" cy="260" r="110"/><circle cx="260" cy="260" r="190" stroke-dasharray="2 6"/><circle cx="260" cy="260" r="250" stroke-dasharray="1 9"/></g>
<g class="sweep"><path d="M260 260 L260 70 A190 190 0 0 1 394 126 Z" fill="url(#sw)"/></g>
<defs><linearGradient id="sw" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#8AD2F2" stop-opacity="0"/><stop offset="1" stop-color="#8AD2F2" stop-opacity=".18"/></linearGradient></defs>
<path class="link" d="M120 400 L260 110 L400 400 L400 220"/>
<path class="flow" data-f="2" pathLength="1" d="M120 400 L260 110"/><path class="flow" data-f="3" pathLength="1" d="M260 110 L400 400"/><path class="flow" data-f="4" pathLength="1" d="M400 400 L400 220"/>
<circle class="pulse" r="4"><animateMotion dur="2.6s" repeatCount="indefinite" path="M120 400 L260 110 L400 400 L400 220"/></circle>
<g class="node" data-n="1"><rect x="60" y="370" width="120" height="70" rx="6"/><svg class="ic" x="102" y="378" width="36" height="36"><use href="#i-boat"/></svg><text x="120" y="430" text-anchor="middle">TAIBOX</text></g>
<g class="node" data-n="2"><circle class="base" cx="260" cy="110" r="44"/><svg class="ic" x="240" y="90" width="40" height="40"><use href="#i-sat"/></svg><text x="260" y="176" text-anchor="middle">SATELLITE</text></g>
<g class="node" data-n="3"><rect x="340" y="370" width="120" height="70" rx="6"/><svg class="ic" x="382" y="376" width="36" height="36"><use href="#i-remote"/></svg><text x="400" y="430" text-anchor="middle">CENTRO A TERRA</text></g>
<g class="node" data-n="4"><rect x="340" y="160" width="120" height="70" rx="6"/><svg class="ic" x="382" y="166" width="36" height="36"><use href="#i-alert"/></svg><text x="400" y="220" text-anchor="middle">AVVISI · SOS</text></g>
</svg></div>
</div></div></section>

<section class="band">{photo('porto.jpg', 'Porto del Mediterraneo')}
<div class="wrap on-photo"><span class="eyebrow rv">{TI}Un solo fornitore</span><h2 class="h-l rv">Dal porto al largo, una sola persona da chiamare.</h2>
<div class="facts rv"><span>{TI}Produttore autorizzato</span><span>{TI}Traffico satellitare</span><span>{TI}Manutenzione</span><span>{TI}Assistenza tecnica</span></div></div></section>

<section class="sec"><div class="wrap">
<div class="sec-head split"><div class="stack">{eb('Il percorso')}<h2 class="h-l rv">Dalla richiesta alla barca in regola.</h2></div><p class="lead rv">Cinque passaggi, seguiti da noi. I moduli sono pronti da scaricare.</p></div>
<ol class="journey hs-m" data-dots>
<li class="rv"><b>Questionario</b><span>Ci racconti barca e tipo di pesca.</span><a class="link-arrow" href="modulistica.html">Scarica {A}</a></li>
<li class="rv"><b>Preventivo</b><span>Offerta per apparato e servizio.</span></li>
<li class="rv"><b>Richiesta di installazione</b><span>Avvia montaggio e registrazione.</span><a class="link-arrow" href="modulistica.html">Scarica {A}</a></li>
<li class="rv"><b>Installazione e collaudo</b><span>Montiamo la TaiBox e verifichiamo che trasmetta.</span></li>
<li class="rv"><b>Assistenza</b><span>Per tutta la vita dell'apparato.</span></li>
</ol></div></section>

<section class="sec mist tight"><div class="wrap"><div class="nums">
<div class="num rv"><b data-count="1988" data-from="1960">1988</b><span>Fondazione, a Roma</span></div>
<div class="num rv"><b>IP<span data-count="67" data-from="0">67</span></b><span>Certificazione TaiBox, gennaio 2026</span></div>
<div class="num rv"><b><span data-count="7" data-from="0">7</span><small>pollici</small></b><span>Display touch integrato</span></div>
<div class="num rv"><b><span data-count="30" data-from="120">30</span><small>min</small></b><span>Pronta per la frequenza 2027</span></div>
</div></div></section>
{FAQ_SEC}
{PARTNERS}
''' + cta('La tua barca è in regola?', 'Mandaci lunghezza e tipo di pesca. Ti diciamo cosa serve e ti prepariamo un preventivo.'))

# ================= CHI SIAMO =================
P['chi-siamo'] = ('Chi siamo', page_hero(crumbs(('Chi siamo',)), 'Chi siamo · dal 1988', ['Dal 1988,', 'tecnologia che', 'lavora in mare.'], 'Tai Sud progetta, produce e assiste apparati di controllo satellitare per la pesca professionale.', mosaic('porto.jpg', ['tl s s ftr', 's s s s', 'fbl s s br'])) + f'''
<section class="sec"><div class="wrap mt">
<div class="stack">{eb('La storia')}<h2 class="h-l rv">Fondata e fatta crescere da Alberto Tirico.</h2>
<p class="lead rv">Alberto Tirico fonda Tai Sud a Roma nel 1988 e la guida per oltre trent'anni.</p>
<p class="muted rv">L'azienda nasce per progettare sistemi informativi ad alto contenuto tecnologico. Cresce nell'integrazione di soluzioni aziendali e, dal 2000, nei progetti chiavi in mano con una rete di partner qualificati. Con la TaiBox entra nel controllo satellitare della pesca.</p>
<p class="muted rv">Oggi la direzione è affidata a Martina Tirico e Alessandro.</p></div>
{photo('magazzino.jpg', 'Apparati TaiBox pronti per la consegna nel magazzino Tai Sud', 'cut rv')}
</div></section>

<section class="sec mist"><div class="wrap two">
<div class="stack sticky">{eb('Le tappe')}<h2 class="h-l rv">Quattro passaggi chiave.</h2></div>
<div class="vtl">
<div class="past rv"><time>1988</time><b>Fondazione a Roma</b><p>Sistemi informativi ad alto contenuto tecnologico.</p></div>
<div class="past rv"><time>2000</time><b>Progetti chiavi in mano</b><p>Commesse gestite dall'inizio alla fine, con partner specializzati.</p></div>
<div class="past rv"><time>TaiBox</time><b>Produttore autorizzato</b><p>La TaiBox entra nell'elenco ufficiale degli apparati ACS. Tai Sud è anche fornitore autorizzato di traffico satellitare e manutenzione.</p></div>
<div class="past rv"><time>Gen 2026</time><b>Certificazione IP67</b><p>La TaiBox risponde ai nuovi requisiti europei per i VMS.</p></div>
</div></div></section>

<section class="sec"><div class="wrap">
<div class="sec-head split"><div class="stack">{eb('Le persone')}<h2 class="h-l rv">Chi guida Tai Sud.</h2></div><p class="lead rv">Un riferimento diretto per ogni cliente.</p></div>
<div class="people hs-m" data-dots>
<div class="person rv"><div class="portrait"><svg class="pg" aria-hidden="true"><defs><pattern id="pg1" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#C9D5E8"/></pattern></defs><rect width="100%" height="100%" fill="url(#pg1)"/></svg><span class="ini">AT</span><span class="ph-note">Foto in arrivo</span></div><div><b>Alberto Tirico</b><span>Fondatore</span></div></div>
<div class="person rv"><div class="portrait"><svg class="pg" aria-hidden="true"><rect width="100%" height="100%" fill="url(#pg1)"/></svg><span class="ini">MT</span><span class="ph-note">Foto in arrivo</span></div><div><b>Martina Tirico</b><span>Amministratrice</span></div></div>
<div class="person rv"><div class="portrait"><svg class="pg" aria-hidden="true"><rect width="100%" height="100%" fill="url(#pg1)"/></svg><span class="ini">A</span><span class="ph-note">Foto in arrivo</span></div><div><b>Alessandro</b><span>Ruolo da confermare</span></div></div>
</div></div></section>

<section class="sec mist"><div class="wrap">
<div class="sec-head split"><div class="stack">{eb('La rete')}<h2 class="h-l rv">Specialisti per ogni progetto.</h2></div><p class="lead rv">Coordiniamo professionisti dei settori in cui lavoriamo.</p></div>
<div class="net">
<div class="rv"><svg><use href="#i-sat"/></svg><b>Comunicazione satellitare</b></div>
<div class="rv"><svg><use href="#i-lock"/></svg><b>Sistemi di sicurezza</b></div>
<div class="rv"><svg><use href="#i-qr"/></svg><b>Tracciabilità alimentare</b></div>
<div class="rv"><svg><use href="#i-history"/></svg><b>Formazione</b></div>
<div class="rv"><svg><use href="#i-code"/></svg><b>Innovazione per la PA</b></div>
</div></div></section>

<section class="sec"><div class="wrap mt wide">
<div class="stack">{eb('Qualità')}<h2 class="h-l rv">ISO 9001:2015, certificato IMQ.</h2><p class="lead rv">Progettazione, produzione, installazione e assistenza seguono un sistema qualità certificato.</p><div class="cert-row rv"><img src="img/imq.png" alt="IMQ Certified, ISO 9001:2015"><img src="img/accredia.png" alt="ACCREDIA"></div><div class="ctas rv"><a class="btn ghost" href="qualita.html">Politica della qualità {A}</a></div></div>
<div class="stack" style="padding:clamp(28px,4vw,48px);background:var(--abyss);color:#fff;border-radius:8px 8px 8px 90px">{eb('Lavora con noi')}<h3 class="h-m" style="color:#fff">Cerchiamo persone competenti, con voglia di crescere.</h3><p style="color:var(--on-d2)">Tecnici, installatori, profili amministrativi. Mandaci il CV.</p><a class="btn white" href="lavora-con-noi.html" style="justify-self:start">Lavora con noi {A}</a></div>
</div></section>
{PARTNERS}
''' + cta('Parliamo della tua flotta.', 'Una barca o una cooperativa: troviamo insieme la soluzione giusta.', ('Contattaci', 'contatti.html'), ('06 97840077', 'tel:+390697840077'), 'pescatore-reti.jpg'))

# ================= PRODOTTI =================
P['prodotti'] = ('Prodotti e servizi', page_hero(crumbs(('Prodotti e servizi',)), 'Prodotti e servizi', ['Tutto quello che', 'serve a bordo.'], 'Due prodotti e i servizi per farli funzionare, da un solo fornitore.', mosaic('faro.jpg', ['s s s tr', 'ftl s s s', 's s s br'])) + f'''
<section class="sec"><div class="wrap mt">
<div style="background:#fff;border:1px solid var(--line);overflow:hidden" class="cut rv"><img src="img/taibox-kit.jpg" alt="Kit TaiBox" loading="lazy"></div>
<div class="stack">{eb('Blue box · ACS')}<h2 class="h-l rv">TaiBox</h2><p class="lead rv">L'apparato di controllo satellitare per pescherecci. Trasmette posizione e rotta a terra, segnala anomalie e manomissioni, invia l'SOS.</p><div class="tags rv"><span>Autorizzata Masaf</span><span>IP67</span><span>Display 7"</span></div><div class="ctas rv"><a class="btn" href="taibox.html">Scopri la TaiBox {A}</a></div></div>
</div></section>
<section class="sec mist"><div class="wrap mt rev">
{mosaic('mercato.jpg', ['tl s s s', 's s s s', 's s s fbr'], 'rv')}
<div class="stack">{eb('Tracciabilità', 'r-bl')}<h2 class="h-l rv">T-Fish</h2><p class="lead rv">Palmare con app e stampante portatile. Registri il lotto e stampi sul posto l'etichetta con codice a barre e QR code.</p><div class="tags rv"><span>App</span><span>QR code</span><span>Zebra</span><span>IP54</span></div><div class="ctas rv"><a class="btn" href="t-fish.html">Scopri T-Fish {A}</a></div></div>
</div></section>
<section class="sec dark" id="servizi"><div class="wrap">
<div class="sec-head split"><div class="stack">{eb('Servizi')}<h2 class="h-l rv">Prima, durante e dopo l'installazione.</h2></div><p class="lead rv">Siamo fornitori autorizzati di traffico satellitare e manutenzione degli apparati.</p></div>
<div class="feats">
<div class="feat rv"><svg><use href="#i-install"/></svg><b>Installazione a bordo</b><span>Montaggio e collaudo della trasmissione.</span></div>
<div class="feat rv"><svg><use href="#i-sat"/></svg><b>Traffico satellitare</b><span>Il servizio di trasmissione dati, da noi.</span></div>
<div class="feat rv"><svg><use href="#i-wrench"/></svg><b>Manutenzione</b><span>Interventi e aggiornamenti dell'apparato.</span></div>
<div class="feat rv"><svg><use href="#i-code"/></svg><b>Sistemi su misura</b><span>Progetti informativi e integrazioni per le aziende.</span></div>
</div></div></section>
''' + cta('Ti serve un preventivo?', 'Scrivici cosa ti serve. Ti rispondiamo con una proposta su misura.'))

# ================= TAIBOX =================
DISPLAY = '''<div class="device rv"><div class="screen"><div class="top"><span>TAIBOX</span><span data-utc>--:--</span></div><div class="mid"><div class="map"><canvas id="mini-map"></canvas></div><div class="stat"><span class="mode" id="mode-lbl">NAVIGAZIONE</span><div><span>GPS</span><em>OK</em></div><div><span>SATELLITE</span><em>OK</em></div><div><span>PROSSIMA TX</span><em id="next-tx">--:--</em></div><div><span>CORRENTE</span><em>BORDO</em></div></div></div><div class="bottom"><button type="button" data-mode="nav" aria-pressed="true">NAVIG.</button><button type="button" data-mode="porto" aria-pressed="false">PORTO</button><button type="button" data-mode="man" aria-pressed="false">MANUT.</button><button type="button" data-mode="sos" class="sos">SOS</button></div></div></div>'''
MODEINFO = '<div class="mode-info rv"><b id="mode-t">Navigazione</b><span id="mode-d">Trasmette la posizione alla frequenza prevista dalla legge. Avvisi e anomalie arrivano al centro di controllo.</span></div>'
P['taibox'] = ('TaiBox, blue box VMS', page_hero(crumbs(('Prodotti', 'prodotti.html'), ('TaiBox',)), 'Blue box · Apparato di controllo satellitare', ['TaiBox. La blue box', 'conforme per legge.'], 'Trasmette posizione e rotta della tua barca al centro di controllo a terra. Display touch 7", IP67, prodotta in Italia.', '<img src="img/taibox-kit.jpg" alt="Kit TaiBox completo">', f'<div class="tags hin"><span>Autorizzata Masaf</span><span>IP67</span><span>Display 7"</span><span>Made in Italy</span></div><div class="ctas hin"><a class="btn" href="contatti.html#taibox">Richiedi un preventivo {A}</a><a class="btn ghost" href="modulistica.html">Moduli</a></div>').replace('<div class="side">', '<div class="side product">') + f'''
<section class="sec"><div class="wrap">
<div class="sec-head split"><div class="stack">{eb('Cosa fa')}<h2 class="h-l rv">Otto funzioni, un solo apparato.</h2></div><p class="lead rv">Tutto quello che il regolamento chiede, in una scatola montata a bordo.</p></div>
<div class="feats">
<div class="feat rv"><svg><use href="#i-gps"/></svg><b>Posizione e rotta</b><span>GPS per posizione, rotta e velocità.</span></div>
<div class="feat rv"><svg><use href="#i-lock"/></svg><b>Anti manomissione</b><span>Segnala guasti e tentativi di manomissione.</span></div>
<div class="feat rv"><svg><use href="#i-limit"/></svg><b>Limiti di pesca</b><span>Avvisa se la barca esce dai limiti consentiti.</span></div>
<div class="feat rv"><svg><use href="#i-history"/></svg><b>Storico rotte</b><span>Archivio elettronico dei movimenti.</span></div>
<div class="feat rv"><svg><use href="#i-display"/></svg><b>Display 7"</b><span>Stato, avvisi ed errori per il comandante.</span></div>
<div class="feat rv"><svg><use href="#i-sos"/></svg><b>Tasto SOS</b><span>Posizione, stato e ora al centro di controllo.</span></div>
<div class="feat rv"><svg><use href="#i-remote"/></svg><b>Da remoto</b><span>Aggiornamenti senza salire a bordo.</span></div>
<div class="feat rv"><svg><use href="#i-anchor"/></svg><b>Modalità Porto</b><span>In standby trasmette ogni 24 ore.</span></div>
</div></div></section>

<section class="band" style="min-height:min(560px,70svh)">{photo('hero.jpg', 'Peschereccio in navigazione')}
<div class="wrap on-photo"><span class="eyebrow rv">{TI}Via satellite</span><h2 class="h-l rv">Trasmette anche dove il telefono non prende.</h2></div></section>

<section class="sec"><div class="wrap mt">
<div class="stack">{eb('Il display')}<h2 class="h-l rv">Tutto sotto controllo, dalla plancia.</h2><p class="lead rv">Il comandante vede se l'apparato trasmette, legge gli avvisi e cambia modalità con un tocco. Prova i tasti.</p>{MODEINFO}<p class="note rv">Schermata illustrativa.</p></div>
{DISPLAY}
</div></section>

<section class="sec mist"><div class="wrap">
<div class="sec-head split"><div class="stack">{eb('Conformità')}<h2 class="h-l rv">Cosa chiede la legge. Cosa fa la TaiBox.</h2></div><p class="lead rv">Requisiti del Regolamento di esecuzione (UE) 2025/2196 per gli apparati VMS.</p></div>
<div class="table-wrap rv"><table class="req"><thead><tr><th>Requisito</th><th>Cosa significa</th><th>TaiBox</th></tr></thead><tbody>
<tr><td>Apparato embedded</td><td>Display integrato con stato, avvisi ed errori</td><td><span class="ok"><svg><use href="#i-check"/></svg>Display 7" touch</span></td></tr>
<tr><td>Protezione IP67</td><td>Resiste ad acqua e polvere</td><td><span class="ok"><svg><use href="#i-check"/></svg>Certificata, gen 2026</span></td></tr>
<tr><td>Memoria in caso di guasto</td><td>Almeno 200 posizioni, inviate al ritorno del segnale</td><td><span class="ok"><svg><use href="#i-check"/></svg>Conforme</span></td></tr>
<tr><td>Modalità Porto e Manutenzione</td><td>In standby trasmette ogni 24 ore</td><td><span class="ok"><svg><use href="#i-check"/></svg>Conforme</span></td></tr>
<tr><td>Trasmissione ogni 30 minuti</td><td>Obbligatoria dal 10 luglio 2027</td><td><span class="ok"><svg><use href="#i-check"/></svg>Pronta</span></td></tr>
</tbody></table></div>
<p class="note">Conformità dichiarata da Tai Sud. Da verificare con la scheda tecnica prima della pubblicazione.</p>
</div></section>

<section class="sec"><div class="wrap mt rev">
<div class="stack">{eb('Nella scatola')}<h2 class="h-l rv">Il kit TaiBox.</h2><p class="lead rv">Montato e collaudato dai nostri tecnici.</p><ul class="kit rv"><li><span>01</span>Unità con display 7"</li><li><span>02</span>Antenna satellitare</li><li><span>03</span>Staffa di montaggio</li><li><span>04</span>Connettore stagno e viteria</li></ul></div>
<div class="cut-r rv" style="overflow:hidden;border:1px solid var(--line)"><img src="img/taibox-kit-wide.jpg" alt="Componenti del kit TaiBox" loading="lazy"></div>
</div></section>
''' + cta('Metti in regola la tua barca.', 'Compila il questionario armatore o scrivici. Ti rispondiamo con la configurazione giusta.', ('Richiedi preventivo', 'contatti.html#taibox'), ('Modulistica', 'modulistica.html'), 'faro.jpg'))

# ================= T-FISH =================
P['t-fish'] = ('T-Fish, tracciabilità del pescato', page_hero(crumbs(('Prodotti', 'prodotti.html'), ('T-Fish',)), 'Etichettatura e tracciabilità', ['T-Fish. Ogni lotto,', 'la sua etichetta.'], 'Palmare con app e stampante portatile. Registri il lotto e stampi sul posto l\'etichetta con codice a barre e QR code.', '<img src="img/tfish-devices.jpg" alt="Palmare e stampante Zebra">', f'<div class="tags hin"><span>App</span><span>QR code</span><span>Zebra</span><span>IP54</span></div><div class="ctas hin"><a class="btn" href="contatti.html#tfish">Richiedi informazioni {A}</a></div>').replace('<div class="side">', '<div class="side product">') + f'''
<section class="sec"><div class="wrap mt">
{mosaic('mercato.jpg', ['tl s s s', 's s s s', 'fbl s s br'], 'rv')}
<div class="stack">{eb('Perché adesso')}<h2 class="h-l rv">La tracciabilità diventa digitale.</h2><p class="lead rv">Con il Regolamento (UE) 2023/2842 i dati del pescato vanno raccolti in digitale, dalla cattura alla vendita. Da gennaio 2029 anche per conserve, crostacei e molluschi.</p><p class="muted rv">Tracciare ogni passaggio vuol dire più sicurezza e trasparenza, per chi vende e per chi compra.</p></div>
</div></section>
<section class="sec dark"><div class="wrap">
<div class="sec-head">{eb('Cosa fa')}<h2 class="h-l rv">Semplice anche in banchina.</h2></div>
<div class="feats three">
<div class="feat rv"><svg><use href="#i-palette"/></svg><b>Etichette su misura</b><span>Forma, contenuto e grafica dall'app.</span></div>
<div class="feat rv"><svg><use href="#i-db"/></svg><b>Archivio automatico</b><span>Ogni etichetta finisce nel database lotti.</span></div>
<div class="feat rv"><svg><use href="#i-qr"/></svg><b>Barcode e QR</b><span>Chiunque risale all'origine del prodotto.</span></div>
<div class="feat rv"><svg><use href="#i-printer"/></svg><b>Stampanti Zebra</b><span>Centinaia di etichette con una carica.</span></div>
<div class="feat rv"><svg><use href="#i-drop"/></svg><b>Resiste all'acqua</b><span>Stampanti IP54 e custodie impermeabili.</span></div>
<div class="feat rv"><svg><use href="#i-label"/></svg><b>Ogni settore</b><span>Non solo pesce: tutte le merci.</span></div>
</div></div></section>
<section class="sec"><div class="wrap">
<div class="sec-head">{eb('Come si usa')}<h2 class="h-l rv">Quattro gesti per ogni lotto.</h2></div>
<ol class="journey hs-m" data-dots style="grid-template-columns:repeat(4,minmax(0,1fr))">
<li class="rv"><b>Registra</b><span>I dati del lotto, dal palmare.</span></li>
<li class="rv"><b>Genera</b><span>Codice a barre e QR, in automatico.</span></li>
<li class="rv"><b>Stampa</b><span>L'etichetta, sul posto, con la Zebra.</span></li>
<li class="rv"><b>Traccia</b><span>Ogni passaggio legge l'etichetta.</span></li>
</ol><p class="note">Passaggi da confermare con il flusso reale dell'app.</p></div></section>
''' + cta('Pescherecci, mercati ittici, grossisti.', 'Raccontaci come lavori: ti proponiamo la configurazione T-Fish adatta.', ('Richiedi informazioni', 'contatti.html#tfish'), ('06 97840077', 'tel:+390697840077'), 'mercato.jpg'))

# ================= NORMATIVA =================
P['normativa'] = ('Normativa VMS e FAQ', page_hero(crumbs(('Normativa',)), 'Reg. (UE) 2023/2842 · Reg. di esecuzione (UE) 2025/2196', ['Le regole sul VMS,', 'spiegate chiare.'], 'Chi è obbligato, quale apparato serve, cosa cambia dal 2027. Con le fonti ufficiali.', '', f'<div class="ctas hin"><a class="btn" href="#faq">Vai alle FAQ {A}</a><a class="btn ghost" href="contatti.html#taibox">Chiedi a un tecnico</a></div>') + f'''
<section class="sec"><div class="wrap two">
<div class="stack sticky">{eb('Le scadenze')}<h2 class="h-l rv">Cosa è in vigore. Cosa arriva.</h2><p class="lead rv">Lo stato di ogni scadenza si aggiorna da solo con la data.</p></div>
<div class="vtl" id="norm-dl"></div>
</div></section>
<section class="sec mist"><div class="wrap">
<div class="sec-head split"><div class="stack">{eb('Gli apparati')}<h2 class="h-l rv">ACS, ACI o ACM: quale serve.</h2></div><p class="lead rv">Dipende da dove peschi e dalla copertura della rete.</p></div>
<div class="types hs-m" data-dots>
<div class="type hl rv"><span class="chip in badge"><i></i>TaiBox</span><small>Satellitare</small><div class="code">ACS</div><p>Trasmette via satellite. Per chi pesca oltre le 12 miglia o dove la rete non arriva.</p></div>
<div class="type rv"><small>Ibrido</small><div class="code">ACI</div><p>Rete mobile più modulo satellitare obbligatorio. Alternativa all'ACS per le unità dai 12 metri.</p></div>
<div class="type rv"><small>Rete mobile</small><div class="code">ACM</div><p>Solo pesca costiera locale entro 12 miglia, con copertura garantita in porto e in mare.</p></div>
</div></div></section>
<section class="band" style="min-height:min(540px,68svh)">{photo('hero.jpg', 'Peschereccio in navigazione')}
<div class="wrap on-photo"><span class="eyebrow rv">{TI}Il comandante</span><h2 class="h-l rv">L'apparato resta acceso. Sempre.</h2><div class="facts rv"><span>{TI}Acceso per tutta la navigazione</span><span>{TI}Alimentato</span><span>{TI}Mai manomesso</span><span>{TI}Dati corretti</span></div></div></section>
<section class="sec" id="faq"><div class="wrap">
<div class="sec-head">{eb('FAQ')}<h2 class="h-l rv">Tutte le domande sul VMS.</h2></div>
<div class="faq-tools"><label class="faq-search"><svg><use href="#i-search"/></svg><input id="faq-q" type="search" placeholder="Cerca: 12 metri, IP67, porto, 2027" aria-label="Cerca nelle FAQ"></label>
<div class="fchips"><button type="button" data-c="tutte" aria-pressed="true">Tutte</button><button type="button" data-c="obbligo" aria-pressed="false">Obblighi</button><button type="button" data-c="frequenza" aria-pressed="false">Frequenza</button><button type="button" data-c="bordo" aria-pressed="false">A bordo</button><button type="button" data-c="taibox" aria-pressed="false">TaiBox</button></div></div>
<div class="faq" data-faq="all"></div>
<p class="muted" id="faq-empty" hidden style="padding:24px 0">Nessuna risposta trovata. <a class="link-arrow" href="contatti.html">Scrivici {A}</a></p>
<div class="stack sm" style="margin-top:64px">{eb('Fonti ufficiali')}<div class="sources">
<a href="https://eur-lex.europa.eu/eli/reg/2023/2842/oj/ita" target="_blank" rel="noopener">{TI}Regolamento (UE) 2023/2842</a>
<a href="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32025R2196" target="_blank" rel="noopener">{TI}Regolamento di esecuzione (UE) 2025/2196</a>
<a href="https://www.controllopesca.politicheagricole.it/flex/cm/pages/ServeBLOB.php/L/IT/IDPagina/153" target="_blank" rel="noopener">{TI}Elenco apparati autorizzati, Masaf</a>
</div></div></div></section>
''' + cta('Hai un dubbio sulla tua barca?', 'Dicci lunghezza e tipo di pesca: ti spieghiamo cosa prevede la legge nel tuo caso.', ('Scrivici', 'contatti.html#taibox')))

# ================= ASSISTENZA =================
HELP = f'<div class="help hin"><span class="eyebrow">{TI}Linea assistenza</span><a class="big" href="tel:+390697840077">06 97840077</a><div class="row"><a href="tel:+390697040156">06 97040156</a><a href="mailto:info@taisud.com">info@taisud.com</a></div><span class="tbd">Orari da confermare</span><a class="btn white" href="contatti.html#assistenza" style="justify-self:start">Apri una richiesta {A}</a></div>'
P['assistenza'] = ('Assistenza tecnica TaiBox', page_hero(crumbs(('Assistenza',)), 'Assistenza tecnica', ['La TaiBox segnala', 'un problema?'], 'Un tecnico ti guida al telefono e, se serve, organizza l\'intervento a bordo.', HELP, '', True) + f'''
<section class="sec"><div class="wrap">
<div class="sec-head split"><div class="stack">{eb('Prima di chiamare')}<h2 class="h-l rv">Tieni a portata di mano.</h2></div><p class="lead rv">Spunta mentre prepari: la chiamata sarà più veloce.</p></div>
<ul class="checks">
<li class="rv"><label><input type="checkbox"><b>Nome della barca</b><span>E porto di iscrizione.</span></label></li>
<li class="rv"><label><input type="checkbox"><b>Numero UE di flotta</b><span>È sulla licenza di pesca.</span></label></li>
<li class="rv"><label><input type="checkbox"><b>Cosa dice il display</b><span>Errore o modalità. Una foto aiuta.</span></label></li>
<li class="rv"><label><input type="checkbox"><b>La corrente</b><span>Se l'apparato è alimentato.</span></label></li>
</ul></div></section>
<section class="sec mist"><div class="wrap mt">
<div class="stack">{eb('Le modalità')}<h2 class="h-l rv">Non spegnere mai l'apparato.</h2><p class="lead rv">In porto o in manutenzione si cambia modalità. Prova i tasti sul display.</p>{MODEINFO}</div>
{DISPLAY}
</div></section>
''' + cta('Siamo anche fornitori di manutenzione.', 'Oltre alla TaiBox gestiamo traffico satellitare e manutenzione degli apparati.', ('Apri una richiesta', 'contatti.html#assistenza'), ('06 97840077', 'tel:+390697840077'), 'faro.jpg'))

# ================= MODULISTICA =================
def doc(step, title, what, who, when, href, meta, send=True):
    s = '<a class="btn ghost sm" href="contatti.html#moduli">Invia compilato</a>' if send else ''
    return f'''<article class="doc rv"><span class="beam-border"></span><div class="top"><div class="ico">PDF</div><div><span class="eyebrow">{step}</span><h3 class="h-s" style="margin-top:6px">{title}</h3></div></div>
<dl><div><dt>A cosa serve</dt><dd>{what}</dd></div><div><dt>Chi lo compila</dt><dd>{who}</dd></div><div><dt>Quando</dt><dd>{when}</dd></div></dl>
<div class="meta">{''.join(f'<span>{x}</span>' for x in meta)}</div>
<div class="acts"><a class="btn sm" href="{href}" target="_blank" rel="noopener"><svg><use href="#i-download"/></svg>Scarica PDF</a>{s}</div></article>'''
P['modulistica'] = ('Contrattualistica e modulistica', page_hero(crumbs(('Modulistica',)), 'Contrattualistica e modulistica', ['I moduli', 'per iniziare.'], 'Scarica, compila, invia. Dal form o a info@taisud.com.', mosaic('reti.jpg', ['tl s s', 's s fbr', 's s .'])) + f'''
<section class="sec tight mist"><div class="wrap"><ol class="journey hs-m" data-dots>
<li><b>Questionario</b><span>Prima del preventivo.</span></li><li><b>Preventivo</b><span>Ti mandiamo l'offerta.</span></li><li><b>Richiesta di installazione</b><span>Dopo l'accettazione.</span></li><li><b>Installazione</b><span>A bordo, con i tecnici.</span></li><li><b>Assistenza</b><span>Per tutta la vita dell'apparato.</span></li>
</ol></div></section>
<section class="sec"><div class="wrap"><div class="docs hs-m" data-dots>
{doc('Passo 01', "Questionario per l'armatore", 'Descrive barca e tipo di pesca, per preparare la configurazione giusta.', "Armatore o comandante", 'Prima del preventivo', 'https://taisud.com/wp-content/uploads/2025/04/questionario-armatore.pdf', ['PDF', 'Da firmare'])}
{doc('Passo 03', 'Richiesta prima installazione', "Avvia l'installazione a bordo e la registrazione dell'apparato.", "Armatore", "Dopo l'accettazione del preventivo", 'https://taisud.com/wp-content/uploads/2025/04/allegato-prima-installazione.pdf', ['PDF', 'Da firmare'])}
{doc('Qualità', 'Certificato ISO 9001:2015', 'Per gare, albi fornitori e uffici acquisti.', 'Consultazione', 'Quando serve', 'https://taisud.com/wp-content/uploads/2025/03/Certificato_iso9001_Tai-Sud.pdf', ['PDF', 'IMQ'], False)}
</div><p class="note">Testi delle schede da confermare dopo la lettura dei PDF.</p></div></section>
''' + cta('Ti aiutiamo a compilarli.', 'Chiamaci: li compiliamo insieme al telefono.', ('Invia i moduli', 'contatti.html#moduli'), ('06 97840077', 'tel:+390697840077')))

# ================= CONTATTI =================
FORM = f'''<form class="form rv" id="cform" novalidate><div id="form-body" style="display:grid;gap:30px">
<fieldset><legend><span class="n">01</span>Motivo</legend><div class="pills">
<label><input type="radio" name="motivo" value="taibox" checked><span>Preventivo TaiBox<small>Blue box VMS</small></span></label>
<label><input type="radio" name="motivo" value="tfish"><span>Preventivo T-Fish<small>Etichette e tracciabilità</small></span></label>
<label><input type="radio" name="motivo" value="assistenza"><span>Assistenza<small>Problema all'apparato</small></span></label>
<label><input type="radio" name="motivo" value="moduli"><span>Invio moduli<small>PDF compilati</small></span></label>
<label><input type="radio" name="motivo" value="candidatura"><span>Candidatura<small>Lavora con noi</small></span></label>
<label><input type="radio" name="motivo" value="altro"><span>Altro<small>Qualsiasi richiesta</small></span></label>
</div></fieldset>
<fieldset><legend><span class="n">02</span>I tuoi dati</legend><div class="fields">
<div class="f"><input id="f-nome" name="nome" placeholder=" " autocomplete="name" required><label for="f-nome">Nome e cognome *</label><span class="err">Inserisci nome e cognome</span></div>
<div class="f"><input id="f-azienda" name="azienda" placeholder=" " autocomplete="organization"><label for="f-azienda">Azienda o cooperativa</label></div>
<div class="f"><input id="f-email" name="email" type="email" placeholder=" " autocomplete="email" required><label for="f-email">Email *</label><span class="err">Inserisci un'email valida</span></div>
<div class="f"><input id="f-tel" name="telefono" type="tel" placeholder=" " autocomplete="tel"><label for="f-tel">Telefono</label></div>
</div></fieldset>
<fieldset data-for="taibox assistenza moduli"><legend><span class="n">03</span>La barca</legend><div class="fields">
<div class="f"><input id="f-barca" name="imbarcazione" placeholder=" "><label for="f-barca">Nome della barca</label></div>
<div class="f"><input id="f-porto" name="porto" placeholder=" "><label for="f-porto">Porto</label></div>
<div class="f" data-for="taibox"><input id="f-lft" name="lunghezza" type="number" min="0" step="0.1" placeholder=" " inputmode="decimal"><label for="f-lft">Lunghezza (m)</label></div>
<div class="f" data-for="taibox"><select id="f-pesca" name="pesca"><option value="">Seleziona</option><option>Strascico</option><option>Circuizione</option><option>Palangari</option><option>Piccola pesca costiera</option><option>Altro</option></select><label for="f-pesca">Tipo di pesca</label></div>
<div class="f" data-for="assistenza moduli"><input id="f-ue" name="numero_ue" placeholder=" "><label for="f-ue">Numero UE di flotta</label></div>
<div class="f" data-for="assistenza"><select id="f-urg" name="problema"><option>Non trasmette</option><option>Errore sul display</option><option>Danno fisico</option><option>Altro</option></select><label for="f-urg">Problema</label></div>
</div></fieldset>
<fieldset data-for="tfish"><legend><span class="n">03</span>La tua attività</legend><div class="fields"><div class="f full"><select id="f-att" name="attivita"><option>Peschereccio</option><option>Mercato ittico</option><option>Grossista</option><option>Trasformazione</option><option>Altro</option></select><label for="f-att">Tipo di attività</label></div></div></fieldset>
<fieldset data-for="candidatura"><legend><span class="n">03</span>Candidatura</legend><div class="fields"><div class="f full"><input id="f-ruolo" name="ruolo" placeholder=" "><label for="f-ruolo">Ruolo che ti interessa</label></div></div></fieldset>
<fieldset><legend><span class="n">04</span>Messaggio</legend>
<div class="f"><textarea id="f-msg" name="messaggio" placeholder=" "></textarea><label for="f-msg" id="msg-label">Di cosa hai bisogno?</label></div>
<div data-for="assistenza moduli candidatura" style="display:grid;gap:10px"><label class="drop" id="drop"><svg><use href="#i-upload"/></svg><span><b>Trascina qui i file</b> o tocca per sceglierli</span><small id="drop-hint">PDF, JPG o PNG, max 10 MB</small><input type="file" id="f-files" multiple accept=".pdf,.jpg,.jpeg,.png"></label><div class="files" id="files"></div></div>
</fieldset>
<label class="consent" id="consent"><input type="checkbox" id="f-priv"><span>Ho letto l'<a href="https://www.iubenda.com/privacy-policy/67795620" target="_blank" rel="noopener">informativa privacy</a> e acconsento al trattamento dei dati per questa richiesta. *</span></label>
<div class="form-foot"><small>* obbligatori</small><button class="btn" type="submit">Invia richiesta {A}</button></div>
</div>
<div class="sent" id="sent" hidden><div class="tick"><svg><use href="#i-check"/></svg></div><h3 class="h-m">Richiesta pronta.</h3><p class="muted">Nel sito finale arriva a info@taisud.com e ricevi una email di conferma. Questo è il prototipo: non è stato inviato nulla.</p><dl id="sent-sum"></dl><button class="btn ghost sm" type="button" id="again">Nuova richiesta</button></div>
</form>'''
P['contatti'] = ('Contatti', page_hero(crumbs(('Contatti',)), 'Contatti', ['Parliamone.'], 'Scegli il motivo: il modulo si adatta.') + f'''
<section class="sec" style="padding-top:clamp(40px,5vw,72px)"><div class="wrap contact-grid">
<div><div class="qa"><a href="tel:+390697840077"><small>Assistenza</small><b>06 97840077</b></a><a href="mailto:info@taisud.com"><small>Email</small><b>info@taisud.com</b></a></div>
<div class="info"><div><span class="k">Telefoni</span><span><a href="tel:+390697840077">(+39) 06 97840077</a><br><a href="tel:+390697040156">(+39) 06 97040156</a></span></div><div><span class="k">Sede</span><span>Viale Gianluigi Bonelli, 341<br>00127 Roma (RM)</span></div><div><span class="k">Dati</span><span>TAI SUD s.r.l.<br>P.IVA 03786241004</span></div></div>
<div class="map-card"><canvas id="map-card"></canvas><a class="btn sm" href="https://www.google.com/maps/search/?api=1&query=Viale+Gianluigi+Bonelli+341+00127+Roma" target="_blank" rel="noopener">Apri in Maps ↗</a></div></div>
{FORM}
</div></section>''')

# ================= LAVORA =================
P['lavora-con-noi'] = ('Lavora con noi', page_hero(crumbs(('Chi siamo', 'chi-siamo.html'), ('Lavora con noi',)), 'Lavora con noi', ['Entra in', 'squadra.'], 'Un\'azienda funziona quando è fatta di persone preparate, con obiettivi in comune.', mosaic('pescatore-reti.jpg', ['tl s s', 's s s', 'fbl s br'])) + f'''
<section class="sec"><div class="wrap two">
<div class="stack">{eb('Chi cerchiamo')}<h2 class="h-l rv">Persone competenti, che vogliono crescere.</h2></div>
<div class="stack"><p class="lead rv">Costruiamo la squadra con cura. Se vuoi lavorare con la tecnologia a bordo, raccontaci cosa sai fare.</p>
<ul class="blist rv"><li>{TI}Tecnici e installatori</li><li>{TI}Elettronica e telecomunicazioni</li><li>{TI}Amministrazione e clienti</li></ul>
<p class="note rv">Profili indicativi, da confermare.</p>
<a class="btn rv" href="contatti.html#candidatura" style="justify-self:start">Invia la candidatura {A}</a></div>
</div></section>''')

# ================= QUALITA =================
P['qualita'] = ('Politica della qualità', page_hero(crumbs(('Chi siamo', 'chi-siamo.html'), ('Qualità',)), 'UNI EN ISO 9001:2015', ['Politica', 'della qualità.'], 'Il nostro lavoro funziona se il cliente è soddisfatto. Per questo applichiamo un sistema qualità conforme alla UNI EN ISO 9001:2015, certificato IMQ.', '', '<div class="cert-row hin"><img src="img/imq.png" alt="IMQ Certified, ISO 9001:2015"><img src="img/accredia.png" alt="ACCREDIA"></div>') + f'''
<section class="sec"><div class="wrap">
<div class="stack sm" style="margin-bottom:32px">{eb('Campo di applicazione')}<p class="lead">Progettazione, produzione, installazione e assistenza tecnica di sistemi e apparecchiature avanzate ICT.</p></div>
<ol class="olist"><li>Qualità dell'organizzazione</li><li>Miglioramento continuo</li><li>Soddisfazione del cliente</li><li>Qualità del servizio</li><li>Rispetto delle norme</li><li>Crescita delle persone</li><li>Continuità del servizio</li><li>Fornitori responsabili</li><li>Sostenibilità ambientale</li></ol>
<p class="muted" style="margin-top:32px;max-width:64ch">La Direzione mette a disposizione le risorse necessarie e verifica i risultati con audit interni, controllo della conformità normativa e riesame annuale degli obiettivi.</p>
<div style="margin-top:32px"><a class="btn ghost" href="https://taisud.com/wp-content/uploads/2025/03/Certificato_iso9001_Tai-Sud.pdf" target="_blank" rel="noopener"><svg><use href="#i-download"/></svg>Scarica il certificato</a></div>
</div></section>''')

exec(open(D + 'overrides.py').read())
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Titillium+Web:wght@400;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">'
def head(slug):
    t, d = SEO[slug]
    return f'<meta name="description" content="{d}"><meta property="og:title" content="{t}"><meta property="og:description" content="{d}"><meta property="og:type" content="website">{FONTS}<style>{css}{EXTRA_CSS.get(slug, "")}</style>'
LIBS = ('<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>'
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>'
        '<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js"></script>')
appjs = open(D + 'app.js').read()
def body(slug):
    ov = f'<div id="intro">{INTRO_LOGO}<button class="skip" type="button">Salta</button></div>' if slug == 'home' else ''
    extra = EXTRA_JS.get(slug, '')
    return '<a class="skip-link" href="#main">Vai al contenuto</a>' + sprite + ov + header(slug) + f'<main id="main" tabindex="-1">{P[slug][1]}</main>' + FOOTER + LIBS + f'<script>{logojs}</script>' + (f'<script>{extra}</script>' if extra else '') + f'<script>{appjs}</script>'
O = D + 'out/'
os.makedirs(O + 'img', exist_ok=True)
for f in os.listdir('/home/claude/site3/out/img'): shutil.copy('/home/claude/site3/out/img/' + f, O + 'img/' + f)
for slug in P:
    t = SEO[slug][0]
    open(O + f'{slug}.html', 'w').write(f'<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{t}</title>{head(slug)}</head><body>{body(slug)}</body></html>')
open(O + 'index.html', 'w').write(f'<title>Tai Sud sito</title>{head("home")}{body("home")}')
print('ok', len(P))
