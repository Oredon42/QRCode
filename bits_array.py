class BitsArray:
    """
        This class stores an array of bits, represented by a string of "0"s and "1"s.
        It also implements methods to append different types of data which are
        converted into bits strings and appended.
    """

    def __init__(self) -> None:
        self.bits = ""

    def clear(self) -> None:
        self.bits = ""

    def length(self) -> None:
        return len(self.bits)

    def appendBytes(self, value: bytes) -> None:
        if len(value) > 0:
            self.bits += f"{int(value.hex(), 16):08b}".zfill(len(value)*8)

    def appendBits(self, value: str) -> None:
        if not set(value) - {"0", "1"}:
            self.bits += value

    def appendInt(self, value: int, size_bits: int = 32) -> None:
        self.bits += f"{value:0{size_bits}b}"

