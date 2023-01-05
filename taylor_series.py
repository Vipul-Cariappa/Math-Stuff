import matplotlib.pyplot as plt
import numpy as np
from sympy import *
import io


x = symbols("x")


def taylor_series(func, at=1, powers_upto=6):
    terms = []

    terms.append(func.subs(x, at))

    factorial = 1
    for i in range(1, powers_upto + 1):
        func = func.diff(x)
        factorial *= i
        term = (func.subs(x, at) * (x - at) ** i) / factorial
        terms.append(term)

    return terms


def taylor_series_latex(func, at):
    f = taylor_series(func, at, powers_upto=4)

    result = 0
    for i in f:
        result += i

    return latex(result)


def taylor_series_computer(func, at=1, powers_upto=4, interval=3.14):
    terms = taylor_series(func, at, powers_upto)

    x_axis = np.linspace(at - interval, at + interval, 50)
    y_axis = []

    for i in range(len(terms)):
        if i > 0:
            y_axis.append(
                np.vectorize(lambda value: float(terms[i].subs(x, value)))(x_axis)
                + y_axis[i - 1]
            )
        else:
            y_axis.append(
                np.vectorize(lambda value: float(terms[i].subs(x, value)))(x_axis)
            )

    return x_axis, y_axis


def taylor_series_visualizer_svg(func, at=1, powers_upto=4, interval=3.14):
    x_axis, y_axis = taylor_series_computer(func, at, powers_upto, interval)

    for i in y_axis:
        plt.plot(x_axis, i)

    buf = io.BytesIO()
    plt.savefig(buf, format="svg")
    buf.seek(0)

    plt.close()

    buf.seek(0)

    return buf


def taylor_series_visualizer(func, at=1, powers_upto=4, interval=3.14):
    x_axis, y_axis = taylor_series_computer(func, at, powers_upto, interval)

    for i in y_axis:
        plt.plot(x_axis, i)

    plt.show()


if __name__ == "__main__":
    string = input("Enter Function to generate taylor series of\n\tf(x) = ")
    pos = float(input("Enter the value around to generate: "))
    no_terms = int(input("Enter number of terms: "))

    func = eval(string)

    print(taylor_series(func, pos, no_terms))
