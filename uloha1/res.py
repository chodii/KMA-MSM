# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 09:26:45 2023

@author: chodo
"""

import sympy as simp
from sympy.abc import i
import random
import numpy as np
from matplotlib import pyplot as plt

x = simp.Symbol("x")
y = simp.Symbol("y")

fun = (1 -x -y)
eq1 = simp.integrate(fun, (x, 0, 1-y))
eq2 = simp.integrate(eq1, (y, 0, 1))
c = 1/eq2

# male f(x)
f_y = simp.integrate(c*fun, (x, 0, 1-y))
f_x = simp.integrate(c*fun, (y, 0, 1-x))
#tohle si raději ještě ověřím, jestli se mi počítá dobře
# coz je fce hustoty
# ted ji dam *x

EX = simp.integrate(x*f_x, (x, 0, 1))
EY = simp.integrate(y*f_y, (y, 0, 1))

# varX, varY
varX = simp.integrate(x*x*f_x, (x, 0, 1)) - EX**2
varY = simp.integrate(y*y*f_y, (y, 0, 1)) - EY**2

# covXY
covXY_pty = simp.integrate(x*y*c*fun, (x, 0, 1-y))
covXY = simp.integrate(covXY_pty, (y, 0, 1)) - EX*EY

var_M = ((varX, covXY), (covXY, varY))

#
ptsx = []
ptsy = []
n_max = 200
accuracy = 1e6
for ix in range(n_max):
    xr = random.randint(0, accuracy)/accuracy
    yr = random.randint(0, accuracy)/accuracy
    zr = random.randint(0, accuracy)/accuracy
    if xr+yr < 1:
        res = fun.subs(((x, xr), (y, yr)))
        if zr < res*c:
            ptsx.append(xr)
            ptsy.append(yr)
print(np.var(ptsx))# jak rychle vzhledem k teor hodnotám konverguje?
print(np.var(ptsy))
plt.scatter(ptsx, ptsy)
n = len(ptsx)
# var matici?
# covarianci?
avg_x = sum(ptsx)/n
avg_y = sum(ptsy)/n
covs = []
for ix in range(n):
    covi = ((ptsx[ix] - avg_x) * (ptsy[ix] - avg_y)) 
    covs.append(covi)
print(sum(covs)/(n-1))