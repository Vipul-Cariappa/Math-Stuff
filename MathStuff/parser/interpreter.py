from dataclasses import dataclass
from parse import *


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


class Interpreter:
    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name)
        return method(node)

    def visit_IntegerNode(self, node: IntegerNode):
        return Integer(node.value)

    def visit_DecimalNode(self, node: DecimalNode):
        return Decimal(node.value)

    def visit_MinusNode(self, node: MinusNode):
        underlying_number = self.visit(node.value)
        if isinstance(underlying_number, Integer):
            return Integer(-underlying_number.value)
        return Decimal(-underlying_number.value)

    def visit_AddNode(self, node: AddNode):
        lhs = self.visit(node.left_node)
        rhs = self.visit(node.right_node)

        if isinstance(lhs, Decimal) or isinstance(rhs, Decimal):
            return Decimal(lhs.value + rhs.value)
        return Integer(lhs.value + rhs.value)

    def visit_SubNode(self, node: SubNode):
        lhs = self.visit(node.left_node)
        rhs = self.visit(node.right_node)

        if isinstance(lhs, Decimal) or isinstance(rhs, Decimal):
            return Decimal(lhs.value - rhs.value)
        return Integer(lhs.value - rhs.value)

    def visit_MulNode(self, node: MulNode):
        lhs = self.visit(node.left_node)
        rhs = self.visit(node.right_node)

        if isinstance(lhs, Decimal) or isinstance(rhs, Decimal):
            return Decimal(lhs.value * rhs.value)
        return Integer(lhs.value * rhs.value)

    def visit_DivNode(self, node: DivNode):
        lhs = self.visit(node.left_node)
        rhs = self.visit(node.right_node)

        if rhs.value == 0:
            raise ZeroDivisionError(f"{lhs} cannot be divided by 0")

        if isinstance(lhs, Decimal) or isinstance(rhs, Decimal):
            return Decimal(lhs.value / rhs.value)
        return Integer(lhs.value / rhs.value)

    def visit_PowNode(self, node: PowNode):
        lhs = self.visit(node.left_node)
        rhs = self.visit(node.right_node)

        if isinstance(lhs, Decimal) or isinstance(rhs, Decimal):
            # return Decimal(lhs.value + rhs.value)
            raise TypeError("Exponentiation with floating point not possible")
        return Integer(lhs.value**rhs.value)

    def visit_NoneType(self, node):
        return None


if __name__ == "__main__":
    from tokenizer import Tokenizer

    print(
        Interpreter().visit(
            Parser(Tokenizer(input("math > ")).generate_tokens()).parse()
        )
    )
