# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 11:01:02 2023

@author: chodo
"""

import sympy as simp
import random
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

x = simp.Symbol("x")
y = simp.Symbol("y")

# fci hustoty
fun = (1 -x -y)
# distrib
eq1 = simp.integrate(fun, (x, 0, 1-y))
eq2 = simp.integrate(eq1, (y, 0, 1))
c = 1/eq2

F_y = simp.integrate(c*fun, (y, 0, 1-x))

F_x = simp.integrate(c*fun, (x, 0, x))

size = 200
U = np.random.uniform(low=0, high=1, size=size)
V = np.random.uniform(low=0, high=1, size=size)
xy = []
for i in range(size):
    #    f_x - U[i] = 0
    #res = f_x.subs(((y, xr))
    res_x_fun = simp.solve([x >= 0, x <= 1, F_y - U[i]], x)
    x_i = simp.solve(res_x_fun, x)[0]
    
    # find y_i
    # c*fun <- x=x_i
    fun_xi = F_x.subs(x, x_i)
    res_y_fun = simp.solve([y >= 0, y <= 1, fun_xi - V[i]], y)
    y_i = simp.solve(res_y_fun, y)
    xy.append((x_i, y_i[0]))
xy = pd.DataFrame(xy)
plt.scatter(xy[:][0], xy[:][1])
plt.show()