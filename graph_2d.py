import matplotlib.pyplot as plt
import numpy as np
from sympy import *


x = symbols("x")


def graph_compute_points(func, start=-3.14, end=3.14):
    x_axis = np.linspace(start, end, 50)
    y_axis = np.vectorize(lambda value: float(func.subs(x, value)))(x_axis)

    return x_axis, y_axis


def graph(func, start=-3.14, end=3.14):
    x_axis, y_axis = graph_compute_points(func, start, end)

    plt.plot(x_axis, y_axis)
    plt.show()


if __name__ == "__main__":
    func = input("f(x): ")
    graph(eval(func))
