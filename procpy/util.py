import sys


def pretty_print_processes(processes, out=sys.stdout):
    formatter = "{:>7}     {:<40}  {:<12}  {:<10}"
    print(formatter.format("PID", "NAME", "PPID", "VIRTMEM"), file=out)
    for process in processes:
        size, unit = process.virtual_memory.human_readable()
        virtmem = "{}{}".format(size, unit)
        entry = formatter.format(
            process.pid,
            process.name,
            process.parent.pid,
            virtmem,
        )
        print(entry, file=out)
