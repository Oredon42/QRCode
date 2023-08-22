from image import Image

from encoder import Encoder
from matrix import Matrix

from utils.functions import getErrorCorrectionLevelFromString
from utils.svg import writeSVG

class QrCode:
    """
        This class represents a QRCode, which can be generated from a text.
    """

    def __init__(self) -> None:
        self._encoder = Encoder()
        self.matrix = Matrix()


    def encode(self, text: str, error_correction_level_str: str = "L") -> Image:
        """ This method encodes the text with given error correction level,
            and generates a QRCode symbol from the encoded message.
            An image of the symbol is returned. """

        error_correction_level = getErrorCorrectionLevelFromString(error_correction_level_str)
        message_bits = self._encoder.encode(text, error_correction_level)

        self.matrix.generate(message_bits, self._encoder.version, error_correction_level)
    
    def saveAsPixmapImage(self, filepath: str, width_px: int) -> None:
        """ Saves a pixmap image of the QRCode resized to width_px to the path filepath. """

        image = Image(self.matrix.data)
        image.resize(width_px, width_px)
        image.save(filepath)
    
    def saveAsVectorialImage(self, filepath: str, width: int) -> None:
        """ Saves a vectorial image of the QRCode resized to width_px to the path filepath. """

        writeSVG(filepath, self.matrix.data, width)
