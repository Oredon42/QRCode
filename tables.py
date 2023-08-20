import math as m
import numpy as np

alignment_patterns_center_coordinates = [
    (), # Version 1
    (6, 18), # Version 2
    (6, 22), # Version 3
    (6, 26), # Version 4
    (6, 30), # Version 5
    (6, 34), # Version 6
    (6, 22, 38), # Version 7
    (6, 24, 42), # Version 8
    (6, 26, 46), # Version 9
    (6, 28, 50), # Version 10
    (6, 30, 54), # Version 11
    (6, 32, 58), # Version 12
    (6, 34, 62), # Version 13
    (6, 26, 46, 66), # Version 14
    (6, 26, 48, 70), # Version 15
    (6, 26, 50, 74), # Version 16
    (6, 30, 54, 78), # Version 17
    (6, 30, 46, 82), # Version 18
    (6, 30, 56, 86), # Version 19
    (6, 34, 58, 90), # Version 20
    (6, 28, 50, 72, 94), # Version 21
    (6, 26, 50, 74, 98), # Version 22
    (6, 30, 54, 78, 102), # Version 23
    (6, 28, 54, 80, 106), # Version 24
    (6, 32, 58, 84, 110), # Version 25
    (6, 30, 58, 86, 114), # Version 26
    (6, 34, 62, 90, 118), # Version 27
    (6, 26, 50, 74, 98, 122), # Version 28
    (6, 30, 54, 78, 102, 126), # Version 29
    (6, 26, 52, 78, 104, 130), # Version 30
    (6, 30, 56, 82, 108, 134), # Version 31
    (6, 34, 60, 86, 112, 138), # Version 32
    (6, 30, 58, 86, 114, 142), # Version 33
    (6, 34, 62, 90, 118, 146), # Version 34
    (6, 30, 54, 78, 102, 126, 150), # Version 35
    (6, 24, 50, 76, 102, 128, 154), # Version 36
    (6, 28, 54, 80, 106, 132, 158), # Version 37
    (6, 32, 58, 84, 110, 136, 162), # Version 38
    (6, 26, 54, 82, 110, 138, 166), # Version 39
    (6, 30, 58, 86, 114, 142, 170) # Version 40
]

class ErrorCorrectionLevel:
    L = 0
    M = 1
    Q = 2
    H = 3

class GroupInformation:
    def __init__(self, blocks_count, data_codewords_count):
        self.blocks_count = blocks_count
        self.data_codewords_count = data_codewords_count

class DataInformation:
    def __init__(self, error_correction_codewords_per_block, groups_informations):
        self.error_correction_codewords_per_block = error_correction_codewords_per_block
        self.groups_informations = groups_informations

    def getDataCapacityBits(self):
        data_capacity = 0
        for infos in self.groups_informations:
            data_capacity += infos.blocks_count * infos.data_codewords_count

        return data_capacity * 8

data_informations = {
    ErrorCorrectionLevel.L: {
        1: DataInformation(7, (GroupInformation(1, 19),)),
        2: DataInformation(10, (GroupInformation(1, 34),)),
        3: DataInformation(15, (GroupInformation(1, 55),)),
        4: DataInformation(20, (GroupInformation(1, 80),)),
        5: DataInformation(26, (GroupInformation(1, 108),)),
        6: DataInformation(18, (GroupInformation(2, 68),)),
        7: DataInformation(20, (GroupInformation(2, 78),)),
        8: DataInformation(24, (GroupInformation(2, 97),)),
        9: DataInformation(30, (GroupInformation(2, 116),)),
        10: DataInformation(18, (GroupInformation(2, 68), GroupInformation(2, 69))),
        11: DataInformation(20, (GroupInformation(4, 81),)),
        12: DataInformation(24, (GroupInformation(2, 92), GroupInformation(2, 93))),
        13: DataInformation(26, (GroupInformation(4, 107),)),
        14: DataInformation(30, (GroupInformation(3, 115), GroupInformation(1, 116))),
        15: DataInformation(22, (GroupInformation(5, 87), GroupInformation(1, 88))),
        16: DataInformation(24, (GroupInformation(5, 98), GroupInformation(1, 99))),
        17: DataInformation(28, (GroupInformation(1, 107), GroupInformation(5, 108))),
        18: DataInformation(30, (GroupInformation(5, 120), GroupInformation(1, 121))),
        19: DataInformation(28, (GroupInformation(3, 113), GroupInformation(4, 114))),
        20: DataInformation(28, (GroupInformation(3, 107), GroupInformation(5, 108))),
        21: DataInformation(28, (GroupInformation(4, 116), GroupInformation(4, 117))),
        22: DataInformation(28, (GroupInformation(2, 111), GroupInformation(7, 112))),
        23: DataInformation(30, (GroupInformation(4, 121), GroupInformation(5, 122))),
        24: DataInformation(30, (GroupInformation(6, 117), GroupInformation(4, 118))),
        25: DataInformation(26, (GroupInformation(8, 106), GroupInformation(4, 107))),
        26: DataInformation(28,  (GroupInformation(0, 114), GroupInformation(2, 115))),
        27: DataInformation(30, (GroupInformation(8, 122), GroupInformation(4, 123))),
        28: DataInformation(30, (GroupInformation(3, 117), GroupInformation(10, 118))),
        29: DataInformation(30, (GroupInformation(7, 116), GroupInformation(7, 117))),
        30: DataInformation(30, (GroupInformation(5, 115), GroupInformation(10, 116))),
        31: DataInformation(30,  (GroupInformation(3, 115), GroupInformation(3, 116))),
        32: DataInformation(30,  (GroupInformation(7, 115),)),
        33: DataInformation(30,  (GroupInformation(7, 115), GroupInformation(1, 116))),
        34: DataInformation(30,  (GroupInformation(3, 115), GroupInformation(6, 116))),
        35: DataInformation(30,  (GroupInformation(2, 121), GroupInformation(7, 122))),
        36: DataInformation(30, (GroupInformation(6, 121), GroupInformation(14, 122))),
        37: DataInformation(30,  (GroupInformation(7, 122), GroupInformation(4, 123))),
        38: DataInformation(30, (GroupInformation(4, 122), GroupInformation(18, 123))),
        39: DataInformation(30,  (GroupInformation(0, 117), GroupInformation(4, 118))),
        40: DataInformation(30,  (GroupInformation(9, 118), GroupInformation(6, 119)))
    },
    ErrorCorrectionLevel.M: {
        1: DataInformation(10, (GroupInformation(1, 16),)),
        2: DataInformation(16, (GroupInformation(1, 28),)),
        3: DataInformation(26, (GroupInformation(1, 44),)),
        4: DataInformation(18, (GroupInformation(2, 32),)),
        5: DataInformation(24, (GroupInformation(2, 43),)),
        6: DataInformation(16, (GroupInformation(4, 27),)),
        7: DataInformation(18, (GroupInformation(4, 31),)),
        8: DataInformation(22, (GroupInformation(2, 38), GroupInformation(2, 39))),
        9: DataInformation(22, (GroupInformation(3, 36), GroupInformation(2, 37))),
        10: DataInformation(26, (GroupInformation(4, 43), GroupInformation(1, 44))),
        11: DataInformation(30, (GroupInformation(1, 50), GroupInformation(4, 51))),
        12: DataInformation(22, (GroupInformation(6, 36), GroupInformation(2, 37))),
        13: DataInformation(22, (GroupInformation(8, 37), GroupInformation(1, 38))),
        14: DataInformation(24, (GroupInformation(4, 40), GroupInformation(5, 41))),
        15: DataInformation(24, (GroupInformation(5, 41), GroupInformation(5, 42))),
        16: DataInformation(28, (GroupInformation(7, 45), GroupInformation(3, 46))),
        17: DataInformation(28, (GroupInformation(10, 46), GroupInformation(1, 47))),
        18: DataInformation(26, (GroupInformation(9, 43), GroupInformation(4, 44))),
        19: DataInformation(26, (GroupInformation(3, 44), GroupInformation(11, 45))),
        20: DataInformation(26, (GroupInformation(3, 41), GroupInformation(13, 42))),
        21: DataInformation(26, (GroupInformation(17, 42),)),
        22: DataInformation(28, (GroupInformation(17, 46),)),
        23: DataInformation(28, (GroupInformation(4, 47), GroupInformation(14, 48))),
        24: DataInformation(28, (GroupInformation(6, 45), GroupInformation(14, 46))),
        25: DataInformation(28, (GroupInformation(8, 47), GroupInformation(13, 48))),
        26: DataInformation(28, (GroupInformation(19, 46), GroupInformation(4, 47))),
        27: DataInformation(28, (GroupInformation(22, 45), GroupInformation(3, 46))),
        28: DataInformation(28, (GroupInformation(3, 45), GroupInformation(23, 46))),
        29: DataInformation(28, (GroupInformation(21, 45), GroupInformation(7, 46))),
        30: DataInformation(28, (GroupInformation(19, 47), GroupInformation(10, 48))),
        31: DataInformation(28, (GroupInformation(2, 46), GroupInformation(29, 47))),
        32: DataInformation(28, (GroupInformation(10, 46), GroupInformation(23, 47))),
        33: DataInformation(28, (GroupInformation(14, 46), GroupInformation(21, 47))),
        34: DataInformation(28, (GroupInformation(14, 46), GroupInformation(23, 47))),
        35: DataInformation(28, (GroupInformation(12, 47), GroupInformation(26, 48))),
        36: DataInformation(28, (GroupInformation(6, 47), GroupInformation(34, 48))),
        37: DataInformation(28, (GroupInformation(29, 46), GroupInformation(14, 47))),
        38: DataInformation(28, (GroupInformation(13, 46), GroupInformation(32, 47))),
        39: DataInformation(28, (GroupInformation(40, 47), GroupInformation(7, 48))),
        40: DataInformation(28, (GroupInformation(18, 47), GroupInformation(31, 48)))
    },
    ErrorCorrectionLevel.Q: {
        1: DataInformation(13, (GroupInformation(1, 13),)),
        2: DataInformation(22, (GroupInformation(1, 22),)),
        3: DataInformation(18, (GroupInformation(2, 17),)),
        4: DataInformation(26, (GroupInformation(2, 24),)),
        5: DataInformation(18, (GroupInformation(2, 15), GroupInformation(2, 16))),
        6: DataInformation(24, (GroupInformation(4, 19),)),
        7: DataInformation(18, (GroupInformation(2, 14), GroupInformation(4, 15))),
        8: DataInformation(22, (GroupInformation(4, 18), GroupInformation(2, 19))),
        9: DataInformation(20, (GroupInformation(4, 16), GroupInformation(4, 17))),
        10: DataInformation(24, (GroupInformation(6, 19), GroupInformation(2, 20))),
        11: DataInformation(28, (GroupInformation(4, 22), GroupInformation(4, 23))),
        12: DataInformation(26, (GroupInformation(4, 20), GroupInformation(6, 21))),
        13: DataInformation(24, (GroupInformation(8, 20), GroupInformation(4, 21))),
        14: DataInformation(20, (GroupInformation(11, 16), GroupInformation(5, 17))),
        15: DataInformation(30, (GroupInformation(5, 24), GroupInformation(7, 25))),
        16: DataInformation(24, (GroupInformation(15, 19), GroupInformation(2, 20))),
        17: DataInformation(28, (GroupInformation(1, 22), GroupInformation(15, 23))),
        18: DataInformation(28, (GroupInformation(17, 22), GroupInformation(1, 23))),
        19: DataInformation(26, (GroupInformation(17, 21), GroupInformation(4, 22))),
        20: DataInformation(30, (GroupInformation(15, 24), GroupInformation(5, 25))),
        21: DataInformation(28, (GroupInformation(17, 22), GroupInformation(6, 23))),
        22: DataInformation(30, (GroupInformation(7, 24), GroupInformation(16, 25))),
        23: DataInformation(30, (GroupInformation(11, 24), GroupInformation(14, 25))),
        24: DataInformation(30, (GroupInformation(11, 24), GroupInformation(16, 25))),
        25: DataInformation(30, (GroupInformation(7, 24), GroupInformation(22, 25))),
        26: DataInformation(28, (GroupInformation(28, 22), GroupInformation(6, 23))),
        27: DataInformation(30, (GroupInformation(8, 23), GroupInformation(26, 24))),
        28: DataInformation(30, (GroupInformation(4, 24), GroupInformation(31, 25))),
        29: DataInformation(30, (GroupInformation(1, 23), GroupInformation(37, 24))),
        30: DataInformation(30, (GroupInformation(15, 24), GroupInformation(25, 25))),
        31: DataInformation(30, (GroupInformation(42, 24), GroupInformation(1, 25))),
        32: DataInformation(30, (GroupInformation(10, 24), GroupInformation(35, 25))),
        33: DataInformation(30, (GroupInformation(29, 24), GroupInformation(19, 25))),
        34: DataInformation(30, (GroupInformation(44, 24), GroupInformation(7, 25))),
        35: DataInformation(30, (GroupInformation(39, 24), GroupInformation(14, 25))),
        36: DataInformation(30, (GroupInformation(46, 24), GroupInformation(10, 25))),
        37: DataInformation(30, (GroupInformation(49, 24), GroupInformation(10, 25))),
        38: DataInformation(30, (GroupInformation(48, 24), GroupInformation(14, 25))),
        39: DataInformation(30, (GroupInformation(43, 24), GroupInformation(22, 25))),
        40: DataInformation(30, (GroupInformation(34, 24), GroupInformation(34, 25)))
    },
    ErrorCorrectionLevel.H: {
        1: DataInformation(17, (GroupInformation(1, 9),)),
        2: DataInformation(28, (GroupInformation(1, 16),)),
        3: DataInformation(22, (GroupInformation(2, 13),)),
        4: DataInformation(16, (GroupInformation(4, 9),)),
        5: DataInformation(22, (GroupInformation(2, 11), GroupInformation(2, 12))),
        6: DataInformation(28, (GroupInformation(4, 15),)),
        7: DataInformation(26, (GroupInformation(4, 13), GroupInformation(1, 14))),
        8: DataInformation(26, (GroupInformation(4, 14), GroupInformation(2, 15))),
        9: DataInformation(24, (GroupInformation(4, 12), GroupInformation(4, 13))),
        10: DataInformation(28, (GroupInformation(6, 15), GroupInformation(2, 16))),
        11: DataInformation(24, (GroupInformation(3, 12), GroupInformation(8, 13))),
        12: DataInformation(28, (GroupInformation(7, 14), GroupInformation(4, 15))),
        13: DataInformation(22, (GroupInformation(12, 11), GroupInformation(4, 12))),
        14: DataInformation(24, (GroupInformation(11, 12), GroupInformation(5, 13))),
        15: DataInformation(24, (GroupInformation(11, 12), GroupInformation(7, 13))),
        16: DataInformation(30, (GroupInformation(3, 15), GroupInformation(13, 16))),
        17: DataInformation(28, (GroupInformation(2, 14), GroupInformation(17, 15))),
        18: DataInformation(28, (GroupInformation(2, 14), GroupInformation(19, 15))),
        19: DataInformation(26, (GroupInformation(9, 13), GroupInformation(16, 14))),
        20: DataInformation(28, (GroupInformation(15, 15), GroupInformation(10, 16))),
        21: DataInformation(30, (GroupInformation(19, 16), GroupInformation(6, 17))),
        22: DataInformation(24, (GroupInformation(34, 13),)),
        23: DataInformation(30, (GroupInformation(16, 15), GroupInformation(14, 16))),
        24: DataInformation(30, (GroupInformation(30, 16), GroupInformation(2, 17))),
        25: DataInformation(30, (GroupInformation(22, 15), GroupInformation(13, 16))),
        26: DataInformation(30, (GroupInformation(33, 16), GroupInformation(4, 17))),
        27: DataInformation(30, (GroupInformation(12, 15), GroupInformation(28, 16))),
        28: DataInformation(30, (GroupInformation(11, 15), GroupInformation(31, 16))),
        29: DataInformation(30, (GroupInformation(19, 15), GroupInformation(26, 16))),
        30: DataInformation(30, (GroupInformation(23, 15), GroupInformation(25, 16))),
        31: DataInformation(30, (GroupInformation(23, 15), GroupInformation(28, 16))),
        32: DataInformation(30, (GroupInformation(19, 15), GroupInformation(35, 16))),
        33: DataInformation(30, (GroupInformation(11, 15), GroupInformation(46, 16))),
        34: DataInformation(30, (GroupInformation(59, 16), GroupInformation(1, 17))),
        35: DataInformation(30, (GroupInformation(22, 15), GroupInformation(41, 16))),
        36: DataInformation(30, (GroupInformation(2, 15), GroupInformation(64, 16))),
        37: DataInformation(30, (GroupInformation(24, 15), GroupInformation(46, 16))),
        38: DataInformation(30, (GroupInformation(42, 15), GroupInformation(32, 16))),
        39: DataInformation(30, (GroupInformation(10, 15), GroupInformation(67, 16))),
        40: DataInformation(30, (GroupInformation(20, 15), GroupInformation(61, 16)))
    }
}

