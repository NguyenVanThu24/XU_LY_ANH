import cv2
import numpy as np

def highpass_spatial(image_path):

    img = cv2.imread(image_path,0)

    # 🔥 CHUYỂN SANG INT để tránh tràn số
    img = img.astype(int)

    rows, cols = img.shape
    result = np.zeros((rows,cols))

    kernel = [
        [-1,-1,-1],
        [-1, 8,-1],
        [-1,-1,-1]
    ]

    for i in range(1,rows-1):
        for j in range(1,cols-1):

            s = 0
            for m in range(-1,2):
                for n in range(-1,2):
                    s += img[i+m][j+n] * kernel[m+1][n+1]

            result[i][j] = s

    # High-boost
    sharpen = img + result

    # Giới hạn lại về 0–255
    sharpen = np.clip(sharpen,0,255)

    return sharpen.astype(np.uint8)