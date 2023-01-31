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

    def _simplify_step_1(self):
        if isinstance(self.lhs, BinaryNode):
            self.lhs._simplify_step_1()

        if isinstance(self.rhs, BinaryNode):
            self.rhs._simplify_step_1()

        if isinstance(self.lhs, MinusNode) and isinstance(self.lhs.value, BinaryNode):
            self.lhs.value._simplify_step_1()

        if isinstance(self.rhs, MinusNode) and isinstance(self.rhs.value, BinaryNode):
            self.rhs.value._simplify_step_1()

        if isinstance(self.rhs, VariableNode):
            self.lhs, self.rhs = self.rhs, self.lhs
        elif isinstance(self.lhs, int) or isinstance(self.lhs, float):
            self.lhs, self.rhs = self.rhs, self.lhs

        return self


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

    def simplify(self):
        if isinstance(self.lhs, AddNode):
            if not isinstance(self.rhs, EquationNodesType):
                if not isinstance(self.lhs.rhs, EquationNodesType):
                    return AddNode(self.lhs.lhs, self.lhs.rhs + self.rhs).simplify()

        if isinstance(self.lhs, VariableNode):
            if isinstance(self.rhs, AddNode):
                if self.lhs is self.rhs.lhs:
                    return AddNode(MulNode(self.lhs, 2), self.rhs.rhs).simplify()

        if not (
            isinstance(self.lhs, EquationNodesType)
            or isinstance(self.rhs, EquationNodesType)
        ):
            return self.lhs + self.rhs

        if isinstance(self.lhs, VariableNode) and self.lhs is self.rhs:
            return MulNode(self.lhs, 2)

        if isinstance(self.lhs, EquationNodesType) and not isinstance(
            self.lhs, VariableNode
        ):
            lhs = self.lhs.simplify()
        else:
            lhs = self.lhs

        if isinstance(self.rhs, EquationNodesType) and not isinstance(
            self.rhs, VariableNode
        ):
            rhs = self.rhs.simplify()
        else:
            rhs = self.rhs

        return AddNode(lhs, rhs)

    def __str__(self) -> str:
        return f"({self.lhs} + {self.rhs})"


@dataclass(repr=True)
class SubNode(BinaryNode):
    lhs: EquationNodesType | int | float
    rhs: EquationNodesType | int | float

    def apply_operation(self, lhs, rhs):
        return lhs - rhs

    def simplify(self):
        return AddNode(self.lhs, MinusNode(self.rhs).simplify()).simplify()

    def __str__(self):
        return f"({self.lhs} - {self.rhs})"


@dataclass(repr=True)
class MulNode(BinaryNode):
    lhs: EquationNodesType | int | float
    rhs: EquationNodesType | int | float

    def apply_operation(self, lhs, rhs):
        return lhs * rhs

    def simplify(self):
        if isinstance(self.lhs, MulNode):
            if not isinstance(self.rhs, EquationNodesType):
                if not isinstance(self.lhs.rhs, EquationNodesType):
                    return MulNode(self.lhs.lhs, self.lhs.rhs + self.rhs).simplify()

        if isinstance(self.lhs, VariableNode):
            if isinstance(self.rhs, MulNode):
                if self.lhs is self.rhs.lhs:
                    return MulNode(PowNode(self.lhs, 2), self.rhs.rhs).simplify()

        if not (
            isinstance(self.lhs, EquationNodesType)
            or isinstance(self.rhs, EquationNodesType)
        ):
            return self.lhs + self.rhs

        if isinstance(self.lhs, VariableNode) and self.lhs is self.rhs:
            return MulNode(self.lhs, 2)

        if isinstance(self.lhs, EquationNodesType) and not isinstance(
            self.lhs, VariableNode
        ):
            lhs = self.lhs.simplify()
        else:
            lhs = self.lhs

        if isinstance(self.rhs, EquationNodesType) and not isinstance(
            self.rhs, VariableNode
        ):
            rhs = self.rhs.simplify()
        else:
            rhs = self.rhs

        return MulNode(lhs, rhs)

    def __str__(self):
        return f"({self.lhs} * {self.rhs})"


@dataclass(repr=True)
class DivNode(BinaryNode):
    lhs: EquationNodesType | int | float
    rhs: EquationNodesType | int | float

    def apply_operation(self, lhs, rhs):
        return lhs / rhs

    def simplify(self):
        # TODO
        return self

    def __str__(self):
        return f"({self.lhs} / {self.rhs})"


@dataclass(repr=True)
class PowNode(BinaryNode):
    lhs: EquationNodesType | int | float
    rhs: EquationNodesType | int | float

    def apply_operation(self, lhs, rhs):
        return lhs**rhs

    def __str__(self):
        return f"({self.lhs} ^ {self.rhs})"


@dataclass(repr=True)
class MinusNode(UnaryNode):
    value: EquationNodesType | int | float

    def __str__(self):
        return f"(-{self.value})"

    def _simplify_step_1(self):
        if isinstance(self.value, BinaryNode):
            self.value._simplify_step_1()

    def simplify(self):
        if isinstance(self.value, BinaryNode):
            return MinusNode(self.value.simplify())


EquationNodesType = Union[
    AddNode,
    SubNode,
    MulNode,
    PowNode,
    MinusNode,
    VariableNode,
]