symbol_remainder_bits = {
    1: 0,
    2: 7,
    3: 7,
    4: 7,
    5: 7,
    6: 7,
    7: 0,
    8: 0,
    9: 0,
    10: 0,
    11: 0,
    12: 0,
    13: 0,
    14: 3,
    15: 3,
    16: 3,
    17: 3,
    18: 3,
    19: 3,
    20: 3,
    21: 4,
    22: 4,
    23: 4,
    24: 4,
    25: 4,
    26: 4,
    27: 4,
    28: 3,
    29: 3,
    30: 3,
    31: 3,
    32: 3,
    33: 3,
    34: 3,
    35: 0,
    36: 0,
    37: 0,
    38: 0,
    39: 0,
    40: 0
}

symbol_capacity_codewords = {
    1: 26,
    2: 44,
    3: 70,
    4: 100,
    5: 134,
    6: 172,
    7: 196,
    8: 242,
    9: 292,
    10: 346,
    11: 404,
    12: 466,
    13: 532,
    14: 581,
    15: 655,
    16: 733,
    17: 815,
    18: 901,
    19: 991,
    20: 1085,
    21: 1156,
    22: 1258,
    23: 1364,
    24: 1474,
    25: 1588,
    26: 1706,
    27: 1828,
    28: 1921,
    29: 2051,
    30: 2185,
    31: 2323,
    32: 2465,
    33: 2611,
    34: 2761,
    35: 2876,
    36: 3034,
    37: 3196,
    38: 3362,
    39: 3532,
    40: 3706
}

alphanumeric_encoding_table = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'A': 10,
    'B': 11,
    'C': 12,
    'D': 13,
    'E': 14,
    'F': 15,
    'G': 16,
    'H': 17,
    'I': 18,
    'J': 19,
    'K': 20,
    'L': 21,
    'M': 22,
    'N': 23,
    'O': 24,
    'P': 25,
    'Q': 26,
    'R': 27,
    'S': 28,
    'T': 29,
    'U': 30,
    'V': 31,
    'W': 32,
    'X': 33,
    'Y': 34,
    'Z': 35,
    ' ': 36,
    '$': 37,
    '%': 38,
    '*': 39,
    '+': 40,
    '-': 41,
    '.': 42,
    '/': 43,
    ':': 44
}

class ModeIndicator:
    Terminator          = '0000'
    Numeric             = '0001'
    Alphanumeric        = '0010'
    StructuredAppend    = '0011'
    Byte8Bit            = '0100'
    FNC1_1              = '0101'
    ECI                 = '0111'
    Kanji               = '1000'
    FNC1_2              = '1001'

# Character count bytes stream size in bits depending on version:
#  -1st element: version 1 to 9
#  -2nd element: version 10 to 26
#  -3rd element: version 27 to 40
character_count_number_of_bits = {
    ModeIndicator.Numeric: [10, 12, 14],
    ModeIndicator.Alphanumeric: [9, 11, 13],
    ModeIndicator.Byte8Bit: [8, 16, 16],
    ModeIndicator.Kanji: [8, 10, 12]
}

