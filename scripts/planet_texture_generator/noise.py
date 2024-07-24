import random
from PIL import Image
import os
from pyperclip import copy

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
                
            
        
        
    


def white_noise(width: int, height: int):
    
    """
    Generates white noise.
    
    :param width: The width of the map, must be an int.
    :param height: The height of the map, must be an int.
    :return: map object, colormode RGB.
    """
    
    
    _map = map(width, height)
    
    for y in range(width):
        for x in range(height):
            _val = random.randint(0,255)
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

def perlin_noise(width, height, start_frequency: int = 10):
    _perlin_map = white_noise(int(width / 10), int(height / 10))
    _perlin_map.resize(width, height)
    for i in range(start_frequency):
        _i = start_frequency - i
        _perlin_map.combine_with(white_noise(int(width / _i), int(height / _i)), 0)
    
    
    return _perlin_map


pnoise = perlin_noise(100,100)

pnoise.write_to_file("perlin_noise.png")