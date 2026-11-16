#!/usr/bin/env python3
"""Descarga los reels de varias cuentas (tuyas y de tu competencia) con sus números.

Uso:
  python3 descargar.py --proyecto ~/Analisis/mi-sector --max 40 cuenta1 cuenta2 https://www.instagram.com/reel/XXXX/
  (añade --cookies chrome si Instagram pide iniciar sesión: usa la sesión de TU navegador, nunca tu contraseña)

Deja en <proyecto>/reels/<cuenta>/ el vídeo (.mp4) y su ficha (.info.json con visitas, me gusta, comentarios,
descripción, duración y fecha). No borra nada que ya exista: si lo vuelves a lanzar, solo baja lo nuevo.
"""
import argparse, os, shutil, subprocess, sys

def url_de(x):
    if x.startswith('http'):
        return x
    x = x.lstrip('@').strip('/')
    return f'https://www.instagram.com/{x}/reels/'

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('fuentes', nargs='+', help='cuentas (@usuario o usuario) o enlaces de reels/perfiles (Instagram, TikTok, YouTube Shorts)')
    ap.add_argument('--proyecto', required=True, help='carpeta del análisis, p. ej. ~/Analisis/mi-sector')
    ap.add_argument('--max', type=int, default=40, help='máximo de reels por cuenta (por defecto 40)')
    ap.add_argument('--cookies', default='', help='navegador del que leer tu sesión si hace falta: chrome, safari, firefox, edge…')
    ap.add_argument('--solo-datos', action='store_true', help='no baja vídeos, solo los números y la descripción')
    a = ap.parse_args()
    if not shutil.which('yt-dlp'):
        sys.exit('Falta yt-dlp. Instálalo con:  brew install yt-dlp   (o  pip install -U yt-dlp)')
    base = os.path.join(os.path.expanduser(a.proyecto), 'reels'); os.makedirs(base, exist_ok=True)
    fallos = []
    for f in a.fuentes:
        u = url_de(f)
        cuenta = f.lstrip('@').strip('/').split('/')[-1] if not f.startswith('http') else '%(uploader_id,channel_id,uploader)s'
        cmd = ['yt-dlp', '--ignore-errors', '--no-overwrites', '--write-info-json', '--no-write-playlist-metafiles',
               '--playlist-end', str(a.max), '-f', 'mp4/best[height<=1280]/best', '--download-archive', os.path.join(base, '.descargados.txt'),
               '-o', os.path.join(base, cuenta, '%(upload_date)s_%(id)s.%(ext)s')]
        if a.cookies:
            cmd += ['--cookies-from-browser', a.cookies]
        if a.solo_datos:
            cmd += ['--skip-download']
        print(f'→ {u}', flush=True)
        r = subprocess.run(cmd + [u])
        if r.returncode:
            fallos.append(f)
    n = sum(1 for _, _, fs in os.walk(base) for x in fs if x.endswith('.info.json'))
    print(f'\nListo: {n} reels con ficha en {base}')
    if fallos:
        print('No se pudo con: ' + ', '.join(fallos) + '\n  Si Instagram pide sesión, repite con  --cookies chrome  (o el navegador donde tengas Instagram abierto).')

if __name__ == '__main__':
    main()
