from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from math import *

string = input("Enter Function to be Plot\n\tf(x) = ")

func_str = "lambda x: " + string.replace("^", "**")
func = eval(func_str)

x = np.linspace(-10, 10, 100)
y = np.apply_along_axis(np.vectorize(func), 0, x)

plt.plot(x, y)
plt.ylabel(string)
plt.xlabel("x")
plt.show()
# file_name = str(datetime.now()).split(".")[0].replace(":", "-") + ".png"
# plt.savefig(file_name, bbox_inches='tight')
