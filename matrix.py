from tables import *

class Matrix:
    quiet_zone_width = 4
    finder_pattern_width = 7
    alignment_pattern_width = 5
    separator_width = 1

    def __init__(self, data_bits, version, correction_level):
        self.version = version
        self.correction_level = correction_level
        self.size = getWidth(version)
        self.data = np.ones((self.size + 2*self.quiet_zone_width, self.size + 2*self.quiet_zone_width)) * ModuleType.Data

        self.reserveFormatInformationArea()
        self.reserveVersionArea()
        self.writeQuietZone()
        self.writeFinderPatterns()
        self.writeSeparatorPatterns()
        self.writeTimingPatterns()
        self.writeAlignmentPatterns()
        self.writeDarkModule()
        data_mask = self.createDataMask()
        self.writeDataBits(data_bits, data_mask)
        self.writeVersionInformationPattern()
        self.maskData(data_mask)

    def writeQuietZone(self):
        pattern = np.ones((self.quiet_zone_width, self.size + 2*self.quiet_zone_width)) * ModuleType.Light

        self._writePattern(pattern, -self.quiet_zone_width, -self.quiet_zone_width)
        self._writePattern(pattern, -self.quiet_zone_width, self.size)
        self._writePattern(np.transpose(pattern), -self.quiet_zone_width, -self.quiet_zone_width)
        self._writePattern(np.transpose(pattern), self.size, -self.quiet_zone_width)

    def writeFinderPatterns(self):
        self._writePattern(finder_pattern, 0, 0)
        self._writePattern(finder_pattern, self.size - self.finder_pattern_width, 0)
        self._writePattern(finder_pattern, 0, self.size - self.finder_pattern_width)

    def writeSeparatorPatterns(self):
        pattern = np.ones((self.separator_width, self.finder_pattern_width + 1)) * ModuleType.Light

        self._writePattern(pattern, 0, self.finder_pattern_width)
        self._writePattern(np.transpose(pattern), self.finder_pattern_width, 0)

        self._writePattern(pattern, self.size - self.finder_pattern_width - 1, self.finder_pattern_width)
        self._writePattern(np.transpose(pattern), self.size - self.finder_pattern_width - 1, 0)

        self._writePattern(pattern, 0, self.size - self.finder_pattern_width - 1)
        self._writePattern(np.transpose(pattern), self.finder_pattern_width, self.size - self.finder_pattern_width - 1)

    def writeTimingPatterns(self):
        pattern = np.ones((self.size - 2*(self.finder_pattern_width + self.separator_width), 1)) * ModuleType.Dark
        pattern[1::2] = ModuleType.Light

        self._writePattern(np.transpose(pattern), self.finder_pattern_width + self.separator_width, 6)
        self._writePattern(pattern, 6, self.finder_pattern_width + self.separator_width)

    def writeAlignmentPatterns(self):
        center_coordinates = getAlignmentPatternCoordinatesList(self.version)

        alignment_pattern_half_width = int(np.floor(self.alignment_pattern_width/2))

        for x, y in center_coordinates:
            if (x != 6 or y != 6) and (y != 6 or x < (self.size - self.finder_pattern_width)) and (x != 6 or y < (self.size - self.finder_pattern_width)):
                self._writePattern(alignment_pattern, x-alignment_pattern_half_width, y-alignment_pattern_half_width)

    def reserveFormatInformationArea(self):
        pattern = np.ones((self.separator_width, self.finder_pattern_width + 2)) * ModuleType.FormatInformation

        self._writePattern(pattern, 0, self.finder_pattern_width + 1)
        self._writePattern(np.transpose(pattern), self.finder_pattern_width + 1, 0)

        pattern = np.ones((self.separator_width, self.finder_pattern_width + 1)) * ModuleType.FormatInformation

        self._writePattern(pattern, self.size - self.finder_pattern_width - 1, self.finder_pattern_width + 1)
        self._writePattern(np.transpose(pattern), self.finder_pattern_width + 1, self.size - self.finder_pattern_width - 1)

    def reserveVersionArea(self):
        if self.version >= 7:
            pattern = np.ones((3, 6)) * ModuleType.Version

            self._writePattern(pattern, 0, self.size - self.finder_pattern_width - 4)
            self._writePattern(np.transpose(pattern), self.size - self.finder_pattern_width - 4, 0)

    def writeDarkModule(self):
        self._writeModule(self.finder_pattern_width + self.separator_width, self.size - self.finder_pattern_width - self.separator_width, ModuleType.Dark)

    def createDataMask(self):
        return self.data == ModuleType.Data

    def writeDataBits(self, data_bits, data_mask):

        x = self.size-1
        y = self.size-1
        upwards = True
        side = True

        def _advance():

            nonlocal x
            nonlocal y
            nonlocal upwards
            nonlocal side

            if side == True:
                x -= 1
            else:
                if upwards == True:
                    y -= 1
                    if y == -1:
                        y = 0
                        upwards = False
                        x -= 2
                else:
                    y += 1
                    if y == self.size:
                        y = self.size-1
                        upwards = True
                        x -= 2
                x += 1
            side = not side

        for b in data_bits.bits:

            while not data_mask[self.quiet_zone_width + y, self.quiet_zone_width + x]:
                if x != self.finder_pattern_width - 1:
                    _advance()
                else:
                    x -= 1
                    
            self._writeModule(x, y, ModuleType.Dark if b == '1' else ModuleType.Light)
            _advance()

    def _applyMaskPattern(self, p, data_mask):
        f = mask_patterns[p]

        for i in range(self.size):
            for j in range(self.size):
                if data_mask[self.quiet_zone_width + j, self.quiet_zone_width + i]:
                    if f(i,j):
                        self._writeModule(i, j, ModuleType.Dark if self._getModule(i, j) == ModuleType.Light else ModuleType.Light)

    def maskData(self, data_mask):
        score = 0

        mask_pattern_index = 0

        data = self.data.copy()

        for p in range(len(mask_patterns)):

            self.data = data.copy()

            self._applyMaskPattern(p, data_mask)
            self.writeFormatInformationPattern(p)

            mask_score = self.evaluatePenaltyScore()
            if mask_score < score:
                score = mask_score
                mask_pattern_index = p

        self.data = data

        self._applyMaskPattern(mask_pattern_index, data_mask)
        self.writeFormatInformationPattern(mask_pattern_index)


    def writeFormatInformationPattern(self, mask_pattern_index):
        pattern = format_information_bits[self.correction_level][mask_pattern_index]
        self._writePattern(pattern[:,:6], 0, self.finder_pattern_width + 1)
        self._writePattern(pattern[:,6:8], 7, self.finder_pattern_width + 1)
        self._writePattern(pattern[:,8:9], 8, self.finder_pattern_width)
        self._writePattern(np.transpose(np.flip(pattern[:,9:15])), 8, 0)
        
        self._writePattern(np.transpose(np.flip(pattern[:,:7])), 8, self.size - self.finder_pattern_width - self.separator_width + 1)
        self._writePattern(pattern[:,7:15], self.size - self.finder_pattern_width - self.separator_width, self.finder_pattern_width + 1)

    def writeVersionInformationPattern(self):
        if self.version >= 7:
            pattern = version_information_bits[self.version]

            self._writePattern(pattern, self.size - self.finder_pattern_width - 4, 0)
            self._writePattern(np.transpose(pattern), 0, self.size - self.finder_pattern_width - 4)

    def evaluatePenaltyScore(self):
        score = 0

        # Penalty score 1

        count_h = [0] * self.size
        count_v = [0] * self.size
        
        for y in range(self.size):
            for x in range(self.size):
                if self._getModule(x,y) == ModuleType.Light:
                    if count_h[x] >= 0:
                        count_h[x] += 1
                    else:
                        count_h[x] = 1
                    if count_h[x] == 5:
                        score += 3
                    elif count_h[x] > 5:
                        score += 1

                elif self._getModule(x,y) == ModuleType.Dark:
                    if count_h[x] <= 0:
                        count_h[x] -= 1
                    else:
                        count_h[x] = -1
                    if count_h[x] == -5:
                        score += 3
                    elif count_h[x] < -5:
                        score += 1

                if self._getModule(y,x) == ModuleType.Light:
                    if count_v[x] >= 0:
                        count_v[x] += 1
                    else:
                        count_v[x] = 1
                    if count_v[x] == 5:
                        score += 3
                    elif count_v[x] > 5:
                        score += 1

                elif self._getModule(y,x) == ModuleType.Dark:
                    if count_v[x] <= 0:
                        count_v[x] -= 1
                    else:
                        count_v[x] = -1
                    if count_v[x] == -5:
                        score += 3
                    elif count_v[x] < -5:
                        score += 1

        # Penalty score 2
        for y in range(self.size-1):
            for x in range(self.size-1):
                if self._getModule(x,y) == self._getModule(x+1,y) == self._getModule(x,y+1) == self._getModule(x+1,y+1):
                    if self._getModule(x,y) == ModuleType.Light or self._getModule(x,y) == ModuleType.Dark:
                        score += 3

        # Penalty score 3
        pattern_1 = np.array([ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Dark, ModuleType.Dark, ModuleType.Light, ModuleType.Dark, ModuleType.Light, ModuleType.Light, ModuleType.Light, ModuleType.Light])
        pattern_2 = np.flip(pattern_1)

        pattern_len = len(pattern_1)

        transposed_data = np.transpose(self.data)

        for y in range(self.size):
            for x in range(self.size-pattern_len):
                if (self.data[self.quiet_zone_width + y, self.quiet_zone_width + x: self.quiet_zone_width + x + pattern_len] == pattern_1).all() \
                or (self.data[self.quiet_zone_width + y, self.quiet_zone_width + x: self.quiet_zone_width + x + pattern_len] == pattern_2).all() \
                or (transposed_data[self.quiet_zone_width + y, self.quiet_zone_width + x:self.quiet_zone_width + x + pattern_len] == pattern_1).all() \
                or (transposed_data[self.quiet_zone_width + y, self.quiet_zone_width + x:self.quiet_zone_width + x + pattern_len] == pattern_2).all():
                    score += 40

        # Penalty score 4
        dark_modules = np.count_nonzero(self.data == ModuleType.Dark)
        light_modules = np.count_nonzero(self.data == ModuleType.Light)

        percentage = (dark_modules / (dark_modules + light_modules)) * 100

        previous_multiple = (m.floor(percentage/5))*5
        next_multiple = previous_multiple+5

        value_1 = int(abs(previous_multiple-50)/5)
        value_2 = int(abs(next_multiple-50)/5)

        score += min(value_1, value_2) * 10

        return score


    def _getModule(self, x: int, y: int):
        return self.data[self.quiet_zone_width + y, self.quiet_zone_width + x]

    def _writeModule(self, x: int, y: int, val: ModuleType):
        self.data[self.quiet_zone_width + y, self.quiet_zone_width + x] = val

    def _writePattern(self, pattern, startX, startY):
        sizeY, sizeX = pattern.shape
        self.data[self.quiet_zone_width + startY:self.quiet_zone_width + startY + sizeY, self.quiet_zone_width + startX:self.quiet_zone_width + startX + sizeX] = pattern