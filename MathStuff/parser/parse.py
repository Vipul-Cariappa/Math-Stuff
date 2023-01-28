from dataclasses import dataclass
from tokenizer import *
from typing import Any


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
class VariableNode:
    value: str

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"VariableNode: {self.value}"


@dataclass
class FunctionNode:
    value: Any
    func: str  # TODO: should change to FuncType

    def __str__(self) -> str:
        return f"{self.func}({self.value})"

    def __repr__(self) -> str:
        return f"FunctionNode: {self.func}({self.value})"


@dataclass
class MinusNode:
    value: Any

    def __str__(self):
        return f"(-{str(self.value)})"

    def __repr__(self):
        return f"MinusNode: {str(self)}"


@dataclass
class NegNode:
    value: Any

    def __str__(self):
        return f"(~{str(self.value)})"

    def __repr__(self):
        return f"MinusNode: {str(self)}"


@dataclass
class AddNode:
    left_node: Any
    right_node: Any

    def __str__(self):
        return f"({self.left_node} + {self.right_node})"

    def __repr__(self) -> str:
        return f"AddNode: {str(self)}"


@dataclass
class SubNode:
    left_node: Any
    right_node: Any

    def __str__(self):
        return f"({self.left_node} - {self.right_node})"

    def __repr__(self) -> str:
        return f"SubNode: {str(self)}"


@dataclass
class MulNode:
    left_node: Any
    right_node: Any

    def __str__(self):
        return f"({self.left_node} * {self.right_node})"

    def __repr__(self) -> str:
        return f"MulNode: {str(self)}"


@dataclass
class DivNode:
    left_node: Any
    right_node: Any

    def __str__(self):
        return f"({self.left_node} / {self.right_node})"

    def __repr__(self) -> str:
        return f"DivNode: {str(self)}"


@dataclass
class PowNode:
    left_node: Any
    right_node: Any

    def __str__(self):
        return f"({self.left_node} ^ {self.right_node})"

    def __repr__(self) -> str:
        return f"PowNode: {str(self)}"


@dataclass
class AndNode:
    left_node: Any
    right_node: Any

    def __str__(self):
        return f"({self.left_node} & {self.right_node})"

    def __repr__(self) -> str:
        return f"AndNode: {str(self)}"


@dataclass
class OrNode:
    left_node: Any
    right_node: Any

    def __str__(self):
        return f"({self.left_node} | {self.right_node})"

    def __repr__(self) -> str:
        return f"OrNode: {str(self)}"


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

        lhs = self._create_logic()

        if self._current_token is MulToken or self._current_token is DivToken:
            token = self._current_token
            self._current_token = self._advance_token()
            rhs = self._create_term()

            if token is MulToken:
                return MulNode(lhs, rhs)

            return DivNode(lhs, rhs)

        return lhs

    def _create_logic(self):
        if self._current_token is None:
            return None

        lhs = self._create_power_term()

        if self._current_token is AndToken or self._current_token is OrToken:
            token = self._current_token
            self._current_token = self._advance_token()
            rhs = self._create_logic()

            if token is AndToken:
                return AndNode(lhs, rhs)

            return OrNode(lhs, rhs)

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

        elif (
            self._current_token is AddToken
            or self._current_token is SubToken
            or self._current_token is NegToken
        ):
            token = self._current_token
            self._current_token = self._advance_token()

            factor = self._create_factor()

            if token is SubToken:
                return MinusNode(factor)
            if token is NegToken:
                return NegNode(factor)
            return factor

        elif isinstance(self._current_token, DecimalToken):
            token = self._current_token
            self._current_token = self._advance_token()
            return DecimalNode(token.value)

        elif isinstance(self._current_token, IntegerToken):
            token = self._current_token
            self._current_token = self._advance_token()
            return IntegerNode(token.value)

        elif isinstance(self._current_token, CharToken):
            token = self._current_token
            self._current_token = self._advance_token()
            return VariableNode(token.value)

        elif isinstance(self._current_token, StringToken):
            func = self._current_token
            self._current_token = self._advance_token()

            if self._current_token is OPToken:
                self._current_token = self._advance_token()
            else:
                raise SyntaxError(f"Expected '(' after function name {func.value}")

            value = self._create_expression()

            if self._current_token is not CPToken:
                raise SyntaxError(f"Expected ')', but got {self._current_token}")

            self._current_token = self._advance_token()

            return FunctionNode(value, func.value)

        else:
            raise SyntaxError(
                f"Got unexpected token {self._current_token} to Parse._create_factor"
            )


if __name__ == "__main__":
    from tokenizer import Tokenizer

    print(Parser(Tokenizer(input("math > ")).generate_tokens()).parse())
