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
        self.line = 1
        self.column = 1

    @property
    def current_line(self):
        return self.stream.split("\n")[self.line - 1]

    def produce_tokens(self):
        while not self.is_stream_exhausted():
            next_token = self.produce_token()
            self._update_cursor(next_token.value)
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

        self._die()

    def is_stream_exhausted(self):
        return self.offset >= len(self.stream)

    def _update_cursor(self, new_input: str):
        """
        Update `line` and `column` fields based on `new_input`.

        Each newline character increments `line` and resets `column` to `1`.
        Each tab character increments `column` by 8.
        Each other character increments `column`.
        """
        for char in new_input:
            if char == "\n":
                self.line += 1
                self.column = 1
            elif char == "\t":
                self.column += 8
            else:
                self.column += 1

    def _die(self):
        hint = "^".rjust(self.column)

        raise UnexpectedInput(
            f"Line {self.line}\n"
            f"{self.current_line}\n"
            f"{hint}")
