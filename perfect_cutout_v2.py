from PIL import Image, ImageDraw, ImageFilter

src = Image.open('/home/prem/.gemini/antigravity/scratch/premkumar-portfolio/assets/images/premkumar.jpg').convert('RGB')
w, h = src.size

crop_h = 860
src_crop = src.crop((0, 0, w, crop_h))

mask = Image.new('L', (w, crop_h), 0)
draw = ImageDraw.Draw(mask)

# Left side points (going down)
pts_left = [
    (200, 80),
    (170, 115),
    (152, 155),
    (145, 195),
    (148, 235),
    (152, 275),
    (155, 315),
    (157, 360), # left ear tip
    (175, 410), # jaw
    (198, 460), # neck
    (206, 510), # neck/collar top
    (192, 560), # collar base
    (150, 590), # shoulder start
    (95, 620),  # shoulder
    (40, 645),  # shoulder
    (0, 665),   # shoulder to edge
    (0, crop_h - 1)
]

# Right side points (going down)
pts_right = [
    (370, 80),
    (400, 115),
    (418, 155),
    (425, 195),
    (422, 235),
    (420, 275),
    (420, 315),
    (430, 360), # right ear tip
    (410, 410), # jaw
    (378, 460), # neck
    (372, 510), # neck/collar top
    (386, 560), # collar base
    (428, 590), # shoulder start
    (485, 620), # shoulder
    (540, 645), # shoulder
    (w - 1, 665), # shoulder to edge
    (w - 1, crop_h - 1)
]

# Crown of hair
top_hair = []
for x in range(200, 371, 5):
    # Arc with peak at x=285, y=45
    norm_x = (x - 285) / 85.0
    y = 45 + 35 * (norm_x ** 2)
    top_hair.append((x, int(y)))

poly = []
poly.extend(top_hair)
poly.extend(pts_right)
poly.append((w - 1, crop_h - 1))
poly.append((0, crop_h - 1))
poly.extend(reversed(pts_left))

draw.polygon(poly, fill=255)

# Soft feathering
mask_smooth = mask.filter(ImageFilter.GaussianBlur(1.5))

cutout = src_crop.copy()
cutout.putalpha(mask_smooth)
cutout.save('/home/prem/.gemini/antigravity/scratch/premkumar-portfolio/assets/images/premkumar_cutout_v2.png')
print('Cutout v2 created!')
