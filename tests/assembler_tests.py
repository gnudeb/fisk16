import re
import unittest

from assembler.tokens import StringToken, RegexToken


class StringTokenTestCase(unittest.TestCase):

    def test_single_sample(self):

        class TestToken(StringToken):
            samples = "%",

        token = TestToken.from_stream("%")

        self.assertIsNotNone(token)
        self.assertEqual(token.value, "%")
        self.assertEqual(token.size, 1)

    def test_multiple_samples(self):

        class TestToken(StringToken):
            samples = "Aa", "Bb"

        token = TestToken.from_stream("AaBb")
        self.assertIsNotNone(token)
        token = TestToken.from_stream("BbAa")
        self.assertIsNotNone(token)

    def test_negative(self):

        class TestToken(StringToken):
            samples = "foo",

        token = TestToken.from_stream("bar")
        self.assertIsNone(token)


class RegexTokenTestCase(unittest.TestCase):

    def test_positive(self):

        class TestToken(RegexToken):
            regex = re.compile("[a-z]+")

        token = TestToken.from_stream("test test")
        self.assertIsNotNone(token)
        self.assertEqual(token.value, "test")
        self.assertEqual(token.size, 4)


if __name__ == '__main__':
    unittest.main()
