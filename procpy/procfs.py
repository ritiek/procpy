import procpy
import os


class ProcFS:
    def __init__(self, _handler=procpy.Process):
        self._handler = _handler

    def _is_process(self, inode):
        inode_path = os.path.join(procpy.PROC_FS, inode)
        return os.path.isdir(inode_path) and inode.isnumeric()

    def snapshot(self):
        processes = []
        for inode in os.listdir(procpy.PROC_FS):
            if self._is_process(inode):
                try:
                    process = self._handler(inode)
                    process.read_stat()
                    processes.append(process)
                except procpy.ReadError:
                    # Ignore cases when some process no longer exists after we
                    # fetched the contents of "/proc/", but before we were able
                    # to read the "/proc/<pid>/stat".
                    pass
        return processes
