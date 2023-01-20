from sympy import *
import numpy as np
import matplotlib.pyplot as plt
import io


x, n = symbols("x n")


def fourier_series_evaluator(func, start, end):
    T = end - start
    cos_term = cos((2 * n * pi * x) / T)
    sin_term = sin((2 * n * pi * x) / T)

    a0 = 2 / T * (integrate(func, (x, start, end)).doit())

    an = 2 / T * (integrate(func * cos_term, (x, start, end)).doit()) * cos_term
    bn = 2 / T * (integrate(func * sin_term, (x, start, end)).doit()) * sin_term

    return (a0, an, bn)


# def fourier_series_latex(func, start, end):
#     a0, an, bn = fourier_series_evaluator(func, start, end)
#     a0, an, bn = (
#         nsimplify(a0, tolerance=0.01, full=True),
#         nsimplify(an, tolerance=0.01, full=True),
#         nsimplify(bn, tolerance=0.01, full=True),
#     )

#     latex_string = latex(a0) + " + "
#     latex_string += "\\sum_{n=1} ^{\\infty} "
#     latex_string += latex(an)
#     latex_string += latex(bn)

#     return latex_string


# TODO: rename this
def fourier_series_latex(func, start, end):
    a0, an, bn = fourier_series_evaluator(func, start, end)
    a0, an, bn = (
        nsimplify(a0, tolerance=0.01, full=True),
        nsimplify(an, tolerance=0.01, full=True),
        nsimplify(bn, tolerance=0.01, full=True),
    )

    # each_graph_equation = []

    latex_string = latex(a0) + " + "
    latex_string += "\\sum_{n=1} ^{\\infty}"
    latex_string += latex(an)
    latex_string += " + " + latex(bn)

    # each_graph_equation.append(latex_string)

    # eq = a0

    # for i in range(4):
    #     ai = an.subs(n, i)
    #     bi = bn.subs(n, i)

    #     each_graph_equation.append(latex(eq := eq + ai + bi))

    # print(*each_graph_equation, sep="\n\n")

    return latex_string


def fourier_graph_compute(func, start, end, terms=6, repeat=1, dir=1):
    a0, an, bn = fourier_series_evaluator(func, start, end)
    T = end - start

    if dir > 0:
        x_axis = np.linspace(start, start + T * repeat, 50)
    else:
        x_axis = np.linspace(end - (T * repeat), end, 50)

    y_axis = []

    for i in range(terms):
        an_i = an.subs(n, i)
        bn_i = bn.subs(n, i)

        if i > 0:
            y_axis.append(
                np.vectorize(
                    lambda value: float(an_i.subs(x, value) + bn_i.subs(x, value))
                )(x_axis)
                + y_axis[i - 1]
            )
        else:
            y_axis.append(
                np.vectorize(
                    lambda value: float(an_i.subs(x, value) + bn_i.subs(x, value) + a0)
                )(x_axis)
            )

    return x_axis, y_axis


def fourier_visualizer(func, start, end, terms=6, repeat=1, dir=1):
    x_axis, y_axis = fourier_graph_compute(func, start, end, terms, repeat, dir)

    for i in y_axis:
        plt.plot(x_axis, i)
    plt.show()


def fourier_visualizer_svg(func, start, end, terms=6, repeat=1, dir=1):
    x_axis, y_axis = fourier_graph_compute(func, start, end, terms, repeat, dir)

    for i in y_axis:
        plt.plot(x_axis, i)

    buf = io.BytesIO()
    plt.savefig(buf, format="svg")
    buf.seek(0)

    plt.close()

    print(str(buf.getvalue()))
    buf.seek(0)

    return buf


if __name__ == "__main__":
    func = eval(input("Enter Function to be Plot\n\tf(x) = "))
    start = float(input("Enter start of period: "))
    end = float(input("Enter end of period: "))
    repeat = int(input("Repeat the period how many time [1]: ") or "1")
    direction = int(input("Repeat in +ve or -ve [1]: ") or "1")

    fourier_visualizer(func, start, end, repeat=repeat, dir=direction)
