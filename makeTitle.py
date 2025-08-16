from PIL import Image, ImageDraw, ImageFont
import os

list_of_titles = ['Meet Your Family','Dad', 'Mom', 'Aunt', 'Little Sis', 'Big Sis', 'Friend', "Mi Prima"]
output_dir = "title_images"
os.makedirs(output_dir, exist_ok=True)

font_path = "font.ttf"
font_size = 120
size = (1000,700)
color = "yellow"

for title in list_of_titles:
    img = Image.new("RGBA", size, (0,0,0,0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, font_size)
    
    # Get text bounding box and adjust for offsets
    bbox = draw.textbbox((0,0), title, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center text in the image
    x = (size[0] - text_width) // 2 - bbox[0]
    y = (size[1] - text_height) // 2 - bbox[1]
    
    draw.text((x, y), title, font=font, fill=color)
    
    img.save(os.path.join(output_dir, f"{title}.png"))
