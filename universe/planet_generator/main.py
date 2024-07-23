from PIL import Image
import os
from random import randint, seed
import time
import colortools as ct
from time import sleep

colors = {}

def calculate_colors(mod):
    global colors
    im = Image.open("C:/Users/yanis/Documents/GitHub/starforge/universe/planet_generator/gradient.png")
    pix = im.load()
    width = im.size[0]
    colors = {}
    color_amount = 100
    increment = width/color_amount
    color_mod = mod
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







def val_to_color(val):
    val /= 255
    for limit in colors:
        if val <= limit:
            return colors[limit]
    return colors[1]




def dict_to_png(data, filename='output.png'):
    # Determine the dimensions of the image
    max_y = max(data.keys())
    max_x = max(max(sub.keys()) for sub in data.values())
    
    # Create a new image with RGB mode with dimensions (max_x + 1, max_y + 1)
    image = Image.new("RGB", (max_x + 1, max_y + 1), (0, 255, 0))

    # Load pixel data
    pixels = image.load()

    # Fill in the pixels based on the dictionary
    for y in data:
        row = data[y]
        for x in row:
            item = row[x]
            pixels[int(x), int(y)] = item

    # Save the image to a file
    image.save(filename)
    print(f"Image written to {filename}")


data = {}

def clamp(val, min, max):
    if val < min:
        return int(min)
    elif val > max:
        return int(max)
    else:
        return int(val)

def set_pixel(x,y,color: tuple):
    global data
    
    
    
    color = clamp(color[0], 0, 255), clamp(color[1], 0, 255), clamp(color[2], 0, 255)
    try:
        data[y][x] = color
    except:
        data[y] = {x: color}

def get_pixel(x,y):
    global data
    return data[y][x]

def generate_heightmap(width, height, roughness: int = 8, layers: int = 5, contrast_boost: float = 1.01, map_seed = "", startrange: tuple = (0,255)):
    global data
    if map_seed == "":
        map_seed = time.time()
    seed(map_seed)
    data = {}
    for y in range(height-1):
        for x in range(width):
            val = randint(startrange[0], startrange[1])
            set_pixel(x,y,(val, val, val))
    heightmap = data
    
    positions = [
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, -1),
        (1, 1),
        (-1, 1),
        (1, -1),
    ]
    roughness_decrement = roughness/layers
    for z in range(layers):
        data = {}
        for y in range(height-1):
            for x in range(width):
                valsum = heightmap[y][x][0]
                vals = 1
                for pos in positions:
                    try:
                        valsum += heightmap[y+pos[0]][x+pos[1]][0]
                    except:
                        pass
                    else:
                        vals+=1
                val = valsum/vals
                roughness -= roughness_decrement
                if roughness > 0:
                    val += randint(-roughness, roughness)
                set_pixel(x,y,(val, val, val))
        heightmap = data
    
    print("Post processing...")
    
    med = 0
    pxls = 0
    
    for y in heightmap:
        row = heightmap[y]
        for x in row:
            med += heightmap[y][x][0]
            pxls += 1
    
    med /= pxls
    
    for y in heightmap:
        row = heightmap[y]
        for x in row:
            difference = heightmap[y][x][0] - med
            val = med + (difference*contrast_boost)
            val = int(val)
            heightmap[y][x] = (val, val, val)
    data = heightmap
    print("Heightmap completed!")
    return data
    

def colorize_map(heightmap):
    data = {}
    for y in heightmap:
        row = heightmap[y]
        for x in row:
            set_pixel(x,y,val_to_color(heightmap[y][x][0]))

    return data
            


while 1:
    modifier = randint(0,360)
    calculate_colors(modifier)
    name = "color_map"
    parent = "universe/planet_generator/exported_planets/"+name+"/"
    os.makedirs(parent, exist_ok=True)
    w = 512
    h = 256
    r = 1000
    l = 20
    c = 5
    t_start = time.time()
    
    map_seed=int(t_start*randint(111,999))+randint(-10000,10000)
    hmap = generate_heightmap(w, h, r, l, c, map_seed)
    print("Colorizing...")
    colormap = hmap
    dict_to_png(hmap, parent+"map.png")
    
    t_end = time.time()
    t = int(t_end-t_start)
    
    print(f"Sample: {w}x{h}\n\nColor modifier: {modifier}\nRoughness: {r}\nLayers: {l}\nContrast: {c}\nSeed: {map_seed}\nRender time: {t} seconds")
    input()