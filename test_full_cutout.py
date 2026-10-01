from PIL import Image, ImageDraw, ImageFilter

src = Image.open('/home/prem/.gemini/antigravity/scratch/premkumar-portfolio/assets/images/premkumar.jpg').convert('RGB')
w, h = src.size
crop_h = 860
src_crop = src.crop((0, 0, w, crop_h))

mask = Image.new('L', (w, crop_h), 0)
draw = ImageDraw.Draw(mask)

# Left boundary points (from top of hair down to bottom-left corner)
pts_left = [
    (110, 110), # hair start top-left
    (80, 140),  # hair edge
    (70, 180),  # hair edge
    (68, 230),  # hair edge
    (72, 280),  # hair above ear
    (78, 320),  # left ear upper
    (85, 350),  # left ear tip
    (100, 380), # left earlobe
    (125, 420), # left jaw
    (155, 460), # left neck
    (170, 510), # left collar top
    (155, 550), # left collar
    (110, 580), # left shoulder start
    (55, 610),  # left shoulder slope
    (0, 640),   # left shoulder hits edge
    (0, crop_h - 1) # bottom left
]

# Right boundary points (from top of hair down to bottom-right corner)
pts_right = [
    (390, 110), # hair start top-right
    (425, 140), # hair edge
    (438, 180), # hair edge
    (440, 230), # hair edge
    (438, 280), # hair above ear
    (445, 320), # right ear upper
    (450, 350), # right ear tip
    (440, 380), # right earlobe
    (410, 420), # right jaw
    (380, 460), # right neck
    (375, 510), # right collar top
    (395, 550), # right collar
    (445, 580), # right shoulder start
    (515, 610), # right shoulder slope
    (w - 1, 640), # right shoulder hits edge
    (w - 1, crop_h - 1) # bottom right
]

# Top crown of hair
top_hair = []
for x in range(110, 391, 5):
    # Smooth crown arc peaking at x=250, y=55
    norm_x = (x - 250) / 140.0
    y = 55 + 55 * (norm_x ** 2)
    top_hair.append((x, int(y)))

poly = []
poly.extend(top_hair)
poly.extend(pts_right)
poly.append((w - 1, crop_h - 1))
poly.append((0, crop_h - 1))
poly.extend(reversed(pts_left))

draw.polygon(poly, fill=255)

# Soft natural feather
mask_smooth = mask.filter(ImageFilter.GaussianBlur(1.8))

cutout = src_crop.copy()
cutout.putalpha(mask_smooth)
cutout.save('/home/prem/.gemini/antigravity/scratch/premkumar-portfolio/assets/images/premkumar_cutout_full.png')
print('Full face cutout created successfully!')