symbol_capacity_characters = {
    ErrorCorrectionLevel.L:
    {
        1: {ModeIndicator.Numeric: 41, ModeIndicator.Alphanumeric: 25, ModeIndicator.Byte8Bit: 17, ModeIndicator.Kanji: 10},
        2: {ModeIndicator.Numeric: 77, ModeIndicator.Alphanumeric: 47, ModeIndicator.Byte8Bit: 32, ModeIndicator.Kanji: 20},
        3: {ModeIndicator.Numeric: 127, ModeIndicator.Alphanumeric: 77, ModeIndicator.Byte8Bit: 53, ModeIndicator.Kanji: 32},
        4: {ModeIndicator.Numeric: 187, ModeIndicator.Alphanumeric: 114, ModeIndicator.Byte8Bit: 78, ModeIndicator.Kanji: 48},
        5: {ModeIndicator.Numeric: 255, ModeIndicator.Alphanumeric: 154, ModeIndicator.Byte8Bit: 106, ModeIndicator.Kanji: 65},
        6: {ModeIndicator.Numeric: 322, ModeIndicator.Alphanumeric: 195, ModeIndicator.Byte8Bit: 134, ModeIndicator.Kanji: 82},
        7: {ModeIndicator.Numeric: 370, ModeIndicator.Alphanumeric: 224, ModeIndicator.Byte8Bit: 154, ModeIndicator.Kanji: 95},
        8: {ModeIndicator.Numeric: 461, ModeIndicator.Alphanumeric: 279, ModeIndicator.Byte8Bit: 192, ModeIndicator.Kanji: 118},
        9: {ModeIndicator.Numeric: 552, ModeIndicator.Alphanumeric: 335, ModeIndicator.Byte8Bit: 230, ModeIndicator.Kanji: 141},
        10: {ModeIndicator.Numeric: 652, ModeIndicator.Alphanumeric: 395, ModeIndicator.Byte8Bit: 271, ModeIndicator.Kanji: 167},
        11: {ModeIndicator.Numeric: 772, ModeIndicator.Alphanumeric: 468, ModeIndicator.Byte8Bit: 321, ModeIndicator.Kanji: 198},
        12: {ModeIndicator.Numeric: 883, ModeIndicator.Alphanumeric: 535, ModeIndicator.Byte8Bit: 367, ModeIndicator.Kanji: 226},
        13: {ModeIndicator.Numeric: 1022, ModeIndicator.Alphanumeric: 619, ModeIndicator.Byte8Bit: 425, ModeIndicator.Kanji: 262},
        14: {ModeIndicator.Numeric: 1101, ModeIndicator.Alphanumeric: 667, ModeIndicator.Byte8Bit: 458, ModeIndicator.Kanji: 282},
        15: {ModeIndicator.Numeric: 1250, ModeIndicator.Alphanumeric: 758, ModeIndicator.Byte8Bit: 520, ModeIndicator.Kanji: 320},
        16: {ModeIndicator.Numeric: 1408, ModeIndicator.Alphanumeric: 854, ModeIndicator.Byte8Bit: 586, ModeIndicator.Kanji: 361},
        17: {ModeIndicator.Numeric: 1548, ModeIndicator.Alphanumeric: 938, ModeIndicator.Byte8Bit: 644, ModeIndicator.Kanji: 397},
        18: {ModeIndicator.Numeric: 1725, ModeIndicator.Alphanumeric: 1046, ModeIndicator.Byte8Bit: 718, ModeIndicator.Kanji: 442},
        19: {ModeIndicator.Numeric: 1903, ModeIndicator.Alphanumeric: 1153, ModeIndicator.Byte8Bit: 792, ModeIndicator.Kanji: 488},
        20: {ModeIndicator.Numeric: 2061, ModeIndicator.Alphanumeric: 1249, ModeIndicator.Byte8Bit: 858, ModeIndicator.Kanji: 528},
        21: {ModeIndicator.Numeric: 2232, ModeIndicator.Alphanumeric: 1352, ModeIndicator.Byte8Bit: 929, ModeIndicator.Kanji: 572},
        22: {ModeIndicator.Numeric: 2409, ModeIndicator.Alphanumeric: 1460, ModeIndicator.Byte8Bit: 1003, ModeIndicator.Kanji: 618},
        23: {ModeIndicator.Numeric: 2620, ModeIndicator.Alphanumeric: 1588, ModeIndicator.Byte8Bit: 1091, ModeIndicator.Kanji: 672},
        24: {ModeIndicator.Numeric: 2812, ModeIndicator.Alphanumeric: 1704, ModeIndicator.Byte8Bit: 1171, ModeIndicator.Kanji: 721},
        25: {ModeIndicator.Numeric: 3057, ModeIndicator.Alphanumeric: 1853, ModeIndicator.Byte8Bit: 1273, ModeIndicator.Kanji: 784},
        26: {ModeIndicator.Numeric: 3283, ModeIndicator.Alphanumeric: 1990, ModeIndicator.Byte8Bit: 1367, ModeIndicator.Kanji: 842},
        27: {ModeIndicator.Numeric: 3517, ModeIndicator.Alphanumeric: 2132, ModeIndicator.Byte8Bit: 1465, ModeIndicator.Kanji: 902},
        28: {ModeIndicator.Numeric: 3669, ModeIndicator.Alphanumeric: 2223, ModeIndicator.Byte8Bit: 1528, ModeIndicator.Kanji: 940},
        29: {ModeIndicator.Numeric: 3909, ModeIndicator.Alphanumeric: 2369, ModeIndicator.Byte8Bit: 1628, ModeIndicator.Kanji: 1002},
        30: {ModeIndicator.Numeric: 4158, ModeIndicator.Alphanumeric: 2520, ModeIndicator.Byte8Bit: 1732, ModeIndicator.Kanji: 1066},
        31: {ModeIndicator.Numeric: 4417, ModeIndicator.Alphanumeric: 2677, ModeIndicator.Byte8Bit: 1840, ModeIndicator.Kanji: 1132},
        32: {ModeIndicator.Numeric: 4686, ModeIndicator.Alphanumeric: 2840, ModeIndicator.Byte8Bit: 1952, ModeIndicator.Kanji: 1201},
        33: {ModeIndicator.Numeric: 4965, ModeIndicator.Alphanumeric: 3009, ModeIndicator.Byte8Bit: 2068, ModeIndicator.Kanji: 1273},
        34: {ModeIndicator.Numeric: 5253, ModeIndicator.Alphanumeric: 3183, ModeIndicator.Byte8Bit: 2188, ModeIndicator.Kanji: 1347},
        35: {ModeIndicator.Numeric: 5529, ModeIndicator.Alphanumeric: 3351, ModeIndicator.Byte8Bit: 2303, ModeIndicator.Kanji: 1417},
        36: {ModeIndicator.Numeric: 5836, ModeIndicator.Alphanumeric: 3537, ModeIndicator.Byte8Bit: 2431, ModeIndicator.Kanji: 1496},
        37: {ModeIndicator.Numeric: 6153, ModeIndicator.Alphanumeric: 3729, ModeIndicator.Byte8Bit: 2563, ModeIndicator.Kanji: 1577},
        38: {ModeIndicator.Numeric: 6479, ModeIndicator.Alphanumeric: 3927, ModeIndicator.Byte8Bit: 2699, ModeIndicator.Kanji: 1661},
        39: {ModeIndicator.Numeric: 6743, ModeIndicator.Alphanumeric: 4087, ModeIndicator.Byte8Bit: 2809, ModeIndicator.Kanji: 1729},
        40: {ModeIndicator.Numeric: 7089, ModeIndicator.Alphanumeric: 4296, ModeIndicator.Byte8Bit: 2953, ModeIndicator.Kanji: 1817}
   },
    ErrorCorrectionLevel.M:
    {
        1: {ModeIndicator.Numeric: 34, ModeIndicator.Alphanumeric: 20, ModeIndicator.Byte8Bit: 14, ModeIndicator.Kanji: 8},
        2: {ModeIndicator.Numeric: 63, ModeIndicator.Alphanumeric: 38, ModeIndicator.Byte8Bit: 26, ModeIndicator.Kanji: 16},
        3: {ModeIndicator.Numeric: 101, ModeIndicator.Alphanumeric: 61, ModeIndicator.Byte8Bit: 42, ModeIndicator.Kanji: 26},
        4: {ModeIndicator.Numeric: 149, ModeIndicator.Alphanumeric: 90, ModeIndicator.Byte8Bit: 62, ModeIndicator.Kanji: 38},
        5: {ModeIndicator.Numeric: 202, ModeIndicator.Alphanumeric: 122, ModeIndicator.Byte8Bit: 84, ModeIndicator.Kanji: 52},
        6: {ModeIndicator.Numeric: 255, ModeIndicator.Alphanumeric: 154, ModeIndicator.Byte8Bit: 106, ModeIndicator.Kanji: 65},
        7: {ModeIndicator.Numeric: 293, ModeIndicator.Alphanumeric: 178, ModeIndicator.Byte8Bit: 122, ModeIndicator.Kanji: 75},
        8: {ModeIndicator.Numeric: 365, ModeIndicator.Alphanumeric: 221, ModeIndicator.Byte8Bit: 152, ModeIndicator.Kanji: 93},
        9: {ModeIndicator.Numeric: 432, ModeIndicator.Alphanumeric: 262, ModeIndicator.Byte8Bit: 180, ModeIndicator.Kanji: 111},
        10: {ModeIndicator.Numeric: 513, ModeIndicator.Alphanumeric: 311, ModeIndicator.Byte8Bit: 213, ModeIndicator.Kanji: 131},
        11: {ModeIndicator.Numeric: 604, ModeIndicator.Alphanumeric: 366, ModeIndicator.Byte8Bit: 251, ModeIndicator.Kanji: 155},
        12: {ModeIndicator.Numeric: 691, ModeIndicator.Alphanumeric: 419, ModeIndicator.Byte8Bit: 287, ModeIndicator.Kanji: 177},
        13: {ModeIndicator.Numeric: 796, ModeIndicator.Alphanumeric: 483, ModeIndicator.Byte8Bit: 331, ModeIndicator.Kanji: 204},
        14: {ModeIndicator.Numeric: 871, ModeIndicator.Alphanumeric: 528, ModeIndicator.Byte8Bit: 362, ModeIndicator.Kanji: 223},
        15: {ModeIndicator.Numeric: 991, ModeIndicator.Alphanumeric: 600, ModeIndicator.Byte8Bit: 412, ModeIndicator.Kanji: 254},
        16: {ModeIndicator.Numeric: 1082, ModeIndicator.Alphanumeric: 656, ModeIndicator.Byte8Bit: 450, ModeIndicator.Kanji: 277},
        17: {ModeIndicator.Numeric: 1212, ModeIndicator.Alphanumeric: 734, ModeIndicator.Byte8Bit: 504, ModeIndicator.Kanji: 310},
        18: {ModeIndicator.Numeric: 1346, ModeIndicator.Alphanumeric: 816, ModeIndicator.Byte8Bit: 560, ModeIndicator.Kanji: 345},
        19: {ModeIndicator.Numeric: 1500, ModeIndicator.Alphanumeric: 909, ModeIndicator.Byte8Bit: 624, ModeIndicator.Kanji: 384},
        20: {ModeIndicator.Numeric: 1600, ModeIndicator.Alphanumeric: 970, ModeIndicator.Byte8Bit: 666, ModeIndicator.Kanji: 410},
        21: {ModeIndicator.Numeric: 1708, ModeIndicator.Alphanumeric: 1035, ModeIndicator.Byte8Bit: 711, ModeIndicator.Kanji: 438},
        22: {ModeIndicator.Numeric: 1872, ModeIndicator.Alphanumeric: 1134, ModeIndicator.Byte8Bit: 779, ModeIndicator.Kanji: 480},
        23: {ModeIndicator.Numeric: 2059, ModeIndicator.Alphanumeric: 1248, ModeIndicator.Byte8Bit: 857, ModeIndicator.Kanji: 528},
        24: {ModeIndicator.Numeric: 2188, ModeIndicator.Alphanumeric: 1326, ModeIndicator.Byte8Bit: 911, ModeIndicator.Kanji: 561},
        25: {ModeIndicator.Numeric: 2395, ModeIndicator.Alphanumeric: 1451, ModeIndicator.Byte8Bit: 997, ModeIndicator.Kanji: 614},
        26: {ModeIndicator.Numeric: 2544, ModeIndicator.Alphanumeric: 1542, ModeIndicator.Byte8Bit: 1059, ModeIndicator.Kanji: 652},
        27: {ModeIndicator.Numeric: 2701, ModeIndicator.Alphanumeric: 1637, ModeIndicator.Byte8Bit: 1125, ModeIndicator.Kanji: 692},
        28: {ModeIndicator.Numeric: 2857, ModeIndicator.Alphanumeric: 1732, ModeIndicator.Byte8Bit: 1190, ModeIndicator.Kanji: 732},
        29: {ModeIndicator.Numeric: 3035, ModeIndicator.Alphanumeric: 1839, ModeIndicator.Byte8Bit: 1264, ModeIndicator.Kanji: 778},
        30: {ModeIndicator.Numeric: 3289, ModeIndicator.Alphanumeric: 1994, ModeIndicator.Byte8Bit: 1370, ModeIndicator.Kanji: 843},
        31: {ModeIndicator.Numeric: 3486, ModeIndicator.Alphanumeric: 2113, ModeIndicator.Byte8Bit: 1452, ModeIndicator.Kanji: 894},
        32: {ModeIndicator.Numeric: 3693, ModeIndicator.Alphanumeric: 2238, ModeIndicator.Byte8Bit: 1538, ModeIndicator.Kanji: 947},
        33: {ModeIndicator.Numeric: 3909, ModeIndicator.Alphanumeric: 2369, ModeIndicator.Byte8Bit: 1628, ModeIndicator.Kanji: 1002},
        34: {ModeIndicator.Numeric: 4134, ModeIndicator.Alphanumeric: 2506, ModeIndicator.Byte8Bit: 1722, ModeIndicator.Kanji: 1060},
        35: {ModeIndicator.Numeric: 4343, ModeIndicator.Alphanumeric: 2632, ModeIndicator.Byte8Bit: 1809, ModeIndicator.Kanji: 1113},
        36: {ModeIndicator.Numeric: 4588, ModeIndicator.Alphanumeric: 2780, ModeIndicator.Byte8Bit: 1911, ModeIndicator.Kanji: 1176},
        37: {ModeIndicator.Numeric: 4775, ModeIndicator.Alphanumeric: 2894, ModeIndicator.Byte8Bit: 1989, ModeIndicator.Kanji: 1224},
        38: {ModeIndicator.Numeric: 5039, ModeIndicator.Alphanumeric: 3054, ModeIndicator.Byte8Bit: 2099, ModeIndicator.Kanji: 1292},
        39: {ModeIndicator.Numeric: 5313, ModeIndicator.Alphanumeric: 3220, ModeIndicator.Byte8Bit: 2213, ModeIndicator.Kanji: 1362},
        40: {ModeIndicator.Numeric: 5596, ModeIndicator.Alphanumeric: 3391, ModeIndicator.Byte8Bit: 2331, ModeIndicator.Kanji: 1435}
    },
    ErrorCorrectionLevel.Q:
    {
        1: {ModeIndicator.Numeric: 27, ModeIndicator.Alphanumeric: 16, ModeIndicator.Byte8Bit: 11, ModeIndicator.Kanji: 7},
        2: {ModeIndicator.Numeric: 48, ModeIndicator.Alphanumeric: 29, ModeIndicator.Byte8Bit: 20, ModeIndicator.Kanji: 12},
        3: {ModeIndicator.Numeric: 77, ModeIndicator.Alphanumeric: 47, ModeIndicator.Byte8Bit: 32, ModeIndicator.Kanji: 20},
        4: {ModeIndicator.Numeric: 111, ModeIndicator.Alphanumeric: 67, ModeIndicator.Byte8Bit: 46, ModeIndicator.Kanji: 28},
        5: {ModeIndicator.Numeric: 144, ModeIndicator.Alphanumeric: 87, ModeIndicator.Byte8Bit: 60, ModeIndicator.Kanji: 37},
        6: {ModeIndicator.Numeric: 178, ModeIndicator.Alphanumeric: 108, ModeIndicator.Byte8Bit: 74, ModeIndicator.Kanji: 45},
        7: {ModeIndicator.Numeric: 207, ModeIndicator.Alphanumeric: 125, ModeIndicator.Byte8Bit: 86, ModeIndicator.Kanji: 53},
        8: {ModeIndicator.Numeric: 259, ModeIndicator.Alphanumeric: 157, ModeIndicator.Byte8Bit: 108, ModeIndicator.Kanji: 66},
        9: {ModeIndicator.Numeric: 312, ModeIndicator.Alphanumeric: 189, ModeIndicator.Byte8Bit: 130, ModeIndicator.Kanji: 80},
        10: {ModeIndicator.Numeric: 364, ModeIndicator.Alphanumeric: 221, ModeIndicator.Byte8Bit: 151, ModeIndicator.Kanji: 93},
        11: {ModeIndicator.Numeric: 427, ModeIndicator.Alphanumeric: 259, ModeIndicator.Byte8Bit: 177, ModeIndicator.Kanji: 109},
        12: {ModeIndicator.Numeric: 489, ModeIndicator.Alphanumeric: 296, ModeIndicator.Byte8Bit: 203, ModeIndicator.Kanji: 125},
        13: {ModeIndicator.Numeric: 580, ModeIndicator.Alphanumeric: 352, ModeIndicator.Byte8Bit: 241, ModeIndicator.Kanji: 149},
        14: {ModeIndicator.Numeric: 621, ModeIndicator.Alphanumeric: 376, ModeIndicator.Byte8Bit: 258, ModeIndicator.Kanji: 159},
        15: {ModeIndicator.Numeric: 703, ModeIndicator.Alphanumeric: 426, ModeIndicator.Byte8Bit: 292, ModeIndicator.Kanji: 180},
        16: {ModeIndicator.Numeric: 775, ModeIndicator.Alphanumeric: 470, ModeIndicator.Byte8Bit: 322, ModeIndicator.Kanji: 198},
        17: {ModeIndicator.Numeric: 876, ModeIndicator.Alphanumeric: 531, ModeIndicator.Byte8Bit: 364, ModeIndicator.Kanji: 224},
        18: {ModeIndicator.Numeric: 948, ModeIndicator.Alphanumeric: 574, ModeIndicator.Byte8Bit: 394, ModeIndicator.Kanji: 243},
        19: {ModeIndicator.Numeric: 1063, ModeIndicator.Alphanumeric: 644, ModeIndicator.Byte8Bit: 442, ModeIndicator.Kanji: 272},
        20: {ModeIndicator.Numeric: 1159, ModeIndicator.Alphanumeric: 702, ModeIndicator.Byte8Bit: 482, ModeIndicator.Kanji: 297},
        21: {ModeIndicator.Numeric: 1224, ModeIndicator.Alphanumeric: 742, ModeIndicator.Byte8Bit: 509, ModeIndicator.Kanji: 314},
        22: {ModeIndicator.Numeric: 1358, ModeIndicator.Alphanumeric: 823, ModeIndicator.Byte8Bit: 565, ModeIndicator.Kanji: 348},
        23: {ModeIndicator.Numeric: 1468, ModeIndicator.Alphanumeric: 890, ModeIndicator.Byte8Bit: 611, ModeIndicator.Kanji: 376},
        24: {ModeIndicator.Numeric: 1588, ModeIndicator.Alphanumeric: 963, ModeIndicator.Byte8Bit: 661, ModeIndicator.Kanji: 407},
        25: {ModeIndicator.Numeric: 1718, ModeIndicator.Alphanumeric: 1041, ModeIndicator.Byte8Bit: 715, ModeIndicator.Kanji: 440},
        26: {ModeIndicator.Numeric: 1804, ModeIndicator.Alphanumeric: 1094, ModeIndicator.Byte8Bit: 751, ModeIndicator.Kanji: 462},
        27: {ModeIndicator.Numeric: 1933, ModeIndicator.Alphanumeric: 1172, ModeIndicator.Byte8Bit: 805, ModeIndicator.Kanji: 496},
        28: {ModeIndicator.Numeric: 2085, ModeIndicator.Alphanumeric: 1263, ModeIndicator.Byte8Bit: 868, ModeIndicator.Kanji: 534},
        29: {ModeIndicator.Numeric: 2181, ModeIndicator.Alphanumeric: 1322, ModeIndicator.Byte8Bit: 908, ModeIndicator.Kanji: 559},
        30: {ModeIndicator.Numeric: 2358, ModeIndicator.Alphanumeric: 1429, ModeIndicator.Byte8Bit: 982, ModeIndicator.Kanji: 604},
        31: {ModeIndicator.Numeric: 2473, ModeIndicator.Alphanumeric: 1499, ModeIndicator.Byte8Bit: 1030, ModeIndicator.Kanji: 634},
        32: {ModeIndicator.Numeric: 2670, ModeIndicator.Alphanumeric: 1618, ModeIndicator.Byte8Bit: 1112, ModeIndicator.Kanji: 684},
        33: {ModeIndicator.Numeric: 2805, ModeIndicator.Alphanumeric: 1700, ModeIndicator.Byte8Bit: 1168, ModeIndicator.Kanji: 719},
        34: {ModeIndicator.Numeric: 2949, ModeIndicator.Alphanumeric: 1787, ModeIndicator.Byte8Bit: 1228, ModeIndicator.Kanji: 756},
        35: {ModeIndicator.Numeric: 3081, ModeIndicator.Alphanumeric: 1867, ModeIndicator.Byte8Bit: 1283, ModeIndicator.Kanji: 790},
        36: {ModeIndicator.Numeric: 3244, ModeIndicator.Alphanumeric: 1966, ModeIndicator.Byte8Bit: 1351, ModeIndicator.Kanji: 832},
        37: {ModeIndicator.Numeric: 3417, ModeIndicator.Alphanumeric: 2071, ModeIndicator.Byte8Bit: 1423, ModeIndicator.Kanji: 876},
        38: {ModeIndicator.Numeric: 3599, ModeIndicator.Alphanumeric: 2181, ModeIndicator.Byte8Bit: 1499, ModeIndicator.Kanji: 923},
        39: {ModeIndicator.Numeric: 3791, ModeIndicator.Alphanumeric: 2298, ModeIndicator.Byte8Bit: 1579, ModeIndicator.Kanji: 972},
        40: {ModeIndicator.Numeric: 3993, ModeIndicator.Alphanumeric: 2420, ModeIndicator.Byte8Bit: 1663, ModeIndicator.Kanji: 1024}
    },
    ErrorCorrectionLevel.H:
    {
        1: {ModeIndicator.Numeric: 17, ModeIndicator.Alphanumeric: 10, ModeIndicator.Byte8Bit: 7, ModeIndicator.Kanji: 4},
        2: {ModeIndicator.Numeric: 34, ModeIndicator.Alphanumeric: 20, ModeIndicator.Byte8Bit: 14, ModeIndicator.Kanji: 8},
        3: {ModeIndicator.Numeric: 58, ModeIndicator.Alphanumeric: 35, ModeIndicator.Byte8Bit: 24, ModeIndicator.Kanji: 15},
        4: {ModeIndicator.Numeric: 82, ModeIndicator.Alphanumeric: 50, ModeIndicator.Byte8Bit: 34, ModeIndicator.Kanji: 21},
        5: {ModeIndicator.Numeric: 106, ModeIndicator.Alphanumeric: 64, ModeIndicator.Byte8Bit: 44, ModeIndicator.Kanji: 27},
        6: {ModeIndicator.Numeric: 139, ModeIndicator.Alphanumeric: 84, ModeIndicator.Byte8Bit: 58, ModeIndicator.Kanji: 36},
        7: {ModeIndicator.Numeric: 154, ModeIndicator.Alphanumeric: 93, ModeIndicator.Byte8Bit: 64, ModeIndicator.Kanji: 39},
        8: {ModeIndicator.Numeric: 202, ModeIndicator.Alphanumeric: 122, ModeIndicator.Byte8Bit: 84, ModeIndicator.Kanji: 52},
        9: {ModeIndicator.Numeric: 235, ModeIndicator.Alphanumeric: 143, ModeIndicator.Byte8Bit: 98, ModeIndicator.Kanji: 60},
        10: {ModeIndicator.Numeric: 288, ModeIndicator.Alphanumeric: 174, ModeIndicator.Byte8Bit: 119, ModeIndicator.Kanji: 74},
        11: {ModeIndicator.Numeric: 331, ModeIndicator.Alphanumeric: 200, ModeIndicator.Byte8Bit: 137, ModeIndicator.Kanji: 85},
        12: {ModeIndicator.Numeric: 374, ModeIndicator.Alphanumeric: 227, ModeIndicator.Byte8Bit: 155, ModeIndicator.Kanji: 96},
        13: {ModeIndicator.Numeric: 427, ModeIndicator.Alphanumeric: 259, ModeIndicator.Byte8Bit: 177, ModeIndicator.Kanji: 109},
        14: {ModeIndicator.Numeric: 468, ModeIndicator.Alphanumeric: 283, ModeIndicator.Byte8Bit: 194, ModeIndicator.Kanji: 120},
        15: {ModeIndicator.Numeric: 530, ModeIndicator.Alphanumeric: 321, ModeIndicator.Byte8Bit: 220, ModeIndicator.Kanji: 136},
        16: {ModeIndicator.Numeric: 602, ModeIndicator.Alphanumeric: 365, ModeIndicator.Byte8Bit: 250, ModeIndicator.Kanji: 154},
        17: {ModeIndicator.Numeric: 674, ModeIndicator.Alphanumeric: 408, ModeIndicator.Byte8Bit: 280, ModeIndicator.Kanji: 173},
        18: {ModeIndicator.Numeric: 746, ModeIndicator.Alphanumeric: 452, ModeIndicator.Byte8Bit: 310, ModeIndicator.Kanji: 191},
        19: {ModeIndicator.Numeric: 813, ModeIndicator.Alphanumeric: 493, ModeIndicator.Byte8Bit: 338, ModeIndicator.Kanji: 208},
        20: {ModeIndicator.Numeric: 919, ModeIndicator.Alphanumeric: 557, ModeIndicator.Byte8Bit: 382, ModeIndicator.Kanji: 235},
        21: {ModeIndicator.Numeric: 969, ModeIndicator.Alphanumeric: 587, ModeIndicator.Byte8Bit: 403, ModeIndicator.Kanji: 248},
        22: {ModeIndicator.Numeric: 1056, ModeIndicator.Alphanumeric: 640, ModeIndicator.Byte8Bit: 439, ModeIndicator.Kanji: 270},
        23: {ModeIndicator.Numeric: 1108, ModeIndicator.Alphanumeric: 672, ModeIndicator.Byte8Bit: 461, ModeIndicator.Kanji: 284},
        24: {ModeIndicator.Numeric: 1228, ModeIndicator.Alphanumeric: 744, ModeIndicator.Byte8Bit: 511, ModeIndicator.Kanji: 315},
        25: {ModeIndicator.Numeric: 1286, ModeIndicator.Alphanumeric: 779, ModeIndicator.Byte8Bit: 535, ModeIndicator.Kanji: 330},
        26: {ModeIndicator.Numeric: 1425, ModeIndicator.Alphanumeric: 864, ModeIndicator.Byte8Bit: 593, ModeIndicator.Kanji: 365},
        27: {ModeIndicator.Numeric: 1501, ModeIndicator.Alphanumeric: 910, ModeIndicator.Byte8Bit: 625, ModeIndicator.Kanji: 385},
        28: {ModeIndicator.Numeric: 1581, ModeIndicator.Alphanumeric: 958, ModeIndicator.Byte8Bit: 658, ModeIndicator.Kanji: 405},
        29: {ModeIndicator.Numeric: 1677, ModeIndicator.Alphanumeric: 1016, ModeIndicator.Byte8Bit: 698, ModeIndicator.Kanji: 430},
        30: {ModeIndicator.Numeric: 1782, ModeIndicator.Alphanumeric: 1080, ModeIndicator.Byte8Bit: 742, ModeIndicator.Kanji: 457},
        31: {ModeIndicator.Numeric: 1897, ModeIndicator.Alphanumeric: 1150, ModeIndicator.Byte8Bit: 790, ModeIndicator.Kanji: 486},
        32: {ModeIndicator.Numeric: 2022, ModeIndicator.Alphanumeric: 1226, ModeIndicator.Byte8Bit: 842, ModeIndicator.Kanji: 518},
        33: {ModeIndicator.Numeric: 2157, ModeIndicator.Alphanumeric: 1307, ModeIndicator.Byte8Bit: 898, ModeIndicator.Kanji: 553},
        34: {ModeIndicator.Numeric: 2301, ModeIndicator.Alphanumeric: 1394, ModeIndicator.Byte8Bit: 958, ModeIndicator.Kanji: 590},
        35: {ModeIndicator.Numeric: 2361, ModeIndicator.Alphanumeric: 1431, ModeIndicator.Byte8Bit: 983, ModeIndicator.Kanji: 605},
        36: {ModeIndicator.Numeric: 2524, ModeIndicator.Alphanumeric: 1530, ModeIndicator.Byte8Bit: 1051, ModeIndicator.Kanji: 647},
        37: {ModeIndicator.Numeric: 2625, ModeIndicator.Alphanumeric: 1591, ModeIndicator.Byte8Bit: 1093, ModeIndicator.Kanji: 673},
        38: {ModeIndicator.Numeric: 2735, ModeIndicator.Alphanumeric: 1658, ModeIndicator.Byte8Bit: 1139, ModeIndicator.Kanji: 701},
        39: {ModeIndicator.Numeric: 2927, ModeIndicator.Alphanumeric: 1774, ModeIndicator.Byte8Bit: 1219, ModeIndicator.Kanji: 750},
        40: {ModeIndicator.Numeric: 3057, ModeIndicator.Alphanumeric: 1852, ModeIndicator.Byte8Bit: 1273, ModeIndicator.Kanji: 784}
    }
}

