from PIL import Image, ImageDraw, ImageFilter

src = Image.open('/home/prem/.gemini/antigravity/scratch/premkumar-portfolio/assets/images/premkumar.jpg').convert('RGB')
w, h = src.size

crop_h = 860
src_crop = src.crop((0, 0, w, crop_h))

mask = Image.new('L', (w, crop_h), 0)
draw = ImageDraw.Draw(mask)

# Left side points (going down)
pts_left = [
    (195, 95),
    (170, 130),
    (155, 170),
    (155, 210),
    (158, 250),
    (162, 290),
    (166, 330),
    (168, 360), # left ear tip
    (185, 405), # jaw
    (205, 455), # neck
    (212, 505), # neck/collar top
    (192, 560), # collar base
    (150, 590), # shoulder start
    (95, 620),  # shoulder
    (40, 645),  # shoulder
    (0, 665),   # shoulder to edge
    (0, crop_h - 1)
]

# Right side points (going down)
pts_right = [
    (355, 95),
    (385, 130),
    (400, 170),
    (405, 210),
    (400, 250),
    (396, 290),
    (402, 330),
    (406, 360), # right ear tip
    (392, 405), # jaw
    (365, 455), # neck
    (368, 505), # neck/collar top
    (386, 560), # collar base
    (428, 590), # shoulder start
    (485, 620), # shoulder
    (540, 645), # shoulder
    (w - 1, 665), # shoulder to edge
    (w - 1, crop_h - 1)
]

# Crown of hair - clean arc matching his actual hairline
top_hair = []
for x in range(195, 356, 5):
    # Arc with peak at x=275, y=72
    norm_x = (x - 275) / 80.0
    y = 72 + 24 * (norm_x ** 2)
    top_hair.append((x, int(y)))

poly = []
poly.extend(top_hair)
poly.extend(pts_right)
poly.append((w - 1, crop_h - 1))
poly.append((0, crop_h - 1))
poly.extend(reversed(pts_left))

draw.polygon(poly, fill=255)

# Soft feathering
mask_smooth = mask.filter(ImageFilter.GaussianBlur(1.8))

cutout = src_crop.copy()
cutout.putalpha(mask_smooth)
cutout.save('/home/prem/.gemini/antigravity/scratch/premkumar-portfolio/assets/images/premkumar_cutout_v3.png')
print('Cutout v3 created!')
