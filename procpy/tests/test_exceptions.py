import procpy
import unittest


class TestExceptions(procpy.tests.TestInitialize):
    def test_read_error_exception(self):
        self.assertTrue(issubclass(procpy.ReadError, Exception))

    def test_process_not_found_error_exception(self):
        self.assertTrue(issubclass(procpy.SwapProcessError, procpy.ReadError))

    def test_swap_process_error(self):
        self.assertTrue(issubclass(procpy.SwapProcessError, procpy.ReadError))


if __name__ == "__main__":
    unittest.main()
