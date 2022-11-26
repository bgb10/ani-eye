from cv2.mat_wrapper import Mat
from numpy import uint8

from src.utils import safe_add

HEXAGON_SHAPE: list[list[int]] = [
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],

]


def add_colors(color1: tuple[int, int, int], color2: tuple[int, int, int]) -> tuple[int, int, int]:
    return color1[0] + color2[0], color1[1] + color2[1], color1[2] + color2[2]


def purpleize_image(image: Mat) -> None:
    for y in range(len(image)):
        for x in range(len(image[y])):
            (b, g, r) = image[y][x]
            image[y][x] = (safe_add(b, 30), safe_add(g, -30), safe_add(r, 20))


def check_overflow(color: tuple[int, int, int]) -> tuple[uint8, uint8, uint8]:
    return uint8(0 if color[0] < 0 else 255 if color[0] > 255 else color[0]), \
           uint8(0 if color[1] < 0 else 255 if color[1] > 255 else color[1]), \
           uint8(0 if color[2] < 0 else 255 if color[2] > 255 else color[2])


def blurring_hexagon(image: Mat) -> Mat:
    new_image: Mat = image.copy()

    for y in range(1, len(image), len(HEXAGON_SHAPE)):
        for x in range(1, len(image[y]), len(HEXAGON_SHAPE[0])):
            for y_hex in range(len(HEXAGON_SHAPE)):
                for x_hex in range(len(HEXAGON_SHAPE[y_hex])):
                    if y + y_hex + 1 >= len(image) or x + x_hex + 1 >= len(image[y]):
                        continue
                    if HEXAGON_SHAPE[y_hex][x_hex] == 1:
                        # (b, g, r) = image[y + y_hex][x + x_hex]
                        # image[y + y_hex][x + x_hex] = (safe_add(b, -20), safe_add(g, -20), safe_add(r, -20))
                        # image[y + y_hex][x + x_hex] = (0, 0, 0)
                        new_bgr: tuple[int, int, int] = (0, 0, 0)
                        new_bgr = add_colors(new_bgr, image[y + y_hex - 1][x + x_hex - 1])
                        new_bgr = add_colors(new_bgr, image[y + y_hex - 1][x + x_hex])
                        new_bgr = add_colors(new_bgr, image[y + y_hex - 1][x + x_hex + 1])

                        new_bgr = add_colors(new_bgr, image[y + y_hex][x + x_hex - 1])
                        new_bgr = add_colors(new_bgr, image[y + y_hex][x + x_hex])
                        new_bgr = add_colors(new_bgr, image[y + y_hex][x + x_hex - 1])

                        new_bgr = add_colors(new_bgr, image[y + y_hex + 1][x + x_hex - 1])
                        new_bgr = add_colors(new_bgr, image[y + y_hex + 1][x + x_hex])
                        new_bgr = add_colors(new_bgr, image[y + y_hex + 1][x + x_hex + 1])
                        new_bgr = (new_bgr[0] // 9, new_bgr[1] // 9, new_bgr[2] // 9)
                        new_bgr: tuple[uint8, uint8, uint8] = check_overflow(new_bgr)

                        new_image[y + y_hex - 1][x + x_hex - 1] = new_bgr
                        new_image[y + y_hex - 1][x + x_hex] = new_bgr
                        new_image[y + y_hex - 1][x + x_hex + 1] = new_bgr

                        new_image[y + y_hex][x + x_hex - 1] = new_bgr
                        new_image[y + y_hex][x + x_hex] = new_bgr
                        new_image[y + y_hex][x + x_hex - 1] = new_bgr

                        new_image[y + y_hex + 1][x + x_hex - 1] = new_bgr
                        new_image[y + y_hex + 1][x + x_hex] = new_bgr
                        new_image[y + y_hex + 1][x + x_hex + 1] = new_bgr
    return new_image


def see(image: Mat) -> Mat:
    purpleize_image(image)
    return blurring_hexagon(image)