class ECIIndicators:
    Code_page_437 = ('cp437', b'\x00') # English
    ISO_IEC_8859_1 = ('latin_1', b'\x01') # Western Europe
    ISO_IEC_8859_2 = ('iso8859_2', b'\x04') # Central and Eastern Europe
    ISO_IEC_8859_3 = ('iso8859_3', b'\x05') # Esperanto, Maltese
    ISO_IEC_8859_4 = ('iso8859_4', b'\x06') # Baltic languages
    ISO_IEC_8859_5 = ('iso8859_5', b'\x07') # Bulgarian, Byelorussian, Macedonian, Russian, Serbian
    ISO_IEC_8859_6 = ('iso8859_6', b'\x08') # Arabic
    ISO_IEC_8859_7 = ('iso8859_7', b'\x09') # Greek
    ISO_IEC_8859_8 = ('iso8859_8', b'\x0A') # Hebrew
    ISO_IEC_8859_9 = ('iso8859_9', b'\x0B') # Turkish
    ISO_IEC_8859_10 = ('iso8859_10', b'\x0C') # Nordic languages
    ISO_IEC_8859_11 = ('iso8859_11', b'\x0D') # Thai languages
    ISO_IEC_8859_13 = ('iso8859_13', b'\x0F') # Baltic languages
    ISO_IEC_8859_14 = ('iso8859_14', b'\x10') # Celtic languages
    ISO_IEC_8859_15 = ('iso8859_15', b'\x11') # Western Europe
    ISO_IEC_8859_16 = ('iso8859_16', b'\x12') # South-Eastern Europe
    Shift_JIS = ('shift_jis', b'\x13') # Japanese
    Windows_1250 = ('cp1250', b'\x14') # Central and Eastern Europe
    Windows_1251 = ('cp1251', b'\x15') # Bulgarian, Byelorussian, Macedonian, Russian, Serbian
    Windows_1252 = ('cp1252', b'\x16') # Western Europe
    Windows_1256 = ('cp1256', b'\x17') # Arabic
    UTF_16 = ('utf_16', b'\x18') # all languages
    UTF_8 = ('utf_8', b'\x19') # all languages
    US_ASCII = ('ascii', b'\x1A') # English
    Big5 = ('big5', b'\x1B') # Traditional Chinese
    GB_18030 = ('gb18030', b'\x1C') # Unified Chinese
    EUC_KR = ('euc_kr', b'\x1D') # Korean

