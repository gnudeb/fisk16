from functools import partial
from typing import Tuple

from .exceptions import ParsingError, UnexpectedTokenError, UnexpectedTokenValueError
from .lexer import Token


class Parser:
    def __init__(self, tokens: Tuple[Token]):
        self.tokens = tokens
        self.cursor = 0

    def expect(self, token_type: str, token_value: str=None):
        try:
            token = self.tokens[self.cursor]
        except IndexError:
            raise ParsingError

        if not token.type == token_type:
            raise UnexpectedTokenError(token_type, token.type)

        if token_value and token.value != token_value:
            raise UnexpectedTokenValueError(token_value, token.value)

        self.cursor += 1
        return token

    def optional(self, rule):
        cursor = self.cursor
        try:
            return rule()
        except ParsingError:
            self.cursor = cursor
            return {}

    def _assert(self, expression):
        if not expression:
            raise ParsingError

    def choose(self, *rules):
        for rule in rules:
            try:
                return rule()
            except ParsingError:
                pass
        raise ParsingError

    def star(self, rule):
        results = []
        while True:
            try:
                results.append(rule())
            except ParsingError:
                return tuple(results)

    def program(self):
        packed_lines = self.star(self.line)
        self.expect("identifier", "end")

        lines = []
        for line in packed_lines:
            lines.extend(item for item in line if item)
        return lines

    def line(self):
        line = (
            self.optional(self.label),
            self.optional(self.command),
        )
        self._assert(any(line))
        return line

    def label(self):
        label = self.expect("identifier").value
        self.expect("colon")
        return {
            "type": "label",
            "label": label
        }

    def command(self):
        mnemonic = self.expect("identifier").value
        if mnemonic not in ('mov', 'inc'):
            raise ParsingError
        return {
            "type": "command",
            "mnemonic": mnemonic,
            "operands": (
                self.optional(self.operand),
                self.optional(self.operand)
            )
        }

    def operand(self):
        return self.choose(
            self.direct_operand,
            self.indirect_operand,
        )

    def direct_operand(self):
        return {
            **self.choose(
                self.register,
                self.number,
            ),
            "indirect": False,
        }

    def indirect_operand(self):
        self.expect("lbracket")
        operand = self.direct_operand()
        self.expect("rbracket")
        return {
            **operand,
            "indirect": True,
        }


    def register(self):
        register = self.expect("identifier").value
        self._assert(register in ('r0', 'r1'))
        return {
            "type": "register",
            "value": register
        }

    def number(self):
        return {
            "type": "number",
            "value": self.expect("number").value
        }
