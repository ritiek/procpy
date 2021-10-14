class Bytes:
    def __init__(self, numeral):
        self.units = ["B", "KB", "MB", "GB"]
        self.numeral = int(numeral)

    def __eq__(self, bytes_):
        return self.numeral == bytes_.numeral

    def __int__(self):
        return self.numeral

    def human_readable(self):
        numeral = self.numeral
        unit_index = 0
        while numeral >= 1024 and unit_index < len(self.units):
            numeral /= 1024.0
            unit_index += 1
        unit = self.units[unit_index]
        return numeral, unit

    def __repr__(self):
        return "Bytes<(numeral={})>".format(self.numeral)
