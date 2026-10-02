
# ===================== v4 overrides =====================
CHECK = f'''<div class="check" data-check>
<div class="chk-in">
<div class="chk-q" data-q="lft"><span>Domanda 1 di 2</span><b>Quanto è lunga la barca fuori tutto?</b><div class="chk-opts"><button type="button" data-v="lt" aria-pressed="false">Meno di 12 metri<small>Piccola pesca</small></button><button type="button" data-v="ge" aria-pressed="false">12 metri o più<small>Obbligo VMS</small></button></div></div>
<div class="chk-q dim" data-q="zona"><span>Domanda 2 di 2</span><b>Dove peschi di solito?</b><div class="chk-opts"><button type="button" data-v="costa" aria-pressed="false" disabled>Entro 12 miglia<small>Con copertura di rete mobile</small></button><button type="button" data-v="largo" aria-pressed="false" disabled>Oltre 12 miglia<small>O senza copertura di rete</small></button></div></div>
</div>
<div class="chk-out" aria-live="polite"></div>
</div>
<p class="chk-legal">Indicazione orientativa basata sul Reg. (UE) 2023/2842 e sul Reg. di esecuzione (UE) 2025/2196. Per il tuo caso fa fede la normativa vigente.</p>'''

exec(open(D + 'hw.py').read())

