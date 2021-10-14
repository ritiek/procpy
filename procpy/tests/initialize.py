import procpy

import shutil
import tempfile
import os
import unittest


class TestInitialize(unittest.TestCase):
    def setUp(self):
        self._old_proc_fs = procpy.PROC_FS
        self.temp_dir = tempfile.mkdtemp()
        procpy.PROC_FS = self.temp_dir

    def create_virtual_process(self, pid, stat):
        pid_dir = os.path.join(self.temp_dir, str(pid))
        os.makedirs(pid_dir)
        stat_file = os.path.join(pid_dir, "stat")
        with open(stat_file, "w") as fout:
            fout.write(stat)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        procpy.PROC_FS = self._old_proc_fs

