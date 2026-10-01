from PIL import Image, ImageDraw, ImageFilter

src = Image.open('/home/prem/.gemini/antigravity/scratch/premkumar-portfolio/assets/images/premkumar.jpg').convert('RGB')
w, h = src.size
crop_h = 860
src_crop = src.crop((0, 0, w, crop_h))

mask = Image.new('L', (w, crop_h), 0)
draw = ImageDraw.Draw(mask)

# Left boundary points (preserving 100% of left ear and hair, removing background wall)
pts_left = [
    (135, 120), # top-left hair
    (110, 155), # hair side
    (96, 195),  # hair side
    (94, 240),  # hair side
    (100, 285), # above left ear
    (100, 325), # left ear top
    (92, 355),  # left ear tip
    (108, 385), # left earlobe
    (135, 420), # left jaw
    (170, 465), # left neck
    (185, 510), # left collar top
    (165, 550), # left collar base
    (125, 580), # left shoulder start
    (65, 610),  # left shoulder slope
    (0, 640),   # left shoulder hits edge
    (0, crop_h - 1) # bottom left
]

# Right boundary points (preserving 100% of right ear and hair, removing background window)
pts_right = [
    (375, 120), # top-right hair
    (405, 155), # hair side
    (416, 195), # hair side
    (416, 240), # hair side
    (406, 285), # above right ear
    (412, 325), # right ear top
    (432, 355), # right ear tip
    (418, 385), # right earlobe
    (395, 420), # right jaw
    (372, 465), # right neck
    (370, 510), # right collar top
    (392, 550), # right collar base
    (440, 580), # right shoulder start
    (515, 610), # right shoulder slope
    (w - 1, 640), # right shoulder hits edge
    (w - 1, crop_h - 1) # bottom right
]

# Crown of hair
top_hair = []
for x in range(135, 376, 5):
    # Arc peaking at x=250, y=70
    norm_x = (x - 250) / 120.0
    y = 70 + 50 * (norm_x ** 2)
    top_hair.append((x, int(y)))

poly = []
poly.extend(top_hair)
poly.extend(pts_right)
poly.append((w - 1, crop_h - 1))
poly.append((0, crop_h - 1))
poly.extend(reversed(pts_left))

draw.polygon(poly, fill=255)

mask_smooth = mask.filter(ImageFilter.GaussianBlur(1.6))

cutout = src_crop.copy()
cutout.putalpha(mask_smooth)
cutout.save('/home/prem/.gemini/antigravity/scratch/premkumar-portfolio/assets/images/premkumar_cutout_clean_v4.png')
print('Clean cutout v4 saved!')
