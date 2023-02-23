from MathStuff import logic

a = logic.Variable("a")
b = logic.Variable("b")
c = logic.Variable("c")


def evaluator2(tb, equation_str, result_str):
    """Args:
        tb: truth table
        equation_str: evalator string to compare against
        result_str: key in the tb for the result
    Works only for equation of two variable
    """
    for i in range(4):
        a = tb["a"][i]
        b = tb["b"][i]

        assert tb[result_str][i] == eval(equation_str)


def evaluator3(tb, equation_str, result_str):
    """Args:
        tb: truth table
        equation_str: evalator string to compare against
        result_str: key in the tb for the result
    Works only for equation of three variable
    """
    for i in range(8):
        a = tb["a"][i]
        b = tb["b"][i]
        c = tb["c"][i]

        assert tb[result_str][i] == eval(equation_str)


def test_negation():
    """
    Truth Table

    | a | ~a |
    ----------
    | 0 |  1 |
    | 1 |  0 |
    """

    eq = ~a
    tb = eq.generate_truth_table()

    for i in range(2):
        x = tb["a"][i]

        assert tb["~ a"][i] == int(not (x))


def test_or():
    """
    Truth Table

    | a | b | a + b |
    -----------------
    | 0 | 0 |   0   |
    | 1 | 0 |   1   |
    | 0 | 1 |   1   |
    | 1 | 1 |   1   |
    """

    eq = a + b
    tb = eq.generate_truth_table()

    evaluator2(tb, "int(a or b)", "a + b")


def test_and():
    """
    Truth Table

    | a | b | a * b |
    -----------------
    | 0 | 0 |   0   |
    | 1 | 0 |   0   |
    | 0 | 1 |   0   |
    | 1 | 1 |   1   |
    """

    eq = a * b
    tb = eq.generate_truth_table()

    evaluator2(tb, "int(a and b)", "a * b")


def test_conditional():
    """
    Truth Table

    | a | b | a -> b |
    ------------------
    | 0 | 0 |   1    |
    | 1 | 0 |   0    |
    | 0 | 1 |   1    |
    | 1 | 1 |   1    |
    """

    eq = a / b
    table = eq.generate_truth_table()

    evaluator2(table, "int((not(a)) or b)", "a -> b")


def test_biconditional():
    """
    Truth Table

    | a | b | a % b |
    -----------------
    | 0 | 0 |   1   |
    | 1 | 0 |   0   |
    | 0 | 1 |   0   |
    | 1 | 1 |   1   |
    """

    eq = a % b
    table = eq.generate_truth_table()

    evaluator2(table, "int((not(a) or b) and (a or (not(b))))", "a <-> b")


def test_xor():
    """
    Truth Table

    | a | b | a ^ b |
    -----------------
    | 0 | 0 |   0   |
    | 1 | 0 |   1   |
    | 0 | 1 |   1   |
    | 1 | 1 |   0   |
    """

    eq = a ^ b
    table = eq.generate_truth_table()

    evaluator2(table, "int((not(a) and b) or (a and (not(b))))", "a ^ b")


def test_complex1():
    """
    Truth Table

    | a | b | c | a + ( b * c )|
    ----------------------------
    | 0 | 0 | 0 |      0       |
    | 1 | 0 | 0 |      1       |
    | 0 | 1 | 0 |      0       |
    | 1 | 1 | 0 |      1       |
    | 0 | 0 | 1 |      0       |
    | 1 | 0 | 1 |      1       |
    | 0 | 1 | 1 |      1       |
    | 1 | 1 | 1 |      1       |
    """

    eq = a + b * c
    table = eq.generate_truth_table()

    evaluator3(table, "int(a or (b and c))", "a + ( b * c )")


def test_complex2():
    """
    Truth Table

    | a | b | (a + ~b) -> b |
    -------------------------
    | 0 | 0 |       0       |
    | 1 | 0 |       0       |
    | 0 | 1 |       1       |
    | 1 | 1 |       1       |
    """

    eq = (a + (~b)) / b
    table = eq.generate_truth_table()

    evaluator2(table, "int(not(a or (not(b))) or b)", "( a + ( ~ b ) ) -> b")


def test_combinations():
    eq = a + b + c
    tb = eq.generate_truth_table()

    for i in range(8):
        an = tb["a"][i]
        bn = tb["b"][i]
        cn = tb["c"][i]

        number = (an << 2) + (bn << 1) + cn

        assert number == i
