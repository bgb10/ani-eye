from numpy import uint8


def safe_add(color: int, value: int) -> uint8:
    new_value = color + value
    return uint8(0 if new_value < 0 else 255 if new_value > 255 else new_value)


def blurring(image, size):
    temp = image.copy()
    rows, cols = temp.shape[:2]

    mask = 1/(size*size)

    for x in range(0, rows - size + 1):
        for y in range(0, cols - size + 1):
            red, green, blue = 0, 0, 0

            for i in range(size):
                for j in range(size):
                    (b, g, r) = image[x + i][y + j]
                    red += r * mask
                    green += g * mask
                    blue += b * mask

            if red < 0:
                red = 0
            elif red > 255:
                red = 255

            if green < 0:
                green = 0
            elif green > 255:
                green = 255

            if blue < 0:
                blue = 0
            elif blue > 255:
                blue = 255

            temp[x + 1][y + 1] = (blue, green, red)

    return temp