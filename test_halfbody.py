from PIL import Image, ImageDraw, ImageFilter
import math

# Load clean cutout
person = Image.open('/home/prem/.gemini/antigravity/scratch/premkumar-portfolio/assets/images/premkumar_cutout_v3.png')
pw, ph = person.size

# High-resolution canvas matching Ali Abdaal graphic template
cw, ch = 800, 850
canvas = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))

circle_cx = 400
circle_cy = 490
circle_r = 250
yellow_color = (253, 200, 68, 255) # #FDC844

# 1. Warm drop shadow behind yellow circle
shadow = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
draw_s = ImageDraw.Draw(shadow)
draw_s.ellipse([circle_cx - circle_r - 6, circle_cy - circle_r + 16, 
                circle_cx + circle_r + 6, circle_cy + circle_r + 28], 
               fill=(180, 140, 75, 50))
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

# 5. Scale Premkumar half-body so his shoulders span ~620px across the canvas
target_w = 640
scale = target_w / float(pw)
target_h = int(ph * scale)
person_scaled = person.resize((target_w, target_h), Image.Resampling.LANCZOS)

# Position: center over circle, head at y=95 (popping out above circle top 240)
person_x = circle_cx - target_w // 2
person_y = 95

# Bottom curved arc clip: only clip the very bottom corners below y=730 with smooth rounded bottom
bottom_clip = Image.new('L', (target_w, target_h), 255)
draw_bc = ImageDraw.Draw(bottom_clip)

# In Ali Abdaal's image, the bottom has a smooth circular bowl shape
for py in range(target_h):
    wy = person_y + py
    if wy > circle_cy + 150: # only near the bottom
        for px in range(target_w):
            wx = person_x + px
            dist = math.hypot(wx - circle_cx, wy - circle_cy)
            # Clip if beyond circle_r + 45
            max_dist = circle_r + 45
            if dist > max_dist:
                if dist < max_dist + 4:
                    bottom_clip.putpixel((px, py), int(255 * (1.0 - (dist - max_dist) / 4.0)))
                else:
                    bottom_clip.putpixel((px, py), 0)

# Multiply alpha
p_r, p_g, p_b, p_a = person_scaled.split()
from PIL import ImageChops
person_scaled.putalpha(ImageChops.multiply(p_a, bottom_clip))

# Paste onto canvas
canvas.paste(person_scaled, (person_x, person_y), person_scaled)

out_file = '/home/prem/.gemini/antigravity/scratch/premkumar-portfolio/assets/images/premkumar-halfbody-editorial.png'
canvas.save(out_file, 'PNG', optimize=True)
print('Halfbody editorial graphic generated successfully!')
