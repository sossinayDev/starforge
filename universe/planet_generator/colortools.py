def hsv_to_rgb(h, s, v):
    """
    Convert HSV to RGB.
    
    :param h: Hue component, a float between 0 and 360.
    :param s: Saturation component, a float between 0 and 1.
    :param v: Value component, a float between 0 and 1.
    :return: A tuple representing the RGB values (red, green, blue),
             where each component is an integer between 0 and 255.
    """
    c = v * s  # Chroma
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c
    
    if 0 <= h < 60:
        r_, g_, b_ = c, x, 0
    elif 60 <= h < 120:
        r_, g_, b_ = x, c, 0
    elif 120 <= h < 180:
        r_, g_, b_ = 0, c, x
    elif 180 <= h < 240:
        r_, g_, b_ = 0, x, c
    elif 240 <= h < 300:
        r_, g_, b_ = x, 0, c
    elif 300 <= h <= 360:
        r_, g_, b_ = c, 0, x
    else:
        r_, g_, b_ = 0, 0, 0  # Should never happen
    
    r = (r_ + m) * 255
    g = (g_ + m) * 255
    b = (b_ + m) * 255
    
    return int(r), int(g), int(b)

def rgb_to_hsv(r, g, b):
    """
    Convert RGB to HSV.
    
    :param r: Red component, an integer between 0 and 255.
    :param g: Green component, an integer between 0 and 255.
    :param b: Blue component, an integer between 0 and 255.
    :return: A tuple representing the HSV values (hue, saturation, value), 
             where hue is in [0, 360], saturation and value are in [0, 1].
    """
    r = r / 255.0
    g = g / 255.0
    b = b / 255.0
    
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    delta = max_val - min_val

    # Compute the value
    v = max_val

    # Compute the saturation
    s = 0 if max_val == 0 else delta / max_val

    # Compute the hue
    if delta == 0:
        h = 0
    elif max_val == r:
        h = 60 * (((g - b) / delta) % 6)
    elif max_val == g:
        h = 60 * (((b - r) / delta) + 2)
    elif max_val == b:
        h = 60 * (((r - g) / delta) + 4)

    if h < 0:
        h += 360

    return h, s, v