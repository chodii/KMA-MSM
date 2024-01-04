# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 10:02:24 2023

@author: chodo
"""

import scipy.integrate as inter
import scipy.special as special

fun = lambda x,y: (6/5)*(x+2*y)

# double:
#inter.dblquad(fun, 0, 1, 0, 1)
# for any: func, [x_range, y_range, ..]
inter.nquad(fun, [(0,1), (0,0.5)])

# single:
#def my_int_fun(x, a, b):
#    return x*x*a + b
#inter.quad(my_int_fun, 0, 1, args=(1, 3))


# indefinite integral
import sympy as simp
x = simp.Symbol("x")
z = simp.Symbol("z")
eq1 = 5 + x**2 + z
eq2 = simp.integrate(eq1, x)
simp.integrate(eq2, z)