exponents_table = [None, 0, 1, 25, 2, 50, 26, 198, 3, 223, 51, 238, 27, 104, 199, 75, 4, 100, 224, 14, 52, 141, 239, 129, 28, 193, 105, 248, 200, 8, 76, 113, 5, 138, 101, 47, 225, 36, 15, 33, 53, 147, 142, 218, 240, 18, 130, 69, 29, 181, 194, 125, 106, 39, 249, 185, 201, 154, 9, 120, 77, 228, 114, 166, 6, 191, 139, 98, 102, 221, 48, 253, 226, 152, 37, 179, 16, 145, 34, 136, 54, 208, 148, 206, 143, 150, 219, 189, 241, 210, 19, 92, 131, 56, 70, 64, 30, 66, 182, 163, 195, 72, 126, 110, 107, 58, 40, 84, 250, 133, 186, 61, 202, 94, 155, 159, 10, 21, 121, 43, 78, 212, 229, 172, 115, 243, 167, 87, 7, 112, 192, 247, 140, 128, 99, 13, 103, 74, 222, 237, 49, 197, 254, 24, 227, 165, 153, 119, 38, 184, 180, 124, 17, 68, 146, 217, 35, 32, 137, 46, 55, 63, 209, 91, 149, 188, 207, 205, 144, 135, 151, 178, 220, 252, 190, 97, 242, 86, 211, 171, 20, 42, 93, 158, 132, 60, 57, 83, 71, 109, 65, 162, 31, 45, 67, 216, 183, 123, 164, 118, 196, 23, 73, 236, 127, 12, 111, 246, 108, 161, 59, 82, 41, 157, 85, 170, 251, 96, 134, 177, 187, 204, 62, 90, 203, 89, 95, 176, 156, 169, 160, 81, 11, 245, 22, 235, 122, 117, 44, 215, 79, 174, 213, 233, 230, 231, 173, 232, 116, 214, 244, 234, 168, 80, 88, 175]
logs_table = [1, 2, 4, 8, 16, 32, 64, 128, 29, 58, 116, 232, 205, 135, 19, 38, 76, 152, 45, 90, 180, 117, 234, 201, 143, 3, 6, 12, 24, 48, 96, 192, 157, 39, 78, 156, 37, 74, 148, 53, 106, 212, 181, 119, 238, 193, 159, 35, 70, 140, 5, 10, 20, 40, 80, 160, 93, 186, 105, 210, 185, 111, 222, 161, 95, 190, 97, 194, 153, 47, 94, 188, 101, 202, 137, 15, 30, 60, 120, 240, 253, 231, 211, 187, 107, 214, 177, 127, 254, 225, 223, 163, 91, 182, 113, 226, 217, 175, 67, 134, 17, 34, 68, 136, 13, 26, 52, 104, 208, 189, 103, 206, 129, 31, 62, 124, 248, 237, 199, 147, 59, 118, 236, 197, 151, 51, 102, 204, 133, 23, 46, 92, 184, 109, 218, 169, 79, 158, 33, 66, 132, 21, 42, 84, 168, 77, 154, 41, 82, 164, 85, 170, 73, 146, 57, 114, 228, 213, 183, 115, 230, 209, 191, 99, 198, 145, 63, 126, 252, 229, 215, 179, 123, 246, 241, 255, 227, 219, 171, 75, 150, 49, 98, 196, 149, 55, 110, 220, 165, 87, 174, 65, 130, 25, 50, 100, 200, 141, 7, 14, 28, 56, 112, 224, 221, 167, 83, 166, 81, 162, 89, 178, 121, 242, 249, 239, 195, 155, 43, 86, 172, 69, 138, 9, 18, 36, 72, 144, 61, 122, 244, 245, 247, 243, 251, 235, 203, 139, 11, 22, 44, 88, 176, 125, 250, 233, 207, 131, 27, 54, 108, 216, 173, 71, 142, 1]  

