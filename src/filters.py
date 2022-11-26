import numpy as np

def makeHorizontalBorder(img: np.ndarray, value: tuple, left: int, right: int):
    h, w = img.shape[:2]
    
    blind_area_left = np.full((h, left, 3), value)
    blind_area_right = np.full((h, right, 3), value)
    img = np.concatenate([blind_area_left, img], 1) # left
    img = np.concatenate([img, blind_area_right], 1) # right
    img = np.array(img, dtype=np.uint8)

    return img

def blur(img: np.ndarray, mask: np.ndarray):
    h, w = img.shape[:2]
    mh, mw = mask.shape[:2] 
    res = img.copy()

    tot = 0
    for mask_y in mask:
        for mask_xy in mask_y:
            tot += abs(mask_xy)

    t = int(mh / 2)

    for y in range(t, h-mh):
        for x in range(t, w-mw):
            sum = [0, 0, 0] # b, g, r
            for j in range(-t, t + 1):
                for i in range(-t, t + 1):
                    sum[0] += img[y + j][x + i][0] * mask[j + t][i + t]
                    sum[1] += img[y + j][x + i][1] * mask[j + t][i + t]
                    sum[2] += img[y + j][x + i][2] * mask[j + t][i + t]
            avg_b = int(sum[0] / tot) 
            avg_g = int(sum[1] / tot)
            avg_r = int(sum[2] / tot)
            255 if avg_b > 255 else avg_b
            255 if avg_g > 255 else avg_g
            255 if avg_r > 255 else avg_r
            0 if avg_b < 0 else avg_b
            0 if avg_g < 0 else avg_g
            0 if avg_r < 0 else avg_r
            res[y][x] = [avg_b, avg_g, avg_r]

    return res

def sharpen(img: np.ndarray, mask: np.ndarray):
    h, w = img.shape[:2]
    mh, mw = mask.shape[:2] 
    res = img.copy()

    # assert mh == mw

    t = int(mh / 2)

    for y in range(t, h-mh):
        for x in range(t, w-mw):
            sum = [0, 0, 0] # b, g, r
            for j in range(-t, t + 1):
                for i in range(-t, t + 1):
                    sum[0] += img[y + j][x + i][0] * mask[j + t][i + t]
                    sum[1] += img[y + j][x + i][1] * mask[j + t][i + t]
                    sum[2] += img[y + j][x + i][2] * mask[j + t][i + t]
            sum[0] = 255 if sum[0] > 255 else sum[0]
            sum[1] = 255 if sum[1] > 255 else sum[1]
            sum[2] = 255 if sum[2] > 255 else sum[2]
            sum[0] = 0 if sum[0] < 0 else sum[0]
            sum[1] = 0 if sum[1] < 0 else sum[1]
            sum[2] = 0 if sum[2] < 0 else sum[2]
            res[y][x] = [sum[0], sum[1], sum[2]]

    return res

def imitateFOV(src: np.ndarray, binocular_radius: int, uniocular_radius: int, ksize: tuple):
    h, w = src.shape[:2]
    
    ocular_radius = binocular_radius + 2 * uniocular_radius
    invisible_area_portion = ((360 - ocular_radius) / 360) / 2
    invisible_area = int(w * invisible_area_portion)
    src = src[0:h, invisible_area:w-invisible_area]

    nh, nw = src.shape[:2]
    blur_area_portion = uniocular_radius / ocular_radius
    blur_area = int(nw * blur_area_portion)

    src = gradiantBlur(src, nw - blur_area, nw, 0, ksize, 5)
    src = gradiantBlur(src, 0, blur_area, 1, ksize, 5)
    
    src = makeHorizontalBorder(src, (0, 0, 0), invisible_area, invisible_area)

    return src

def gradiantBlur(src: np.ndarray, start: int, end:int, direction: int, ksize: tuple, div:int):
    # assert start <= end

    portion = int((end - start) / div)

    h, w = src.shape[:2]
    
    if direction == 0:
        cur = start
        while cur + portion <= end - portion:
            src[0:h, cur:end] = blur(src[0:h, cur:end], np.full(ksize, 1))
            cur += portion
        src[0:h, end-portion:end] = blur(src[0:h, end-portion:end], np.full(ksize, 1))
    else:
        cur = end
        while cur - portion >= start:
            src[0:h, start:cur] = blur(src[0:h, start:cur], np.full(ksize, 1))
            cur -= portion
        src[0:h, start:start+portion] = blur(src[0:h, start:start+portion], np.full(ksize, 1))

    return src

def greyscale(src:np.ndarray):
    h, w = src.shape[:2]
    for y in range(h):
        for x in range(w):
            b = src.item(y, x, 0)
            g = src.item(y, x, 1)
            r = src.item(y, x, 2)
            g = int((b + g + r) / 3)
            nb = g
            ng = g
            nr = g
            src.itemset((y, x, 0), nb)
            src.itemset((y, x, 1), ng)
            src.itemset((y, x, 2), nr)
    
    return src


def calcBrightness(src: np.ndarray):
    cnt = 0
    sum = 0

    for line in src:
        for pixel in line:
            b, g, r = pixel
            sum += (0.2126*r + 0.7152*g + 0.0722*b)
            cnt += 1

    return sum / cnt

def addBrightness(src: np.ndarray, value: int):
    # used nditer to iterate, but it is much slower than below
    # with np.nditer(src, op_flags=['readwrite']) as it:
    #     for x in it:
    #         x[...] = 255 if x + value >= 255 else x + value # x[...] means class ndarray to value
    
    h, w = src.shape[:2]
    for y in range(h):
        for x in range(w):
            b = src.item(y, x, 0)
            g = src.item(y, x, 1)
            r = src.item(y, x, 2)
            nb = 255 if b + value >= 255 else b + value
            ng = 255 if g + value >= 255 else g + value 
            nr = 255 if r + value >= 255 else r + value
            src.itemset((y, x, 0), nb)
            src.itemset((y, x, 1), ng)
            src.itemset((y, x, 2), nr)
    
    return src