P['home'] = ('Blue box VMS per pescherecci', f'''
<section class="hero fleet"><canvas id="fleet" aria-hidden="true"></canvas>
<div class="wrap"><div class="copy">
<span class="eyebrow hin">{TI}Blue box VMS · Autorizzata Masaf</span>
{h1(['Il tuo peschereccio,', '<em>sempre in regola.</em>'])}
<p class="lead hin">TaiBox è l'apparato di controllo satellitare autorizzato dal Masaf. Lo installiamo a bordo, gestiamo il traffico satellitare e la manutenzione.</p>
<div class="ctas hin"><a class="btn" href="contatti.html#taibox">Richiedi il preventivo {A}</a><a class="btn ghost" href="#verifica">Verifica la tua barca</a></div>
<div class="ping hin" id="ping" role="status"><i></i><small>Esempio</small><span>In attesa di trasmissione</span></div>
</div></div>
<div class="hero-foot"><div class="wrap"><div class="hero-legend" aria-hidden="true"><span><i class="lg-boat"></i>Peschereccio con TaiBox</span><span><i class="lg-sat"></i>Trasmissione via satellite</span><span><i class="lg-ctl"></i>Centro di controllo a terra</span></div></div></div>
</section>

<div class="trust"><div class="wrap">
<div class="t rv">{TI}<b>Autorizzata Masaf</b><span>TaiBox è nell'elenco ufficiale degli apparati autorizzati. <a href="https://www.controllopesca.politicheagricole.it/flex/cm/pages/ServeBLOB.php/L/IT/IDPagina/153" target="_blank" rel="noopener">Controlla ↗</a></span></div>
<div class="t rv">{ti("r-tl")}<b>Certificata IP67</b><span>Conforme alle nuove specifiche europee, da gennaio 2026</span></div>
<div class="t rv">{ti("r-br")}<b>Un unico referente</b><span>Apparato, traffico satellitare, installazione e manutenzione</span></div>
<div class="t rv"><div class="badges"><img src="img/imq.png" alt="IMQ, ISO 9001:2015"><img src="img/accredia.png" alt="ACCREDIA"></div><span>Dal 1988 · Qualità ISO 9001:2015</span></div>
</div></div>

<section class="sec"><div class="wrap mt">
{mosaic('pescatore-mz.jpg', ['tl s . .', 's s s tr', '. fbl s br'], 'mz-light rv')}
<div class="stack">{eb('Chi siamo')}<h2 class="h-l rv">Dal 1988, tecnologia che lavora in mare.</h2>
<p class="lead rv">Fondata a Roma da Alberto Tirico, Tai Sud è il riferimento di armatori e cooperative per il controllo satellitare della pesca.</p>
<ul class="blist rv"><li>{TI}TaiBox nell'elenco degli apparati autorizzati Masaf</li><li>{TI}Fornitore autorizzato di traffico satellitare e manutenzione</li><li>{TI}Sistema qualità ISO 9001:2015 certificato IMQ</li></ul>
<a class="link-arrow rv" href="chi-siamo.html">La nostra storia {A}</a></div>
</div></section>

<section class="sec dark"><div class="wrap">
<div class="sec-head split"><div class="stack">{eb('Normativa VMS')}<h2 class="h-l rv">Le scadenze del VMS.</h2><p class="lead rv">Dal 10 gennaio 2026 VMS e giornale di pesca elettronico sono obbligatori dai 12 metri in su. Dal 10 luglio 2027 la posizione va trasmessa ogni 30 minuti.</p></div>
<div class="countdown rv"><b id="cd-days">--</b><span>giorni al<br>10 luglio 2027</span></div></div>
<div class="tl hs-m" id="home-dl" data-dots></div>
<div style="margin-top:44px" class="rv"><a class="link-arrow" href="normativa.html">Scadenze, obblighi e FAQ {A}</a></div>
</div></section>

<section class="sec mist" id="verifica"><div class="wrap">
<div class="sec-head split"><div class="stack">{eb('Verifica rapida')}<h2 class="h-l rv">La tua barca deve avere il VMS?</h2></div><p class="lead rv">Due risposte e vedi cosa prevede il regolamento per la tua barca.</p></div>
{CHECK}
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head split"><div class="stack">{eb('Prodotti e servizi')}<h2 class="h-l rv">Due prodotti, un unico referente.</h2></div><p class="lead rv">Dalla plancia al banco del pesce. Apparati, servizio satellitare e assistenza dalla stessa azienda.</p></div>
<div class="sol-grid">
<a class="sol rv" href="taibox.html"><span class="beam-border"></span><div class="ph"><img src="img/taibox-kit-wide.jpg" alt="Kit TaiBox con antenna satellitare" loading="lazy"><span class="chip"><i></i>Conforme alle nuove specifiche</span></div>
<div class="body"><span class="eyebrow">{TI}Blue box · ACS</span><h3 class="h-m">TaiBox</h3><ul class="blist"><li>{TI}Posizione e rotta al centro di controllo a terra, via satellite</li><li>{TI}Display touch 7" integrato, certificazione IP67</li><li>{TI}Tasto SOS e rapporti automatici di anomalia e manomissione</li></ul><span class="link-arrow">Scopri la TaiBox {A}</span></div></a>
<a class="sol rv" href="t-fish.html"><span class="beam-border"></span><div class="ph dev"><img src="img/tfish-devices.jpg" alt="Palmare T-Fish e stampante Zebra portatile" loading="lazy"></div>
<div class="body"><span class="eyebrow">{ti("r-bl")}Tracciabilità</span><h3 class="h-m">T-Fish</h3><ul class="blist"><li>{TI}Palmare con app e stampante Zebra portatile</li><li>{TI}Etichette con codice a barre e QR code, stampate sul posto</li><li>{TI}Archivio automatico dei lotti</li></ul><span class="link-arrow">Scopri T-Fish {A}</span></div></a>
</div>
<div class="svc-row rv">
<div class="svc"><svg><use href="#i-install"/></svg><b>Installazione</b><span>Montaggio e collaudo della trasmissione.</span></div>
<div class="svc"><svg><use href="#i-sat"/></svg><b>Traffico satellitare</b><span>Fornitore autorizzato del servizio.</span></div>
<div class="svc"><svg><use href="#i-wrench"/></svg><b>Manutenzione</b><span>Interventi a bordo e da remoto.</span></div>
<div class="svc"><svg><use href="#i-phone"/></svg><b>Assistenza</b><span>Un tecnico al telefono.</span></div>
</div></div></section>

{HOWSEC}



<section class="band">{photo('porto.jpg', 'Porto del Mediterraneo')}
<div class="wrap on-photo"><span class="eyebrow rv">{TI}Un unico referente</span><h2 class="h-l rv">Dal porto al largo, un solo numero da chiamare.</h2>
<div class="facts rv"><span>{TI}Apparato autorizzato</span><span>{TI}Traffico satellitare</span><span>{TI}Manutenzione</span><span>{TI}Assistenza tecnica</span></div></div></section>

<section class="sec"><div class="wrap">
<div class="sec-head split"><div class="stack">{eb('Il percorso')}<h2 class="h-l rv">Dalla richiesta alla barca in regola.</h2></div><p class="lead rv">Cinque passaggi, seguiti dai nostri tecnici. I moduli da compilare sono nella pagina Modulistica.</p></div>
<ol class="journey hs-m" data-dots>
<li class="rv"><b>Questionario armatore</b><span>Descrivi barca e tipo di pesca.</span><a class="link-arrow" href="modulistica.html#questionario">Vai al modulo {A}</a></li>
<li class="rv"><b>Preventivo</b><span>Ricevi l'offerta per apparato e servizio.</span><span class="meta">Via email</span></li>
<li class="rv"><b>Richiesta di installazione</b><span>Firmi e avvii installazione e registrazione.</span><a class="link-arrow" href="modulistica.html#installazione">Vai al modulo {A}</a></li>
<li class="rv"><b>Installazione e collaudo</b><span>Montiamo la TaiBox e verifichiamo la trasmissione.</span><span class="meta">Tecnico a bordo</span></li>
<li class="rv"><b>Assistenza e manutenzione</b><span>Traffico satellitare, interventi e aggiornamenti nel tempo.</span><span class="meta">06 97840077</span></li>
</ol></div></section>

{FAQ_SEC.replace('Risposte brevi sulle regole VMS e sulla TaiBox.', 'Obblighi, frequenze e TaiBox in risposte brevi.').replace('>Tutte le FAQ ', '>Leggi tutte le FAQ ')}
{PARTNERS}
<section class="sec cta-mz"><div class="wrap">
<div class="mz-copy stack">{eb('Preventivo TaiBox')}<h2 class="h-l rv">Metti in regola la tua barca.</h2><p class="lead rv">Mandaci lunghezza e tipo di pesca. Ti indichiamo l'apparato richiesto e ti inviamo il preventivo.</p><div class="ctas rv"><a class="btn" href="contatti.html#taibox">Richiedi il preventivo {A}</a><a class="btn ghost" href="tel:+390697840077">Chiama 06 97840077</a></div></div>
{mosaic('hero.jpg', ['. tl s s .', 'tl s s s tr', 'fbl s s br .'], 'mz rv')}
</div></section>
''')