# def generateTables():

#     logs_table = [1] * 256
#     exponents_table = [None] * 256
#     for i in range(255):
#         logs_table[i+1] = 2 * logs_table[i]
#         if logs_table[i+1] > 255:
#             logs_table[i+1] = logs_table[i+1] ^ 285
#         exponents_table[logs_table[i+1]] = i+1
#     exponents_table[1] = 0

generator_polynomials = {
    7: [0, 87, 229, 146, 149, 238, 102, 21],
    10: [0, 251, 67, 46, 61, 118, 70, 64, 94, 32, 45],
    13: [0, 74, 152, 176, 100, 86, 100, 106, 104, 130, 218, 206, 140, 78],
    15: [0, 8, 183, 61, 91, 202, 37, 51, 58, 58, 237, 140, 124, 5, 99, 206],
    16: [0, 120, 104, 107, 109, 102, 161, 76, 3, 91, 191, 147, 169, 182, 194, 225, 120],
    17: [0, 43, 139, 206, 78, 43, 239, 123, 206, 214, 147, 24, 99, 150, 39, 243, 163, 136],
    18: [0, 215, 234, 158, 94, 184, 97, 118, 170, 79, 187, 152, 148, 252, 179, 5, 98, 96, 153],
    20: [0, 17, 60, 79, 50, 61, 163, 26, 187, 202, 180, 221, 225, 83, 239, 156, 164, 212, 212, 188, 190],
    22: [0, 210, 171, 247, 242, 93, 230, 14, 109, 221, 53, 200, 74, 8, 172, 98, 80, 219, 134, 160, 105, 165, 231],
    24: [0, 229, 121, 135, 48, 211, 117, 251, 126, 159, 180, 169, 152, 192, 226, 228, 218, 111, 0, 117, 232, 87, 96, 227, 21],
    26: [0, 173, 125, 158, 2, 103, 182, 118, 17, 145, 201, 111, 28, 165, 53, 161, 21, 245, 142, 13, 102, 48, 227, 153, 145, 218, 70],
    28: [0, 168, 223, 200, 104, 224, 234, 108, 180, 110, 190, 195, 147, 205, 27, 232, 201, 21, 43, 245, 87, 42, 195, 212, 119, 242, 37, 9, 123],
    30: [0, 41, 173, 145, 152, 216, 31, 179, 182, 50, 48, 110, 86, 239, 96, 222, 125, 42, 173, 226, 193, 224, 130, 156, 37, 251, 216, 238, 40, 192, 180],
    32: [0, 10, 6, 106, 190, 249, 167, 4, 67, 209, 138, 138, 32, 242, 123, 89, 27, 120, 185, 80, 156, 38, 69, 171, 60, 28, 222, 80, 52, 254, 185, 220, 241],
    34: [0, 111, 77, 146, 94, 26, 21, 108, 19, 105, 94, 113, 193, 86, 140, 163, 125, 58, 158, 229, 239, 218, 103, 56, 70, 114, 61, 183, 129, 167, 13, 98, 62, 129, 51],
    36: [0, 200, 183, 98, 16, 172, 31, 246, 234, 60, 152, 115, 0, 167, 152, 113, 248, 238, 107, 18, 63, 218, 37, 87, 210, 105, 177, 120, 74, 121, 196, 117, 251, 113, 233, 30, 120],
    40: [0, 59, 116, 79, 161, 252, 98, 128, 205, 128, 161, 248, 57, 163, 56, 235, 106, 53, 26, 187, 174, 226, 104, 170, 7, 175, 35, 181, 114, 88, 41, 47, 163, 125, 134, 72, 20, 232, 53, 35, 15],
    42: [0, 59, 116, 79, 161, 252, 98, 128, 205, 128, 161, 247, 57, 163, 56, 235, 106, 53, 26, 187, 174, 226, 104, 170, 7, 175, 35, 181, 114, 88, 41, 47, 163, 125, 134, 72, 20, 232, 53, 35, 15],
    44: [0, 190, 7, 61, 121, 71, 246, 69, 55, 168, 188, 89, 243, 191, 25, 72, 123, 9, 145, 14, 247, 1, 238, 44, 78, 143, 62, 224, 126, 118, 114, 68, 163, 52, 194, 217, 147, 204, 169, 37, 130, 113, 102, 73, 181],
    46: [0, 112, 94, 88, 112, 253, 224, 202, 115, 187, 99, 89, 5, 54, 113, 129, 44, 58, 16, 135, 216, 169, 211, 36, 1, 4, 96, 60, 241, 73, 104, 234, 8, 249, 245, 119, 174, 52, 25, 157, 224, 43, 202, 223, 19, 82, 15],
    48: [0, 228, 25, 196, 130, 211, 146, 60, 24, 251, 90, 39, 102, 240, 61, 178, 63, 46, 123, 115, 18, 221, 111, 135, 160, 182, 205, 107, 206, 95, 150, 120, 184, 91, 21, 247, 156, 140, 238, 191, 11, 94, 227, 84, 50, 163, 39, 34, 108],
    50: [0, 232, 125, 157, 161, 164, 9, 118, 46, 209, 99, 203, 193, 35, 3, 209, 111, 195, 242, 203, 225, 46, 13, 32, 160, 126, 209, 130, 160, 242, 215, 242, 75, 77, 42, 189, 32, 113, 65, 124, 69, 228, 114, 235, 175, 124, 170, 215, 232, 133, 205],
    52: [0, 116, 50, 86, 186, 50, 220, 251, 89, 192, 46, 86, 127, 124, 19, 184, 233, 151, 215, 22, 14, 59, 145, 37, 242, 203, 134, 254, 89, 190, 94, 59, 65, 124, 113, 100, 233, 235, 121, 22, 76, 86, 97, 39, 242, 200, 220, 101, 33, 239, 254, 116, 51],
    54: [0, 183, 26, 201, 87, 210, 221, 113, 21, 46, 65, 45, 50, 238, 184, 249, 225, 102, 58, 209, 218, 109, 165, 26, 95, 184, 192, 52, 245, 35, 254, 238, 175, 172, 79, 123, 25, 122, 43, 120, 108, 215, 80, 128, 201, 235, 8, 153, 59, 101, 31, 193, 76, 31, 156],
    56: [0, 106, 120, 107, 157, 164, 216, 112, 116, 2, 91, 248, 163, 36, 201, 202, 229, 6, 144, 254, 155, 135, 208, 170, 209, 12, 139, 127, 142, 182, 249, 177, 174, 190, 28, 10, 85, 239, 184, 101, 124, 152, 206, 96, 23, 163, 61, 27, 196, 247, 151, 154, 202, 207, 20, 61, 10],
    58: [0, 82, 116, 26, 247, 66, 27, 62, 107, 252, 182, 200, 185, 235, 55, 251, 242, 210, 144, 154, 237, 176, 141, 192, 248, 152, 249, 206, 85, 253, 142, 65, 165, 125, 23, 24, 30, 122, 240, 214, 6, 129, 218, 29, 145, 127, 134, 206, 245, 117, 29, 41, 63, 159, 142, 233, 125, 148, 123],
    60: [0, 107, 140, 26, 12, 9, 141, 243, 197, 226, 197, 219, 45, 211, 101, 219, 120, 28, 181, 127, 6, 100, 247, 2, 205, 198, 57, 115, 219, 101, 109, 160, 82, 37, 38, 238, 49, 160, 209, 121, 86, 11, 124, 30, 181, 84, 25, 194, 87, 65, 102, 190, 220, 70, 27, 209, 16, 89, 7, 33, 240],
    62: [0, 65, 202, 113, 98, 71, 223, 248, 118, 214, 94, 0, 122, 37, 23, 2, 228, 58, 121, 7, 105, 135, 78, 243, 118, 70, 76, 223, 89, 72, 50, 70, 111, 194, 17, 212, 126, 181, 35, 221, 117, 235, 11, 229, 149, 147, 123, 213, 40, 115, 6, 200, 100, 26, 246, 182, 218, 127, 215, 36, 186, 110, 106],
    64: [0, 45, 51, 175, 9, 7, 158, 159, 49, 68, 119, 92, 123, 177, 204, 187, 254, 200, 78, 141, 149, 119, 26, 127, 53, 160, 93, 199, 212, 29, 24, 145, 156, 208, 150, 218, 209, 4, 216, 91, 47, 184, 146, 47, 140, 195, 195, 125, 242, 238, 63, 99, 108, 140, 230, 242, 31, 204, 11, 178, 243, 217, 156, 213, 231],
    66: [0, 5, 118, 222, 180, 136, 136, 162, 51, 46, 117, 13, 215, 81, 17, 139, 247, 197, 171, 95, 173, 65, 137, 178, 68, 111, 95, 101, 41, 72, 214, 169, 197, 95, 7, 44, 154, 77, 111, 236, 40, 121, 143, 63, 87, 80, 253, 240, 126, 217, 77, 34, 232, 106, 50, 168, 82, 76, 146, 67, 106, 171, 25, 132, 93, 45, 105],
    68: [0, 247, 159, 223, 33, 224, 93, 77, 70, 90, 160, 32, 254, 43, 150, 84, 101, 190, 205, 133, 52, 60, 202, 165, 220, 203, 151, 93, 84, 15, 84, 253, 173, 160, 89, 227, 52, 199, 97, 95, 231, 52, 177, 51, 125, 137, 241, 166, 225, 118, 2, 54, 32, 82, 215, 175, 198, 43, 238, 235, 27, 101, 184, 127, 3, 5, 8, 163, 238]
}

