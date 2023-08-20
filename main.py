from qrcode import QrCode

from tables import ErrorCorrectionLevel

import cv2

if __name__ == "__main__":
    qr_code = QrCode()
    image = qr_code.encode("Hello World!", ErrorCorrectionLevel.L)
    image.save("qr_code.jpg")
    image.show()

    cv2.waitKey(0)
