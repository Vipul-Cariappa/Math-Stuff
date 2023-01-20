from collections.abc import Iterable
from sympy import *


def convert_to_latex(item):
    if not isinstance(item, Iterable):
        return latex(item)

    item_latex = []
    for i in item:
        item_latex.append(latex(i))

    return item_latex
