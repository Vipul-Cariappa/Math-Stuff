from dataclasses import dataclass
from typing import Union, TypeVar


EquationNodesType = Union[
    "AddNode",
    "SubNode",
    "MulNode",
    "PowNode",
    "MinusNode",
    "VariableNode",
]


class UnaryNode:
    def substitute(
        self, variable: EquationNodesType, value: EquationNodesType | int | float
    ):
        if isinstance(self.value, VariableNode) and self.value is variable:
            self.value = value
        elif isinstance(self.value, EquationNodesType):
            self.value.substitute(variable, value)


class BinaryNode:
    def substitute(self, variable: str, value: EquationNodesType | int | float):
        if isinstance(self.lhs, VariableNode) and self.lhs is variable:
            self.lhs = value
        elif isinstance(self.lhs, EquationNodesType):
            self.lhs.substitute(variable, value)

        if isinstance(self.rhs, VariableNode) and self.rhs is variable:
            self.rhs = value
        elif isinstance(self.lhs, EquationNodesType):
            self.rhs.substitute(variable, value)


@dataclass(repr=True)
class VariableNode:
    value: str

    def substitute(self, variable, value):
        if self.value == variable:
            self.value = value

    def __str__(self):
        return self.value


@dataclass(repr=True)
class AddNode(BinaryNode):
    lhs: EquationNodesType | int | float
    rhs: EquationNodesType | int | float

    def __str__(self) -> str:
        return f"({self.lhs} + {self.rhs})"


@dataclass(repr=True)
class SubNode(BinaryNode):
    lhs: EquationNodesType | int | float
    rhs: EquationNodesType | int | float

    def __str__(self):
        return f"({self.lhs} - {self.rhs})"


@dataclass(repr=True)
class MulNode(BinaryNode):
    lhs: EquationNodesType | int | float
    rhs: EquationNodesType | int | float

    def __str__(self):
        return f"({self.lhs} * {self.rhs})"


@dataclass(repr=True)
class DivNode(BinaryNode):
    lhs: EquationNodesType | int | float
    rhs: EquationNodesType | int | float

    def __str__(self):
        return f"({self.lhs} / {self.rhs})"


@dataclass(repr=True)
class PowNode(BinaryNode):
    lhs: EquationNodesType | int | float
    rhs: EquationNodesType | int | float

    def __str__(self):
        return f"({self.lhs} ^ {self.rhs})"


@dataclass(repr=True)
class MinusNode(UnaryNode):
    value: EquationNodesType | int | float

    def __str__(self):
        return f"(-{self.value})"


EquationNodesType = Union[
    AddNode,
    SubNode,
    MulNode,
    PowNode,
    MinusNode,
    VariableNode,
]
