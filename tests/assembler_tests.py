import unittest

from assembler.lexer import Lexer
from assembler.rules import StringRule, RegexRule, Token

# TODO: Write `Rule`s tests


class LexerTestCase(unittest.TestCase):

    def setUp(self):
        self.lexer = Lexer(
            RegexRule("NUMBER", "[0-9]+"),
            StringRule("SYMBOL", "+", "-"),
        )

    def test_simple_input(self):
        tokens = self.lexer.tokens("1+2-3")

        self.assertEqual(list(tokens), [
            Token("NUMBER", "1"),
            Token("SYMBOL", "+"),
            Token("NUMBER", "2"),
            Token("SYMBOL", "-"),
            Token("NUMBER", "3"),
        ])
