from src.utils import blurring

def changeToDogColor(image):

    rows, cols = image.shape[:2]

    for x in range(rows):
        for y in range(cols):
            (b, g, r) = image[x, y]
            # Dog Blue = Human Blue
            # Dog Red = (Human Green + Human Red) / 2
            # Dog Green = Dog Red
            dogR = (int(g) + int(r)) / 2
            image[x, y] = (b, dogR, dogR)

    return image

def changeToDogBrightness(image):
    blueSum, greenSum, redSum = 0, 0, 0

    rows, cols = image.shape[:2]

    for x in range(rows):
        for y in range(cols):
            (b, g, r) = image[x, y]
            blueSum += b
            greenSum += g
            redSum += r

    imageSize = rows * cols
    blueAvg = blueSum / imageSize
    greenAvg = greenSum / imageSize
    redAvg = redSum / imageSize

    brightnessAvg = redAvg * 0.3 + greenAvg * 0.59 + blueAvg * 0.11

    for x in range(rows):
        for y in range(cols):
            (b, g, r) = image[x, y]
            image[x, y] = ((b + brightnessAvg) / 2, (g + brightnessAvg) / 2, (r + brightnessAvg) / 2)

    return image

def see(image):
    colorIm = changeToDogColor(image)
    brightnessIm = changeToDogBrightness(colorIm)
    blurIm = blurring(brightnessIm, 5)

    return blurIm