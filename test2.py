from PIL import Image

im = Image.open('assets/screenshots/01_BG_0519ac9edd037cf5.png')
im = im.crop((0,0,im.width, min(7000,im.height)))

im.save('assets/screenshots/01_BG_0519ac9edd037cf5.png')
print(f"""
    {im.size=}
    {im.width=}
    {im.height=}
    """   
)
