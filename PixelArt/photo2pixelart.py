#!/usr/bin/env python
#__usage__ = "To Convert Image pixel data to readable bytes"
from PIL import Image
import numpy as np
FILENAME = 'Pause_32x32.png'
EXPORT_NAME = 'Pause_32x32.txt'
i = Image.open(FILENAME)
iar = np.asarray(i)

def getIfromRGB(rgb):
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    if len(rgb) == 4:
        alpha = rgb[3] # 0.0 (fully transparent) and 1.0 (fully opaque)
    else:
        alpha = 255
    if alpha >= 125: 
        RGBint = (red<<16) + (green<<8) + blue
    else:
        RGBint = 0
    return RGBint

with open(EXPORT_NAME, 'w') as file:
    file.write('image=(')
    for idx, row in enumerate(iar):
        if idx == 0:
            line = "("
        else:
            line = ",("
        
        for i, element in enumerate(row):
            ec = getIfromRGB(element)
            #if ec > 1:
            #    ec %= 10
            line += f"{ec:8}" # f"{ec:1}"
            if i != 31:
                line += ","
        line += ")\n"
        file.write(line)
    file.write(")")
