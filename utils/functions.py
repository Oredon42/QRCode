from utils.tables import *

def getSymbolWidth(version: int) -> int:
    """ Returns the width of a QRCode of given version in modules. """

    return 21+(version-1)*4


def getAlignmentPatternCoordinatesList(version: int) -> list:
    """ Returns alignment patterns coordinate centers for given version. """

    coordinates_list = []

    elements = alignment_patterns_center_coordinates[version]

    # Compute coordinates combinatorial
    for i in range(len(elements)):
        elemA = elements[i]
        for j in range(len(elements)):
            elemB = elements[j]

            coordinates_list.append((elemA, elemB))
            
    return coordinates_list


def determineVersion(text: str, mode: ModeIndicator, correction_level: ErrorCorrectionLevel) -> int:
    """ Returns smallest version able to contain text size depending on mode. """
    
    version = 1

    char_count = len(text)

    while version < 40:
        if char_count <= symbol_capacity_characters[correction_level][version][mode]:
            break
        version += 1

    return version


def getCodeLengthSizeBits(mode: ModeIndicator, version: int) -> int:
    """ Returns the size of the "character count" data stream in bits
        depending on given mode and version. """
    
    if version <= 9:
        return character_count_number_of_bits[mode][0]
    elif version <= 26:
        return character_count_number_of_bits[mode][1]
    else:
        return character_count_number_of_bits[mode][2]
    

def getErrorCorrectionLevelFromString(correction_level: str) -> ErrorCorrectionLevel:
    """ Returns an ErrorCorrectionLevel corresponding to a given string. """

    error_correction_levels = {
        "L": ErrorCorrectionLevel.L,
        "M": ErrorCorrectionLevel.M,
        "Q": ErrorCorrectionLevel.Q,
        "H": ErrorCorrectionLevel.H,
    }

    if correction_level in error_correction_levels:
        return error_correction_levels[correction_level]
    else:
        return ErrorCorrectionLevel.Invalid
    

def getDataInformationCapacityBits(data_infos: DataInformation) -> int:
    """ Returns the codewords capacity in bits of a given DataInformation. """

    data_capacity = 0
    for infos in data_infos.groups_informations:
        data_capacity += infos.blocks_count * infos.data_codewords_count

    return data_capacity * 8
