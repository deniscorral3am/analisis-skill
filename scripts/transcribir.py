#!/usr/bin/env python3
"""Transcribe todos los reels de un proyecto con faster-whisper (en tu ordenador, gratis).

Uso:  python3 transcribir.py --proyecto ~/Analisis/mi-sector [--modelo small] [--idioma es]

Por cada vídeo deja al lado un .txt con la transcripción y los tiempos de cada frase. Salta los que ya tienen .txt.
Usa un solo proceso para no saturar el ordenador.
"""
import argparse, glob, os, sys

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--proyecto', required=True)
    ap.add_argument('--modelo', default='small', help='tiny, base, small (por defecto), medium… más grande = mejor y más lento')
    ap.add_argument('--idioma', default='es')
    a = ap.parse_args()
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit('Falta faster-whisper. Instálalo con:  pip install faster-whisper')
    vids = sorted(glob.glob(os.path.join(os.path.expanduser(a.proyecto), 'reels', '**', '*.mp4'), recursive=True))
    pend = [v for v in vids if not os.path.exists(v[:-4] + '.txt')]
    print(f'{len(vids)} vídeos, {len(pend)} por transcribir')
    if not pend:
        return
    m = WhisperModel(a.modelo, device='cpu', compute_type='int8')
    for i, v in enumerate(pend, 1):
        try:
            segs, _ = m.transcribe(v, language=a.idioma, vad_filter=True)
            lin = [f'[{s.start:6.2f}] {s.text.strip()}' for s in segs]
            open(v[:-4] + '.txt', 'w').write('\n'.join(lin) + '\n')
            print(f'{i}/{len(pend)} ✓ {os.path.basename(v)}', flush=True)
        except Exception as e:
            print(f'{i}/{len(pend)} ✗ {os.path.basename(v)}: {e}', flush=True)

if __name__ == '__main__':
    main()
