from image import Image

from encoder import Encoder
from matrix import Matrix

from utils.functions import getErrorCorrectionLevelFromString

class QrCode:
    """
        This class represents a QRCode, which can be generated from a text.
    """

    def __init__(self) -> None:
        self._encoder = Encoder()

    def encode(self, text: str, error_correction_level_str: str = "L") -> Image:
        """ This method encodes the text with given error correction level,
            and generates a QRCode symbol from the encoded message.
            An image of the symbol is returned. """

        error_correction_level = getErrorCorrectionLevelFromString(error_correction_level_str)
        message_bits = self._encoder.encode(text, error_correction_level)

        matrix = Matrix(message_bits, self._encoder.version, error_correction_level)
        image = Image(matrix.data)

        return image