# ---- chi siamo copy
cs = P['chi-siamo'][1]
for a, b in [
    ("'Chi siamo · dal 1988'", "'Chi siamo'"),
    ('Tai Sud progetta, produce e assiste apparati di controllo satellitare per la pesca professionale.', 'Tai Sud fornisce, installa e assiste apparati di controllo satellitare per la pesca professionale.'),
    ('Fondata e fatta crescere da Alberto Tirico.', 'Fondata e guidata da Alberto Tirico.'),
    ('Alberto Tirico fonda Tai Sud a Roma nel 1988 e la guida per oltre trent\'anni.', 'Alberto Tirico fonda Tai Sud a Roma nel 1988, la costruisce e la guida per oltre trent\'anni.'),
    ('Quattro passaggi chiave.', 'Le tappe principali.'),
    ('<time>TaiBox</time><b>Produttore autorizzato</b>', '<time>Oggi</time><b>TaiBox nell\'elenco Masaf</b>'),
    ('<p class="lead rv">Un riferimento diretto per ogni cliente.</p>', '<p class="lead rv">Le persone che rispondono dei nostri apparati.</p>'),
    ('<span>Amministratrice</span>', '<span>Direzione</span>'),
    ('<span>Ruolo da confermare</span>', '<span>Direzione</span>'),
    ('<p class="lead rv">Coordiniamo professionisti dei settori in cui lavoriamo.</p>', '<p class="lead rv">Lavoriamo con professionisti qualificati nei settori in cui operiamo.</p>'),
    ('Progettazione, produzione, installazione e assistenza seguono un sistema qualità certificato.', 'Progettazione, produzione, installazione e assistenza seguono un sistema qualità certificato da IMQ, organismo accreditato ACCREDIA.'),
    ('Cerchiamo persone competenti, con voglia di crescere.', 'Cerchiamo tecnici e persone competenti.'),
    ('Tecnici, installatori, profili amministrativi. Mandaci il CV.', 'Installazione, elettronica, amministrazione. Inviaci il CV.'),
    ('Una barca o una cooperativa: troviamo insieme la soluzione giusta.', 'Una sola barca o un\'intera cooperativa. Ti proponiamo la configurazione adatta.'),
]:
    cs = cs.replace(a, b)
P['chi-siamo'] = ('Chi siamo', cs.replace('Tai Sud progetta, produce e assiste', 'Tai Sud fornisce, installa e assiste'))

# ---- prodotti: split hero
P['prodotti'] = ('Prodotti e servizi', f'''
{page_hero(crumbs(('Prodotti e servizi',)), 'Prodotti e servizi', ['Quello che serve', 'a bordo e in banchina.'], 'Due prodotti e i servizi che li tengono operativi, da un unico referente.', mosaic('faro.jpg', ['. s s tr', 'ftl s s s', 's s br .']))}
<div class="split2">
<a href="taibox.html">{photo('hero.jpg', 'Peschereccio in navigazione')}<small>Per armatori e comandanti</small><b>TaiBox</b><span>La blue box che trasmette posizione e rotta al centro di controllo a terra.</span><em>Scopri la TaiBox {A}</em></a>
<a href="t-fish.html">{photo('mercato.jpg', 'Pescato su ghiaccio')}<small>Per pescherecci, mercati e grossisti</small><b>T-Fish</b><span>Etichette con codice a barre e QR code, stampate sul posto.</span><em>Scopri T-Fish {A}</em></a>
</div>
<section class="sec"><div class="wrap mt">
<div style="background:#fff;border:1px solid var(--line);overflow:hidden" class="cut rv"><img src="img/taibox-kit.jpg" alt="Kit TaiBox" loading="lazy"></div>
<div class="stack">{eb('Blue box · ACS')}<h2 class="h-l rv">TaiBox</h2><p class="lead rv">Apparato di controllo satellitare per pescherecci. Invia posizione e rotta al centro di controllo a terra, segnala anomalie e tentativi di manomissione, trasmette l'SOS.</p><div class="tags rv"><span>Autorizzata Masaf</span><span>IP67</span><span>Display 7"</span></div><div class="ctas rv"><a class="btn" href="taibox.html">Scopri la TaiBox {A}</a></div></div>
</div></section>
<section class="sec mist"><div class="wrap mt rev">
{mosaic('mercato.jpg', ['tl s s .', 's s s s', '. s s fbr'], 'rv')}
<div class="stack">{eb('Tracciabilità', 'r-bl')}<h2 class="h-l rv">T-Fish</h2><p class="lead rv">Palmare con app e stampante portatile. Registri il lotto e stampi sul posto l'etichetta con codice a barre e QR code.</p><div class="tags rv"><span>App</span><span>QR code</span><span>Zebra</span><span>IP54</span></div><div class="ctas rv"><a class="btn" href="t-fish.html">Scopri T-Fish {A}</a></div></div>
</div></section>
<section class="sec dark" id="servizi"><div class="wrap">
<div class="sec-head split"><div class="stack">{eb('Servizi')}<h2 class="h-l rv">Prima, durante e dopo l'installazione.</h2></div><p class="lead rv">Siamo fornitore autorizzato di traffico satellitare e manutenzione degli apparati.</p></div>
<div class="feats">
<div class="feat rv"><svg><use href="#i-install"/></svg><b>Installazione a bordo</b><span>Montaggio della TaiBox e collaudo della trasmissione.</span></div>
<div class="feat rv"><svg><use href="#i-sat"/></svg><b>Traffico satellitare</b><span>Il servizio di trasmissione dei dati, gestito da noi.</span></div>
<div class="feat rv"><svg><use href="#i-wrench"/></svg><b>Manutenzione</b><span>Interventi a bordo e aggiornamenti da remoto.</span></div>
<div class="feat rv"><svg><use href="#i-code"/></svg><b>Sistemi su misura</b><span>Progetti informativi e integrazioni per aziende.</span></div>
</div></div></section>
<section class="sec tight"><div class="wrap"><div class="check coop"><div class="chk-in"><span class="eyebrow">{TI}Cooperative e flotte</span><h3 class="h-m">Più barche, un solo referente.</h3><p class="muted">Per cooperative e armatori con più unità prepariamo un'offerta unica per apparati, traffico satellitare e manutenzione.</p></div><div class="chk-in coop-cta"><a class="btn" href="contatti.html#taibox">Offerta per la flotta {A}</a></div></div></div></section>
''' + cta('Chiedi un preventivo su misura.', 'Indica prodotto e numero di barche. Ti inviamo una proposta per apparati e servizi.', ('Richiedi il preventivo', 'contatti.html#taibox'), ('Chiama 06 97840077', 'tel:+390697840077')))

