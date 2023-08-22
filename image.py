import cv2
import numpy as np
from utils.structures import ModuleType

class Image:
    """ This class represent the image of a QRCode.
        In the future, it will be possible to resize the image, to overwrite a subregion
        with another Image, to save a vectorial file, ...
    """

    def __init__(self, data: np.array, dark_level: int = 0, light_level: int = 255):
        self.data = data
        self.dark_level = dark_level
        self.light_level = light_level

        self.data[self.data == ModuleType.Dark] = self.dark_level
        self.data[self.data == ModuleType.Light] = self.light_level

    def width(self) -> int:
        """ Returns the width of the image. """

        return self.data.shape[0]
    
    def height(self) -> int:
        """ Returns the height of the image. """

        return self.data.shape[1]
    
    def resize(self, width, height) -> None:
        """ Resize image to given width and height using nearest neighbor interpolation. """

        self.data = cv2.resize(self.data, (width, height), interpolation=cv2.INTER_NEAREST)

    def overwriteSubregion(self, leftX: int, topY: int, overwrite_image) -> None:
        """ Overwrites a subregion of the image starting at coordinates (leftX, topY)
            with given image. """

        self.data[overwrite_image.width:leftX + overwrite_image.width, overwrite_image.height:topY + overwrite_image.height] = overwrite_image.data

    def show(self, title: str = "") -> None:
        """ Displays the image. """

        cv2.imshow(title, self.data)

    def save(self, path: str) -> None:
        """ Saves the image in a file. """

        cv2.imwrite(path, self.data)