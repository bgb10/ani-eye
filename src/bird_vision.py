import cv2
import numpy as np
import math


def see(image):#not complete, only purple scaled
    height = image.shape[0]
    width = image.shape[1]

    for y in range(0, height):
        for x in range(0, width):
            b=image.item(y, x, 0)
            r=image.item(y, x, 2)
            b = (b+r)/2
            r=b
            image[y, x] = [b, 0, r]


    #distort func: must change own func
    exp =1.5
    scale = 1

    mapy, mapx = np.indices((height, width), dtype=np.float32)

    mapx = 2*mapx/(width-1)-1
    mapy = 2*mapy/(height-1)-1

    r, theta = cv2.cartToPolar(mapx, mapy)

    r[r<scale] = r[r<scale] **exp

    mapx, mapy = cv2.polarToCart(r, theta)

    mapx = ((mapx+1)*width-1)/2
    mapy = ((mapy+1)*height-1)/2

    distort = cv2.remap(image, mapx, mapy, cv2.INTER_LINEAR)

    return distort

   