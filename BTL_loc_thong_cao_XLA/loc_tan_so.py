import cv2
import numpy as np

def highpass_frequency(image_path):

    # Đọc ảnh xám
    img = cv2.imread(image_path,0)

    # 🔥 Chuyển sang int để tránh tràn số
    img = img.astype(int)

    # FFT
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)

    rows, cols = img.shape
    crow, ccol = rows//2 , cols//2

    # Tạo mask thông cao bằng vòng for
    mask = np.ones((rows,cols))

    r = 30   # bán kính vùng tần số thấp cần loại bỏ

    for i in range(crow-r,crow+r):
        for j in range(ccol-r,ccol+r):
            if i>=0 and j>=0 and i<rows and j<cols:
                mask[i][j] = 0

    # Lọc thông cao
    hpf = fshift * mask

    # Biến đổi ngược
    f_ishift = np.fft.ifftshift(hpf)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)

    # High-boost để làm nổi bật chi tiết
    sharpen = np.zeros((rows,cols))

    for i in range(rows):
        for j in range(cols):
            sharpen[i][j] = img[i][j] + int(img_back[i][j])

    # Giới hạn giá trị 0–255
    sharpen = np.clip(sharpen,0,255)

    return sharpen.astype(np.uint8)