MODEINFO = MODEINFO.replace('Trasmette la posizione alla frequenza prevista dalla legge. Avvisi e anomalie arrivano al centro di controllo.', 'Trasmette la posizione alla frequenza prevista dal regolamento. Anomalie e infrazioni arrivano al centro di controllo a terra.').replace('<div class="mode-info rv">', '<div class="mode-info rv" aria-live="polite">')
P['taibox'] = (P['taibox'][0], P['taibox'][1].replace(P['taibox'][1][P['taibox'][1].index('<div class="mode-info'):P['taibox'][1].index('</div>', P['taibox'][1].index('<div class="mode-info'))+6], MODEINFO))
# ---- taibox tweaks
tb = P['taibox'][1]
for a, b in [
    ("['TaiBox. La blue box', 'conforme per legge.']", ""),
    ('Trasmette posizione e rotta della tua barca al centro di controllo a terra. Display touch 7", IP67, prodotta in Italia.', 'Trasmette posizione e rotta della barca al centro di controllo a terra. Display touch 7" integrato, certificazione IP67, nell\'elenco degli apparati autorizzati dal Masaf.'),
    ('Richiedi un preventivo {A}</a><a class="btn ghost" href="modulistica.html">Moduli</a>', ''),
    ('<p class="lead rv">Tutto quello che il regolamento chiede, in una scatola montata a bordo.</p>', '<p class="lead rv">Le funzioni richieste dal regolamento, in un apparato montato a bordo.</p>'),
    ('<b>Anti manomissione</b><span>Segnala guasti e tentativi di manomissione.</span>', '<b>Anti manomissione</b><span>Rapporto automatico di anomalia, anche per manomissione.</span>'),
    ('<b>Limiti di pesca</b><span>Avvisa se la barca esce dai limiti consentiti.</span>', '<b>Limiti di pesca</b><span>Rapporto di infrazione se la barca esce dai limiti.</span>'),
    ('<b>Da remoto</b><span>Aggiornamenti senza salire a bordo.</span>', '<b>Da remoto</b><span>Telecontrollo e aggiornamenti senza salire a bordo.</span>'),
    ('<h2 class="h-l rv">Trasmette anche dove il telefono non prende.</h2>', '<h2 class="h-l rv">Trasmette anche dove la rete mobile non arriva.</h2>'),
    ('<h2 class="h-l rv">Tutto sotto controllo, dalla plancia.</h2>', '<h2 class="h-l rv">Lo stato dell\'apparato, sotto gli occhi del comandante.</h2>'),
    ('<section class="sec"><div class="wrap mt">\n<div class="stack">{eb', '<section class="sec"><div class="wrap mt">\n<div class="stack">{eb'),
    ('Cosa chiede la legge. Cosa fa la TaiBox.', 'I requisiti del regolamento, punto per punto.'),
    ('<p class="note">Conformità dichiarata da Tai Sud. Da verificare con la scheda tecnica prima della pubblicazione.</p>', '<div class="stack sm rv" style="margin-top:24px;padding:22px 24px;border:1px solid var(--line);border-radius:6px 6px 6px 32px;background:#fff;max-width:640px"><b>Controlla l\'elenco ufficiale.</b><span class="muted">TaiBox compare nell\'elenco degli apparati di controllo satellitare autorizzati dal Masaf.</span><a class="link-arrow" href="https://www.controllopesca.politicheagricole.it/flex/cm/pages/ServeBLOB.php/L/IT/IDPagina/153" target="_blank" rel="noopener">Apri l\'elenco Masaf ↗</a></div>'),
    ('<span class="eyebrow rv">{TI}Nella scatola</span>', ''),
    ('Compila il questionario armatore o scrivici. Ti rispondiamo con la configurazione giusta.', 'Compila il questionario armatore o scrivici. Ti proponiamo la configurazione adatta alla tua barca.'),
]:
    if a: tb = tb.replace(a, b)
tb = tb.replace('<div class="wrap mt">\n<div class="stack">' + eb('Il display'), '<div class="wrap mt disp">\n<div class="stack">' + eb('Il display'))
tb = tb.replace("TaiBox. La blue box</span></span><span class=\"ln\"><span>conforme per legge.", "TaiBox.</span></span><span class=\"ln\"><span>La blue box che ti tiene in regola.")
tb = tb.replace(f'<a class="btn" href="contatti.html#taibox">Richiedi un preventivo {A}</a><a class="btn ghost" href="modulistica.html">Moduli</a>', f'<a class="btn" href="contatti.html#taibox">Richiedi il preventivo {A}</a><a class="btn ghost" href="modulistica.html#questionario">Scarica il questionario</a>')
P['taibox'] = ('TaiBox, blue box VMS per pescherecci', tb)

# ---- t-fish: interactive story
tf = P['t-fish'][1]
s0 = tf.index('<section class="sec"><div class="wrap">\n<div class="sec-head">' + eb('Come si usa'))
s1 = tf.index('</section>', s0) + 10
TFC = open(D + 'tf.html').read().replace('<p class="tf__lede">', '<p class="tf__lede rv">')
tf = tf[:s0] + TFC + tf[s1:]
tf = tf.replace('Richiedi informazioni ' + A, 'Richiedi il preventivo T-Fish ' + A).replace('<b>Ogni settore</b><span>Non solo pesce: tutte le merci.</span>', '<b>Ogni settore</b><span>Utilizzabile anche fuori dal settore ittico.</span>')
tf = tf.replace('La tracciabilità diventa digitale.', 'La tracciabilità del pescato diventa digitale.').replace('Semplice anche in banchina.', 'Pensato per la banchina.')
tf = tf.replace("Raccontaci come lavori: ti proponiamo la configurazione T-Fish adatta.", "Raccontaci come gestisci oggi le etichette. Ti proponiamo la configurazione T-Fish adatta.")
tf = tf.replace("'Pescherecci, mercati ittici, grossisti.'", "'Per pescherecci, mercati ittici e grossisti.'")
P['t-fish'] = ('T-Fish, tracciabilità del pescato', tf.replace('Pescherecci, mercati ittici, grossisti.', 'Per pescherecci, mercati ittici e grossisti.'))

