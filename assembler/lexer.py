from .exceptions import UnexpectedInput
from .rules import Rule


class Lexer:

    def __init__(self, *rules: Rule):
        self.rules = rules
        self.stream = ""

    def tokens(self, stream: str):
        self.stream = stream

        while self.stream:
            yield self.next_token()

    def next_token(self):
        token = None

        for rule in self.rules:
            token, self.stream = rule.match(self.stream)
            if token is None:
                continue
            return token

        if token is None:
            raise UnexpectedInput(self.stream.split("\n")[:2])
