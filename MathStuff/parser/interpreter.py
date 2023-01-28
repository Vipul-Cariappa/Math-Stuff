from dataclasses import dataclass
from parse import *
from math import sin, cos, tan, exp
from typing import Any


@dataclass
class Integer:
    value: int

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"Integer: {str(self.value)}"


@dataclass
class Decimal:
    value: float

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"Decimal: {str(self.value)}"


@dataclass
class Boolean:
    value: bool

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"Boolean: {str(self.value)}"


@dataclass
class PlaceHolder:
    value: Any

    def __str__(self):
        return str(self.value)

    def __repr__(self) -> str:
        return f"PlaceHolder: {self.value}"


class Interpreter:
    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name)
        return method(node)

    def visit_IntegerNode(self, node: IntegerNode):
        return Integer(node.value)

    def visit_DecimalNode(self, node: DecimalNode):
        return Decimal(node.value)

    def visit_VariableNode(self, node: VariableNode):
        return PlaceHolder(node)

    def visit_FunctionNode(self, node: FunctionNode):
        value = self.visit(node.value)
        if node.func == "sin":
            return Decimal(sin(value.value))
        if node.func == "cos":
            return Decimal(cos(value.value))
        if node.func == "tan":
            return Decimal(tan(value.value))
        if node.func == "exp":
            return Decimal(exp(value.value))
        raise NameError(f"Could not find given function {node.func}")

    def visit_MinusNode(self, node: MinusNode):
        underlying_number = self.visit(node.value)
        if isinstance(underlying_number, Integer):
            return Integer(-underlying_number.value)
        return Decimal(-underlying_number.value)

    def visit_NegNode(self, node: NegNode):
        underlying_number = self.visit(node.value)
        return Boolean(not bool(underlying_number.value))

    def visit_AddNode(self, node: AddNode):
        lhs = self.visit(node.left_node)
        rhs = self.visit(node.right_node)

        if isinstance(lhs, Decimal) or isinstance(rhs, Decimal):
            return Decimal(float(lhs.value) + float(rhs.value))
        return Integer(int(lhs.value) + int(rhs.value))

    def visit_SubNode(self, node: SubNode):
        lhs = self.visit(node.left_node)
        rhs = self.visit(node.right_node)

        if isinstance(lhs, Decimal) or isinstance(rhs, Decimal):
            return Decimal(float(lhs.value) - float(rhs.value))
        return Integer(int(lhs.value) - int(rhs.value))

    def visit_MulNode(self, node: MulNode):
        lhs = self.visit(node.left_node)
        rhs = self.visit(node.right_node)

        if isinstance(lhs, Decimal) or isinstance(rhs, Decimal):
            return Decimal(float(lhs.value) * float(rhs.value))
        return Integer(int(lhs.value) * int(rhs.value))

    def visit_DivNode(self, node: DivNode):
        lhs = self.visit(node.left_node)
        rhs = self.visit(node.right_node)

        if rhs.value == 0:
            raise ZeroDivisionError(f"{lhs} cannot be divided by 0")

        if isinstance(lhs, Decimal) or isinstance(rhs, Decimal):
            return Decimal(float(lhs.value) / float(rhs.value))
        return Integer(int(lhs.value) / int(rhs.value))

    def visit_PowNode(self, node: PowNode):
        lhs = self.visit(node.left_node)
        rhs = self.visit(node.right_node)

        if isinstance(lhs, Decimal) or isinstance(rhs, Decimal):
            return Decimal(float(lhs.value) ** float(rhs.value))
        return Integer(int(lhs.value) ** int(rhs.value))

    def visit_AndNode(self, node: AndNode):
        lhs = self.visit(node.left_node)
        rhs = self.visit(node.right_node)

        return Boolean(bool(lhs.value) and bool(rhs.value))

    def visit_OrNode(self, node: AndNode):
        lhs = self.visit(node.left_node)
        rhs = self.visit(node.right_node)

        return Boolean(bool(lhs.value) or bool(rhs.value))

    def visit_NoneType(self, node: None):
        return node


if __name__ == "__main__":
    from tokenizer import Tokenizer

    print(
        Interpreter().visit(
            Parser(Tokenizer(input("math > ")).generate_tokens()).parse()
        )
    )
