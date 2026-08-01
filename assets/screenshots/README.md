# App screenshots

Five real device screenshots plus one screen recording, all 1080 × 2400, shown
on the homepage inside a CSS device frame. Nothing is cropped, tinted or
rotated — the frame only adds a bezel and rounds the corners.

| File | Screen | Feature |
|---|---|---|
| `video-alarm.mp4` | Screen recording — a video alarm ringing at 5:49 PM over a playing clip | 01 Wake up to a video |
| `shuffle` | Shuffle playlist — four entries, Random, videos' sound | 02 Shuffle playlists |
| `wake-me-with` | Edit alarm → "Wake me with" sheet, Sound tab | 03 Five tones |
| `alarms` | Alarms list — Next alarm card and three rows | 04 Alarms that fit the day |
| `world-clock` | Clock tab — local time, Tokyo, London, Bermuda | 05 World clock |
| `timer` | Timer — 03:38 of 05:00, Cancel / +1:00 / Pause | 06 Timer and stopwatch |

The five stills each exist twice: a `.webp` that every current browser gets and
a `.png` fallback served to anything that cannot decode WebP. The markup is a
`<picture>`, so the browser picks.

## The video

`video-alarm.mp4` is encoded from `alarm.gif`, a 104 MB screen recording that is
**deliberately not committed** — it is over GitHub's 100 MB per-file limit and
`.gitignore` excludes `assets/screenshots/*.gif`. Keep the master somewhere
outside the repo.

- 630 × 1400, twice the 318 px box it is displayed in
- H.264 Main / yuv420p, which every browser that ships `<video>` can decode
- **No audio track at all**, so autoplay is never blocked and `muted` is honest
- 320 KB, down from 104 MB

`video-alarm-poster.jpg` is frame 90, shown before playback starts and left in
place for visitors who ask for reduced motion.

To re-encode after replacing the recording:

```sh
ffmpeg -i alarm.gif -vf scale=630:1400:flags=lanczos \
  -c:v libx264 -crf 28 -preset veryslow -profile:v main -level 4.0 \
  -pix_fmt yuv420p -an -movflags +faststart video-alarm.mp4
ffmpeg -i alarm.gif -vf "scale=630:1400:flags=lanczos,select=eq(n\,90)" \
  -vframes 1 -q:v 6 video-alarm-poster.jpg
```

## Replacing a still

Drop in the new PNG, then regenerate its WebP:

```python
from PIL import Image
Image.open('alarms.png').convert('RGB').save('alarms.webp', 'WEBP', quality=88, method=6)
```

Keep the filename and the 9:20 aspect ratio. The `width`/`height` attributes in
`index.html` are set to 1080 × 2400 so the page reserves the right space before
the image loads — if a screenshot is ever a different size, change those too.
