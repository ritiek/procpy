import sys


def pretty_print_processes(processes, out=sys.stdout):
    formatter = "{:>7}     {:<40}  {:<7}  {:<10}  {:<6}  {:<7}  {:<10}"
    heading = formatter.format("PID", "NAME", "PPID", "VIRTMEM", "UTIME", "STIME", "OWNER")
    print(heading, file=out)
    for process in processes:
        size, unit = process.virtual_memory.human_readable()
        virtmem = "{}{}".format(size, unit)
        entry = formatter.format(
            process.pid,
            process.name,
            process.parent.pid,
            virtmem,
            process.utime,
            process.stime,
            process.owner,
        )
        print(entry, file=out)
