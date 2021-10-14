#!/usr/bin/env python3

import procpy


def pretty_print(processes):
    formatter = "{:>7}     {:<40}  {:<12}  {:<10}"
    print(formatter.format("PID", "NAME", "PPID", "VIRTMEM"))
    for process in processes:
        size, unit = process.virtual_memory.human_readable()
        virtmem = "{}{}".format(round(size, 2), unit)
        print(formatter.format(process.pid, process.name, process.parent.pid, virtmem))


if __name__ == "__main__":
    procfs = procpy.ProcFS()
    processes = procfs.snapshot()
    pretty_print(processes)