# ---- normativa
COV = open(D + 'cov.html').read()
COUNT = '<div class="hero-count hin"><small>Prossima scadenza</small><b data-days>--</b><p>giorni al 10 luglio 2027. Da quel giorno la posizione va trasmessa ogni 30 minuti.</p><div class="bar"><i data-dl-bar></i></div><small style="color:var(--on-d2)">10.01.2026 · obbligo VMS dai 12 metri</small></div>'
nt = P['normativa'][1]
P['normativa'] = ('Obbligo VMS 12 metri: scadenze e FAQ', page_hero(crumbs(('Normativa',)), 'Reg. (UE) 2023/2842 · Reg. di esecuzione (UE) 2025/2196', ['Le regole sul VMS,', 'spiegate in chiaro.'], 'Chi è obbligato, quale apparato serve, cosa cambia dal 2027. Con i link alle fonti ufficiali.', COUNT, f'<div class="ctas hin"><a class="btn" href="#verifica">Verifica la tua barca {A}</a><a class="btn ghost" href="#faq">Vai alle FAQ</a></div>') + f'''
<section class="sec" id="verifica"><div class="wrap">
<div class="sec-head split"><div class="stack">{eb('Verifica rapida')}<h2 class="h-l rv">La tua barca deve avere il VMS?</h2></div><p class="lead rv">Due risposte e vedi cosa prevede il regolamento per la tua barca.</p></div>
{CHECK}
</div></section>
<section class="sec mist"><div class="wrap two">
<div class="stack sticky">{eb('Le scadenze')}<h2 class="h-l rv">In vigore e in arrivo.</h2><p class="lead rv">Ogni scadenza riporta lo stato aggiornato alla data di oggi.</p></div>
<div class="vtl" id="norm-dl"></div>
</div></section>
<div style="background:#fff">{COV}</div>
''' + nt[nt.index('<section class="band"'):].replace("L'apparato resta acceso. Sempre.", "L'apparato resta acceso per tutta la navigazione.").replace('Il comandante</span>', 'Obblighi a bordo</span>').replace('Tutte le domande sul VMS.', 'Domande frequenti sul VMS.').replace('<div class="faq" data-faq="all"></div>', '<div class="faq-meta"><span id="faq-count" aria-live="polite"></span><button type="button" id="faq-all" class="link-arrow" style="font:inherit;letter-spacing:inherit">Mostra tutte</button></div><div class="faq" data-faq="all"></div>').replace('Nessuna risposta trovata. <a class="link-arrow" href="contatti.html">Scrivici', 'Nessuna risposta per questa ricerca. <a class="link-arrow" href="contatti.html#taibox">Chiedi a un tecnico').replace("'Hai un dubbio sulla tua barca?'", "x"))
P['normativa'] = (P['normativa'][0], P['normativa'][1].replace('Hai un dubbio sulla tua barca?', 'Un tecnico verifica il tuo caso.').replace('Dicci lunghezza e tipo di pesca: ti spieghiamo cosa prevede la legge nel tuo caso.', 'Indica lunghezza, tipo di pesca e zona. Ti diciamo quale apparato richiede la legge per la tua barca.').replace('>Scrivici {A}<', '>Chiedi la verifica {A}<').replace('{TI}', TI))

