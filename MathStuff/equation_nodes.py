from dataclasses import dataclass
from typing import Union, TypeVar
import math


EquationNodesType = Union[
    "AddNode",
    "SubNode",
    "MulNode",
    "PowNode",
    "LogNode",
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

    def _get_anti_operations_list(self, search, stack):
        if self.lhs is search:
            stack.append((self.__class__, "left"))
            stack.append(self.lhs)
            return True

        if self.rhs is search:
            stack.append((self.__class__, "right"))
            stack.append(self.rhs)
            return True

        if isinstance(
            self.lhs, EquationNodesType
        ) and self.lhs._get_anti_operations_list(search, stack):
            stack.append((self.__class__, "left"))
            return True

        if isinstance(
            self.rhs, EquationNodesType
        ) and self.rhs._get_anti_operations_list(search, stack):
            stack.append((self.__class__, "right"))
            return True

        return False


@dataclass(repr=True)
class VariableNode:
    value: str

    def substitute(self, variable, value):
        if self.value == variable:
            self.value = value

    def _get_anti_operations_list(self, search, stack):
        if search.eq.value == self.value:
            stack.append((self.__class__, "me"))
            return True
        return False

    def __str__(self):
        return self.value


@dataclass(repr=True)
class AddNode(BinaryNode):
    lhs: EquationNodesType | int | float
    rhs: EquationNodesType | int | float

    def simplify(self):
        if isinstance(self.lhs, EquationNodesType) and not isinstance(
            self.lhs, VariableNode
        ):
            self.lhs = self.lhs.simplify()
        else:
            self.lhs = self.lhs

        if isinstance(self.rhs, EquationNodesType) and not isinstance(
            self.rhs, VariableNode
        ):
            self.rhs = self.rhs.simplify()
        else:
            self.rhs = self.rhs

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

        return self

    def __str__(self) -> str:
        return f"({self.lhs} + {self.rhs})"


@dataclass(repr=True)
class SubNode(BinaryNode):
    lhs: EquationNodesType | int | float
    rhs: EquationNodesType | int | float

    def simplify(self):
        return AddNode(self.lhs, MinusNode(self.rhs).simplify()).simplify()

    def __str__(self):
        return f"({self.lhs} - {self.rhs})"


@dataclass(repr=True)
class MulNode(BinaryNode):
    lhs: EquationNodesType | int | float
    rhs: EquationNodesType | int | float

    def simplify(self):
        if isinstance(self.lhs, EquationNodesType) and not isinstance(
            self.lhs, VariableNode
        ):
            self.lhs = self.lhs.simplify()
        else:
            self.lhs = self.lhs

        if isinstance(self.rhs, EquationNodesType) and not isinstance(
            self.rhs, VariableNode
        ):
            self.rhs = self.rhs.simplify()
        else:
            self.rhs = self.rhs

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
            return self.lhs * self.rhs

        if isinstance(self.lhs, VariableNode) and self.lhs is self.rhs:
            return MulNode(self.lhs, 2)

        return self

    def __str__(self):
        return f"({self.lhs} * {self.rhs})"


@dataclass(repr=True)
class DivNode(BinaryNode):
    lhs: EquationNodesType | int | float
    rhs: EquationNodesType | int | float

    def simplify(self):
        # TODO
        if isinstance(self.lhs, EquationNodesType) and not isinstance(
            self.lhs, VariableNode
        ):
            self.lhs = self.lhs.simplify()
        else:
            self.lhs = self.lhs

        if isinstance(self.rhs, EquationNodesType) and not isinstance(
            self.rhs, VariableNode
        ):
            self.rhs = self.rhs.simplify()
        else:
            self.rhs = self.rhs

        if not (
            isinstance(self.lhs, EquationNodesType)
            or isinstance(self.rhs, EquationNodesType)
        ):
            return self.lhs / self.rhs

        return self

    def __str__(self):

        return f"({self.lhs} / {self.rhs})"


@dataclass(repr=True)
class PowNode(BinaryNode):
    lhs: EquationNodesType | int | float
    rhs: EquationNodesType | int | float

    def simplify(self):
        # TODO
        if isinstance(self.lhs, EquationNodesType) and not isinstance(
            self.lhs, VariableNode
        ):
            self.lhs = self.lhs.simplify()
        else:
            self.lhs = self.lhs

        if isinstance(self.rhs, EquationNodesType) and not isinstance(
            self.rhs, VariableNode
        ):
            self.rhs = self.rhs.simplify()
        else:
            self.rhs = self.rhs

        if not (
            isinstance(self.lhs, EquationNodesType)
            or isinstance(self.rhs, EquationNodesType)
        ):
            return self.lhs**self.rhs

        return self

    def __str__(self):
        return f"({self.lhs} ^ {self.rhs})"


@dataclass(repr=True)
class LogNode(BinaryNode):
    lhs: EquationNodesType | int | float
    rhs: EquationNodesType | int | float

    def simplify(self):
        # TODO
        if isinstance(self.lhs, EquationNodesType) and not isinstance(
            self.lhs, VariableNode
        ):
            self.lhs = self.lhs.simplify()
        else:
            self.lhs = self.lhs

        if isinstance(self.rhs, EquationNodesType) and not isinstance(
            self.rhs, VariableNode
        ):
            self.rhs = self.rhs.simplify()
        else:
            self.rhs = self.rhs

        if not (
            isinstance(self.lhs, EquationNodesType)
            or isinstance(self.rhs, EquationNodesType)
        ):
            return math.log(self.lhs, self.rhs)

        return self

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

    def _get_anti_operations_list(self, search, stack):
        if self.value is search:
            stack.append(self.__class__)
            stack.append(self.value)
            return True

        if isinstance(
            self.value, EquationNodesType
        ) and self.value._get_anti_operations_list(search, stack):
            stack.append((self.__class__, "down"))
            return True

        return False

    def simplify(self):
        if isinstance(self.value, BinaryNode):
            return MinusNode(self.value.simplify())

        if isinstance(self.value, MinusNode):
            return self.value.simplify()

        if not isinstance(self.value, VariableNode):
            return -(self.value)


EquationNodesType = Union[
    AddNode,
    SubNode,
    MulNode,
    PowNode,
    LogNode,
    MinusNode,
    VariableNode,
]
