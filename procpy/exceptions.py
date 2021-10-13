class ReadError(Exception):
    pass


class ProcessNotFoundError(ReadError):
    pass


class SwapProcessError(ReadError):
    pass