# ---- assistenza
HELP2 = f'<div class="help hin"><span class="eyebrow">{TI}Linea assistenza</span><div class="lines"><span>Assistenza TaiBox</span><a class="big" href="tel:+390697840077">06 97840077</a></div><div class="row"><span>Altro numero <a href="tel:+390697040156">06 97040156</a></span><a href="mailto:info@taisud.com">info@taisud.com</a></div><span class="tbd">[Orari di assistenza]</span><a class="btn white" href="contatti.html#assistenza" style="justify-self:start">Apri una richiesta {A}</a></div>'
P['assistenza'] = ('Assistenza tecnica TaiBox', page_hero(crumbs(('Assistenza',)), 'Assistenza tecnica', ['Assistenza TaiBox,', 'direttamente con un tecnico.'], 'Ti guidiamo al telefono e, se serve, organizziamo l\'intervento a bordo.', HELP2, '', True) + f'''
<section class="sec"><div class="wrap">
<div class="sec-head split"><div class="stack">{eb('Che cosa succede')}<h2 class="h-l rv">Scegli il problema.</h2></div><p class="lead rv">Apri la richiesta già impostata. Per un apparato che non trasmette chiama anche lo 06 97840077.</p></div>
<div class="symptoms">
<a class="sym rv" href="contatti.html#assistenza"><span class="code">Urgente</span><b>L'apparato non trasmette</b><p>La posizione non arriva al centro di controllo o il display segnala assenza di segnale.</p><span class="link-arrow">Apri la richiesta {A}</span></a>
<a class="sym rv" href="contatti.html#assistenza"><span class="code">Display</span><b>Errore sul display</b><p>Compare un messaggio di errore o un avviso che non riconosci. Fotografa lo schermo.</p><span class="link-arrow">Apri la richiesta {A}</span></a>
<a class="sym rv" href="contatti.html#assistenza"><span class="code">Hardware</span><b>Danno fisico</b><p>Antenna, cavi o unità danneggiati. Organizziamo l'intervento a bordo.</p><span class="link-arrow">Apri la richiesta {A}</span></a>
</div></div></section>
<section class="sec mist"><div class="wrap">
<div class="sec-head split"><div class="stack">{eb('Prima di chiamare')}<h2 class="h-l rv">Quattro informazioni da preparare.</h2></div><p class="lead rv">Spunta le voci mentre le prepari. La chiamata sarà più rapida.</p></div>
<ul class="checks">
<li class="rv"><label><input type="checkbox"><b>Nome della barca</b><span>E porto di iscrizione.</span></label></li>
<li class="rv"><label><input type="checkbox"><b>Numero UE di flotta</b><span>Lo trovi sui documenti della barca.</span></label></li>
<li class="rv"><label><input type="checkbox"><b>Messaggio sul display</b><span>Errore o modalità attiva. Una foto aiuta.</span></label></li>
<li class="rv"><label><input type="checkbox"><b>Alimentazione</b><span>Se l'apparato riceve corrente.</span></label></li>
</ul></div></section>
<section class="sec"><div class="wrap mt disp">
<div class="stack">{eb('Le modalità')}<h2 class="h-l rv">In porto si cambia modalità, non si spegne.</h2><p class="lead rv">L'apparato si spegne solo dopo averlo comunicato alle autorità. In porto o in manutenzione si imposta la modalità dal display. Prova i tasti.</p>{MODEINFO}</div>
{DISPLAY}
</div></section>
<section class="sec dark"><div class="wrap two">
<div class="stack">{eb('Guasto in navigazione')}<h2 class="h-l rv">Se il segnale si perde, i dati non si perdono.</h2></div>
<ul class="blist rv" style="font-size:17px"><li>{TI}<span style="color:var(--on-d2)">La TaiBox salva in memoria almeno 200 posizioni e le invia appena il segnale torna.</span></li><li>{TI}<span style="color:var(--on-d2)">Il comandante deve assicurarsi che l'apparato resti acceso, alimentato e non manomesso.</span></li><li>{TI}<span style="color:var(--on-d2)">Chiama l'assistenza: ti diciamo come procedere e, se serve, organizziamo l'intervento.</span></li></ul>
</div></section>
''' + cta('Manutenzione e traffico satellitare, da noi.', 'Siamo fornitore autorizzato di manutenzione e traffico satellitare per gli apparati.', ('Apri una richiesta', 'contatti.html#assistenza'), ('Chiama 06 97840077', 'tel:+390697840077'), 'faro.jpg'))

# ---- modulistica
def doc2(idn, step, title, what, who, when, href, meta, send=True):
    s = '<a class="btn ghost sm" href="contatti.html#moduli">Invia il modulo compilato</a>' if send else ''
    return f'''<article class="doc rv" id="{idn}"><span class="beam-border"></span><div class="top"><div class="ico">PDF</div><div><span class="when">{step}</span><h3 class="h-s" style="margin-top:6px">{title}</h3></div></div>
<dl><div><dt>A cosa serve</dt><dd>{what}</dd></div>{f'<div><dt>Chi lo compila</dt><dd>{who}</dd></div>' if who else ''}{f'<div><dt>Quando</dt><dd>{when}</dd></div>' if when else ''}</dl>
<div class="meta">{''.join(f'<span>{x}</span>' for x in meta)}</div>
<div class="acts"><a class="btn sm" href="{href}" target="_blank" rel="noopener"><svg><use href="#i-download"/></svg>Scarica PDF<span class="sr"> (si apre in una nuova scheda)</span></a>{s}</div></article>'''
P['modulistica'] = ('Modulistica TaiBox', page_hero(crumbs(('Modulistica',)), 'Contrattualistica e modulistica', ['I moduli', 'per iniziare.'], 'Scarica i PDF, compilali e inviali dal modulo online o a info@taisud.com.', mosaic('reti.jpg', ['tl s .', 's s ftr', 'fbl s br'])).replace('class="page-hero"', 'class="page-hero mod"') + f'''
<section class="sec"><div class="wrap">
<div class="sec-head">{eb('Per iniziare con la TaiBox')}<h2 class="h-l rv">Due moduli, in quest'ordine.</h2></div>
<div class="docs" style="grid-template-columns:repeat(auto-fit,minmax(min(100%,360px),1fr))">
{doc2('questionario', 'Prima del preventivo', "Questionario per l'armatore", 'Descrive barca e tipo di pesca, per preparare la configurazione.', "Armatore o comandante", 'Prima di chiedere il preventivo', 'https://taisud.com/wp-content/uploads/2025/04/questionario-armatore.pdf', ['PDF', 'Da firmare'])}
{doc2('installazione', "Dopo l'accettazione", 'Richiesta di prima installazione', "Avvia l'installazione a bordo e la registrazione dell'apparato.", "Armatore", "Dopo aver accettato il preventivo", 'https://taisud.com/wp-content/uploads/2025/04/allegato-prima-installazione.pdf', ['PDF', 'Da firmare'])}
</div></div></section>
<section class="sec mist tight"><div class="wrap">
<div class="sec-head" style="margin-bottom:32px">{eb('Il percorso completo')}</div>
<ol class="journey hs-m" data-dots>
<li><b>Questionario</b><span>Prima del preventivo.</span><a class="link-arrow" href="#questionario">Vai al modulo {A}</a></li><li><b>Preventivo</b><span>Ricevi l'offerta.</span><span class="meta">Via email</span></li><li><b>Richiesta di installazione</b><span>Dopo l'accettazione.</span><a class="link-arrow" href="#installazione">Vai al modulo {A}</a></li><li><b>Installazione</b><span>A bordo, con i nostri tecnici.</span><span class="meta">Tecnico a bordo</span></li><li><b>Assistenza</b><span>Manutenzione e traffico satellitare.</span><span class="meta">06 97840077</span></li>
</ol></div></section>
<section class="sec"><div class="wrap">
<div class="iso-row"><div class="stack">{eb('Documenti aziendali')}<h2 class="h-l rv">Per gare e uffici acquisti.</h2><p class="lead rv">Il certificato del sistema qualità, pronto da allegare a gare, albi fornitori e qualifiche.</p></div>
<div class="docs one">{doc2('iso', 'Qualità', 'Certificato ISO 9001:2015', 'UNI EN ISO 9001:2015, rilasciato da IMQ con accreditamento ACCREDIA.', '', '', 'https://taisud.com/wp-content/uploads/2025/03/Certificato_iso9001_Tai-Sud.pdf', ['PDF', 'IMQ'], False)}</div></div>
</div></section>
''' + cta('Ti aiutiamo a compilarli.', 'Chiamaci e li compiliamo insieme al telefono.', ('Chiama 06 97840077', 'tel:+390697840077'), ('Invia i moduli', 'contatti.html#moduli')))

