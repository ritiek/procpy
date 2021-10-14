import procpy

from io import StringIO
import getpass


class TestProcFS(procpy.tests.TestInitialize):
    def setUp(self):
        super().setUp()
        self.pids = (1337, 3585, 45086)
        stats = (
            ("1337 (tmux: client) S 1337 93385 91239 34819 "
            "93385 4194304 276 0 3 0 1 0 0 0 20 0 1 0 3557720 "
            "9011200 372 18446744073709551615 93915331723264 "
            "93915332289125 140731588120800 0 0 0 0 3674116 "
            "134433283 0 0 0 17 0 0 0 0 0 0 93915332497968 "
            "93915332569544 93915340509184 140731588121938 "
            "140731588121945 140731588121945 140731588128746 0"),

            ("3585 (dolphin) S 818 3585 3585 0 -1 4194304 3358 "
            "0 162 0 1162 1470 0 0 20 0 3 0 61364 301756416 "
            "1139 18446744073709551615 93871585140736 "
            "93871585700821 140722575996416 0 0 0 0 4096 0 0 "
            "0 0 17 6 0 0 0 0 0 93871585936472 93871585988640 "
            "93871594770432 140722576004632 140722576004658 "
            "140722576004658 140722576007143 0"),

            ("45086 (fusermount) S 3498 3506 3506 0 -1 1077936384 "
            "127 0 0 0 0 0 0 0 20 0 1 0 61316 2523136 259 "
            "18446744073709551615 1 1 0 0 0 0 2147221247 4096 "
            "0 0 0 0 17 5 0 0 0 0 0 0 0 0 0 0 0 0 0"),
        )
        for pid, stat in zip(self.pids, stats):
            self.create_virtual_process(pid, stat)

    def _assert_processes(self, process, process_):
        self.assertEqual(process.pid, process_.pid)
        self.assertEqual(process.name, process_.name)
        self.assertEqual(process.parent.pid, process_.parent.pid)
        self.assertEqual(process.virtual_memory, process_.virtual_memory)
        self.assertEqual(process.utime, process_.utime)
        self.assertEqual(process.stime, process_.stime)
        self.assertEqual(process.owner, process_.owner)

    def test_snapshot(self):
        procfs = procpy.ProcFS()
        processes = procfs.snapshot()
        for process in processes:
            self.assertTrue(process.pid in self.pids)
            process_ = procpy.Process(process.pid)
            self._assert_processes(process, process_)

    def test_pretty_print(self):
        # TODO: Looks ugly. Is there a better way to assert for output?
        expected_header = "    PID     NAME                                      PPID     VIRTMEM     UTIME   STIME    OWNER     "
        expected_output = ["  45086     fusermount                                3498     2.41MB      0       0        {owner:<10}",
                           "   3585     dolphin                                   818      287.78MB    1162    1470     {owner:<10}",
                           "   1337     tmux: client                              1337     8.59MB      1       0        {owner:<10}"]

        for n, line in enumerate(expected_output):
            expected_output[n] = line.format(owner=getpass.getuser())

        procfs = procpy.ProcFS()
        processes = procfs.snapshot()

        output = StringIO()
        procpy.pretty_print_processes(processes, out=output)
        output = output.getvalue().split("\n")

        header = output.pop(0)
        # Ignore the empty line at the end of the output.
        output.pop()
        # I noticed that the output can either be in ascending or descending
        # order depending on the machine.
        # (probably depends on OS things and/or Python version?)
        # Let's sort everything for consistency in any case.
        expected_output.sort()
        output.sort()

        self.assertEqual(header, expected_header)
        self.assertEqual(output, expected_output)
