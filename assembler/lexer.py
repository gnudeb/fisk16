from typing import NamedTuple, Union, Tuple
import re


Token = NamedTuple("Token", [
    ("type", str),
    ("value", Union[str, int])
])


class Rule:
    def __init__(self, name: str, regex: str):
        self.name = name
        self.regex = re.compile(regex)

    def __str__(self):
        return "<Rule '{}'>".format(self.name)

    def __repr__(self):
        return self.__str__()

    def match(self, string) -> Tuple[Token, int]:
        match = self.regex.match(string)
        if match:
            token = Token(self.name, match.group())
            return token, match.end()


rules = [Rule(name, regex) for name, regex in (
    ("whitespace", r"[ \t]+"),
    ("newline", r"\n"),
    ("identifier", "[a-zA-Z][_a-zA-Z0-9]*"),
    ("number", "[0-9]+"),
    ("colon", ":"),
    ("comment", r";[^\n]*\n"),
    ("comma", ","),
    ("lbracket", r"\["),
    ("rbracket", r"\]"),
)]


def _lex(code: str, tokens: Tuple=()) -> Tuple[Token]:
    if not code:
        return tokens
    for rule in rules:
        match = rule.match(code)
        if match:
            new_token, offset = match
            return _lex(code[offset:], (*tokens, new_token))

    raise RuntimeError("Lexical error at \n{}".format(code[:10]))


def lex(code: str):
    ignore = ("whitespace", "newline", "comment", "comma")
    return tuple(token for token in _lex(code) if token.type not in ignore)
