from dataclasses import dataclass
from tokenizer import *


@dataclass
class IntegerNode:
    value: int

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"IntegerNode: {str(self.value)}"


@dataclass
class DecimalNode:
    value: float

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"DecimalNode: {str(self.value)}"


@dataclass
class MinusNode:
    value: any

    def __str__(self):
        return f"(-{str(self.value)})"

    def __repr__(self):
        return f"MinusNode: {str(self)}"


@dataclass
class AddNode:
    left_node: any
    right_node: any

    def __str__(self):
        return f"({self.left_node} + {self.right_node})"

    def __repr__(self) -> str:
        return f"AddNode: {str(self)}"


@dataclass
class SubNode:
    left_node: any
    right_node: any

    def __str__(self):
        return f"({self.left_node} - {self.right_node})"

    def __repr__(self) -> str:
        return f"SubNode: {str(self)}"


@dataclass
class MulNode:
    left_node: any
    right_node: any

    def __str__(self):
        return f"({self.left_node} * {self.right_node})"

    def __repr__(self) -> str:
        return f"MulNode: {str(self)}"


@dataclass
class DivNode:
    left_node: any
    right_node: any

    def __str__(self):
        return f"({self.left_node} / {self.right_node})"

    def __repr__(self) -> str:
        return f"DivNode: {str(self)}"


@dataclass
class PowNode:
    left_node: any
    right_node: any

    def __str__(self):
        return f"({self.left_node} ^ {self.right_node})"

    def __repr__(self) -> str:
        return f"PowNode: {str(self)}"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self._tokens_iterator = iter(tokens)
        self._current_token = self._advance_token()

    def _advance_token(self):
        try:
            return next(self._tokens_iterator)
        except StopIteration:
            return None

    def parse(self):
        result = self._create_expression()

        if self._current_token is None:
            return result

        raise SyntaxError(f"Did not expect {self._current_token} after {result}")

    def _create_expression(self):
        if self._current_token is None:
            return None

        lhs = self._create_term()

        if self._current_token is AddToken or self._current_token is SubToken:
            token = self._current_token
            self._current_token = self._advance_token()
            rhs = self._create_expression()

            if token is AddToken:
                return AddNode(lhs, rhs)

            return SubNode(lhs, rhs)

        elif self._current_token is None or self._current_token is CPToken:
            return lhs

        raise SyntaxError(
            f"Expected AddToken or SubToken here but got {self._current_token}"
        )

    def _create_term(self):
        if self._current_token is None:
            return None

        lhs = self._create_power_term()

        if self._current_token is MulToken or self._current_token is DivToken:
            token = self._current_token
            self._current_token = self._advance_token()
            rhs = self._create_term()

            if token is MulToken:
                return MulNode(lhs, rhs)

            return DivNode(lhs, rhs)

        return lhs

    def _create_power_term(self):
        if self._current_token is None:
            return None

        lhs = self._create_factor()

        if self._current_token is PowToken:
            token = self._current_token
            self._current_token = self._advance_token()
            rhs = self._create_power_term()

            return PowNode(lhs, rhs)

        return lhs

    def _create_factor(self):
        if self._current_token is None:
            return None

        if self._current_token is OPToken:
            self._current_token = self._advance_token()
            result = self._create_expression()

            if self._current_token is not CPToken:
                raise SyntaxError(f"Expected ')', but got {self._current_token}")

            self._current_token = self._advance_token()
            return result

        elif self._current_token is AddToken or self._current_token is SubToken:
            token = self._current_token
            self._current_token = self._advance_token()

            factor = self._create_factor()

            if token is SubToken:
                return MinusNode(factor)
            return factor

        elif isinstance(self._current_token, DecimalToken):
            token = self._current_token
            self._current_token = self._advance_token()
            return DecimalNode(token.value)

        elif isinstance(self._current_token, IntegerToken):
            token = self._current_token
            self._current_token = self._advance_token()
            return IntegerNode(token.value)

        else:
            raise SyntaxError(
                f"Got unexpected token {self._current_token} to Parse._create_factor"
            )


if __name__ == "__main__":
    from tokenizer import Tokenizer

    print(Parser(Tokenizer(input("math > ")).generate_tokens()).parse())
