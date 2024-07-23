from PIL import Image
from pyperclip import copy
import colortools as ct

im = Image.open("C:/Users/yanis/Documents/GitHub/starforge/universe/planet_generator/gradient.png")
pix = im.load()
width = im.size[0]
colors = {}
color_amount = 100
increment = width/color_amount
color_mod = 180
x = 0
for iter in range(color_amount):
    color = pix[x,0]
    
    color = ct.rgb_to_hsv(color[0], color[1], color[2])
    h = color[0]+color_mod
    while h> 360:
        h -= 360
    
    s = color[1]
    v = color[2]
    
    color = ct.hsv_to_rgb(h, s, v)
    
    colors[x/width] = color
    x+=increment

colors[1] = color

copy("colors = "+str(colors))
print(("colors = "+str(colors)))