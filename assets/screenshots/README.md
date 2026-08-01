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
- 316 KB, down from 104 MB

`video-alarm-poster.jpg` is frame 90, shown before playback starts and left in
place for visitors who ask for reduced motion.

### The CapCut watermark

The recording carried a CapCut export watermark at x907–1079, y41–93, which is
painted out before encoding. It overlapped rows 41–47 of the phone's own status
icons (x892–1011, y14–47), so the two had to be separated rather than boxed out.

Brightness does it exactly: over the temporal mean the watermark never exceeds
luminance 150 (p99 = 143) while the icons are above 205, with only 90
anti-aliased pixels in between. Both are static, so the icon mask is computed
once from the mean and reused for every frame, which makes it immune to the
GIF's per-frame dithering.

The fill is real wall texture copied from 220 px to the left, not a synthetic
colour — behind the watermark is the ring screen's dimming scrim over a blank
wall, flat to within ~1/255 from x660 to x899, and the source strip matches the
destination to within 2/255 per channel. A flat fill visibly lacked the dither
grain; copying keeps it. Verified afterwards on the encoded output: the cleared
zone matches neighbouring clean wall to within 0.4/255 mean, and zero icon
pixels were lost across 50 sampled frames.

### Re-encoding after replacing the recording

If the new capture has no watermark, drop `patch()` and pipe the GIF straight
in. Otherwise re-measure the two rectangles first — they are specific to this
recording.

```python
# patch.py — see the constants above; Y0,Y1,X0,X1 = 38,98,900,1080; DX = 220
import sys, numpy as np
from PIL import Image
im = Image.open('alarm.gif')
frames = []
for i in range(0, 250, 5):
    im.seek(i); frames.append(np.asarray(im.convert('RGB')))
keep = icon_mask(frames)          # lum > 175 over the temporal mean, grown 1px
im.seek(0)
while True:
    sys.stdout.buffer.write(patch(np.asarray(im.convert('RGB')), keep).tobytes())
    try: im.seek(im.tell() + 1)
    except EOFError: break
```

```sh
python3 patch.py | ffmpeg -f rawvideo -pix_fmt rgb24 -s 1080x2400 -r 25 -i - \
  -vf scale=630:1400:flags=lanczos \
  -c:v libx264 -crf 28 -preset veryslow -profile:v main -level 4.0 \
  -pix_fmt yuv420p -an -movflags +faststart video-alarm.mp4
ffmpeg -i video-alarm.mp4 -vf "select=eq(n\,90)" -vframes 1 -q:v 6 video-alarm-poster.jpg
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
