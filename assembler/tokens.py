import re
from typing import Pattern


class Token:
    """
    Base token class from which all useful token classes are derived.

    This class is abstract and is intended to be subclassed by user, though
    `StringToken` and `RegexToken` should be enough for regular applications.

    `Token`'s subclasses must implement `from_stream`, as it is a primary way
    of using `Token`s.
    """

    ignore = False

    def __init__(self, value: str):
        self.value = value
        self.offset = None

    def __repr__(self):
        class_name = self.__class__.__name__

        if not self.offset:
            return f"<{class_name} {self.sanitized_value}>"

        return f"<{self.offset}:{class_name} {self.sanitized_value}>"

    @property
    def size(self):
        """Return the length of this token's value."""
        return len(self.value)

    @property
    def sanitized_value(self):
        return self.value\
            .replace("\n", "<NL>")\
            .replace("\t", "<TAB>")\
            .replace(" ", "<SPC>")

    @classmethod
    def from_stream(cls, stream: str):
        """Return a token representing a matched sequence or `None`."""
        raise NotImplementedError


class StringToken(Token):
    """
    This token matches any string sample from `samples`.

    This class is intended to be subclassed in a following way:

    >>> class PunctuationMark(StringToken):
    ...     samples = ".", ",", "!", "?"

    The class, defined above, will return a token upon call to `from_stream`
    if first character of code stream is one of `sample`s.
    """

    samples = ()
    # TODO: Implement `ignore_case` parameter

    @classmethod
    def from_stream(cls, stream: str):
        for sample in cls.samples:
            if stream.startswith(sample):
                return cls(sample)

        return None


class RegexToken(Token):
    """This token matches a `regex`.

    This class is intended to be subclassed in a following way:

    >>> class Identifier(RegexToken):
    ...     regex = re.compile("[_a-zA-Z][_a-zA-Z0-9]{0,30}")

    The class, defined above, will return a token upon call to `from_stream`
    if code stream starts with a valid C identifier.
    """

    regex: Pattern = None

    @classmethod
    def from_stream(cls, stream: str):
        match = cls.regex.match(stream)
        if match:
            matched_string = match.group()
            return cls(matched_string)
