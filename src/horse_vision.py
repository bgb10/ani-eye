import cv2
import numpy as np
import math

def see(image):
    image_change = image.copy()
    height = image.shape[0]
    width = image.shape[1]

    mask = [[1, 2, 1],[2, 4, 2],[1, 2, 1]]

    for y in range(1, height-1):
        for x in range(1, width-1):
            valB = 0
            valG = 0
            valR = 0
            for i in (0, 2):
                for j in (0, 2):
                    valB += mask[j][i]*image.item(y+i-1, x+j-1, 0)
                    valG += mask[j][i]*image.item(y+i-1, x+j-1, 1)
                    valR += mask[j][i]*image.item(y+i-1, x+j-1, 2)
            valB/=4
            valG/=4
            valR/=4
            if(valB>255): valB = 255
            if(valG>255): valG = 255
            if(valR>255): valR = 255
            if float(x) < width/2-width/8 or float(x) > width/2+width/8:
                image_change[y, x] = [valB, valG, valR]


    for y in range(0, height):
        for x in range(0, width):
            b=image_change.item(y, x, 0)
            g=image_change.item(y, x, 1)
            r=image_change.item(y, x, 2)

            newG = (g+r)/2
            newR = newG
            image_change[y, x] = [b, newG, newR]
    return image_change