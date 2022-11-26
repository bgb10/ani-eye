def changeToBeeColor(image):
    rows, cols = image.shape[:2]

    for x in range(rows):
        for y in range(cols):
            (b, g, r) = image[x, y]

            if (g <= b) or (r > 150 and abs(g-b) < 40):
                image[x, y] = (r, b, g)

    return image

def see(image):
    colorIm = changeToBeeColor(image)

    return colorIm