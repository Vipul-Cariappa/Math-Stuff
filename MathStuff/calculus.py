from sympy import *
import sympy

x = symbols("x")


def differentiate(func):
    return diff(func, x)


def integrate(func):
    return sympy.integrate(func, x)


def differentiate_latex(func):
    d = differentiate(func)
    return latex(d)


def integrate_latex(func):
    i = integrate(func)
    return latex(i)