# ---- qualita
P['qualita'] = ('Politica della qualità ISO 9001:2015', page_hero(crumbs(('Chi siamo', 'chi-siamo.html'), ('Qualità',)), 'UNI EN ISO 9001:2015', ['Politica', 'della qualità.'], 'Un sistema qualità conforme alla UNI EN ISO 9001:2015, certificato IMQ con accreditamento ACCREDIA, governa ogni fase del nostro lavoro.', '<div class="cert-doc"><div class="top"><img src="img/imq.png" alt="IMQ Certified, ISO 9001:2015"><img src="img/accredia.png" alt="ACCREDIA"></div><b>Certificato ISO 9001:2015</b><span>TAI SUD s.r.l.<br>Progettazione, produzione, installazione e assistenza tecnica di sistemi e apparecchiature avanzate ICT</span><div class="seal"><i class="tile-ico"></i><i class="tile-ico r-tr"></i><i class="tile-ico"></i></div></div>', f'<div class="ctas hin"><a class="btn ghost" href="https://taisud.com/wp-content/uploads/2025/03/Certificato_iso9001_Tai-Sud.pdf" target="_blank" rel="noopener"><svg><use href="#i-download"/></svg>Scarica il certificato</a></div>') + f'''
<section class="sec"><div class="wrap">
<div class="sec-head">{eb('I nostri impegni')}<h2 class="h-l rv">Nove principi, un solo obiettivo: il cliente soddisfatto.</h2></div>
<ol class="princ"><li class="rv">Qualità dell'organizzazione</li><li class="rv">Miglioramento continuo</li><li class="rv">Soddisfazione del cliente</li><li class="rv">Qualità del servizio</li><li class="rv">Rispetto delle norme</li><li class="rv">Crescita delle persone</li><li class="rv">Continuità del servizio</li><li class="rv">Fornitori responsabili</li><li class="rv">Sostenibilità ambientale</li></ol>
<p class="muted" style="margin-top:32px;max-width:64ch">La Direzione assegna le risorse necessarie e verifica i risultati con audit interni, controllo della conformità normativa e riesame annuale degli obiettivi.</p>
</div></section>''')

# ---- lavora
lv = P['lavora-con-noi'][1]
lv = lv.replace("Un\\'azienda funziona quando è fatta di persone preparate, con obiettivi in comune.", "x").replace("Un'azienda funziona quando è fatta di persone preparate, con obiettivi in comune.", "Cerchiamo persone preparate per installare, mantenere e supportare apparati che lavorano in mare.")
lv = lv.replace('Persone competenti, che vogliono crescere.', 'Competenza tecnica e affidabilità.').replace('<p class="lead rv">Costruiamo la squadra con cura. Se vuoi lavorare con la tecnologia a bordo, raccontaci cosa sai fare.</p>', '<p class="lead rv">Se lavori con elettronica, telecomunicazioni o assistenza clienti, raccontaci cosa sai fare.</p>')
P['lavora-con-noi'] = ('Lavora con noi', lv)

