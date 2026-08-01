"""Remove the CapCut watermark from the video-alarm recording.

The watermark is a static translucent grey mark at x907..1079, y41..93 of the
1080x2400 source. The phone's own status icons sit at x892..1011, y14..47 and
must survive; the two overlap in rows 41..47.

Brightness separates them exactly. Measured over the temporal mean of the
recording, the watermark never exceeds luminance 150 (p99 = 143) while the
icons are above 205 for 1806 pixels, with only 90 anti-aliased pixels in
between. Both are static, so the icon mask is computed once from the mean and
reused for every frame, which makes it immune to the GIF's per-frame dithering.

The fill is real wall texture copied from DX pixels to the left rather than a
synthetic colour. Behind the watermark is the ring screen's dimming scrim over
a blank wall, flat to within ~1/255 from x660 to x899, and the source strip
matches the destination surround to within 2/255 per channel. Copying keeps the
dither grain that a flat fill visibly lacks.
"""
import numpy as np

Y0, Y1, X0, X1 = 38, 98, 900, 1080
DX = 220          # how far left to copy clean wall from
FEATHER = 7       # soften the left seam
ICON = 175        # between the watermark's 150 ceiling and the icons' 205 floor


def icon_mask(frames):
    """Pixels inside the region that belong to the status icons, not the mark."""
    mean = np.mean([f[Y0:Y1, X0:X1].astype(np.float32) for f in frames], axis=0)
    m = mean.mean(axis=2) > ICON
    g = m.copy()   # grow one pixel, to keep anti-aliased icon edges
    g[1:, :] |= m[:-1, :]; g[:-1, :] |= m[1:, :]
    g[:, 1:] |= m[:, :-1]; g[:, :-1] |= m[:, 1:]
    return g


def patch(a, keep):
    out = a.copy()
    orig = a[Y0:Y1, X0:X1]
    src = a[Y0:Y1, X0-DX:X1-DX]
    w = np.ones((1, X1-X0, 1), np.float32)
    w[0, :FEATHER, 0] = np.linspace(0.0, 1.0, FEATHER)
    new = (orig * (1-w) + src * w).round().astype(np.uint8)
    new[keep] = orig[keep]
    out[Y0:Y1, X0:X1] = new
    return out
