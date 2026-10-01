from PIL import Image, ImageDraw, ImageFilter, ImageChops
import math

# Load clean cutout
person = Image.open('/home/prem/.gemini/antigravity/scratch/premkumar-portfolio/assets/images/premkumar_cutout_v3.png')
pw, ph = person.size

# High-resolution canvas matching the Ali Abdaal graphic template
cw, ch = 800, 850
canvas = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))

# Geometry for the warm yellow circle
# Positioned so head pops out of the top, and chest clips at the bottom
circle_cx = 390
circle_cy = 475
circle_r = 255
yellow_color = (253, 200, 68, 255) # Warm sunny yellow #FDC844

# 1. Warm ambient drop shadow underneath the yellow circle
shadow = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
draw_s = ImageDraw.Draw(shadow)
draw_s.ellipse([circle_cx - circle_r - 6, circle_cy - circle_r + 18, 
                circle_cx + circle_r + 6, circle_cy + circle_r + 30], 
               fill=(180, 140, 75, 55))
shadow = shadow.filter(ImageFilter.GaussianBlur(22))
canvas = Image.alpha_composite(canvas, shadow)

# 2. Draw solid yellow speech-bubble circle
draw = ImageDraw.Draw(canvas)
# Main circle
draw.ellipse([circle_cx - circle_r, circle_cy - circle_r, 
              circle_cx + circle_r, circle_cy + circle_r], fill=yellow_color)

# Speech bubble pointer on the right side pointing towards text
pointer_pts = [
    (circle_cx + circle_r - 18, circle_cy - 42),
    (circle_cx + circle_r + 85, circle_cy - 10),
    (circle_cx + circle_r - 12, circle_cy + 42)
]
draw.polygon(pointer_pts, fill=yellow_color)

# 3. Decorative yellow accent arc on the left (matching Ali Abdaal template)
arc_bbox = [circle_cx - circle_r - 42, circle_cy - circle_r - 35, 
            circle_cx + circle_r + 42, circle_cy + circle_r + 45]
draw.arc(arc_bbox, start=145, end=255, fill=(253, 200, 68, 230), width=6)

# Accent dot at upper end of arc
dot_x = circle_cx - circle_r - 28
dot_y = circle_cy - circle_r + 85
draw.ellipse([dot_x - 7, dot_y - 7, dot_x + 7, dot_y + 7], fill=(253, 200, 68, 255))

# 4. Scale and position Premkumar's half-body cutout
# Target width ~560px (shoulders span the circle width comfortably)
target_w = 560
scale = target_w / float(pw)
target_h = int(ph * scale)
person_scaled = person.resize((target_w, target_h), Image.Resampling.LANCZOS)

# Position:
# circle top is circle_cy - circle_r = 475 - 255 = 220
# Head pops out to y=105 (pop-out of 115px above yellow circle)
person_x = circle_cx - target_w // 2 - 2
person_y = 105

# 5. Circular Bottom Clipping:
# The bottom of Premkumar's chest curves along the bottom arc of the circle.
# The top (head & shoulders popping out) is NOT clipped!
clip_mask = Image.new('L', (target_w, target_h), 255)

for py in range(target_h):
    world_y = person_y + py
    if world_y > circle_cy: # below circle center
        for px in range(target_w):
            world_x = person_x + px
            dist = math.hypot(world_x - circle_cx, world_y - circle_cy)
            if dist > circle_r:
                if dist < circle_r + 2:
                    clip_mask.putpixel((px, py), int(255 * (1.0 - (dist - circle_r) / 2.0)))
                else:
                    clip_mask.putpixel((px, py), 0)

# Multiply alpha channel with clip_mask
p_r, p_g, p_b, p_a = person_scaled.split()
final_alpha = ImageChops.multiply(p_a, clip_mask)
person_scaled.putalpha(final_alpha)

# 6. Paste onto canvas
canvas.paste(person_scaled, (person_x, person_y), person_scaled)

# Save final graphic
out_file = '/home/prem/.gemini/antigravity/scratch/premkumar-portfolio/assets/images/premkumar-hero-editorial.png'
canvas.save(out_file, 'PNG', optimize=True)
print('Final hero graphic generated successfully!')
