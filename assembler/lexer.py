from typing import Tuple, Type

from .exceptions import UnexpectedInput
from .tokens import Token


# TODO: Maybe it would be a better idea not to force subclassing
#  and instead store `tokens` and `stream` as a fields of `Lexer`'s instance

# TODO: Write tests


class Lexer:
    """
    This class is used to transform a code stream into a stream of tokens.

    This class is intended to be subclassed.
    """

    tokens: Tuple[Type[Token]] = ()

    @classmethod
    def produce_tokens(cls, stream: str):

        offset = 0

        while offset < len(stream):
            next_token, offset = cls.produce_token(stream, offset)
            if not next_token.ignore:
                yield next_token

        # Trying to match one more token if `tokens` contain something like
        # `EndOfFile` token that matches empty string
        try:
            last_token, _ = cls.produce_token(stream, offset)
        except UnexpectedInput:
            return

        if last_token and not last_token.ignore:
            yield last_token

    @classmethod
    def produce_token(cls, stream: str, offset: int) -> Tuple[Token, int]:
        for token_cls in cls.tokens:
            effective_stream = stream[offset:]
            token = token_cls.from_stream(effective_stream)
            if token is not None:
                token.offset = offset
                new_offset = offset + token.size
                return token, new_offset

        raise UnexpectedInput(stream.split("\n", 1)[0])
