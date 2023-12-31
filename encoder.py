from utils.functions import *
from bits_array import BitsArray

class TokenType:
    Numeric = 0
    Alphanumeric = 1
    Bit8 = 2
    Kanji = 3

class Encoder:
    """
        This class implements the differents steps for QRCode data encodation as described in the standard.
        Data encodation is performed in 4 steps:
            -Data analysis, to chose the most adequate version and mode for data representation
            -Data encodation, to build the message stream in chosen mode
            -Error correction coding, create error correction codes from message stream, using Reed-Solomon algorithm
            -Structure final message, to mix message stream and error correction stream for future placement in matrix.
    """

    def __init__(self) -> None:
        self.version = 0
        self.correction_level = ErrorCorrectionLevel.L


    def encode(self, text: str, correction_level: ErrorCorrectionLevel = ErrorCorrectionLevel.L) -> BitsArray:
        """ Performs the 4 steps of encodation on text, with given correction level,
            and returns a BitsArray containing formatted final message to be placed in matrix. """

        self.correction_level = correction_level

        mode = self._dataAnalysis(text)
        message_codewords_groups = self._dataEncodation(text, mode)
        error_codewords_groups = self._errorCorrectionCoding(message_codewords_groups)

        return self._structureFinalMessage(message_codewords_groups, error_codewords_groups)

    def _dataAnalysis(self, text: str) -> ModeIndicator:
        """ This function analyses the text and returns a ModeIndicator
            corresponding to global data type
            (the one with the least memory footprint according to data). """

        def _getTokenType(token: str) -> TokenType:
            """ Returns the type of given token. """
            btoken = token.encode("utf-8")

            if len(btoken) > 1:
                return TokenType.Kanji
            elif btoken >= b"\x30" and btoken <= b"\x39":
                return TokenType.Numeric
            elif (btoken >= b"\x41" and btoken <= b"\x5A") or btoken in [b"\x20", b"\x24", b"\x25", b"\x2A", b"\x2B", b"\x2D", b"\x2E", b"\x2F", b"\x3A"]:
                return TokenType.Alphanumeric
            else:
                return TokenType.Bit8

        # Determine TokenType for each char in text
        token_types = [_getTokenType(token) for token in text]

        # TODO: more efficient analysis with mode switching

        # Count token types for each ModeIndicator,
        # From the most to the least memory greedy

        kanji_count = token_types.count(TokenType.Kanji)

        if kanji_count > 0:
            return ModeIndicator.Kanji
        
        bit8_count = token_types.count(TokenType.Bit8)

        if bit8_count > 0:
            return ModeIndicator.Byte8Bit
        
        alphanumeric_count = token_types.count(TokenType.Alphanumeric)

        if alphanumeric_count > 0:
            return ModeIndicator.Alphanumeric
        
        return ModeIndicator.Numeric


    def _dataEncodation(self, text: str, mode: ModeIndicator) -> list:
        """ This function builts a message bytes stream from text
            according to mode. The stream is divided into groups,
            which are divided into blocs. """
        
        # Determine the smallest version able to represent text
        self.version = determineVersion(text, mode, self.correction_level)

        # Build "character count" stream
        characters_count_size_bits = getCodeLengthSizeBits(mode, self.version)
        characters_count_bits = f"{len(text):0{characters_count_size_bits}b}"

        # Create ECI (Currently not handled)
        ECI_mode_indicator = ""
        ECI_assignment_number = ""

        # Build data stream according to mode

        if mode == ModeIndicator.Numeric:
            data_bits = BitsArray()

            # Digits are grouped by 3
            for i in range(0, len(text)-2, 3):
                # Each 3 digit group represents a 3 digit int
                # which is stored with 10 bits
                data_bits.appendInt(int(text[i:i+3]), 10)

            remainder_digits = len(text) % 3
            # Handle remainings digits
            if remainder_digits == 2:
                data_bits.appendInt(int(text[-2:]), 7)
            elif remainder_digits == 1:
                data_bits.appendInt(int(text[-1:]), 4)

        elif mode == ModeIndicator.Alphanumeric:
            data_bits = BitsArray()

            # Characters are grouped by 2
            for i in range(0, len(text)-1, 2):
                # Each 2 chars group is combined using an
                # encoding table and stored with 11 digits
                value1 = alphanumeric_encoding_table[text[i]]
                value2 = alphanumeric_encoding_table[text[i+1]]
                # Formula described in standard to mix 2 alphanumeric chars
                data_bits.appendInt(value1*45 + value2, 11)

            remainder_digits = len(text) % 2
            # Handle remaining digit
            if remainder_digits == 1:
                data_bits.appendInt(alphanumeric_encoding_table[text[-1:]], 6)

        elif mode == ModeIndicator.Byte8Bit:
            data_bits = BitsArray()

            # In 8-bit mode, char string is simply encoded in
            # adequate format (default is ISO-8859-1, or latin1)
            data_bits.appendBytes(bytes(text, "ISO-8859-1"))

        elif mode == ModeIndicator.Kanji:
            data_bits = BitsArray()

            for c in text:
                # Kanjis in shift-JIS are represented by 2 bytes
                b = bytes(c, "shift_jis")
                i = int.from_bytes(b, "big")
                # Apply standard formulas to store char in 13 bits
                if i >= 33088 and i <= 40956:
                    i -= 33088
                    msf = (i >> 8)
                    lsf = i & 255
                    value = msf * 192 + lsf
                elif i >= 57408 and i <= 60351:
                    i -= 49472
                    msf = (i >> 8)
                    lsf = i & 255
                    value = msf * 192 + lsf
                data_bits.appendInt(value, 13)

        else:
            print("Other modes are currently not handled :(")

        # Build final bytes stream
        bits = BitsArray()

        bits.appendBits(ECI_mode_indicator)
        bits.appendBits(ECI_assignment_number)

        bits.appendBits(mode)
        bits.appendBits(characters_count_bits)
        bits.appendBits(data_bits.bits)

        data_capacity = getDataInformationCapacityBits(data_informations[self.correction_level][self.version])

        # Terminator (0000)
        remaining_bits = data_capacity - bits.length()
        if remaining_bits > 0:
            bits.appendInt(0, min(4, remaining_bits))

        # Padding (data must end to a multiple of 8)
        remaining_multiple_8_bits = m.ceil(bits.length()/8)*8 - bits.length()
        if remaining_multiple_8_bits > 0:
            bits.appendInt(0, remaining_multiple_8_bits)

        # Pad Codewords (pad remaining space with 11101100 and 00010001 codewords)
        error_correction_codewords = int((data_capacity-bits.length())/8)
        for _ in range(0, error_correction_codewords-1, 2):
            bits.appendBits("1110110000010001")
        if error_correction_codewords % 2 == 1:
            bits.appendBits("11101100")

        # Conversion to codewords groups
        # Data is divided in groups and blocks (sub-groups) to be spatially dispatched in matrix
        data_bits = bits.bits
        message_codewords_groups = []

        i = 0
        for infos in data_informations[self.correction_level][self.version].groups_informations:
            # Create group
            message_codewords_groups.append([])
 
            for _ in range(infos.blocks_count):
                # Create block in group
                message_codewords_groups[-1].append([])
                
                for _ in range(infos.data_codewords_count):
                    # Extract codewords to fill the block
                    codeword_bits = data_bits[i:i+8]
                    message_codewords_groups[-1][-1].append(int(codeword_bits, 2))
                    i += 8

        return message_codewords_groups

    def _errorCorrectionCoding(self, message_codewords_groups: list) -> list:
        """ This function builts an Error correction codes bytes stream from message
            codewords groups according to mode. The stream is divided into groups,
            which are divided into blocs corresponding to message groups/blocs.  """

        # Source: https://www.thonky.com/qr-code-tutorial/error-correction-coding

        # Get generator alpha exponents according to version and error correction level
        generator_size = data_informations[self.correction_level][self.version].error_correction_codewords_per_block
        generator_alphas = generator_polynomials[generator_size]

        error_codewords_groups = []

        # Reed-Solomon Error correction algorithm
        # Bit-wise modulo 2 and byte-wise modulo 285
        # The algorithm is performed independently on each message block
        for group in message_codewords_groups:
            error_codewords_groups.append([])

            for block in group:

                # Get current block message codewords
                message_coefficients = block.copy()

                # Iterate on every message coefficient
                iterations_count = len(message_coefficients)

                i = 0
                while i < iterations_count:
                    # Discard potentials leadings 0
                    while message_coefficients[0] == 0:
                        message_coefficients = message_coefficients[1:]
                        # Increment i, as we skip one message coefficient
                        i += 1
                    if i >= iterations_count:
                        break

                    # Lead term is the coefficient we want to be 0 after division
                    lead_term = message_coefficients[0]

                    # Get alpha exponent of lead term
                    exponent = exponents_table[lead_term]

                    # multiply generator polynomial and message leading exponent
                    # multiply coefficients <=> add exponents
                    # and modulo 255 to stay in GF(256)
                    added_exponents = [(a+exponent) % 255 for a in generator_alphas]
                    # convert generator alphas to coefficients
                    generator_coefficients = [logs_table[a] for a in added_exponents]
                    # fill with 0 to have both coefficients lists of same length
                    len_diff = (len(message_coefficients)-len(generator_coefficients))
                    generator_coefficients.extend([0] * len_diff)
                    message_coefficients.extend([0] * -len_diff)
                    # substract multiplication result and message coefficients
                    # substract coefficients <=> XOR coefficients
                    xor_result = [gc ^ mc for gc, mc in zip(generator_coefficients, message_coefficients)]
                    # Discard leading 0
                    xor_result = xor_result[1:]
                    
                    # New coefficients are the result of the division
                    message_coefficients = xor_result
                    
                    # Loop iteration
                    i += 1

                # The remainders of divisions are error correction codewords
                error_codewords_groups[-1].append(message_coefficients)

        return error_codewords_groups

    def _structureFinalMessage(self, message_codewords_groups: list, error_codewords_groups: list) -> BitsArray:
        """ Combines message blocs and error correction blocs to be ready
            to be placed in matrix. Message and error correction blocks are interleaved. """

        def _interleave_different_len_lists(lists: list) -> list:
            """ Interleave elements of a list of lists which
                can be of different lenghts. """

            max_len = 0
            elements_count = 0
            for l in lists:
                max_len = max(len(l), max_len)
                elements_count += len(l)
        
            out = [0] * elements_count

            i = 0
            for j in range(max_len):
                for l in lists:
                    if j < len(l):
                        out[i] = l[j]
                        i += 1

            return out

        # Interleave Message codewords
        message_blocks = [block for group in message_codewords_groups for block in group]
        # Special case, zip cannot be used as blocks can be of different lenghts :(
        interleaved_message_codewords = _interleave_different_len_lists(message_blocks)

        # Interleave Error codewords
        error_blocks = [block for group in error_codewords_groups for block in group]
        interleaved_error_codewords = [codeword for t in zip(*error_blocks) for codeword in t]

        # Structure final message (append message and error correction interleaved lists)
        final_message = interleaved_message_codewords + interleaved_error_codewords

        # Convert to bits
        bits_message = BitsArray()

        for i in final_message:
            bits_message.appendInt(i, 8)

        # Append remainder 0 to match total symbol capacity
        remainder_bits = symbol_remainder_bits[self.version]
        if remainder_bits > 0:
            bits_message.appendInt(0, remainder_bits)

        return bits_message