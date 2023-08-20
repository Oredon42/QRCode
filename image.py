import cv2

class Image:
    def __init__(self, data, black_level=0, white_level=255):
        self.data = data
        self.black_level = black_level
        self.white_level = white_level

        self.data[self.data == -1] = self.black_level
        self.data[self.data == 1] = self.white_level

    def width(self):
        return self.data.shape[0]
    
    def height(self):
        return self.data.shape[1]

    def overwriteSubregion(self, leftX, topY, overwrite_image):
        self.data[overwrite_image.width:leftX + overwrite_image.width, overwrite_image.height:topY + overwrite_image.height] = overwrite_image.data

    def show(self, title=""):
        cv2.imshow(title, self.data)

    def save(self, path):
        cv2.imwrite(path, self.data)