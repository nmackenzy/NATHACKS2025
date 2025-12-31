from PIL import Image, ImageTk, ImageOps, ImageDraw

def load_image(path, size=(100, 100)):
    try:
        img = Image.open(path).convert("RGBA")
    except:
        img = Image.open("images/default.png").convert("RGBA")
    
    img = ImageOps.fit(img, size, centering=(0.5, 0.5))
    
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    
    img.putalpha(mask)
    
    return ImageTk.PhotoImage(img)
