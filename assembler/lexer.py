from typing import Tuple, Type

from .exceptions import UnexpectedInput
from .tokens import Token

# TODO: Write tests


class Lexer:
    """
    This class is used to transform a code stream into a stream of tokens.

    This class is intended to be subclassed.
    """

    tokens: Tuple[Type[Token]] = ()

    def __init__(self, stream: str):
        self.stream: str = stream
        self.offset = 0

    def produce_tokens(self):
        while not self.is_stream_exhausted():
            next_token = self.produce_token()
            if not next_token.ignore:
                yield next_token

        # Trying to match one more token if `tokens` contain something like
        # `EndOfFile` token that matches empty string
        try:
            last_token = self.produce_token()
        except UnexpectedInput:
            return

        if last_token and not last_token.ignore:
            yield last_token

    def produce_token(self) -> Token:
        for token_cls in self.tokens:
            effective_stream = self.stream[self.offset:]
            token = token_cls.from_stream(effective_stream)
            if token is not None:
                token.offset = self.offset
                self.offset += token.size
                return token
        # TODO: Output whole line that caused error, not just ending
        raise UnexpectedInput(self.stream[self.offset:].split("\n", 1)[0])

    def is_stream_exhausted(self):
        return self.offset >= len(self.stream)
