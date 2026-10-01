from PIL import Image, ImageDraw, ImageFilter, ImageChops
import math

# Load clean cutout
person = Image.open('/home/prem/.gemini/antigravity/scratch/premkumar-portfolio/assets/images/premkumar_cutout_v3.png')
pw, ph = person.size

# High-resolution canvas matching Ali Abdaal graphic template
cw, ch = 800, 850
canvas = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))

circle_cx = 400
circle_cy = 490
circle_r = 245
yellow_color = (253, 200, 68, 255) # #FDC844

# 1. Warm drop shadow behind yellow circle
shadow = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
draw_s = ImageDraw.Draw(shadow)
draw_s.ellipse([circle_cx - circle_r - 6, circle_cy - circle_r + 16, 
                circle_cx + circle_r + 6, circle_cy + circle_r + 28], 
               fill=(180, 140, 75, 45))
shadow = shadow.filter(ImageFilter.GaussianBlur(22))
canvas = Image.alpha_composite(canvas, shadow)

# 2. Draw yellow circle
draw = ImageDraw.Draw(canvas)
draw.ellipse([circle_cx - circle_r, circle_cy - circle_r, 
              circle_cx + circle_r, circle_cy + circle_r], fill=yellow_color)

# 3. Speech bubble pointer on right side
pointer_pts = [
    (circle_cx + circle_r - 18, circle_cy - 42),
    (circle_cx + circle_r + 85, circle_cy - 10),
    (circle_cx + circle_r - 12, circle_cy + 42)
]
draw.polygon(pointer_pts, fill=yellow_color)

# 4. Decorative yellow arc on left
arc_bbox = [circle_cx - circle_r - 42, circle_cy - circle_r - 35, 
            circle_cx + circle_r + 42, circle_cy + circle_r + 45]
draw.arc(arc_bbox, start=145, end=255, fill=(253, 200, 68, 230), width=6)
dot_x = circle_cx - circle_r - 28
dot_y = circle_cy - circle_r + 85
draw.ellipse([dot_x - 7, dot_y - 7, dot_x + 7, dot_y + 7], fill=(253, 200, 68, 255))

# 5. Scale person cutout properly so full shoulders and chest are visible
target_w = 480
scale = target_w / float(pw)
target_h = int(ph * scale)
person_scaled = person.resize((target_w, target_h), Image.Resampling.LANCZOS)

# Position: center horizontally, head top pops out 100px above circle top (245)
person_x = circle_cx - target_w // 2
# In cutout v3, top of hair is at y=72 in 860px image. 72 * scale = 72 * 0.833 = 60px.
# We want hair top at canvas y = 145.
person_y = int(145 - 60) # 85px

# 6. Smooth circular bottom mask for the chest
# In Ali Abdaal's reference, the bottom curves along the yellow circle
bottom_mask = Image.new('L', (target_w, target_h), 255)
for py in range(target_h):
    wy = person_y + py
    # only clip below circle center + 100
    if wy > circle_cy + 100:
        for px in range(target_w):
            wx = person_x + px
            dist = math.hypot(wx - circle_cx, wy - circle_cy)
            if dist > circle_r:
                if dist < circle_r + 3:
                    bottom_mask.putpixel((px, py), int(255 * (1.0 - (dist - circle_r) / 3.0)))
                else:
                    bottom_mask.putpixel((px, py), 0)

p_r, p_g, p_b, p_a = person_scaled.split()
person_scaled.putalpha(ImageChops.multiply(p_a, bottom_mask))

# Paste person on top of yellow circle
canvas.paste(person_scaled, (person_x, person_y), person_scaled)

out_file = '/home/prem/.gemini/antigravity/scratch/premkumar-portfolio/assets/images/premkumar-halfbody-editorial.png'
canvas.save(out_file, 'PNG', optimize=True)
print('Halfbody graphic v4 created successfully!')
