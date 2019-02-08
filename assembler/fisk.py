import re

from .lexer import Lexer
from .tokens import Token, RegexToken, StringToken


class Whitespace(RegexToken):

    regex = re.compile("[ \t]+")
    ignore = True


class Newline(StringToken):

    samples = "\n",
    ignore = True


class Comment(RegexToken):

    regex = re.compile(r";[^\n]*")
    ignore = True


class Number(RegexToken):

    regex = re.compile("[0-9]+")


class Identifier(RegexToken):

    regex = re.compile("[a-zA-Z_][a-zA-Z0-9_]*")


class Symbol(StringToken):

    samples = ":", ","


class EndOfFile(RegexToken):

    regex = re.compile("^$")


class Fisk16Lexer(Lexer):

    tokens = (
        Whitespace,
        Newline,
        Comment,
        Number,
        Identifier,
        Symbol,
        EndOfFile,
    )
