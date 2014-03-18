from unittest import TestCase

try:
    from StringIO import StringIO as BytesIO
except ImportError:
    import io
    BytesIO = io.BytesIO

from routeros_api import base_api


class TestEncodeLength(TestCase):
    def test_zero(self):
        result = base_api._encode_length(0)
        expected_number = 0
        expected_length = 1
        expected = (expected_number, expected_length)
        self.assertEqual(expected, result)

    def test_one(self):
        result = base_api._encode_length(1)
        expected_number = 1
        expected_length = 1
        expected = (expected_number, expected_length)
        self.assertEqual(expected, result)

    def test_over_0x80(self):
        result = base_api._encode_length(300)
        expected_number = 33068
        expected_length = 2
        expected = (expected_number, expected_length)
        self.assertEqual(expected, result)

    def test_over_0x3FFF(self):
        result = base_api._encode_length(17000)
        expected_number = 12599912
        expected_length = 3
        expected = (expected_number, expected_length)
        self.assertEqual(expected, result)

    def test_0x10000000(self):
        result = base_api._encode_length(0x10000000)
        expected_number = 0xF010000000
        expected_length = 5
        expected = (expected_number, expected_length)
        self.assertEqual(expected, result)

    def test_to_big(self):
        self.assertRaises(ValueError, base_api._encode_length, 0x100000000)


class TestDecodeLength(TestCase):
    def test_zero(self):
        data = BytesIO(b"\x00")
        self.assertEqual(0, base_api.decode_length(data))

    def test_over_0x80(self):
        data = BytesIO(b"\x81\x2c")
        self.assertEqual(300, base_api.decode_length(data))

    def test_over_0x3FFF(self):
        data = BytesIO(b"\xc0\x42\x68")
        self.assertEqual(17000, base_api.decode_length(data))

    def test_0x10000000(self):
        data = BytesIO(b"\xF0\x10\x00\x00\x00")
        self.assertEqual(0x10000000, base_api.decode_length(data))

    def test_wrong_prefix(self):
        data = BytesIO(b"\xF8")
        self.assertRaises(ValueError, base_api.decode_length, data)


class TestToBytes(TestCase):
    def test_zero(self):
        result = base_api.to_bytes(0, 1)
        expected = b'\x00'
        self.assertEqual(expected, result)

    def test_multiple_bytes(self):
        result = base_api.to_bytes(0x1112, 2)
        expected = b'\x11\x12'
        self.assertEqual(expected, result)
