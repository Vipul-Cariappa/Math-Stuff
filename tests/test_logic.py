from MathStuff import logic

a = logic.Variable("a")
b = logic.Variable("b")
c = logic.Variable("c")
d = logic.Variable("d")
e = logic.Variable("e")


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


def evaluator4(tb, equation_str, result_str):
    """
    Works for equation with four variables
    """

    for i in range(16):
        a = tb["a"][i]
        b = tb["b"][i]
        c = tb["c"][i]
        d = tb["d"][i]

        assert tb[result_str][i] == eval(equation_str)


def evaluator5(tb, equation_str, result_str):
    """
    Works for equation wiht five variables
    """
    for i in range(32):
        a = tb["a"][i]
        b = tb["b"][i]
        c = tb["c"][i]
        d = tb["d"][i]
        e = tb["e"][i]

        assert tb[result_str][i] == eval(equation_str)


def test_negation():
    """
    Truth Table

    | a | ~a |
    ----------
    | 0 |  1 |
    | 1 |  0 |
    ----------
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
    -----------------
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
    -----------------
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
    ------------------
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
    -----------------
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
    -----------------
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
    ----------------------------
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
    -------------------------
    """

    eq = (a + (~b)) / b
    table = eq.generate_truth_table()

    evaluator2(table, "int(not(a or (not(b))) or b)", "( a + ( ~ b ) ) -> b")


def test_complex3():
    """
    Truth Table

    | a | b | c | d | (a + c) * (b + d) |
    -------------------------------------
    | 0 | 0 | 0 | 0 |       0           |
    | 0 | 0 | 0 | 1 |       0           |
    | 0 | 0 | 1 | 0 |       0           |
    | 0 | 0 | 1 | 1 |       1           |
    | 0 | 1 | 0 | 0 |       0           |
    | 0 | 1 | 0 | 1 |       0           |
    | 0 | 1 | 1 | 0 |       1           |
    | 0 | 1 | 1 | 1 |       1           |
    | 1 | 0 | 0 | 0 |       0           |
    | 1 | 0 | 0 | 1 |       1           |
    | 1 | 0 | 1 | 0 |       0           |
    | 1 | 0 | 1 | 1 |       1           |
    | 1 | 1 | 0 | 0 |       1           |
    | 1 | 1 | 0 | 1 |       1           |
    | 1 | 1 | 1 | 0 |       1           |
    | 1 | 1 | 1 | 1 |       1           |
    -------------------------------------
    """
    eq = (a + c) * (b + d)
    tb = eq.generate_truth_table()

    evaluator4(tb, "int((a or c) and (b or d))", "( a + c ) * ( b + d )")


def test_complex4():
    """
    Truth Table

    | a | b | c | d | e | (a + b + ~e) * (c + d) |
    ----------------------------------------------
    | 0 | 0 | 0 | 0 | 0 |           0            |
    | 0 | 0 | 0 | 0 | 1 |           0            |
    | 0 | 0 | 0 | 1 | 0 |           1            |
    | 0 | 0 | 0 | 1 | 1 |           0            |
    | 0 | 0 | 1 | 0 | 0 |           1            |
    | 0 | 0 | 1 | 0 | 1 |           0            |
    | 0 | 0 | 1 | 1 | 0 |           1            |
    | 0 | 0 | 1 | 1 | 1 |           0            |
    | 0 | 1 | 0 | 0 | 0 |           0            |
    | 0 | 1 | 0 | 0 | 1 |           0            |
    | 0 | 1 | 0 | 1 | 0 |           1            |
    | 0 | 1 | 0 | 1 | 1 |           1            |
    | 0 | 1 | 1 | 0 | 0 |           1            |
    | 0 | 1 | 1 | 0 | 1 |           1            |
    | 0 | 1 | 1 | 1 | 0 |           1            |
    | 0 | 1 | 1 | 1 | 1 |           1            |
    | 1 | 0 | 0 | 0 | 0 |           0            |
    | 1 | 0 | 0 | 0 | 1 |           0            |
    | 1 | 0 | 0 | 1 | 0 |           1            |
    | 1 | 0 | 0 | 1 | 1 |           1            |
    | 1 | 0 | 1 | 0 | 0 |           1            |
    | 1 | 0 | 1 | 0 | 1 |           1            |
    | 1 | 0 | 1 | 1 | 0 |           1            |
    | 1 | 0 | 1 | 1 | 1 |           1            |
    | 1 | 1 | 0 | 0 | 0 |           0            |
    | 1 | 1 | 0 | 0 | 1 |           0            |
    | 1 | 1 | 0 | 1 | 0 |           1            |
    | 1 | 1 | 0 | 1 | 1 |           1            |
    | 1 | 1 | 1 | 0 | 0 |           1            |
    | 1 | 1 | 1 | 0 | 1 |           1            |
    | 1 | 1 | 1 | 1 | 0 |           1            |
    | 1 | 1 | 1 | 1 | 1 |           1            |
    ----------------------------------------------
    """

    eq = (a + b + (~e)) * (c + d)
    table = eq.generate_truth_table()

    evaluator5(
        table,
        "int((a or b or (not(e))) and (c or d))",
        "( ( a + b ) + ( ~ e ) ) * ( c + d )",
    )


def test_combinations1():
    """
    Check uniqueness of each combination in one variable combination
    """
    eq = ~a
    tb = eq.generate_truth_table()

    for i in range(2):
        an = tb["a"][i]

        number = an

        assert number == i


def test_combinations2():
    """
    Check uniqueness of each combination in two variable combination
    """
    eq = a + b
    tb = eq.generate_truth_table()

    for i in range(4):
        an = tb["a"][i]
        bn = tb["b"][i]

        number = (an << 1) + bn

        assert number == i


def test_combinations3():
    """
    Check uniqueness of each combination in three variable combination
    """

    eq = a + b + c
    tb = eq.generate_truth_table()

    for i in range(8):
        an = tb["a"][i]
        bn = tb["b"][i]
        cn = tb["c"][i]

        number = (an << 2) + (bn << 1) + cn

        assert number == i


def test_combinations4():
    """
    Check uniqueness of each combination in four variable combination
    """
    eq = a + b + c + d
    table = eq.generate_truth_table()

    for i in range(16):
        an = table["a"][i]
        bn = table["b"][i]
        cn = table["c"][i]
        dn = table["d"][i]

        number = (an << 3) + (bn << 2) + (cn << 1) + dn

        assert number == i


def test_combinations5():
    """
    Check uniqueness of each combination in five variable combination
    """
    eq = a + b + c + d + e
    tb = eq.generate_truth_table()

    for i in range(32):
        an = tb["a"][i]
        bn = tb["b"][i]
        cn = tb["c"][i]
        dn = tb["d"][i]
        en = tb["e"][i]

        number = (an << 4) + (bn << 3) + (cn << 2) + (dn << 1) + en

        assert number == i
