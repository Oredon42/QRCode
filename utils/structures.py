class ErrorCorrectionLevel:
    """ Error correction levels enumeration """

    L = 0
    M = 1
    Q = 2
    H = 3
    Invalid = 4

class ModeIndicator:
    """ Bits representing data mode indicator """

    Terminator          = "0000"
    Numeric             = "0001"
    Alphanumeric        = "0010"
    StructuredAppend    = "0011"
    Byte8Bit            = "0100"
    FNC1_1              = "0101"
    ECI                 = "0111"
    Kanji               = "1000"
    FNC1_2              = "1001"
    Invalid             = "1111"

class ModuleType:
    """ Type assigned to each module during symbol building """

    Data=-1
    Dark=0
    Light=1
    FormatInformation=2
    Version=3

class GroupInformation:
    """ Stores blocks count and data codewords count for a message group """

    def __init__(self, blocks_count, data_codewords_count):
        self.blocks_count = blocks_count
        self.data_codewords_count = data_codewords_count

class DataInformation:
    """ Stores groups informations and error codewords count for a version/error correction level """

    def __init__(self, error_correction_codewords_per_block, groups_informations):
        self.error_correction_codewords_per_block = error_correction_codewords_per_block
        self.groups_informations = groups_informations
    