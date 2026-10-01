from PIL import Image, ImageDraw, ImageFilter
import math

# 1. Load original Premkumar photo
src = Image.open('/home/prem/.gemini/antigravity/scratch/premkumar-portfolio/assets/images/premkumar.jpg').convert('RGB')
sw, sh = src.size

# We want half-body from y=0 to y=850
crop_h = 860
src_crop = src.crop((0, 0, sw, crop_h))
w, h = src_crop.size
center_x = 288

# 2. Extract precise left and right boundaries for Premkumar's silhouette
left_boundary = []
right_boundary = []

for y in range(h):
    if y >= 640:
        # Full width for chest / shoulders
        left_boundary.append(0)
        right_boundary.append(w - 1)
        continue
    
    # Left boundary (scan from center_x to 0)
    lx = 0
    for x in range(center_x, -1, -1):
        r, g, b = src_crop.getpixel((x, y))
        br = (r + g + b) / 3
        # Left background is beige wall (br > 115 and r-b < 35) or plant (g > r and g > 60)
        is_wall = (br > 115 and (r - b < 35 or br > 140))
        is_plant = (g > r + 3 and g > 55)
        if is_wall or is_plant:
            lx = x + 1
            break
    
    # Smooth check: if y < 220 (top of hair), hair width is around x=100..450
    if y < 140 and lx < 80:
        lx = 100
    left_boundary.append(lx)

    # Right boundary (scan from center_x to w-1)
    rx = w - 1
    for x in range(center_x, w):
        r, g, b = src_crop.getpixel((x, y))
        br = (r + g + b) / 3
        
        # Right background is cool window/room:
        # b >= r - 12 and br > 65
        # or br > 110
        # or g > r + 2 and br > 70
        is_window = (b >= r - 12 and br > 65) or (br > 125) or (g > r + 5 and br > 65)
        if is_window:
            rx = x - 1
            break
            
    if y < 140 and rx > 480:
        rx = 460
    right_boundary.append(rx)

# Apply 9-point median filter to smooth contour
smooth_l = []
smooth_r = []
k = 9
for i in range(h):
    s = max(0, i - k//2)
    e = min(h, i + k//2 + 1)
    win_l = sorted(left_boundary[s:e])
    win_r = sorted(right_boundary[s:e])
    smooth_l.append(win_l[len(win_l)//2])
    smooth_r.append(win_r[len(win_r)//2])

# Build alpha mask for Premkumar
person_mask = Image.new('L', (w, h), 0)
draw_mask = ImageDraw.Draw(person_mask)

poly = []
poly.append((smooth_l[0], 0))
for y in range(h):
    poly.append((smooth_r[y], y))
poly.append((w - 1, h - 1))
poly.append((0, h - 1))
for y in range(h - 1, -1, -1):
    poly.append((smooth_l[y], y))

draw_mask.polygon(poly, fill=255)
person_mask = person_mask.filter(ImageFilter.GaussianBlur(1.2))

# Cutout image of Premkumar (transparent background)
person_cutout = src_crop.copy()
person_cutout.putalpha(person_mask)

# 3. Create the Editorial Graphic Canvas (800 x 850) matching Ali Abdaal reference
cw, ch = 800, 850
canvas = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
draw = ImageDraw.Draw(canvas)

# Yellow circle geometry
circle_cx = 380
circle_cy = 480
circle_r = 250
yellow_color = (253, 200, 68, 255) # #FDC844

# A. Soft drop shadow under yellow circle
shadow = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
draw_s = ImageDraw.Draw(shadow)
draw_s.ellipse([circle_cx - circle_r - 4, circle_cy - circle_r + 14, 
                circle_cx + circle_r + 4, circle_cy + circle_r + 24], fill=(180, 140, 75, 45))
shadow = shadow.filter(ImageFilter.GaussianBlur(16))
canvas = Image.alpha_composite(canvas, shadow)
draw = ImageDraw.Draw(canvas)

# B. Draw solid yellow speech-bubble circle
# Main circle
draw.ellipse([circle_cx - circle_r, circle_cy - circle_r, 
              circle_cx + circle_r, circle_cy + circle_r], fill=yellow_color)

# Speech bubble triangle pointer on right side
pointer = [
    (circle_cx + circle_r - 15, circle_cy - 40),
    (circle_cx + circle_r + 85, circle_cy - 8),
    (circle_cx + circle_r - 10, circle_cy + 42)
]
draw.polygon(pointer, fill=yellow_color)

# C. Outer decorative yellow curved arc on the left (matching reference)
arc_bbox = [circle_cx - circle_r - 42, circle_cy - circle_r - 35, 
            circle_cx + circle_r + 42, circle_cy + circle_r + 45]
draw.arc(arc_bbox, start=145, end=255, fill=(253, 200, 68, 220), width=6)
# Small accent pill dot at end of arc
dot_x = circle_cx - circle_r - 30
dot_y = circle_cy - circle_r + 85
draw.ellipse([dot_x - 7, dot_y - 7, dot_x + 7, dot_y + 7], fill=(253, 200, 68, 255))

# D. Place Premkumar's Half-Body Cutout
# Scale person cutout to fit perfectly inside the yellow circle
# Head pops up above circle top (circle top is 480 - 250 = 230).
# Head should start around y = 110 (120px pop-out above yellow circle).
target_person_w = 540
target_person_h = int(h * (target_person_w / w))
person_scaled = person_cutout.resize((target_person_w, target_person_h), Image.Resampling.LANCZOS)

person_x = circle_cx - target_person_w // 2 - 2  # centered over circle
person_y = 110  # head pops out above circle top (230)

# E. Circular Bottom Clipping:
# Create a clipping mask so the bottom of the body curves cleanly along the yellow circle's bottom arc!
# Top portion (above circle midline) is NOT clipped (allowing head to pop out)!
clip_mask = Image.new('L', (target_person_w, target_person_h), 255)
draw_clip = ImageDraw.Draw(clip_mask)

# For every pixel in person_scaled, check if it's below circle center and outside circle_r
for py in range(target_person_h):
    world_y = person_y + py
    if world_y > circle_cy:
        # Check distance from circle center
        for px in range(target_person_w):
            world_x = person_x + px
            dist = math.hypot(world_x - circle_cx, world_y - circle_cy)
            if dist > circle_r:
                # Feather near boundary
                if dist < circle_r + 2:
                    clip_mask.putpixel((px, py), int(255 * (1 - (dist - circle_r) / 2)))
                else:
                    clip_mask.putpixel((px, py), 0)

# Apply clipping mask to person's alpha channel
p_r, p_g, p_b, p_a = person_scaled.split()
# Combine person alpha and clip mask
from PIL import ImageChops
final_a = ImageChops.multiply(p_a, clip_mask)
person_scaled.putalpha(final_a)

# Paste person onto canvas
canvas.paste(person_scaled, (person_x, person_y), person_scaled)

# Save result
output_path = '/home/prem/.gemini/antigravity/scratch/premkumar-portfolio/assets/images/premkumar-halfbody-editorial.png'
canvas.save(output_path, 'PNG', optimize=True)
print(f'Editorial half-body graphic created successfully at {output_path}!')
