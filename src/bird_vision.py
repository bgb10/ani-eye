import cv2
import numpy as np
import math


def see(image):
    height = image.shape[0]
    width = image.shape[1]

    for y in range(0, height):
        for x in range(0, width):
            b=image.item(y, x, 0)
            g=image.item(y, x, 1)
            r=image.item(y, x, 2)
            if(abs(b-r)<15):
                b = (b+r)/2+60
                r = b
                image[y, x] = [b, 0, r]



            # b = (b+r)/2+50
            # r=b
            # image[y, x] = [b, g, r]


            

    image_distort = image.copy()

    #distort func
    exp =2.
    scale = 1

    mapY, mapX = np.indices((height, width), dtype=np.float32)

    mapX = 2*mapX/(width-1)-1
    mapY = 2*mapY/(height-1)-1

    r = np.sqrt((mapX*mapX)+(mapY*mapY))
    theta = np.arccos(mapX/r)
    index = 0

    for i in range(height):
        for j in range(width):
            if(mapY[i][j]<0):
                theta[i][j] = 2.*np.pi-theta[i][j]
            

    r[r<scale]=r[r<scale]**exp

    mapX = r*np.cos(theta)
    mapY = r*np.sin(theta)

    mapX = ((mapX+1)*width-1)/2
    mapY = ((mapY+1)*height-1)/2

    intX = mapX.astype(int)
    intY = mapY.astype(int)

    fx1 = mapX-intX
    fx2 = 1-fx1
    fy1 = mapY-intY
    fy2 = 1-fy1

    w1 = fx2*fy2
    w2 = fx1*fy2
    w3 = fx2*fy1
    w4 = fx1*fy1

    intX[intX<width-1] = intX[intX<width-1]+1
    intY[intY<height-1] = intY[intY<height-1]+1

    p1 = image[intY-1, intX-1]
    p2 = image[intY-1, intX]
    p3 = image[intY, intX-1]
    p4 = image[intY, intX]
    for y in range(0, height):
        for x in range(0, width):
            image_distort[y, x] = w1[y, x]*p1[y, x] + w2[y, x]*p2[y, x] + w3[y, x]*p3[y, x] + w4[y, x]*p4[y, x]
    

    return image_distort

   