class ModuleType:
    Data=-1
    Dark=0
    Light=1
    FormatInformation=2
    Version=3
    Pouet=200
    Toto=50

finder_pattern = np.array([
    [ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark],
    [ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Dark],
    [ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Dark],
    [ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Dark],
    [ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Dark],
    [ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Dark],
    [ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark],
])

alignment_pattern = np.array([
    [ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark],
    [ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Dark],
    [ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Dark],
    [ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Dark],
    [ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark]
])

mask_patterns = [
    lambda col,row: ((row+col) % 2) == 0,
    lambda _,row: (row % 2) == 0,
    lambda col,_: (col % 3) == 0,
    lambda col,row: ((row+col) % 3) == 0,
    lambda col,row: ((m.floor(row/2) + m.floor(col/3)) % 2) == 0,
    lambda col,row: (((row*col) % 2) + ((row*col) % 3)) == 0,
    lambda col,row: ((((row*col) % 2) + ((row*col) % 3)) % 2) == 0,
    lambda col,row: ((((row+col) % 2) + ((row*col) % 3)) % 2) == 0
]

format_information_bits = {
    ErrorCorrectionLevel.L: [
        np.array([[ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Light]]),
        np.array([[ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Dark]]),
        np.array([[ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Light]]),
        np.array([[ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Dark]]),
        np.array([[ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark]]),
        np.array([[ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light]]),
        np.array([[ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Dark]]),
        np.array([[ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Light]])
    ],
    ErrorCorrectionLevel.M: [
        np.array([[ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Light]]),
        np.array([[ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Dark]]),
        np.array([[ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Light]]),
        np.array([[ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Dark]]),
        np.array([[ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Dark]]),
        np.array([[ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Light]]),
        np.array([[ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark]]),
        np.array([[ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light]])
    ],
    ErrorCorrectionLevel.Q: [
        np.array([[ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark]]),
        np.array([[ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light]]),
        np.array([[ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Dark]]),
        np.array([[ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Light]]),
        np.array([[ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Light]]),
        np.array([[ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Dark]]),
        np.array([[ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Light]]),
        np.array([[ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Dark]])
    ],
    ErrorCorrectionLevel.H: [
        np.array([[ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Dark]]),
        np.array([[ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Light]]),
        np.array([[ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark]]),
        np.array([[ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light]]),
        np.array([[ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Light]]),
        np.array([[ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Dark]]),
        np.array([[ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Light]]),
        np.array([[ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Dark]])
    ]
}

