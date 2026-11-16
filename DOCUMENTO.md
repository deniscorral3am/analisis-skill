# El análisis: qué reel grabar cada semana

Así decidimos qué grabar: le pasamos a Claude nuestros reels y los de las cuentas que más venden del sector, los
descarga, los transcribe y los desmonta. Gancho, estructura y llamada a la acción de cada uno, ordenados por visitas y
comentarios. Lo que se repite entre los mejores es lo que grabamos.

## Lo que necesitas
- Claude Code con tu cuenta de Claude.
- `yt-dlp`, `ffmpeg` y Python 3 con `faster-whisper` (se instalan en 2 minutos; la skill te dice cómo).
- Tus cuentas y entre 3 y 10 de tu competencia.

## Cómo funciona
| Paso | Qué hace | Archivo |
|---|---|---|
| 1. Descargar | Baja los reels con visitas, me gusta, comentarios, descripción y fecha | `scripts/descargar.py` |
| 2. Transcribir | Transcribe cada vídeo en tu ordenador, con el tiempo de cada frase | `scripts/transcribir.py` |
| 3. Ordenar | Compara cada reel con la mediana de su cuenta y saca gancho, CTA y ritmo | `scripts/tabla.py` |
| 4. Desmontar | Claude lee los mejores y encuentra los patrones | el prompt de abajo |
| 5. Grabar | 5 guiones con gancho, estructura y CTA | `INFORME.md` |

### Por qué «x veces su mediana» y no solo visitas
Una cuenta de 500.000 seguidores siempre tendrá más visitas. Lo que te interesa es qué reel le funcionó **mejor de lo
normal a cada cuenta**. Por eso cada reel se mide contra la mediana de su propia cuenta (visitas 60 %, comentarios
40 %). Los comentarios pesan porque son los que piden el recurso: son los que venden.

## El prompt del análisis
```text
Lee top.md (los mejores reels con su transcripción) y reels.csv. Para cada reel del top desmonta:
1) el gancho (primeros 3 s): tipo (pregunta, cifra, contradicción, demostración, «esto es lo que…»), palabras exactas;
2) la estructura por bloques con sus segundos (gancho → problema → demostración → prueba → CTA, o la que sea);
3) el ritmo (frases por 10 s, duración) y el formato (a cámara, dúo, pantalla, b-roll);
4) la llamada a la acción (palabra, qué promete).
Después dame los PATRONES: solo los que se repiten en al menos 3 reels del top, cada uno con los enlaces que lo
prueban, separando mi cuenta de la competencia. Dime también qué tienen en común los del fondo de la tabla.
Con eso escribe 5 reels para grabar esta semana en mi voz: gancho, bloques con segundos, guion corto y CTA.
No inventes cifras: todo número sale de reels.csv.
```

## Lo que no hace
- No publica nada ni comenta en ninguna cuenta.
- No te pide tu contraseña: si Instagram pide sesión, usa la de tu navegador (`--cookies chrome`).
- No vuelve a subir vídeos de otros: los descarga solo para analizarlos.
