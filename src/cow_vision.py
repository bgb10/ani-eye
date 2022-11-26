from typing import Tuple

from cv2.mat_wrapper import Mat
from numpy import uint8

from src.fly_vision import safe_add


def color_average(color: Tuple[uint8, uint8, uint8]) -> uint8:
    return sum(color) // len(color)


def see(image: Mat) -> Mat:
    for y in range(len(image)):
        for x in range(len(image[y])):
            color = (b, g, r) = image[y][x]
            if (result := color_average(color)) > 240:
                image[y][x] = (result - 30, result - 30, result)
            else:
                image[y][x] = (safe_add(r, -80), safe_add(g, -20), safe_add(int(b), int(g)))
    return image