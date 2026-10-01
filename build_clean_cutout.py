from PIL import Image, ImageDraw, ImageFilter
import math

src = Image.open('/home/prem/.gemini/antigravity/scratch/premkumar-portfolio/assets/images/premkumar.jpg').convert('RGB')
w, h = src.size
gray = src.convert('L')

crop_h = 860
src_crop = src.crop((0, 0, w, crop_h))
gray_crop = gray.crop((0, 0, w, crop_h))

# Find left boundary for each y
left_pts = []
for y in range(crop_h):
    if y >= 640:
        left_pts.append(0)
        continue
    if y > 560:
        # Left shoulder sloping from x=165 at y=560 to x=0 at y=640
        # Line equation: x = 165 - (y - 560) * (165 / 80)
        expected_x = int(165 - (y - 560) * (165.0 / 80.0))
        # Search around expected_x +- 20
        best_x = expected_x
        max_d = 0
        for x in range(max(0, expected_x - 25), min(w//2, expected_x + 25)):
            d = gray_crop.getpixel((x - 3, y)) - gray_crop.getpixel((x + 3, y))
            if d > max_d:
                max_d = d
                best_x = x
        left_pts.append(best_x)
        continue
    
    # y <= 560: head, ear, jaw, neck
    # Expected search window: 60 <= x <= 220
    best_x = 90
    max_d = 0
    for x in range(40, 220):
        # difference between wall (bright) and subject (dark)
        d = gray_crop.getpixel((x - 4, y)) - gray_crop.getpixel((x + 4, y))
        if d > max_d:
            max_d = d
            best_x = x
    left_pts.append(best_x)

# Find right boundary for each y
right_pts = []
for y in range(crop_h):
    if y >= 630:
        right_pts.append(w - 1)
        continue
    if y > 540:
        # Right shoulder sloping from x=385 at y=540 to x=575 at y=630
        expected_x = int(385 + (y - 540) * ((575.0 - 385.0) / 90.0))
        best_x = expected_x
        max_d = 0
        for x in range(max(300, expected_x - 30), min(w - 4, expected_x + 30)):
            # wall/window is right, subject is left -> p(x+3) - p(x-3) > 0
            d = gray_crop.getpixel((x + 3, y)) - gray_crop.getpixel((x - 3, y))
            if d > max_d:
                max_d = d
                best_x = x
        right_pts.append(best_x)
        continue
    
    # y <= 540: head, ear, jaw, neck
    # Search window: 360 <= x <= 450
    best_x = 410
    max_d = 0
    for x in range(360, min(w - 4, 450)):
        d = gray_crop.getpixel((x + 3, y)) - gray_crop.getpixel((x - 3, y))
        if d > max_d:
            max_d = d
            best_x = x
    right_pts.append(best_x)

# Smooth both boundaries with 15-point median filter
smooth_l = []
smooth_r = []
k = 15
for i in range(crop_h):
    s = max(0, i - k//2)
    e = min(crop_h, i + k//2 + 1)
    wl = sorted(left_pts[s:e])
    wr = sorted(right_pts[s:e])
    smooth_l.append(wl[len(wl)//2])
    smooth_r.append(wr[len(wr)//2])

# Build mask
mask = Image.new('L', (w, crop_h), 0)
draw = ImageDraw.Draw(mask)

poly = []
poly.append((smooth_l[0], 0))
for y in range(crop_h):
    poly.append((smooth_r[y], y))
poly.append((w - 1, crop_h - 1))
poly.append((0, crop_h - 1))
for y in range(crop_h - 1, -1, -1):
    poly.append((smooth_l[y], y))

draw.polygon(poly, fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(1.5))

cutout = src_crop.copy()
cutout.putalpha(mask)
cutout.save('/home/prem/.gemini/antigravity/scratch/premkumar-portfolio/assets/images/premkumar_cutout_clean.png')
print('Clean cutout saved!')
