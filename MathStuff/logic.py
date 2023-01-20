import math


class _ADD:
    def __str__(self):
        return "+"


class _MUL:
    def __str__(self):
        return "*"


class _XOR:
    def __str__(self):
        return "^"


class _NEG:
    def __str__(self):
        return "~"


class _COND:
    def __str__(self):
        return "->"


class _BICOND:
    def __str__(self):
        return "<->"


class _OB:
    def __str__(self):
        return "("


class _CB:
    def __str__(self):
        return ")"


ADD = _ADD()
MUL = _MUL()
XOR = _XOR()
NEG = _NEG()
COND = _COND()
BICOND = _BICOND()
OB = _OB()
CB = _CB()


class Variable:
    def __init__(self, name):
        self.name = name
        self.table = None

    def generate_table_md(self):
        self.table = dict()
        self.table[str(self)] = [0, 1]
        return f"| {str(self)} |\n| - |\n| 0 |\n| 1 |"

    def __add__(self, other):
        # self + other
        eq = Equation()

        if isinstance(other, int):
            eq.eq.append(self)
            eq.eq.append(ADD)
            eq.eq.append(1 if other else 0)

            eq.string.extend(eq.eq)
            return eq

        if isinstance(other, Variable):
            eq.eq.append(self)
            eq.eq.append(ADD)
            eq.eq.append(other)

            eq.string.extend(eq.eq)
            return eq

        if isinstance(other, Equation):
            eq.eq.append(self)
            eq.eq.append(ADD)
            eq.eq.append(OB)
            eq.eq.extend(other.eq)
            eq.eq.append(CB)

            eq.sub_eqs.extend(other.sub_eqs)
            eq.sub_eqs.append(other)

            eq.string.extend([self, ADD, OB, *(other.string), CB])
            return eq

        raise TypeError("...")

    def __radd__(self, other):
        # other + self
        eq = Equation()

        if isinstance(other, int):
            eq.eq.append(1 if other else 0)
            eq.eq.append(ADD)
            eq.eq.append(self)

            eq.string.extend(eq.eq)
            return eq

        if isinstance(other, Variable):
            eq.eq.append(other)
            eq.eq.append(ADD)
            eq.eq.append(self)

            eq.string.extend(eq.eq)
            return eq

        if isinstance(other, Equation):
            eq.eq.append(OB)
            eq.eq.extend(other.eq)
            eq.eq.append(CB)
            eq.eq.append(ADD)
            eq.eq.append(self)

            eq.sub_eqs.extend(other.sub_eqs)
            eq.sub_eqs.append(other)

            eq.string.extend([OB, *(other.string), CB, ADD, self])
            return eq

        raise TypeError("...")

    def __mul__(self, other):
        # self * other
        eq = Equation()

        if isinstance(other, int):
            eq.eq.append(self)
            eq.eq.append(MUL)
            eq.eq.append(1 if other else 0)

            eq.string.extend(eq.eq)
            return eq

        if isinstance(other, Variable):
            eq.eq.append(self)
            eq.eq.append(MUL)
            eq.eq.append(other)

            eq.string.extend(eq.eq)
            return eq

        if isinstance(other, Equation):
            eq.eq.append(self)
            eq.eq.append(MUL)
            eq.eq.append(OB)
            eq.eq.extend(other.eq)
            eq.eq.append(CB)

            eq.sub_eqs.extend(other.sub_eqs)
            eq.sub_eqs.append(other)

            eq.string.extend([self, MUL, OB, *(other.string), CB])
            return eq

        raise TypeError("...")

    def __rmul__(self, other):
        # other * self
        eq = Equation()

        if isinstance(other, int):
            eq.eq.append(1 if other else 0)
            eq.eq.append(MUL)
            eq.eq.append(self)

            eq.string.extend(eq.eq)
            return eq

        if isinstance(other, Variable):
            eq.eq.append(other)
            eq.eq.append(MUL)
            eq.eq.append(self)

            eq.string.extend(eq.eq)
            return eq

        if isinstance(other, Equation):
            eq.eq.append(OB)
            eq.eq.extend(other.eq)
            eq.eq.append(CB)
            eq.eq.append(ADD)
            eq.eq.append(self)

            eq.sub_eqs.extend(other.sub_eqs)
            eq.sub_eqs.append(other)

            eq.string.extend([OB, *(other.string), CB, MUL, self])
            return eq

        raise TypeError("...")

    def __xor__(self, other):
        # self * other
        eq = Equation()

        if isinstance(other, int):
            eq.eq.append(self)
            eq.eq.append(XOR)
            eq.eq.append(1 if other else 0)

            eq.string.extend(eq.eq)
            return eq

        if isinstance(other, Variable):
            eq.eq.append(self)
            eq.eq.append(XOR)
            eq.eq.append(other)

            eq.string.extend(eq.eq)
            return eq

        if isinstance(other, Equation):
            eq.eq.append(self)
            eq.eq.append(XOR)
            eq.eq.append(OB)
            eq.eq.extend(other.eq)
            eq.eq.append(CB)

            eq.sub_eqs.extend(other.sub_eqs)
            eq.sub_eqs.append(other)

            eq.string.extend([self, XOR, OB, *(other.string), CB])
            return eq

        raise TypeError("...")

    def __rxor__(self, other):
        # other * self
        eq = Equation()

        if isinstance(other, int):
            eq.eq.append(1 if other else 0)
            eq.eq.append(XOR)
            eq.eq.append(self)

            eq.string.extend(eq.eq)
            return eq

        if isinstance(other, Variable):
            eq.eq.append(other)
            eq.eq.append(MUL)
            eq.eq.append(self)

            eq.string.extend(eq.eq)
            return eq

        if isinstance(other, Equation):
            eq.eq.append(OB)
            eq.eq.extend(other.eq)
            eq.eq.append(CB)
            eq.eq.append(ADD)
            eq.eq.append(self)

            eq.sub_eqs.extend(other.sub_eqs)
            eq.sub_eqs.append(other)

            eq.string.extend([OB, *(other.string), CB, XOR, self])
            return eq

        raise TypeError("...")

    def __invert__(self):
        # ~self
        eq = Equation()
        eq.eq.append(NEG)
        eq.eq.append(self)

        eq.string.extend(eq.eq)
        return eq

    def __mod__(self, other):
        # self % other (self <-> other)
        # (self -> other) * (other -> self)
        # (~self + other) * (~other + self)
        eq = (~self + other) * (~other + self)

        if isinstance(other, Equation):
            eq.string = [self, BICOND, OB, *(other.string), CB]
        else:
            eq.string = [self, BICOND, other]

        return eq

    def __rmod__(self, other):
        # other % self (other <-> self)
        # (other -> self) * (self -> other)
        # (~other + self) * (~self + other)
        eq = (~other + self) * (~self + other)

        if isinstance(other, Equation):
            eq.string = [OB, *(other.string), CB, BICOND, self]
        else:
            eq.string = [other, BICOND, self]

        return eq

    def __truediv__(self, other):
        # self % other (self -> other)
        # ~self + other
        eq = ~self + other

        if isinstance(other, Equation):
            eq.string = [self, COND, OB, *(other.string), CB]
        else:
            eq.string = [self, COND, other]

        return eq

    def __rtruediv__(self, other):
        # other / self (other -> self)
        # ~other + self
        eq = ~other + self

        if isinstance(other, Equation):
            eq.string = [OB, *(other.string), CB, COND, self]
        else:
            eq.string = [other, COND, self]

        return eq

    def __str__(self):
        return self.name


