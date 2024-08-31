import random
from PIL import Image
import os
from pyperclip import copy

def clamp(val, min, max):
    if val < min:
        return min
    if val > max:
        return max
    return val

class map:
    def __init__(self, width, height, colormode: str = "RGB"):
        self.width = width
        self.height = height
        self.color_mode = colormode
        self.pixels = {}
        for y in range(height):
            row = {}
            for x in range(width):
                row[x] = (0,0,0)
            self.pixels[y]=row
    
    def set_pixel(self, x: int, y: int, color: tuple):
        """
        Sets a pixel on the map.
        
        :param x: X position of the pixel. Must be an int.
        :param y: Y position of the pixel. Must be an int.
        :param color: A tuple containing the color values. For example RBG.
        :return: None
        """
        
        if self.color_mode == "RGB":
            r = int(clamp(color[0], 0, 255))
            g = int(clamp(color[1], 0, 255))
            b = int(clamp(color[2], 0, 255))
            color = (r, g, b)
            
            
        
        if (x < 0 or x >= self.width)  or  (y < 0 or y >= self.height):
            raise ValueError("The position provided is not on the map.")
        else:
            self.pixels[y][x] = color
    
    def get_pixel(self, x, y):
        """
        Get the color of a pixel on the map.
        
        :param x: X position of the pixel. Must be an int.
        :param y: Y position of the pixel. Must be an int.
        :return: The color values as a tuple, or None if the pixel isn't on the map.
        """
        
        if (x < 0 or x > self.width)  or  (y < 0 or y > self.height):
            raise ValueError("The position provided is not on the map.")
        else:
            return self.pixels[y][x]
    
    def resize(self, width: int, height: int):
        """
        Resize the map to a new size

        :param width: The new width of the map. INT
        :param height: The new height of the map. INT
        :return: None
        """
        if self.width == 0 or self.height == 0:
            raise ValueError("Original image has no size.")

        row_factor = self.height / height
        col_factor = self.width / width
        _new_image_dict = {}

        for i in range(height):
            _new_image_dict[i] = {}
            for j in range(width):
                orig_i = int(i * row_factor)
                orig_j = int(j * col_factor)
                _new_image_dict[i][j] = self.pixels[orig_i][orig_j]

        self.pixels = _new_image_dict
        self.width = width
        self.height = height
    
        
            
    
    def write_to_file(self, path: str = "exported_map.png"):
        """
        Write the map to an image.
        
        :param path: The path of the image: String
        :return: None
        """
        _image = Image.new(self.color_mode, (self.width, self.height))
        for y in range(self.height):
            for x in range(self.width):
                _image.putpixel((x, y), self.pixels[y][x])
        
        _path = ""
        for item in path.split("/")[0:-1]:
            _path += item
            _path += "/"
        try:
            os.makedirs(_path, exist_ok=True)
        except:
            pass
        
        _image.save(path) 
    
    def combine_with(self, other: map, occupancy: float = 1):
        other.resize(self.width, self.height)
        
        _data = map(self.width, self.height)
        
        for y in range(self.height):
            for x in range(self.width):
                r = self.get_pixel(x,y)[0] + (other.get_pixel(x,y)[0] * occupancy)
                r /= 1+occupancy
                r = int(r)
                g = self.get_pixel(x,y)[1] + (other.get_pixel(x,y)[1] * occupancy)
                g /= 1+occupancy
                g = int(g)
                b = self.get_pixel(x,y)[2] + (other.get_pixel(x,y)[2] * occupancy)
                b /= 1+occupancy
                b = int(b)
                _data.set_pixel(x,y, (r,g,b))
        
        self.pixels = _data.pixels
    
    def modify(self, mod):
        for x in range(self.width):
            for y in range(self.height):
                val1 = self.get_pixel(x,y)[0] + mod
                val2 = self.get_pixel(x,y)[1] + mod
                val3 = self.get_pixel(x,y)[2] + mod
                self.set_pixel(x, y, (val1, val2, val3)) 
                 
            
        
        
    


def white_noise(width: int, height: int, value_range: tuple = (0,255)):
    
    """
    Generates white noise.
    
    :param width: The width of the map, must be an int.
    :param height: The height of the map, must be an int.
    :return: map object, colormode RGB.
    """
    
    
    _map = map(width, height)
    
    for y in range(width):
        for x in range(height):
            _val = random.randint(value_range[0], value_range[1])
            _map.set_pixel(x, y, (_val, _val, _val))
            
    return _map

def colored_noise(width: int, height: int):
    
    """
    Generates colored noise.
    
    :param width: The width of the map, must be an int.
    :param height: The height of the map, must be an int.
    :return: map object, colormode RGB.
    """
    
    
    _map = map(width, height)
    
    for y in range(width):
        for x in range(height):
            _map.set_pixel(x, y, (random.randint(0,255), random.randint(0,255), random.randint(0,255)))
            
    return _map

def perlin_noise(width, height, frequency, contrast: float = 1, lightendarken: int = 0):
    _perlin_map = white_noise(int(frequency*(width/100)), int(frequency*(height/100)), (100,200))
    
    area_size = int(frequency*(_perlin_map.width/75))
    
    _perlin_map.modify(lightendarken)
    
    _perlin_map.resize(int(width/2), int(height/2))
    
    for x in range(_perlin_map.width):
        for y in range(_perlin_map.height):
            
            area_sum = _perlin_map.get_pixel(x, y)[0]
            pixels_counted = 1
            
            for x2 in range(-area_size,area_size+1):
                for y2 in range(-area_size,area_size+1):
                    try:
                        area_sum += _perlin_map.get_pixel(x+x2, y+y2)[0]
                    except:
                        pass
                    else:
                        pixels_counted += 1
                        
            area_sum /= pixels_counted
            
            difference = area_sum-150
            val = 150 + (difference*contrast)
            
            col = (val, val, val)
            _perlin_map.set_pixel(x, y, col)
    
    
    _perlin_map.resize(width, height)
    return _perlin_map

def perlin_noise_extended(width: int, height: int, octaves: int, persistence: float):
    _p_n_e = map(width, height)
    
    
    
    ocpcy = 1
    
    frequency_start = 20
    frequency_end = width
    diff = frequency_end-frequency_start
    contrast = 1.85
    for i in range(octaves):
        
        frequency = diff*(i/octaves)
        frequency += frequency_start
        
        print(frequency, ocpcy, contrast)
        _layer = perlin_noise(width, height, frequency, contrast, (-i)*10)
        _layer.modify(20)
        if i == 0:
            _p_n_e = _layer
        else:
            _p_n_e.combine_with(_layer, ocpcy)
        
        ocpcy = int(clamp(ocpcy-(1-persistence), 0, 1)*100)/100
        contrast += 0.5
    
    return _p_n_e


random.seed("DUMB")
pnoise = perlin_noise_extended(64,64, 5, 0.8)

pnoise.write_to_file("perlin_noise.png")