
class LexerError(Exception):
    pass


class UnexpectedInput(LexerError):
    pass


class ParsingError(Exception):
    pass


class UnexpectedTokenError(ParsingError):
    def __init__(self, expected, found):
        msg = "Expected token of type '{}', found '{}'".format(expected, found)
        super().__init__(msg)


class UnexpectedTokenValueError(ParsingError):
    def __init__(self, expected, found):
        msg = "Expected token with value '{}', found '{}'".format(expected, found)
        super().__init__(msg)

