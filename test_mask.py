from PIL import Image, ImageFilter, ImageDraw
import math

# Load image
img = Image.open('/home/prem/.gemini/antigravity/scratch/premkumar-portfolio/assets/images/premkumar.jpg').convert('RGB')
w, h = img.size
crop_h = 820
img = img.crop((0, 0, w, crop_h))
w, h = img.size

# We want to create an alpha mask where 255 = Premkumar, 0 = Background
# Let's find for each row y from 0 to h:
# left boundary x_left(y) and right boundary x_right(y)
left_bounds = []
right_bounds = []

for y in range(h):
    if y >= 660:
        # Below y=660, shoulders cover full width
        left_bounds.append(0)
        right_bounds.append(w - 1)
        continue
    
    # 1. Left boundary: scan from left (x=0) to center (x=288)
    # Background is bright wall or plant leaf.
    # Shoulder on left starts at y=560 (x=160) to y=660 (x=0)
    lx = 0
    for x in range(0, 288):
        r, g, b = img.getpixel((x, y))
        br = (r + g + b) / 3
        
        # Check if we hit Premkumar
        # At hair level (y < 280): hair is dark br < 60
        is_hair = (y < 280 and br < 55)
        # At ear/face level (220 <= y <= 480): skin tone
        is_skin = (180 <= y <= 550 and r > 95 and r > b + 25 and r > g + 5 and br < 185)
        # At neck/collar level (450 <= y <= 580): collar or skin
        is_collar = (450 <= y <= 580 and br < 50)
        # At shoulder level (550 <= y < 660): black shirt br < 65
        is_shoulder = (y > 550 and br < 65)
        
        if is_hair or is_skin or is_collar or is_shoulder:
            lx = x
            break
    left_bounds.append(lx)

    # 2. Right boundary: scan from right (x=w-1) to center (x=288)
    rx = w - 1
    if y >= 620:
        right_bounds.append(w - 1)
        continue
        
    for x in range(w - 1, 288, -1):
        r, g, b = img.getpixel((x, y))
        br = (r + g + b) / 3
        
        is_hair = (y < 280 and br < 45)
        is_skin = (180 <= y <= 550 and r > 95 and r > b + 25 and r > g + 5 and br < 185)
        is_collar = (450 <= y <= 580 and br < 50)
        is_shoulder = (y > 550 and br < 65)
        
        if is_hair or is_skin or is_collar or is_shoulder:
            rx = x
            break
    right_bounds.append(rx)

# Smooth the boundaries with a median/moving average filter to remove any single-pixel bumps
window = 11
smooth_left = []
smooth_right = []
for i in range(h):
    start = max(0, i - window // 2)
    end = min(h, i + window // 2 + 1)
    l_win = sorted(left_bounds[start:end])
    r_win = sorted(right_bounds[start:end])
    smooth_left.append(l_win[len(l_win)//2])
    smooth_right.append(r_win[len(r_win)//2])

# Build mask image
mask = Image.new('L', (w, h), 0)
draw = ImageDraw.Draw(mask)

# Create polygon along the silhouette
poly = []
# Top boundary across hair
poly.append((smooth_left[0], 0))
for y in range(0, h):
    poly.append((smooth_right[y], y))
poly.append((w - 1, h - 1))
poly.append((0, h - 1))
for y in range(h - 1, -1, -1):
    poly.append((smooth_left[y], y))

draw.polygon(poly, fill=255)

# Soft feather edge
mask_feathered = mask.filter(ImageFilter.GaussianBlur(1.5))

# Apply alpha to crop
img.putalpha(mask_feathered)
img.save('/home/prem/.gemini/antigravity/scratch/premkumar-portfolio/assets/images/premkumar_cutout_test.png')
print('Cutout saved successfully!')
