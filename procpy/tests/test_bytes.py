import procpy


class TestBytes(procpy.tests.TestInitialize):
    def setUp(self):
        super().setUp()
        self.bytes = procpy.Bytes(34295)

    def test_human_readable(self):
        size, unit = self.bytes.human_readable()
        self.assertEqual((round(size, 2), unit), (33.49, "KB"))

    def test_equals(self):
        self.assertEqual(self.bytes, procpy.Bytes(34295))

    def test_int_value(self):
        self.assertEqual(int(self.bytes), 34295)

    def test_repr(self):
        self.assertEqual(repr(self.bytes), "Bytes<(numeral=34295)>")
