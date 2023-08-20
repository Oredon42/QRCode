from image import Image
from tables import ErrorCorrectionLevel

from encoder import Encoder
from matrix import Matrix

class QrCode:

    def __init__(self):
        self._encoder = Encoder()

        self.white_value = 255

        self.quiet_zone_width = 4
        self.finder_pattern_width = 7
        self.alignment_pattern_width = 5
        self.separator_width = 1

    def encode(self, text, error_correction_level=ErrorCorrectionLevel.L):

        message_bits = self._encoder.encode(text, error_correction_level)

        matrix = Matrix(message_bits, self._encoder.version, error_correction_level)
        image = Image(matrix.data)

        return image
