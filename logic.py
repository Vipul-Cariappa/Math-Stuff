class _ADD:
    def __str__(self):
        return "+"


class _MUL:
    def __str__(self):
        return "*"


class _NEG:
    def __str__(self):
        return "~"


class _OB:
    def __str__(self):
        return "("


class _CB:
    def __str__(self):
        return ")"


ADD = _ADD()
MUL = _MUL()
NEG = _NEG()
OB = _OB()
CB = _CB()


class Variable:
    def __init__(self, name):
        self.name = name

    def __add__(self, other):
        # self + other
        eq = Equation()

        if isinstance(other, int):
            eq.eq.append(self)
            eq.eq.append(ADD)
            eq.eq.append(1 if other else 0)
            return eq

        if isinstance(other, Variable):
            eq.eq.append(self)
            eq.eq.append(ADD)
            eq.eq.append(other)
            return eq

        if isinstance(other, Equation):
            eq.eq.append(self)
            eq.eq.append(ADD)
            eq.eq.append(OB)
            eq.eq.extend(other.eq)
            eq.eq.append(CB)
            return eq

        raise TypeError("...")

    def __radd__(self, other):
        # other + self
        eq = Equation()

        if isinstance(other, int):
            eq.eq.append(1 if other else 0)
            eq.eq.append(ADD)
            eq.eq.append(self)
            return eq

        if isinstance(other, Variable):
            eq.eq.append(other)
            eq.eq.append(ADD)
            eq.eq.append(self)
            return eq

        if isinstance(other, Equation):
            eq.eq.append(OB)
            eq.eq.extend(other.eq)
            eq.eq.append(CB)
            eq.eq.append(ADD)
            eq.eq.append(self)
            return eq

        raise TypeError("...")

    def __mul__(self, other):
        # self * other
        eq = Equation()

        if isinstance(other, int):
            eq.eq.append(self)
            eq.eq.append(MUL)
            eq.eq.append(1 if other else 0)
            return eq

        if isinstance(other, Variable):
            eq.eq.append(self)
            eq.eq.append(MUL)
            eq.eq.append(other)
            return eq

        if isinstance(other, Equation):
            eq.eq.append(self)
            eq.eq.append(MUL)
            eq.eq.append(OB)
            eq.eq.extend(other.eq)
            eq.eq.append(CB)
            return eq

        raise TypeError("...")

    def __rmul__(self, other):
        # other * self
        eq = Equation()

        if isinstance(other, int):
            eq.eq.append(1 if other else 0)
            eq.eq.append(MUL)
            eq.eq.append(self)
            return eq

        if isinstance(other, Variable):
            eq.eq.append(other)
            eq.eq.append(MUL)
            eq.eq.append(self)
            return eq

        if isinstance(other, Equation):
            eq.eq.append(OB)
            eq.eq.extend(other.eq)
            eq.eq.append(CB)
            eq.eq.append(ADD)
            eq.eq.append(self)
            return eq

        raise TypeError("...")

    def __invert__(self):
        # ~self
        eq = Equation()
        eq.eq.append(NEG)
        eq.eq.append(self)
        return eq

    def __str__(self):
        return self.name