# ---- contatti form tweaks
ct = P['contatti'][1]
for a, b in [
    ("['Parliamone.'], 'Scegli il motivo: il modulo si adatta.'", ""),
    ('<label for="f-email">Email *</label><span class="err">Inserisci un\'email valida</span>', '<label for="f-email">Email</label><span class="err" id="e-email">Inserisci un\'email valida, oppure il telefono.</span>'),
    ('<input id="f-email" name="email" type="email" placeholder=" " autocomplete="email" required>', '<input id="f-email" name="email" type="email" placeholder=" " autocomplete="email" aria-describedby="e-email">'),
    ('<div class="f"><input id="f-tel" name="telefono" type="tel" placeholder=" " autocomplete="tel"><label for="f-tel">Telefono</label></div>', '<div class="f"><input id="f-tel" name="telefono" type="tel" placeholder=" " autocomplete="tel" aria-describedby="tel-hint e-tel"><label for="f-tel">Telefono</label><span class="hint" id="tel-hint"></span><span class="err" id="e-tel">Inserisci un numero valido.</span></div>'),
    ('<input id="f-nome" name="nome" placeholder=" " autocomplete="name" required><label for="f-nome">Nome e cognome *</label><span class="err">Inserisci nome e cognome</span>', '<input id="f-nome" name="nome" placeholder=" " autocomplete="name" required aria-describedby="e-nome"><label for="f-nome">Nome e cognome *</label><span class="err" id="e-nome">Inserisci nome e cognome.</span>'),
    ('<label for="f-porto">Porto</label>', '<label for="f-porto">Porto di iscrizione</label>'),
    ('<label for="f-lft">Lunghezza (m)</label>', '<label for="f-lft">Lunghezza fuori tutto (m)</label>'),
    ('<option>Piccola pesca costiera</option>', '<option>Pesca costiera locale (entro 12 miglia)</option>'),
    ('<select id="f-urg" name="problema"><option>Non trasmette</option>', '<select id="f-urg" name="problema"><option value="">Seleziona</option><option>Non trasmette</option>'),
    ('<span>Assistenza<small>Problema all\'apparato</small></span>', '<span>Assistenza<small>Guasto o errore</small></span>'),
    ('<span>Invio moduli<small>PDF compilati</small></span>', '<span>Invio moduli<small>Questionario o installazione</small></span>'),
    ('<span>Candidatura<small>Lavora con noi</small></span>', '<span>Candidatura<small>Invia il tuo CV</small></span>'),
    ('<span>Altro<small>Qualsiasi richiesta</small></span>', '<span>Altro<small>Altre richieste</small></span>'),
    ('<div class="files" id="files"></div></div>', '<div class="files" id="files"></div><p class="file-err" id="file-err" role="alert"></p></div>'),
    ('per questa richiesta. *</span></label>', 'per gestire questa richiesta. *</span></label><p class="consent-err" id="consent-err" hidden>Serve il consenso per inviare la richiesta.</p>'),
    ('<small>* obbligatori</small><button class="btn" type="submit">Invia richiesta {A}</button>'.replace('{A}', A), '<small>* obbligatorio. Serve almeno telefono o email.</small><button class="btn" type="submit">Invia la richiesta ' + A + '</button>'),
    ('<div class="sent" id="sent" hidden><div class="tick"><svg><use href="#i-check"/></svg></div><h3 class="h-m">Richiesta pronta.</h3>', '<div class="sent" id="sent" hidden role="status"><div class="tick"><svg><use href="#i-check"/></svg></div><h3 class="h-m" tabindex="-1">Richiesta pronta.</h3><p class="urgent" id="urgent" hidden>Per un apparato che non trasmette chiama anche lo <a href="tel:+390697840077"><b>06 97840077</b></a>.</p>'),
    ('<button class="btn ghost sm" type="button" id="again">Nuova richiesta</button>', '<button class="btn ghost sm" type="button" id="again">Invia un\'altra richiesta</button>'),
    ('Apri in Maps ↗', 'Apri in Google Maps ↗'),
]:
    if a: ct = ct.replace(a, b)
ct = ct.replace("Scegli il motivo: il modulo si adatta.", "Scegli il motivo della richiesta. Il modulo mostra solo i campi che servono.")
P['contatti'] = ('Contatti, preventivi e assistenza', ct)

SEO = {
 'home': ('Blue box pesca e VMS per pescherecci | TaiBox, Tai Sud', 'TaiBox, apparato di controllo satellitare autorizzato Masaf. Obbligo VMS dai 12 metri: fornitura, installazione, traffico satellitare e assistenza.'),
 'chi-siamo': ('Chi siamo | Tai Sud, apparati di controllo satellitare dal 1988', 'Tai Sud, Roma, dal 1988. TaiBox per il controllo satellitare dei pescherecci, traffico satellitare e manutenzione. Sistema qualità ISO 9001:2015.'),
 'prodotti': ('Prodotti e servizi | Blue box VMS e tracciabilità pescato | Tai Sud', 'TaiBox, apparato di controllo satellitare per pescherecci, e T-Fish per la tracciabilità del pescato. Installazione, traffico satellitare, manutenzione.'),
 'taibox': ('TaiBox | Blue box VMS per pescherecci, autorizzata Masaf', 'Apparato di controllo satellitare per l\'obbligo VMS dai 12 metri. Display touch 7", IP67, SOS, rapporti di anomalia. Installazione e assistenza Tai Sud.'),
 't-fish': ('T-Fish | Tracciabilità del pescato ed etichette con QR code', 'Palmare con app e stampante Zebra per etichette con codice a barre e QR code. Tracciabilità digitale del pescato secondo il Reg. (UE) 2023/2842.'),
 'normativa': ('Obbligo VMS 12 metri: scadenze e FAQ | Normativa pesca', 'VMS e giornale di pesca elettronico obbligatori dai 12 metri dal 10 gennaio 2026. Trasmissione ogni 30 minuti dal 2027. Apparati ACS, ACI, ACM spiegati.'),
 'assistenza': ('Assistenza tecnica TaiBox | Blue box VMS | Tai Sud', 'Assistenza tecnica per apparati TaiBox: errori sul display, mancata trasmissione, manutenzione. Linea diretta 06 97840077, info@taisud.com.'),
 'modulistica': ('Modulistica TaiBox | Questionario armatore e installazione', 'Scarica il questionario armatore e la richiesta di prima installazione della blue box TaiBox. Certificato ISO 9001:2015 per gare e albi fornitori.'),
 'contatti': ('Contatti Tai Sud | Preventivo blue box VMS e assistenza', 'Preventivo TaiBox o T-Fish, assistenza tecnica, invio moduli. Tai Sud, Viale G. Bonelli 341, Roma. Tel. 06 97840077, info@taisud.com.'),
 'lavora-con-noi': ('Lavora con noi | Tecnici e installatori | Tai Sud Roma', 'Tai Sud cerca tecnici, installatori e profili amministrativi per apparati di controllo satellitare della pesca. Invia il tuo CV.'),
 'qualita': ('Politica della qualità ISO 9001:2015 | Tai Sud', 'Sistema qualità UNI EN ISO 9001:2015 certificato IMQ, accreditato ACCREDIA, per progettazione, produzione, installazione e assistenza di apparati ICT.'),
}
EXTRA_CSS = {'normativa': open(D + 'coverage.css').read(), 't-fish': open(D + 'tfish.css').read()}
EXTRA_JS = {'home': open(D + 'fleet.js').read(), 'normativa': open(D + 'coverage.js').read(), 't-fish': open(D + 'tfish.js').read()}

