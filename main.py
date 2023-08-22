from qrcode import QrCode

import cv2

if __name__ == "__main__":
    qr_code = QrCode()
    qr_code.saveAsPixmapImage("qr_code.jpg", 256)
    qr_code.saveAsVectorialImage("qr_code.svg", 256)

    cv2.waitKey(0)
