import os

PROC_FS = "/proc/"
PROC_STAT = "stat"


class ReadError(Exception):
    pass


class ProcessNotFoundError(ReadError):
    pass


class SwapProcessError(ReadError):
    pass


class Bytes:
    def __init__(self, numeral):
        units = ["B", "KB", "MB", "GB"]
        self.units = units
        self.numeral = int(numeral)

    def __int__(self):
        return self.units

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
        stat_file = os.path.join(PROC_FS, str(self.pid), PROC_STAT)
        try:
            with open(stat_file, "r") as fin:
                content = fin.read()
        except FileNotFoundError:
            if self.pid == 0:
                raise SwapProcessError("PID 0: unable to read stat for swap process")
            else:
                raise ProcessNotFoundError('PID {}: "{}" does not exist'.format(
                    self.pid,
                    os.path.join(PROC_FS, str(self.pid), PROC_STAT))
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


class ProcFS:
    def __init__(self, _handler=Process):
        self._handler = _handler

    def _is_process(self, inode):
        inode_path = os.path.join(PROC_FS, inode)
        return os.path.isdir(inode_path) and inode.isnumeric()

    def snapshot(self):
        processes = []
        for inode in os.listdir(PROC_FS):
            if self._is_process(inode):
                try:
                    process = self._handler(inode)
                    process.read_stat()
                    processes.append(process)
                except ReadError:
                    # Ignore cases when some process no longer exists after we
                    # fetched the contents of "/proc/", but before we were able
                    # to read the "/proc/<pid>/stat".
                    pass
        return processes


def pretty_print(processes):
    formatter = "{:>7}     {:<40}  {:<12}  {:<10}"
    print(formatter.format("PID", "NAME", "PPID", "VIRTMEM"))
    for process in processes:
        size, unit = process.virtual_memory.human_readable()
        virtmem = "{}{}".format(round(size, 2), unit)
        print(formatter.format(process.pid, process.name, process.parent.pid, virtmem))


if __name__ == "__main__":
    procfs = ProcFS()
    processes = procfs.snapshot()
    pretty_print(processes)
