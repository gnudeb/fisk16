from typing import Tuple, Type

from .exceptions import UnexpectedInput
from .tokens import Token


# TODO: Maybe it would be a better idea not to force subclassing
#  and instead store `tokens` and `stream` as a fields of `Lexer`'s instance


class Lexer:
    """
    This class is used to transform a code stream into a stream of tokens.

    This class is intended to be subclassed.
    """

    tokens: Tuple[Type[Token]] = ()

    @classmethod
    def produce_tokens(cls, stream: str):
        # TODO: Implement offset tracking (as a field in `Token` instance)
        while stream:
            next_token, stream = cls.produce_token(stream)
            if not next_token.ignore:
                yield next_token

        # Trying to match one more token if `tokens` contain something like
        # `EndOfFile` token that matches empty string
        try:
            last_token, _ = cls.produce_token(stream)
        except UnexpectedInput:
            return

        if last_token and not last_token.ignore:
            yield last_token

    @classmethod
    def produce_token(cls, stream: str):
        for token_cls in cls.tokens:
            token = token_cls.from_stream(stream)
            if token is not None:
                remaining_stream = stream[token.size:]
                return token, remaining_stream
        # TODO: Modify the lexing algorithm to not mangle `stream`
        raise UnexpectedInput(stream.split("\n", 1)[0])
