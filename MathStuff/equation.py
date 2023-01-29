from typing import Self, Any, Sequence, Union, TypeVar
from equation_nodes import *


class MathError(Exception):
    pass


class PartEquation:
    def __init__(self, node: EquationNodesType | str):
        if isinstance(node, str):
            self.eq: EquationNodesType = VariableNode(node)
        else:
            self.eq: EquationNodesType = node

    def substitute(self, values: Sequence[tuple[Self, int | float | Self]]):
        for variable, value in values:
            if type(self) is type(value):
                self.eq.substitute(variable.eq, value.eq)
            else:
                self.eq.substitute(variable.eq, value)

        return self

    def simplify(self):
        pass

    def graph(self):
        pass

    def __str__(self) -> str:
        return str(self.eq)

    def __add__(self, other: Self | int | float) -> Self:
        if type(self) is type(other):
            return PartEquation(AddNode(self.eq, other.eq))

        return PartEquation(AddNode(self.eq, other))

    def __radd__(self, other: int | float) -> Self:
        return PartEquation(AddNode(other, self.eq))

    def __sub__(self, other: Self | int | float) -> Self:
        if type(self) is type(other):
            return PartEquation(SubNode(self.eq, other.eq))

        return PartEquation(SubNode(self.eq, other))

    def __rsub__(self, other: int | float) -> Self:
        return PartEquation(SubNode(other, self.eq))

    def __mul__(self, other: int | float) -> Self:
        if type(self) is type(other):
            return PartEquation(MulNode(self.eq, other.eq))

        return PartEquation(MulNode(self.eq, other))

    def __rmul__(self, other: int | float) -> Self:
        return PartEquation(MulNode(other, self.eq))

    def __div__(self, other: Self | int | float) -> Self:
        if type(self) is type(other):
            return PartEquation(DivNode(self.eq, other.eq))

        return PartEquation(DivNode(self.eq, other))

    def __rdiv__(self, other: int | float) -> Self:
        return PartEquation(DivNode(other, self.eq))

    def __pow__(self, other: Self | int | float) -> Self:
        if type(self) is type(other):
            return PartEquation(PowNode(self.eq, other.eq))

        return PartEquation(PowNode(self.eq, other))

    def __neg__(self) -> Self:
        return PartEquation(MinusNode(self.eq))


class Equation:
    def __init__(
        self, lhs: PartEquation | int | float, rhs: PartEquation | int | float
    ):
        self.lhs = lhs
        self.rhs = rhs

        if not isinstance(lhs, PartEquation) and not isinstance(rhs, PartEquation):
            if lhs != rhs:
                raise MathError(
                    "lhs and rhs of a equation can not be unequal constants"
                )

    def solve(self):
        pass

    def simplify(self):
        pass

    def graph(self):
        pass


if __name__ == "__main__":
    # initializing some variables to easy manual testing
    x = PartEquation("x")
    y = PartEquation("y")
    z = PartEquation("z")

    str((x + y + z * x - y + z).substitute([(x, 1)]))
