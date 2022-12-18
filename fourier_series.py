from sympy import *
import numpy as np
import matplotlib.pyplot as plt


def fourier_series_(func, start, end):
    n = symbols("n")
    T = end - start
    cos_term = cos((2 * n * pi * x) / T)
    sin_term = sin((2 * n * pi * x) / T)

    a0 = 2 / T * (integrate(func, (x, start, end)).doit())

    an = 2 / T * (integrate(func * cos_term, (x, start, end)).doit()) * cos_term
    bn = 2 / T * (integrate(func * sin_term, (x, start, end)).doit()) * sin_term

    return a0 + an + bn


def fourier_visualizer(func, start, end, terms=6, repeat=1, dir=1):
    n = symbols("n")
    T = end - start
    cos_term = cos((2 * n * pi * x) / T)
    sin_term = sin((2 * n * pi * x) / T)

    a0 = 2 / T * (integrate(func, (x, start, end)).doit())

    an = 2 / T * (integrate(func * cos_term, (x, start, end)).doit()) * cos_term
    bn = 2 / T * (integrate(func * sin_term, (x, start, end)).doit()) * sin_term

    if dir > 0:
        x_axis = np.linspace(float(start), float(start + T * repeat), 100)
    else:
        x_axis = np.linspace(float(end - (T * repeat)), float(end), 100)
    y_axis = []

    for i in range(terms):
        an_i = an.subs(n, i)
        bn_i = bn.subs(n, i)

        if i > 0:
            y_axis.append(
                tmp := np.vectorize(
                    lambda value: float(an_i.subs(x, value) + bn_i.subs(x, value))
                )(x_axis)
                + y_axis[i - 1]
            )
        else:
            y_axis.append(
                tmp := np.vectorize(
                    lambda value: float(an_i.subs(x, value) + bn_i.subs(x, value) + a0)
                )(x_axis)
            )
        plt.plot(x_axis, y_axis[i])
    plt.show()


x = symbols("x")
func = eval(input("Enter Function to be Plot\n\tf(x) = "))
start = float(input("Enter start of period: "))
end = float(input("Enter end of period: "))
repeat = int(input("Repeat the period how many time [1]: ") or "1")
direction = int(input("Repeat in +ve or -ve [1]: ") or "1")

fourier_visualizer(func, start, end, repeat=repeat, dir=direction)
