#!/usr/bin/env python3

import procpy


if __name__ == "__main__":
    procfs = procpy.ProcFS()
    processes = procfs.snapshot()
    procpy.pretty_print_processes(processes)
