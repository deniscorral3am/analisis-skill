# /analisis: qué reel grabar cada semana

La skill de Claude Code que descarga tus reels y los de tu competencia, los transcribe, los desmonta (gancho,
estructura y llamada a la acción), los ordena por visitas y comentarios y te dice qué grabar.

| Parte | Qué tienes |
|---|---|
| `scripts/descargar.py` | Baja los reels con sus números (yt-dlp) |
| `scripts/transcribir.py` | Transcripción en tu ordenador (faster-whisper) |
| `scripts/tabla.py` | Ranking contra la mediana de cada cuenta, gancho, CTA y ritmo |
| `DOCUMENTO.md` | El método y el prompt del análisis |

Hecho por Denís Corral · [@deniscorralvillarraso](https://instagram.com/deniscorralvillarraso) · [Sell Your AI](https://sellyourai.io).

## Cómo usarlo
```bash
git clone https://github.com/deniscorral3am/analisis-skill ~/.claude/skills/analisis
```
Abre Claude Code y escribe `/analisis`. Necesitas `yt-dlp`, `ffmpeg` y `pip install faster-whisper`.

## Licencia
MIT
