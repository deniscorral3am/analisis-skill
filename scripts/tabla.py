#!/usr/bin/env python3
"""Ordena todos los reels del proyecto por visitas y comentarios y saca gancho, CTA y ritmo de cada uno.

Uso:  python3 tabla.py --proyecto ~/Analisis/mi-sector [--top 30]

Deja <proyecto>/reels.csv (todos) y <proyecto>/top.md (los mejores, con su transcripción) para que Claude busque
los patrones. Cada reel se compara con la MEDIANA de su propia cuenta («x mediana»): así una cuenta pequeña con un
reel que le ha ido 5 veces mejor de lo normal pesa tanto como una grande.
"""
import argparse, csv, glob, json, os, re, statistics as st

def frases(txt):
    out = []
    for l in txt.splitlines():
        m = re.match(r'\[\s*([\d.]+)\]\s*(.*)', l)
        if m:
            out.append((float(m.group(1)), m.group(2)))
    return out

CTA = re.compile(r'\b(comenta|escribe|pon|deja)\s+(?:la palabra\s+)?[«"“]?([A-ZÁÉÍÓÚÑa-záéíóúñ0-9]{2,20})', re.I)

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--proyecto', required=True)
    ap.add_argument('--top', type=int, default=30)
    a = ap.parse_args()
    P = os.path.expanduser(a.proyecto); filas = []
    for j in glob.glob(os.path.join(P, 'reels', '**', '*.info.json'), recursive=True):
        try:
            d = json.load(open(j))
        except Exception:
            continue
        base = j[:-len('.info.json')]; txt = open(base + '.txt').read() if os.path.exists(base + '.txt') else ''
        fr = frases(txt); dur = d.get('duration') or 0
        texto = ' '.join(x for _, x in fr)
        gancho = ' '.join(x for t, x in fr if t < 3.0) or (fr[0][1] if fr else '')
        cta = CTA.search(texto) or CTA.search(d.get('description') or '')
        filas.append({
            'cuenta': (d.get('uploader_id') or d.get('channel') or d.get('uploader') or os.path.basename(os.path.dirname(j))).lstrip('@'),
            'fecha': d.get('upload_date', ''), 'url': d.get('webpage_url', ''),
            'visitas': d.get('view_count') or 0, 'me_gusta': d.get('like_count') or 0, 'comentarios': d.get('comment_count') or 0,
            'duracion_s': round(dur, 1), 'frases_por_10s': round(len(fr) / dur * 10, 1) if dur else '',
            'gancho': gancho[:200], 'cta': (cta.group(2).upper() if cta else ''),
            'descripcion': (d.get('description') or '').replace('\n', ' ')[:200], 'transcripcion': base + '.txt' if txt else ''})
    if not filas:
        raise SystemExit('No hay reels con ficha. Lanza antes descargar.py')
    por = {}
    for f in filas:
        por.setdefault(f['cuenta'], []).append(f)
    for c, fs in por.items():
        mv = st.median([f['visitas'] for f in fs]) or 1; mc = st.median([f['comentarios'] for f in fs]) or 1
        for f in fs:
            f['x_mediana_visitas'] = round(f['visitas'] / mv, 2); f['x_mediana_comentarios'] = round(f['comentarios'] / mc, 2)
            f['puntos'] = round(0.6 * f['x_mediana_visitas'] + 0.4 * f['x_mediana_comentarios'], 2)
    filas.sort(key=lambda f: (f['puntos'], f['visitas']), reverse=True)
    campos = ['puntos', 'cuenta', 'fecha', 'visitas', 'x_mediana_visitas', 'comentarios', 'x_mediana_comentarios', 'me_gusta',
              'duracion_s', 'frases_por_10s', 'cta', 'gancho', 'descripcion', 'url', 'transcripcion']
    with open(os.path.join(P, 'reels.csv'), 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=campos, extrasaction='ignore'); w.writeheader(); w.writerows(filas)
    with open(os.path.join(P, 'top.md'), 'w') as fh:
        fh.write(f'# Top {a.top} reels ({len(filas)} analizados, {len(por)} cuentas)\n\n')
        for i, f in enumerate(filas[:a.top], 1):
            fh.write(f"## {i}. @{f['cuenta']} · {f['visitas']:,} visitas ({f['x_mediana_visitas']}x su mediana) · {f['comentarios']:,} comentarios\n")
            fh.write(f"{f['url']} · {f['duracion_s']} s · CTA: {f['cta'] or '—'}\n\n**Gancho:** {f['gancho']}\n\n")
            if f['transcripcion']:
                fh.write('```\n' + open(f['transcripcion']).read().strip() + '\n```\n\n')
    print(f"{len(filas)} reels de {len(por)} cuentas → {os.path.join(P, 'reels.csv')} y top.md")
    for f in filas[:5]:
        print(f"  {f['puntos']:>5}  @{f['cuenta']:<20} {f['visitas']:>9,} vis  {f['gancho'][:60]}")

if __name__ == '__main__':
    main()
