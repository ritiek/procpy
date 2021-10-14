import procpy
import os


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
        # Set an offset value based on whether the name field in process stat
        # contains spaces or not. This offset value helps us to correctly map
        # other properties since we split the values in stat on the space
        # character.
        last_name_index = 1
        for i, value in enumerate(self._process_info[last_name_index:]):
            if len(value) == 1:
                break
            last_name_index += 1
        name = self._process_info[1:last_name_index]
        return len(name) - 1

    def __repr__(self):
        return "Process<(pid={})>".format(self.pid)

    @property
    def name(self):
        # TODO: Perhaps we could create a cache decorator for the below `if`
        # condition and use that instead, as well as for all other properties
        # too.
        if len(self._process_info) == 0:
            self.read_stat()
        name = self._process_info[1:self._name_offset + 2]
        name = " ".join(name)
        return name[1:-1]

    @property
    def parent(self):
        if len(self._process_info) == 0:
            self.read_stat()
        return Process(self._process_info[3 + self._name_offset])

    @property
    def virtual_memory(self):
        if len(self._process_info) == 0:
            self.read_stat()
        return procpy.Bytes(self._process_info[22 + self._name_offset])

    @property
    def utime(self):
        if len(self._process_info) == 0:
            self.read_stat()
        return int(self._process_info[14 + self._name_offset])

    @property
    def stime(self):
        if len(self._process_info) == 0:
            self.read_stat()
        return int(self._process_info[15 + self._name_offset])
