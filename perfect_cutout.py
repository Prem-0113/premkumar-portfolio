from PIL import Image, ImageDraw, ImageFilter
import math

src = Image.open('/home/prem/.gemini/antigravity/scratch/premkumar-portfolio/assets/images/premkumar.jpg').convert('RGB')
w, h = src.size

crop_h = 860
src_crop = src.crop((0, 0, w, crop_h))

# Create mask
mask = Image.new('L', (w, crop_h), 0)
draw = ImageDraw.Draw(mask)

# Define precise contour points along Premkumar's actual silhouette:
# Left side points (going down)
pts_left = [
    (140, 130), # top-left hair
    (110, 160), # hair slope
    (88, 200),  # hair side
    (80, 240),  # temple
    (78, 280),  # above ear
    (76, 330),  # left ear top
    (80, 360),  # left ear tip
    (96, 390),  # ear bottom / jaw
    (116, 420), # jawline
    (146, 450), # neck
    (162, 480), # neck
    (168, 520), # collar top
    (165, 555), # collar base
    (135, 580), # shoulder start
    (90, 605),  # shoulder curve
    (40, 625),  # shoulder slope
    (0, 645),   # shoulder hits left border
    (0, crop_h - 1) # bottom left corner
]

# Right side points (going down from top right of hair)
pts_right = [
    (390, 130), # top-right hair
    (410, 160), # hair slope
    (424, 200), # hair side
    (425, 240), # temple
    (422, 280), # above right ear
    (426, 320), # right ear top
    (436, 360), # right ear tip
    (430, 385), # right earlobe
    (412, 415), # jawline
    (388, 445), # neck
    (384, 480), # neck
    (386, 520), # collar top
    (394, 550), # collar base
    (430, 570), # shoulder start
    (485, 595), # shoulder curve
    (535, 615), # shoulder slope
    (w - 1, 630), # shoulder hits right border
    (w - 1, crop_h - 1) # bottom right corner
]

# Top curve of hair (smooth arc from left hair to right hair)
top_hair = []
for x in range(140, 391, 5):
    # Parabolic crown curve with peak at x=265, y=60
    norm_x = (x - 265) / 125.0
    y = 60 + 70 * (norm_x ** 2)
    top_hair.append((x, int(y)))

# Construct complete polygon:
# top hair from left to right -> pts_right down -> bottom edge -> pts_left up
poly = []
poly.extend(top_hair)
poly.extend(pts_right)
poly.append((w - 1, crop_h - 1))
poly.append((0, crop_h - 1))
poly.extend(reversed(pts_left))

draw.polygon(poly, fill=255)

# Smooth edges with subtle Gaussian blur for natural photographic edge
mask_smooth = mask.filter(ImageFilter.GaussianBlur(1.2))

# Apply alpha
cutout = src_crop.copy()
cutout.putalpha(mask_smooth)
cutout.save('/home/prem/.gemini/antigravity/scratch/premkumar-portfolio/assets/images/premkumar_cutout_perfect.png')
print('Perfect cutout created!')
