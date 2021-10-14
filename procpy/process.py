import procpy
import os


class Bytes:
    def __init__(self, numeral):
        self.units = ["B", "KB", "MB", "GB"]
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
        self.pid = int(pid)
        self._process_info = []
        self._name_offset = 0

    def read_stat(self):
        stat_file = os.path.join(procpy.PROC_FS, str(self.pid), procpy.PROC_STAT)
        try:
            with open(stat_file, "r") as fin:
                content = fin.read()
        except FileNotFoundError:
            if self.pid == 0:
                raise procpy.SwapProcessError("PID 0: unable to read stat for swap process")
            else:
                raise procpy.ProcessNotFoundError('PID {}: "{}" does not exist'.format(
                    self.pid,
                    os.path.join(procpy.PROC_FS, str(self.pid), procpy.PROC_STAT))
                )
        self._process_info = content.split()
        self._name_offset = self._calculate_name_offset()

    def _calculate_name_offset(self):
        last_name_index = 1
        for i, value in enumerate(self._process_info[last_name_index:]):
            if len(value) == 1:
                break
            last_name_index += 1
        name = self._process_info[1:last_name_index]
        return len(name) - 1

    def __repr__(self):
        return 'Process<(pid={})>'.format(self.pid)

    @property
    def name(self):
        name = self._process_info[1:self._name_offset + 2]
        name = " ".join(name)
        return name[1:-1]

    @property
    def parent(self):
        return Process(self._process_info[3 + self._name_offset])

    @property
    def virtual_memory(self):
        return Bytes(self._process_info[22 + self._name_offset])