class Equation:
    def __init__(self):
        self.eq = []
        self.table = None

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
        variable_count = 0
        variables = []
        table = dict()

        eq_string = str(self)

        for i in self.eq:
            if isinstance(i, Variable) and i not in variables:
                variables.append(i)
                table[str(i)] = []
                variable_count += 1

        combinations = 2**variable_count
        table[eq_string] = [0] * combinations  # to store result

        for i in range(combinations):
            results_list = table[eq_string]
            eval_string = eq_string

            for j in range(variable_count):
                table[str(variables[j])].append(1 if i & (1 << j) else 0)

                eval_string = eval_string.replace(
                    str(variables[j]), "1" if i & (1 << j) else "0"
                )

            results_list[i] = (
                1
                if eval(
                    eval_string.replace("+", "or")
                    .replace("*", "and")
                    .replace("~", "not")
                )
                else 0
            )

        self.table = table

        return table

    def display_table(self):
        if self.table is None:
            self.generate_truth_table()

        table_length = len(self.table[str(self)])

        for i in self.table.keys():
            print(i, end="\t")
        print("\n")

        for i in range(table_length):
            for j in self.table.keys():
                print(self.table[j][i], end="\t")
            print("\n")
        print("\n")

    def __add__(self, other):
        # self + other
        eq = Equation()

        if isinstance(other, int):
            eq.eq.extend(self.eq)
            eq.eq.append(ADD)
            eq.eq.append(1 if other else 0)
            return eq

        if isinstance(other, Variable):
            eq.eq.extend(self.eq)
            eq.eq.append(ADD)
            eq.eq.append(other)
            return eq

        if isinstance(other, Equation):
            # adding exisiting operations
            eq.eq.append(OB)
            eq.eq.extend(self.eq)
            eq.eq.append(CB)

            # add operator
            eq.eq.append(ADD)

            # adding other's operations
            eq.eq.append(OB)
            eq.eq.extend(other.eq)
            eq.eq.append(CB)
            return eq

        raise TypeError("...")

    def __radd__(self, other):
        # other + self
        eq = Equation()

        if isinstance(other, int):
            eq.eq.append(1 if other else 0)
            eq.eq.append(ADD)
            eq.eq.extend(self.eq)
            return eq

        if isinstance(other, Variable):
            eq.eq.append(other)
            eq.eq.append(ADD)
            eq.eq.extend(self.eq)
            return eq

        if isinstance(other, Equation):
            # adding other's operations
            eq.eq.append(OB)
            eq.eq.extend(other.eq)
            eq.eq.append(CB)

            # add operator
            eq.eq.append(ADD)

            # adding exisiting operations
            eq.eq.append(OB)
            eq.eq.extend(self.eq)
            eq.eq.append(CB)

            return eq

        raise TypeError("...")

    def __mul__(self, other):
        # self * other
        eq = Equation()

        if isinstance(other, int):
            eq.eq.extend(self.eq)
            eq.eq.append(MUL)
            eq.eq.append(1 if other else 0)
            return eq

        if isinstance(other, Variable):
            eq.eq.extend(self.eq)
            eq.eq.append(MUL)
            eq.eq.append(other)
            return eq

        if isinstance(other, Equation):
            # adding exisiting operations
            eq.eq.append(OB)
            eq.eq.extend(self.eq)
            eq.eq.append(CB)

            # add operator
            eq.eq.append(MUL)

            # adding other's operations
            eq.eq.append(OB)
            eq.eq.extend(other.eq)
            eq.eq.append(CB)
            return eq

        raise TypeError("...")

    def __rmul__(self, other):
        # other * self
        eq = Equation()

        if isinstance(other, int):
            eq.eq.append(1 if other else 0)
            eq.eq.append(MUL)
            eq.eq.extend(self.eq)
            return eq

        if isinstance(other, Variable):
            eq.eq.append(other)
            eq.eq.append(MUL)
            eq.eq.extend(self.eq)
            return eq

        if isinstance(other, Equation):
            # adding other's operations
            eq.eq.append(OB)
            eq.eq.extend(other.eq)
            eq.eq.append(CB)

            # add operator
            eq.eq.append(MUL)

            # adding exisiting operations
            eq.eq.append(OB)
            eq.eq.extend(self.eq)
            eq.eq.append(CB)

            return eq

        raise TypeError("...")

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

    def __str__(self):
        result = ""
        for i in self.eq:
            result += str(i) + " "

        return result[:-1]


if __name__ == "__main__":
    # Example use
    x = Variable("x")
    y = Variable("y")
    z = Variable("z")

    # (x + (y * z)).display_table()
    (~x + (y * z)).display_table()
