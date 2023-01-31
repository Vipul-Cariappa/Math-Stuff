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
        if isinstance(self.eq, EquationNodesType):
            self.eq._simplify_step_1()
            simplified = self.eq.simplify()
            if isinstance(simplified, EquationNodesType):
                return PartEquation(simplified)
            return simplified
        return self

    def graph(self):
        pass

    def __str__(self) -> str:
        return str(self.eq)

    def __repr__(self) -> str:
        return repr(self.eq)

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

    def __rpow__(self, other: int | float) -> Self:
        return PartEquation(PowNode(other, self.eq))

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

    def solve(self, to):
        # FIXME: Assuming lhs has x and x appears only once in the equation

        # Step 1: make a list of anti operations to perform
        operations = []
        self.lhs.eq._get_anti_operations_list(to, operations)
        # print(operations)

        solution = self.rhs
        eq = self.lhs.eq

        while operations:
            operation, side = operations.pop()

            if operation is AddNode:
                if side == "left":
                    solution = SubNode(solution, eq.rhs)
                    eq = eq.lhs
                elif side == "right":
                    solution = SubNode(solution, eq.lhs)
                    eq = eq.rhs
            elif operation is SubNode:
                if side == "left":
                    solution = AddNode(solution, eq.rhs)
                    eq = eq.lhs
                elif side == "right":
                    solution = AddNode(solution, eq.lhs)
                    eq = eq.rhs
            elif operation is MulNode:
                if side == "left":
                    solution = DivNode(solution, eq.rhs)
                    eq = eq.lhs
                elif side == "right":
                    solution = DivNode(solution, eq.lhs)
                    eq = eq.rhs
            elif operation is DivNode:
                if side == "left":
                    solution = MulNode(solution, eq.rhs)
                    eq = eq.lhs
                elif side == "right":
                    solution = MulNode(solution, eq.lhs)
                    eq = eq.rhs
            elif operation is PowNode:
                if side == "left":
                    solution = PowNode(solution, (1 / eq.rhs))
                    eq = eq.lhs
                elif side == "right":
                    solution = LogNode(solution, eq.lhs)
                    eq = eq.rhs
            elif operation is MinusNode:
                solution = MinusNode(solution)
                eq = eq.value
            elif operation is VariableNode:
                break
            else:
                raise Exception("Broken")

        if isinstance(solution, int | float | complex):
            return solution

        return solution.simplify()

    def simplify(self):
        pass

    def graph(self):
        pass

    def __str__(self):
        return f"{self.lhs} = {self.rhs}"

    def __repr__(self):
        return f"{repr(self.lhs)} = {repr(self.rhs)}"


if __name__ == "__main__":
    # initializing some variables to easy manual testing
    x = PartEquation("x")
    y = PartEquation("y")
    z = PartEquation("z")

    eq = Equation(x * 4 + 120, 0)
    print(eq)
    print(eq.solve(x))
