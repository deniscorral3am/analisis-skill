---
name: analisis
description: Claude te dice qué reel grabar cada semana. Descarga tus reels y los de tu competencia (Instagram, TikTok o YouTube Shorts) con sus visitas y comentarios, los transcribe en tu ordenador, los desmonta (gancho, estructura, ritmo y llamada a la acción), los ordena comparando cada reel con lo normal de su cuenta, encuentra los patrones que se repiten en los que mejor funcionan y te entrega los guiones de los próximos reels listos para grabar. Úsala cuando digan /analisis, «comenta ANÁLISIS», «qué reel grabo», «analiza a mi competencia», «analiza mis reels», «qué funciona en mi sector» o pasen cuentas de Instagram para analizar.
---

# /analisis: qué reel grabar esta semana

Al terminar, el usuario tiene en `~/Analisis/<proyecto>/` todos los reels descargados y transcritos, `reels.csv`
ordenado, `top.md` con los mejores y `INFORME.md` con los patrones y los guiones de sus próximos reels. Todo el método
y el prompt del análisis están en `DOCUMENTO.md`: léelo entero antes de empezar.

Español de España, cercano y corto. **Una pregunta cada vez.**

## Reglas
- **Nunca pidas la contraseña de Instagram.** Si Instagram pide sesión, se usa `--cookies <navegador>` (la sesión que ya
  tiene abierta en su navegador) y se lo explicas antes.
- Solo contenido público. Los vídeos descargados son para analizar en su ordenador: no se vuelven a publicar.
- **Nunca inventes números.** Todo dato sale de `reels.csv`; si una cifra falta (p. ej. visitas ocultas), dilo.
- Copiar estructuras y patrones sí; copiar el guion palabra por palabra de otro creador no.
- Un proceso pesado cada vez (la transcripción usa mucha memoria).

## El recorrido
### Paso 0. Herramientas
Comprueba `yt-dlp --version`, `python3 -c "import faster_whisper"` y `ffmpeg -version`. Si falta algo:
`brew install yt-dlp ffmpeg` y `pip install faster-whisper`. Espera a que esté.

### Paso 1. Las cuentas (2 preguntas)
1. Su cuenta (o sus cuentas) y de qué va su contenido.
2. Entre 3 y 10 cuentas de su sector que vendan o crezcan (si no sabe cuáles, búscalas con él y que las confirme).
Nombre del proyecto en minúsculas con guiones (p. ej. `agencias-ia`).

### Paso 2. Descargar
`python3 scripts/descargar.py --proyecto ~/Analisis/<proyecto> --max 40 <cuentas…>`. Si falla por sesión, repite con
`--cookies chrome` (o su navegador). Para muchas cuentas, `--max 40` basta: lo que importa es lo reciente.

### Paso 3. Transcribir
`python3 scripts/transcribir.py --proyecto ~/Analisis/<proyecto>` (modelo `small`; `medium` si el audio es malo).

### Paso 4. Ordenar
`python3 scripts/tabla.py --proyecto ~/Analisis/<proyecto> --top 30`. Enséñale los 5 primeros: cuenta, visitas,
cuántas veces su mediana y el gancho.

### Paso 5. Desmontar y encontrar patrones
Lee `top.md` entero y sigue el prompt de análisis de `DOCUMENTO.md`. Cada patrón tiene que salir en **al menos 3
reels del top** y lo citas con su enlace. Separa lo que funciona en su cuenta de lo que funciona en la competencia.

### Paso 6. Qué grabar
Escribe `INFORME.md`: los patrones, lo que NO funciona (los del fondo de la tabla) y **5 reels para grabar** con
gancho (primeros 3 s), estructura por bloques, guion corto en su voz y la llamada a la acción. Pregúntale cuál graba
primero y ajústalo con él.

### Cada semana
Repite los pasos 2 a 6: solo baja lo nuevo y la tabla se rehace sola. Compara con el informe anterior.
