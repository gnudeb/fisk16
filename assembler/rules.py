import re
from typing import NamedTuple, Pattern, Optional, Tuple


class Token(NamedTuple):
    type: str
    value: str

    @property
    def size(self):
        return len(self.value)


class Rule:

    def __init__(self, name: str):
        self.name = name

    def match(self, stream: str) -> Tuple[Optional[Token], str]:
        """Match input `stream` to internal rule and return matched string"""
        raise NotImplementedError


class StringRule(Rule):

    def __init__(self, name: str, *samples: str):
        super().__init__(name)
        self.samples = samples

    def match(self, stream: str) -> Tuple[Optional[Token], str]:
        for sample in self.samples:
            if stream.startswith(sample):
                token = Token(self.name, sample)
                return token, stream[token.size:]

        return None, stream


class RegexRule(Rule):

    def __init__(self, name: str, regex: str):
        super().__init__(name)
        self.regex: Pattern = re.compile(regex)

    def match(self, stream: str) -> Tuple[Optional[Token], str]:
        match = self.regex.match(stream)
        if not match:
            return None, stream

        try:
            value = match.groups()[0]
        except IndexError:
            value = match.group()

        _, size = match.span()

        return Token(self.name, value), stream[size:]

