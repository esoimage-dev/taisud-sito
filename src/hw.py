HW_STEPS = [
 ('Bordo', 'La TaiBox rileva la posizione', 'Il GPS calcola posizione, rotta e velocità. Il comandante vede lo stato dell\'apparato sul display.'),
 ('Satellite', 'Trasmette via satellite', 'Alla frequenza prevista dal regolamento, anche dove la rete mobile non arriva.'),
 ('Terra', 'Il centro di controllo riceve', 'I dati arrivano a terra. Da remoto si controlla e si aggiorna l\'apparato.'),
 ('Avvisi', 'Anomalie, infrazioni, SOS', 'Guasti, tentativi di manomissione e uscite dai limiti generano un rapporto automatico. L\'SOS parte con un tasto.'),
]
def _hw_items():
    out = []
    for i, (k, t, d) in enumerate(HW_STEPS, 1):
        out.append(f'<li class="hw-it{" on" if i == 1 else ""}" data-s="{i}"><button type="button" class="hw-btn" aria-expanded="{"true" if i == 1 else "false"}" aria-controls="hw-d{i}"><span class="hw-n">0{i}</span><span class="hw-k">{k}</span><span class="hw-t">{t}</span><span class="hw-pm" aria-hidden="true"></span></button><div class="hw-d" id="hw-d{i}"><div><p>{d}</p></div></div><span class="hw-bar" aria-hidden="true"><i></i></span></li>')
    return ''.join(out)
HOWSEC = f'''<section class="sec dark hw-sec"><div class="wrap">
<div class="sec-head split"><div class="stack">{eb('Come funziona')}<h2 class="h-l rv">Dalla barca al centro di controllo.</h2></div><p class="lead rv">Quattro passaggi, ogni volta che la TaiBox trasmette. Seleziona un passaggio per vederlo nello schema.</p></div>
<div class="hw" data-hw>
<div class="hw-stage rv" aria-hidden="true">
<div class="hw-cap"><span class="hw-cap-n">01 / 04</span><span class="hw-cap-k">Bordo</span></div>
<svg viewBox="30 40 460 440">
<g class="rings"><circle cx="260" cy="260" r="110"/><circle cx="260" cy="260" r="190" stroke-dasharray="2 6"/></g>
<g class="sweep"><path d="M260 260 L260 70 A190 190 0 0 1 394 126 Z" fill="url(#hwsw)"/></g>
<defs><linearGradient id="hwsw" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#8AD2F2" stop-opacity="0"/><stop offset="1" stop-color="#8AD2F2" stop-opacity=".2"/></linearGradient></defs>
<path class="link" d="M120 370 L260 154 L400 370 L400 230"/>
<path class="flow" data-f="2" pathLength="1" d="M120 370 L260 154"/><path class="flow" data-f="3" pathLength="1" d="M260 154 L400 370"/><path class="flow" data-f="4" pathLength="1" d="M400 370 L400 230"/>
<circle class="pulse" r="4.5"><animateMotion dur="2.8s" repeatCount="indefinite" path="M120 370 L260 154 L400 370 L400 230"/></circle>
<g class="node" data-n="1"><rect x="56" y="370" width="128" height="74" rx="8"/><svg class="ic" x="102" y="378" width="36" height="36"><use href="#i-boat"/></svg><text x="120" y="432" text-anchor="middle">TAIBOX</text></g>
<g class="node" data-n="2"><circle class="base" cx="260" cy="110" r="44"/><svg class="ic" x="240" y="90" width="40" height="40"><use href="#i-sat"/></svg><text x="260" y="178" text-anchor="middle">SATELLITE</text></g>
<g class="node" data-n="3"><rect x="336" y="370" width="128" height="74" rx="8"/><svg class="ic" x="382" y="376" width="36" height="36"><use href="#i-remote"/></svg><text x="400" y="432" text-anchor="middle">CENTRO</text></g>
<g class="node" data-n="4"><rect x="336" y="156" width="128" height="74" rx="8"/><svg class="ic" x="382" y="162" width="36" height="36"><use href="#i-alert"/></svg><text x="400" y="218" text-anchor="middle">AVVISI · SOS</text></g>
</svg></div>
<ol class="hw-list">{_hw_items()}</ol>
</div></div></section>'''
