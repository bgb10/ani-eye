# imports
import numpy as np
import cv2
import src.filters as f

def see(src: cv2.Mat):
    grey = f.greyscale(src)

    sharpen = f.sharpen(grey, np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]))
    
    # μμΌκ° 360λ

    return sharpen