class Equation:
    def __init__(self):
        self.eq = []
        self.sub_eqs = []
        self.table = None
        self.string = []

    def solve(self, *args):
        pass

    def generate_truth_table(self):
        """
        eq: x + y
        table = {
            "x": [0, 0, 1, 1],
            "y": [0, 1, 0, 1],
            "x + y": [0, 1, 1, 1],
        }
        """

        if self.table is not None:
            # the equation is already solved
            return self.table

        # solve all the sub equations
        # Note: solved sub equations is not used or solving sub equations is not necessary to solve given equation
        for i in self.sub_eqs:
            i.generate_truth_table()

        variable_count = 0
        variables = []
        sub_eq_strings = []
        table = dict()

        eq_string = str(self)

        for i in self.eq:
            if isinstance(i, Variable) and i not in variables:
                variables.append(i)
                table[str(i)] = []
                variable_count += 1

        combinations = 2**variable_count
        table[eq_string] = [0] * combinations  # to store result

        for i in self.sub_eqs:
            sub_eq_str = str(i)
            table[sub_eq_str] = [0] * combinations
            sub_eq_strings.append(sub_eq_str)

        for i in range(combinations):
            results_list = table[eq_string]
            eval_string = repr(self)

            for j in range(variable_count):
                table[str(variables[j])].append(1 if i & (1 << j) else 0)

                eval_string = eval_string.replace(
                    str(variables[j]), "1" if i & (1 << j) else "0"
                )

            results_list[i] = (
                1
                if eval(
                    eval_string := eval_string.replace("+", "or")
                    .replace("*", "and")
                    .replace("~", "not")
                    .replace("^", "!=")
                )
                else 0
            )

        for eq in self.sub_eqs:
            eq_string = repr(eq)

            for i in range(combinations):
                eval_string = eq_string
                results_list = table[str(eq)]

                for j in range(variable_count):
                    eval_string = eval_string.replace(
                        str(variables[j]), "1" if i & (1 << j) else "0"
                    )

                results_list[i] = (
                    1
                    if eval(
                        eval_string := eval_string.replace("+", "or")
                        .replace("*", "and")
                        .replace("~", "not")
                        .replace("^", "!=")
                    )
                    else 0
                )

        self.table = table

        return table

    def display_table(self):
        if self.table is None:
            self.generate_truth_table()

        table_length = len(self.table[str(self)])
        header_string_length = [len(i) for i in self.table.keys()]

        print("|", end="")
        for i in self.table.keys():
            print(f" {i} |", end="")
        print("\n")

        for i in range(table_length):
            print("|", end="")
            for index, j in enumerate(self.table.keys()):
                print(
                    " " * math.floor((header_string_length[index] - 1) / 2)
                    + f" {self.table[j][i]}"
                    + " " * math.ceil((header_string_length[index] - 1) / 2)
                    + " |",
                    end="",
                )
            print("\n")
        print("\n")

    def generate_table_md(self):
        if self.table is None:
            self.generate_truth_table()

        table_md = ""

        table_length = len(self.table[str(self)])
        header_string_length = [len(i) for i in self.table.keys()]

        table_md += "|"
        for i in self.table.keys():
            table_md += f" {i} |"
        table_md += "\n"

        table_md += "|"
        for _ in self.table.keys():
            table_md += f" - |"
        table_md += "\n"

        for i in range(table_length):
            table_md += "|"
            for index, j in enumerate(self.table.keys()):
                table_md += (
                    " " * math.floor((header_string_length[index] - 1) / 2)
                    + f" {self.table[j][i]}"
                    + " " * math.ceil((header_string_length[index] - 1) / 2)
                    + " |"
                )
            table_md += "\n"
        table_md += "\n"

        return table_md

    def __add__(self, other):
        # self + other
        eq = Equation()

        if isinstance(other, int):
            eq.eq.append(OB)
            eq.eq.extend(self.eq)
            eq.eq.append(CB)
            eq.eq.append(ADD)
            eq.eq.append(1 if other else 0)

            eq.string.extend([OB, *(self.string), CB, ADD, other])
            return eq

        if isinstance(other, Variable):
            eq.eq.append(OB)
            eq.eq.extend(self.eq)
            eq.eq.append(CB)
            eq.eq.append(ADD)
            eq.eq.append(other)

            eq.string.extend([OB, *(self.string), CB, ADD, other])
            return eq

        if isinstance(other, Equation):
            # adding existing operations
            eq.eq.append(OB)
            eq.eq.extend(self.eq)
            eq.eq.append(CB)

            # add operator
            eq.eq.append(ADD)

            # adding other's operations
            eq.eq.append(OB)
            eq.eq.extend(other.eq)
            eq.eq.append(CB)

            # adding sub equations
            eq.sub_eqs.append(self)
            eq.sub_eqs.extend(self.sub_eqs)
            eq.sub_eqs.append(other)
            eq.sub_eqs.extend(other.sub_eqs)

            eq.string.extend([OB, *(self.string), CB, ADD, OB, *(other.string), CB])
            return eq

        raise TypeError("...")

    def __radd__(self, other):
        # other + self
        eq = Equation()

        if isinstance(other, int):
            eq.eq.append(1 if other else 0)
            eq.eq.append(ADD)
            eq.eq.append(OB)
            eq.eq.extend(self.eq)
            eq.eq.append(CB)

            eq.string.extend([other, ADD, OB, *(self.string), CB])
            return eq

        if isinstance(other, Variable):
            eq.eq.append(other)
            eq.eq.append(ADD)
            eq.eq.append(OB)
            eq.eq.extend(self.eq)
            eq.eq.append(CB)

            eq.string.extend([other, ADD, OB, *(self.string), CB])
            return eq

        if isinstance(other, Equation):
            # adding other's operations
            eq.eq.append(OB)
            eq.eq.extend(other.eq)
            eq.eq.append(CB)

            # add operator
            eq.eq.append(ADD)

            # adding existing operations
            eq.eq.append(OB)
            eq.eq.extend(self.eq)
            eq.eq.append(CB)

            # adding sub equations
            eq.sub_eqs.append(self)
            eq.sub_eqs.extend(self.sub_eqs)
            eq.sub_eqs.append(other)
            eq.sub_eqs.extend(other.sub_eqs)

            eq.string.extend([OB, *(other.string), CB, ADD, OB, *(self.string), CB])
            return eq

        raise TypeError("...")

    def __mul__(self, other):
        # self * other
        eq = Equation()

        if isinstance(other, int):
            eq.eq.append(OB)
            eq.eq.extend(self.eq)
            eq.eq.append(CB)
            eq.eq.append(MUL)
            eq.eq.append(1 if other else 0)

            eq.string.extend([OB, *(self.string), CB, MUL, other])
            return eq

        if isinstance(other, Variable):
            eq.eq.append(OB)
            eq.eq.extend(self.eq)
            eq.eq.append(CB)
            eq.eq.append(MUL)
            eq.eq.append(other)

            eq.string.extend([OB, *(self.string), CB, MUL, other])
            return eq

        if isinstance(other, Equation):
            # adding existing operations
            eq.eq.append(OB)
            eq.eq.extend(self.eq)
            eq.eq.append(CB)

            # add operator
            eq.eq.append(MUL)

            # adding other's operations
            eq.eq.append(OB)
            eq.eq.extend(other.eq)
            eq.eq.append(CB)

            # adding sub equations
            eq.sub_eqs.append(self)
            eq.sub_eqs.extend(self.sub_eqs)
            eq.sub_eqs.append(other)
            eq.sub_eqs.extend(other.sub_eqs)

            eq.string.extend([OB, *(self.string), CB, MUL, OB, *(other.string), CB])
            return eq

        raise TypeError("...")

    def __rmul__(self, other):
        # other * self
        eq = Equation()

        if isinstance(other, int):
            eq.eq.append(1 if other else 0)
            eq.eq.append(MUL)
            eq.eq.append(OB)
            eq.eq.extend(self.eq)
            eq.eq.append(CB)

            eq.string.extend([other, MUL, OB, *(self.string), CB])
            return eq

        if isinstance(other, Variable):
            eq.eq.append(other)
            eq.eq.append(MUL)
            eq.eq.append(OB)
            eq.eq.extend(self.eq)
            eq.eq.append(CB)

            eq.string.extend([other, MUL, OB, *(self.string), CB])
            return eq

        if isinstance(other, Equation):
            # adding other's operations
            eq.eq.append(OB)
            eq.eq.extend(other.eq)
            eq.eq.append(CB)

            # add operator
            eq.eq.append(MUL)

            # adding existing operations
            eq.eq.append(OB)
            eq.eq.extend(self.eq)
            eq.eq.append(CB)

            # adding sub equations
            eq.sub_eqs.append(self)
            eq.sub_eqs.extend(self.sub_eqs)
            eq.sub_eqs.append(other)
            eq.sub_eqs.extend(other.sub_eqs)

            eq.string.extend([OB, *(other.string), CB, MUL, OB, *(self.string), CB])
            return eq

        raise TypeError("...")

    def __xor__(self, other):
        # self + other
        eq = Equation()

        if isinstance(other, int):
            eq.eq.append(OB)
            eq.eq.extend(self.eq)
            eq.eq.append(CB)
            eq.eq.append(XOR)
            eq.eq.append(1 if other else 0)

            eq.string.extend([OB, *(self.string), CB, XOR, other])
            return eq

        if isinstance(other, Variable):
            eq.eq.append(OB)
            eq.eq.extend(self.eq)
            eq.eq.append(CB)
            eq.eq.append(XOR)
            eq.eq.append(other)

            eq.string.extend([OB, *(self.string), CB, XOR, other])
            return eq

        if isinstance(other, Equation):
            # adding existing operations
            eq.eq.append(OB)
            eq.eq.extend(self.eq)
            eq.eq.append(CB)

            # add operator
            eq.eq.append(XOR)

            # adding other's operations
            eq.eq.append(OB)
            eq.eq.extend(other.eq)
            eq.eq.append(CB)

            # adding sub equations
            eq.sub_eqs.append(self)
            eq.sub_eqs.extend(self.sub_eqs)
            eq.sub_eqs.append(other)
            eq.sub_eqs.extend(other.sub_eqs)

            eq.string.extend([OB, *(self.string), CB, XOR, OB, *(other.string), CB])
            return eq

        raise TypeError("...")

    def __rxor__(self, other):
        # other + self
        eq = Equation()

        if isinstance(other, int):
            eq.eq.append(1 if other else 0)
            eq.eq.append(XOR)
            eq.eq.append(OB)
            eq.eq.extend(self.eq)
            eq.eq.append(CB)

            eq.string.extend([other, XOR, OB, *(self.string), CB])
            return eq

        if isinstance(other, Variable):
            eq.eq.append(other)
            eq.eq.append(XOR)
            eq.eq.append(OB)
            eq.eq.extend(self.eq)
            eq.eq.append(CB)

            eq.string.extend([other, XOR, OB, *(self.string), CB])
            return eq

        if isinstance(other, Equation):
            # adding other's operations
            eq.eq.append(OB)
            eq.eq.extend(other.eq)
            eq.eq.append(CB)

            # add operator
            eq.eq.append(XOR)

            # adding existing operations
            eq.eq.append(OB)
            eq.eq.extend(self.eq)
            eq.eq.append(CB)

            # adding sub equations
            eq.sub_eqs.append(self)
            eq.sub_eqs.extend(self.sub_eqs)
            eq.sub_eqs.append(other)
            eq.sub_eqs.extend(other.sub_eqs)

            eq.string.extend([OB, *(other.string), CB, XOR, OB, *(self.string), CB])
            return eq

        raise TypeError("...")

    def __mod__(self, other):
        # self % other (self <-> other)
        # (self -> other) * (other -> self)
        # (~self + other) * (~other + self)
        eq = (~self + other) * (~other + self)

        if isinstance(other, Equation):
            eq.string = [OB, *(self.string), CB, BICOND, OB, *(other.string), CB]
        else:
            eq.string = [OB, *(self.string), CB, BICOND, other]

        return eq

    def __rmod__(self, other):
        # other % self (other <-> self)
        # (other -> self) * (self -> other)
        # (~other + self) * (~self + other)
        eq = (~other + self) * (~self + other)

        if isinstance(other, Equation):
            eq.string = [OB, *(other.string), CB, BICOND, OB, *(self.string), CB]
        else:
            eq.string = [
                other,
                BICOND,
                OB,
                *(self.eq),
                CB,
            ]

        return eq

    def __truediv__(self, other):
        # self % other (self -> other)
        # ~self + other
        eq = ~self + other

        if isinstance(other, Equation):
            eq.string = [OB, *(self.string), CB, COND, OB, *(other.string), CB]
        else:
            eq.string = [OB, *(self.string), CB, COND, other]

        return eq

    def __rtruediv__(self, other):
        # other / self (other -> self)
        # ~other + self
        eq = ~other + self

        if isinstance(other, Equation):
            eq.string = [OB, *(other.string), CB, COND, OB, *(self.string), CB]
        else:
            eq.string = [
                other,
                COND,
                OB,
                *(self.string),
                CB,
            ]

        return eq

    def __invert__(self):
        # ~self
        eq = Equation()
        eq.eq.append(NEG)
        eq.eq.append(OB)
        eq.eq.extend(self.eq)
        eq.eq.append(CB)

        return eq

    def __eq__(self, other):
        # self == other
        pass

    def __repr__(self) -> str:
        return " ".join((str(i) for i in self.eq))

    def __str__(self):
        return " ".join((str(i) for i in self.string))


a = Variable("a")
b = Variable("b")
c = Variable("c")
d = Variable("d")
e = Variable("e")
p = Variable("p")
q = Variable("q")
r = Variable("r")
s = Variable("s")
u = Variable("u")
v = Variable("v")
w = Variable("w")
x = Variable("x")
y = Variable("y")
z = Variable("z")


def truth_table_generator(expression_string: str):
    try:
        expression = eval(expression_string)
        return expression.generate_table_md(), expression.table
    except:
        return None, None


if __name__ == "__main__":
    (x % y).display_table()
