class BitsArray:
    def __init__(self):
        self.bits = ''

    def clear(self):
        self.bits = ''

    def length(self):
        return len(self.bits)

    def fillToSize(self, size: int, fill_value = '0'):
        if fill_value in ('0','1'):
            self.bits += fill_value * size - len(self.bits)

    def appendBytes(self, value: bytes):
        if len(value) > 0:
            self.bits += f'{int(value.hex(), 16):08b}'.zfill(len(value)*8)

    def appendBits(self, value: str):
        if not set(value) - {'0', '1'}:
            self.bits += value

    def appendInt(self, value: int, size_bits = 32):
        self.bits += f'{value:0{size_bits}b}'

