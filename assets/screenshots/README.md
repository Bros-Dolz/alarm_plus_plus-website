# App screenshots

Six real device screenshots, 1080 × 2400, shown on the homepage inside a CSS
device frame. Nothing is cropped, tinted or rotated — the frame only adds a
bezel and rounds the corners.

| File | Screen | Feature |
|---|---|---|
| `ringing` | Ring screen — 4:10 PM, Dentist, Snooze 10 min, Dismiss | 01 Wake up to a video |
| `shuffle` | Shuffle playlist — four entries, Random, videos' sound | 02 Shuffle playlists |
| `wake-me-with` | Edit alarm → "Wake me with" sheet, Sound tab | 03 Five tones |
| `alarms` | Alarms list — Next alarm card and three rows | 04 Alarms that fit the day |
| `world-clock` | Clock tab — local time, Tokyo, London, Bermuda | 05 World clock |
| `timer` | Timer — 03:38 of 05:00, Cancel / +1:00 / Pause | 06 Timer and stopwatch |

Each exists twice: a `.webp` that every current browser gets (273 KB for all
six) and a `.png` fallback served to anything that cannot decode WebP. The
markup is a `<picture>`, so the browser picks.

## Replacing one

Drop in the new PNG, then regenerate its WebP:

```python
from PIL import Image
Image.open('alarms.png').convert('RGB').save('alarms.webp', 'WEBP', quality=88, method=6)
```

Keep the filename and the 9:20 aspect ratio. The `width`/`height` attributes in
`index.html` are set to 1080 × 2400 so the page reserves the right space before
the image loads — if a screenshot is ever a different size, change those too.
