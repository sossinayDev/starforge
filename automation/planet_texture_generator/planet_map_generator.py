import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
import imagery
import time

width = 100
height = 100
seed = 192837465


terrain_colors = {
    "0": (0, 50, 255),
    "45": (0, 255, 246),
    "50": (255, 225, 0),
    "60": (186, 135, 18),
    "65": (3, 193, 7),
    "100": (82, 178, 83),
    "120": (104, 132, 105),
    "150": (140, 140, 140),
    "256": (255, 255, 255)
}

terraincolormap = imagery.colormap()
terraincolormap.import_gradient(terrain_colors)

map = imagery.map(width, height)

noise1 = PerlinNoise(octaves=5)
noise2 = PerlinNoise(octaves=8)
noise3 = PerlinNoise(octaves=14)
noise4 = PerlinNoise(octaves=25)

xpix, ypix = width, height
for i in range(xpix):
    for j in range(ypix):
        noise_val = noise1([i/xpix, j/ypix])
        noise_val += 0.5 * noise2([i/xpix, j/ypix])
        noise_val += 0.25 * noise3([i/xpix, j/ypix])
        noise_val += 0.125 * noise4([i/xpix, j/ypix])
        map.set_pixel(i,j,terraincolormap.value((noise_val+0.5)*255))
    

map.write_to_file()