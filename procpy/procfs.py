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
            if not self._is_process(inode):
                continue
            process = self._handler(inode)
            try:
                process.read_stat()
            except procpy.ReadError:
                # Ignore cases when some process no longer exists after we
                # fetched the contents of "/proc/", but before we were able
                # to read the "/proc/<pid>/stat".
                continue
            processes.append(process)
        return processes
