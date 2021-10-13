import procpy
import os


class Bytes:
    def __init__(self, numeral):
        units = ["B", "KB", "MB", "GB"]
        self.units = units
        self.numeral = int(numeral)

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


class Process:
    def __init__(self, pid):
        self.pid = pid
        self._process_info = []

    def read_stat(self):
        stat_file = os.path.join(procpy.PROC_FS, str(self.pid), procpy.PROC_STAT)
        try:
            with open(stat_file, "r") as fin:
                content = fin.read()
        except FileNotFoundError:
            if self.pid == 0:
                raise SwapProcessError("PID 0: unable to read stat for swap process")
            else:
                raise ProcessNotFoundError('PID {}: "{}" does not exist'.format(
                    self.pid,
                    os.path.join(procpy.PROC_FS, str(self.pid), procpy.PROC_STAT))
                )
        self._process_info = content.split()

    def __repr__(self):
        return 'Process<(pid={})>'.format(self.pid)

    @property
    def name(self):
        return self._process_info[1][1:-1]

    @property
    def parent(self):
        return Process(self._process_info[3])

    @property
    def virtual_memory(self):
        return Bytes(self._process_info[23])