version_information_bits = {
    7: np.array([[ModuleType.Light, ModuleType.Light, ModuleType.Dark], [ModuleType.Light, ModuleType.Dark, ModuleType.Light], [ModuleType.Light, ModuleType.Dark, ModuleType.Light], [ModuleType.Light, ModuleType.Dark, ModuleType.Dark], [ModuleType.Dark, ModuleType.Dark, ModuleType.Dark], [ModuleType.Light, ModuleType.Light, ModuleType.Light]]),
    8: np.array([[ModuleType.Light, ModuleType.Light, ModuleType.Dark], [ModuleType.Dark, ModuleType.Dark, ModuleType.Dark], [ModuleType.Light, ModuleType.Dark, ModuleType.Dark], [ModuleType.Light, ModuleType.Dark, ModuleType.Light], [ModuleType.Light, ModuleType.Light, ModuleType.Light], [ModuleType.Dark, ModuleType.Light, ModuleType.Light]]),
    9: np.array([[ModuleType.Dark, ModuleType.Light, ModuleType.Light], [ModuleType.Dark, ModuleType.Dark, ModuleType.Light], [ModuleType.Light, ModuleType.Dark, ModuleType.Light], [ModuleType.Dark, ModuleType.Light, ModuleType.Dark], [ModuleType.Dark, ModuleType.Light, ModuleType.Light], [ModuleType.Dark, ModuleType.Light, ModuleType.Light]]),
    10: np.array([[ModuleType.Dark, ModuleType.Dark, ModuleType.Light], [ModuleType.Light, ModuleType.Dark, ModuleType.Light], [ModuleType.Dark, ModuleType.Dark, ModuleType.Light], [ModuleType.Light, ModuleType.Dark, ModuleType.Light], [ModuleType.Light, ModuleType.Dark, ModuleType.Light], [ModuleType.Dark, ModuleType.Light, ModuleType.Light]]),
    11: np.array([[ModuleType.Light, ModuleType.Dark, ModuleType.Dark], [ModuleType.Light, ModuleType.Dark, ModuleType.Dark], [ModuleType.Dark, ModuleType.Dark, ModuleType.Dark], [ModuleType.Dark, ModuleType.Light, ModuleType.Dark], [ModuleType.Dark, ModuleType.Dark, ModuleType.Light], [ModuleType.Dark, ModuleType.Light, ModuleType.Light]]),
    12: np.array([[ModuleType.Light, ModuleType.Dark, ModuleType.Light], [ModuleType.Light, ModuleType.Light, ModuleType.Dark], [ModuleType.Dark, ModuleType.Light, ModuleType.Dark], [ModuleType.Dark, ModuleType.Dark, ModuleType.Light], [ModuleType.Light, ModuleType.Light, ModuleType.Dark], [ModuleType.Dark, ModuleType.Light, ModuleType.Light]]),
    13: np.array([[ModuleType.Dark, ModuleType.Dark, ModuleType.Dark], [ModuleType.Light, ModuleType.Light, ModuleType.Light], [ModuleType.Dark, ModuleType.Light, ModuleType.Light], [ModuleType.Light, ModuleType.Light, ModuleType.Dark], [ModuleType.Dark, ModuleType.Light, ModuleType.Dark], [ModuleType.Dark, ModuleType.Light, ModuleType.Light]]),
    14: np.array([[ModuleType.Dark, ModuleType.Light, ModuleType.Dark], [ModuleType.Dark, ModuleType.Light, ModuleType.Light], [ModuleType.Light, ModuleType.Light, ModuleType.Light], [ModuleType.Dark, ModuleType.Dark, ModuleType.Light], [ModuleType.Light, ModuleType.Dark, ModuleType.Dark], [ModuleType.Dark, ModuleType.Light, ModuleType.Light]]),
    15: np.array([[ModuleType.Light, ModuleType.Light, ModuleType.Light], [ModuleType.Dark, ModuleType.Light, ModuleType.Dark], [ModuleType.Light, ModuleType.Light, ModuleType.Dark], [ModuleType.Light, ModuleType.Light, ModuleType.Dark], [ModuleType.Dark, ModuleType.Dark, ModuleType.Dark], [ModuleType.Dark, ModuleType.Light, ModuleType.Light]]),
    16: np.array([[ModuleType.Light, ModuleType.Light, ModuleType.Light], [ModuleType.Dark, ModuleType.Dark, ModuleType.Dark], [ModuleType.Dark, ModuleType.Light, ModuleType.Dark], [ModuleType.Dark, ModuleType.Light, ModuleType.Dark], [ModuleType.Light, ModuleType.Light, ModuleType.Light], [ModuleType.Light, ModuleType.Dark, ModuleType.Light]]),
    17: np.array([[ModuleType.Dark, ModuleType.Light, ModuleType.Dark], [ModuleType.Dark, ModuleType.Dark, ModuleType.Light], [ModuleType.Dark, ModuleType.Light, ModuleType.Light], [ModuleType.Light, ModuleType.Dark, ModuleType.Light], [ModuleType.Dark, ModuleType.Light, ModuleType.Light], [ModuleType.Light, ModuleType.Dark, ModuleType.Light]]),
    18: np.array([[ModuleType.Dark, ModuleType.Dark, ModuleType.Dark], [ModuleType.Light, ModuleType.Dark, ModuleType.Light], [ModuleType.Light, ModuleType.Light, ModuleType.Light], [ModuleType.Dark, ModuleType.Light, ModuleType.Dark], [ModuleType.Light, ModuleType.Dark, ModuleType.Light], [ModuleType.Light, ModuleType.Dark, ModuleType.Light]]),
    19: np.array([[ModuleType.Light, ModuleType.Dark, ModuleType.Light], [ModuleType.Light, ModuleType.Dark, ModuleType.Dark], [ModuleType.Light, ModuleType.Light, ModuleType.Dark], [ModuleType.Light, ModuleType.Dark, ModuleType.Light], [ModuleType.Dark, ModuleType.Dark, ModuleType.Light], [ModuleType.Light, ModuleType.Dark, ModuleType.Light]]),
    20: np.array([[ModuleType.Light, ModuleType.Dark, ModuleType.Dark], [ModuleType.Light, ModuleType.Light, ModuleType.Dark], [ModuleType.Light, ModuleType.Dark, ModuleType.Dark], [ModuleType.Light, ModuleType.Light, ModuleType.Dark], [ModuleType.Light, ModuleType.Light, ModuleType.Dark], [ModuleType.Light, ModuleType.Dark, ModuleType.Light]]),
    21: np.array([[ModuleType.Dark, ModuleType.Dark, ModuleType.Light], [ModuleType.Light, ModuleType.Light, ModuleType.Light], [ModuleType.Light, ModuleType.Dark, ModuleType.Light], [ModuleType.Dark, ModuleType.Dark, ModuleType.Light], [ModuleType.Dark, ModuleType.Light, ModuleType.Dark], [ModuleType.Light, ModuleType.Dark, ModuleType.Light]]),
    22: np.array([[ModuleType.Dark, ModuleType.Light, ModuleType.Light], [ModuleType.Dark, ModuleType.Light, ModuleType.Light], [ModuleType.Dark, ModuleType.Dark, ModuleType.Light], [ModuleType.Light, ModuleType.Light, ModuleType.Dark], [ModuleType.Light, ModuleType.Dark, ModuleType.Dark], [ModuleType.Light, ModuleType.Dark, ModuleType.Light]]),
    23: np.array([[ModuleType.Light, ModuleType.Light, ModuleType.Dark], [ModuleType.Dark, ModuleType.Light, ModuleType.Dark], [ModuleType.Dark, ModuleType.Dark, ModuleType.Dark], [ModuleType.Dark, ModuleType.Dark, ModuleType.Light], [ModuleType.Dark, ModuleType.Dark, ModuleType.Dark], [ModuleType.Light, ModuleType.Dark, ModuleType.Light]]),
    24: np.array([[ModuleType.Light, ModuleType.Light, ModuleType.Dark], [ModuleType.Light, ModuleType.Light, ModuleType.Light], [ModuleType.Dark, ModuleType.Dark, ModuleType.Light], [ModuleType.Dark, ModuleType.Dark, ModuleType.Dark], [ModuleType.Light, ModuleType.Light, ModuleType.Light], [ModuleType.Dark, ModuleType.Dark, ModuleType.Light]]),
    25: np.array([[ModuleType.Dark, ModuleType.Light, ModuleType.Light], [ModuleType.Light, ModuleType.Light, ModuleType.Dark], [ModuleType.Dark, ModuleType.Dark, ModuleType.Dark], [ModuleType.Light, ModuleType.Light, ModuleType.Light], [ModuleType.Dark, ModuleType.Light, ModuleType.Light], [ModuleType.Dark, ModuleType.Dark, ModuleType.Light]]),
    26: np.array([[ModuleType.Dark, ModuleType.Dark, ModuleType.Light], [ModuleType.Dark, ModuleType.Light, ModuleType.Dark], [ModuleType.Light, ModuleType.Dark, ModuleType.Dark], [ModuleType.Dark, ModuleType.Dark, ModuleType.Dark], [ModuleType.Light, ModuleType.Dark, ModuleType.Light], [ModuleType.Dark, ModuleType.Dark, ModuleType.Light]]),
    27: np.array([[ModuleType.Light, ModuleType.Dark, ModuleType.Dark], [ModuleType.Dark, ModuleType.Light, ModuleType.Light], [ModuleType.Light, ModuleType.Dark, ModuleType.Light], [ModuleType.Light, ModuleType.Light, ModuleType.Light], [ModuleType.Dark, ModuleType.Dark, ModuleType.Light], [ModuleType.Dark, ModuleType.Dark, ModuleType.Light]]),
    28: np.array([[ModuleType.Light, ModuleType.Dark, ModuleType.Light], [ModuleType.Dark, ModuleType.Dark, ModuleType.Light], [ModuleType.Light, ModuleType.Light, ModuleType.Light], [ModuleType.Light, ModuleType.Dark, ModuleType.Dark], [ModuleType.Light, ModuleType.Light, ModuleType.Dark], [ModuleType.Dark, ModuleType.Dark, ModuleType.Light]]),
    29: np.array([[ModuleType.Dark, ModuleType.Dark, ModuleType.Dark], [ModuleType.Dark, ModuleType.Dark, ModuleType.Dark], [ModuleType.Light, ModuleType.Light, ModuleType.Dark], [ModuleType.Dark, ModuleType.Light, ModuleType.Light], [ModuleType.Dark, ModuleType.Light, ModuleType.Dark], [ModuleType.Dark, ModuleType.Dark, ModuleType.Light]]),
    30: np.array([[ModuleType.Dark, ModuleType.Light, ModuleType.Dark], [ModuleType.Light, ModuleType.Dark, ModuleType.Dark], [ModuleType.Dark, ModuleType.Light, ModuleType.Dark], [ModuleType.Light, ModuleType.Dark, ModuleType.Dark], [ModuleType.Light, ModuleType.Dark, ModuleType.Dark], [ModuleType.Dark, ModuleType.Dark, ModuleType.Light]]),
    31: np.array([[ModuleType.Light, ModuleType.Light, ModuleType.Light], [ModuleType.Light, ModuleType.Dark, ModuleType.Light], [ModuleType.Dark, ModuleType.Light, ModuleType.Light], [ModuleType.Dark, ModuleType.Light, ModuleType.Light], [ModuleType.Dark, ModuleType.Dark, ModuleType.Dark], [ModuleType.Dark, ModuleType.Dark, ModuleType.Light]]),
    32: np.array([[ModuleType.Dark, ModuleType.Light, ModuleType.Dark], [ModuleType.Light, ModuleType.Dark, ModuleType.Light], [ModuleType.Dark, ModuleType.Dark, ModuleType.Dark], [ModuleType.Light, ModuleType.Light, ModuleType.Dark], [ModuleType.Light, ModuleType.Light, ModuleType.Light], [ModuleType.Light, ModuleType.Light, ModuleType.Dark]]),
    33: np.array([[ModuleType.Light, ModuleType.Light, ModuleType.Light], [ModuleType.Light, ModuleType.Dark, ModuleType.Dark], [ModuleType.Dark, ModuleType.Dark, ModuleType.Light], [ModuleType.Dark, ModuleType.Dark, ModuleType.Light], [ModuleType.Dark, ModuleType.Light, ModuleType.Light], [ModuleType.Light, ModuleType.Light, ModuleType.Dark]]),
    34: np.array([[ModuleType.Light, ModuleType.Dark, ModuleType.Light], [ModuleType.Dark, ModuleType.Dark, ModuleType.Dark], [ModuleType.Light, ModuleType.Dark, ModuleType.Light], [ModuleType.Light, ModuleType.Light, ModuleType.Dark], [ModuleType.Light, ModuleType.Dark, ModuleType.Light], [ModuleType.Light, ModuleType.Light, ModuleType.Dark]]),
    35: np.array([[ModuleType.Dark, ModuleType.Dark, ModuleType.Dark], [ModuleType.Dark, ModuleType.Dark, ModuleType.Light], [ModuleType.Light, ModuleType.Dark, ModuleType.Dark], [ModuleType.Dark, ModuleType.Dark, ModuleType.Light], [ModuleType.Dark, ModuleType.Dark, ModuleType.Light], [ModuleType.Light, ModuleType.Light, ModuleType.Dark]]),
    36: np.array([[ModuleType.Dark, ModuleType.Dark, ModuleType.Light], [ModuleType.Dark, ModuleType.Light, ModuleType.Light], [ModuleType.Light, ModuleType.Light, ModuleType.Dark], [ModuleType.Dark, ModuleType.Light, ModuleType.Dark], [ModuleType.Light, ModuleType.Light, ModuleType.Dark], [ModuleType.Light, ModuleType.Light, ModuleType.Dark]]),
    37: np.array([[ModuleType.Light, ModuleType.Dark, ModuleType.Dark], [ModuleType.Dark, ModuleType.Light, ModuleType.Dark], [ModuleType.Light, ModuleType.Light, ModuleType.Light], [ModuleType.Light, ModuleType.Dark, ModuleType.Light], [ModuleType.Dark, ModuleType.Light, ModuleType.Dark], [ModuleType.Light, ModuleType.Light, ModuleType.Dark]]),
    38: np.array([[ModuleType.Light, ModuleType.Light, ModuleType.Dark], [ModuleType.Light, ModuleType.Light, ModuleType.Dark], [ModuleType.Dark, ModuleType.Light, ModuleType.Light], [ModuleType.Dark, ModuleType.Light, ModuleType.Dark], [ModuleType.Light, ModuleType.Dark, ModuleType.Dark], [ModuleType.Light, ModuleType.Light, ModuleType.Dark]]),
    39: np.array([[ModuleType.Dark, ModuleType.Light, ModuleType.Light], [ModuleType.Light, ModuleType.Light, ModuleType.Light], [ModuleType.Dark, ModuleType.Light, ModuleType.Dark], [ModuleType.Light, ModuleType.Dark, ModuleType.Light], [ModuleType.Dark, ModuleType.Dark, ModuleType.Dark], [ModuleType.Light, ModuleType.Light, ModuleType.Dark]]),
    40: np.array([[ModuleType.Dark, ModuleType.Light, ModuleType.Light], [ModuleType.Dark, ModuleType.Light, ModuleType.Dark], [ModuleType.Dark, ModuleType.Light, ModuleType.Light], [ModuleType.Light, ModuleType.Dark, ModuleType.Dark], [ModuleType.Light, ModuleType.Light, ModuleType.Light], [ModuleType.Dark, ModuleType.Light, ModuleType.Dark]])
}

def getWidth(version):
    return 21+(version-1)*4

def getAlignmentPatternCoordinatesList(version):

    coordinates_list = []

    elements = alignment_patterns_center_coordinates[version-1]

    for i in range(len(elements)):
        elemA = elements[i]
        for j in range(len(elements)):
            elemB = elements[j]

            coordinates_list.append((elemA, elemB))
            
    return coordinates_list

def determineVersion(text: str, mode: ModeIndicator, correction_level: ErrorCorrectionLevel):
    ''' Returns smallest version matching text size depending on mode. '''
    
    version = 1

    char_count = len(text)

    while version < 40:
        if char_count <= symbol_capacity_characters[correction_level][version][mode]:
            break
        version += 1

    return version

def getStreamSizeInBits(text, mode, version):
    return getEncodedDataSizeBits(text, mode) + getCodeLengthSizeBits(mode, version)

def getEncodedDataSizeBits(text: str, mode: ModeIndicator) -> int:
    ''' Returns text encoded size in bits depending on mode. '''

    D = len(text)
    if mode == ModeIndicator.Numeric:
        R = 0 if (D % 3) == 0 else 1 if (D % 3) == 1 else 2
        return m.floor(D/3) * 10 + R
    elif mode == ModeIndicator.Alphanumeric:
        return m.ceil(len(text)/2*11)
    elif mode == ModeIndicator.Byte8Bit:
        return D*8
    elif mode == ModeIndicator.Kanji:
        return D*13
    else:
        print("Invalid ModeIndicator")
        return -1

def getCodeLengthSizeBits(mode: ModeIndicator, version: int) -> int:
    ''' Returns characters count bytes stream size in bits
        depending on version. '''
    
    if version <= 9:
        return character_count_number_of_bits[mode][0]
    elif version <= 26:
        return character_count_number_of_bits[mode][1]
    else:
        return character_count_number_of_bits[mode][2]
    