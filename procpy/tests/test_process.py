import procpy

import getpass


class TestProcess(procpy.tests.TestInitialize):
    def setUp(self):
        super().setUp()
        self.pid = 1337
        stat = ("1337 (tmux: client) S 1337 93385 91239 34819 "
                "93385 4194304 276 0 3 0 1 0 0 0 20 0 1 0 3557720 "
                "9011200 372 18446744073709551615 93915331723264 "
                "93915332289125 140731588120800 0 0 0 0 3674116 "
                "134433283 0 0 0 17 0 0 0 0 0 0 93915332497968 "
                "93915332569544 93915340509184 140731588121938 "
                "140731588121945 140731588121945 140731588128746 0")
        self.create_virtual_process(self.pid, stat)

    def test_existing_process(self):
        process = procpy.Process(self.pid)
        parent_process = procpy.Process(self.pid)
        self.assertEqual(process.name, "tmux: client")
        self.assertEqual(process.parent.pid, parent_process.pid)
        self.assertEqual(process.virtual_memory, procpy.Bytes(9011200))
        self.assertEqual(process.utime, 1)
        self.assertEqual(process.stime, 0)
        self.assertEqual(process.owner, getpass.getuser())

    def test_non_existing_process(self):
        process = procpy.Process(1338)
        with self.assertRaises(procpy.ProcessNotFoundError):
            process.read_stat()

    def test_swapper_process(self):
        process = procpy.Process(0)
        with self.assertRaises(procpy.SwapProcessError):
            process.read_stat()

    def test_process_repr(self):
        process = procpy.Process(34523)
        self.assertEqual(repr(process), "Process<(pid=34523)>")
