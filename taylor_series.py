import matplotlib.pyplot as plt
import numpy as np
from sympy import *


x = symbols("x")


def taylor_series(func, at=1, power_upto=6):
    terms = []

    terms.append(func.subs(x, at))

    factorial = 1
    for i in range(1, power_upto + 1):
        func = func.diff(x)
        factorial *= i
        term = (func.subs(x, at) * (x - at) ** i) / factorial
        # print(f"{i = }, {func = }, {factorial = }, {term = }, {func.subs(x, 1) = }")
        terms.append(term)

    return terms


def visualize(terms, at, interval=5):
    x_axis = np.linspace(at - interval, at + interval, 100)
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
        plt.plot(x_axis, y_axis[i])

    plt.show()


string = input("Enter Function to generate taylor series of\n\tf(x) = ")
pos = float(input("Enter the value around to generate: "))
no_terms = int(input("Enter number of terms: "))

func = eval(string)

print(taylor_series(func, pos, no_terms))
