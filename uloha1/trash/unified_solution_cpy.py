# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 18:54:29 2023

@author: chodo
"""

from matplotlib import pyplot as plt
import numpy as np
import random
import sympy as simp
import pandas as pd
def main():
    x = simp.Symbol("x")
    y = simp.Symbol("y")
    
    # fci hustoty
    fun = (1 -x -y)
    # distrib
    eq1 = simp.integrate(fun, (x, 0, 1-y))
    eq2 = simp.integrate(eq1, (y, 0, 1))
    c = 1/eq2
    F_y = simp.integrate(c*fun, (y, 0, 1-x))
    F_x_to_y = simp.integrate(c*fun, (x, 0, 1-y))
    
    F_x = simp.integrate(c*fun, (x, 0, x))
    
    # statistics
    EX = simp.integrate(x*F_y, (x, 0, 1))
    EY = simp.integrate(y*F_x_to_y, (y, 0, 1))
    # varX, varY
    varX = simp.integrate(x*x*F_y, (x, 0, 1)) - EX**2
    varY = simp.integrate(y*y*F_x_to_y, (y, 0, 1)) - EY**2
    # covXY
    covXY_pty = simp.integrate(x*y*c*fun, (x, 0, 1-y))
    covXY = simp.integrate(covXY_pty, (y, 0, 1)) - EX*EY
    
    theoretical_stat = {"EX":EX, "EY":EY, "varX":varX, "varY":varY, "covXY":covXY}
    
    size = 1000
    xy = []
    method = "analytical"
    U = np.random.uniform(low=0, high=1, size=size)
    V = np.random.uniform(low=0, high=1, size=size)
    W = np.random.uniform(low=0, high=1, size=size)
    if method == "analytical":
        meth_sum_x = 0
        meth_sum_y = 0
        meth_xex_sum = 0
        meth_yey_sum = 0
        cov_sum = 0
        meth_stat = {"EX":[], "EY":[], "varX":[], "varY":[], "covXY":[]}
        
        for i in range(size):
            res = meth1(F_x, x, U[i], F_y, y, V[i], c*fun)
            xy.append(res)
            
            meth_sum_x += res[0]
            meth_sum_y += res[1]
            division = 1.0/(i+1)
            mex = meth_sum_x * division
            mey = meth_sum_y * division
            meth_stat["EX"].append(mex)
            meth_stat["EY"].append(mey)
            
            meth_xex_sum += (res[0] - mex)
            meth_yey_sum += (res[1] - mey)
            if i > 0:
                meth_stat["varX"].append(meth_xex_sum / i)
                meth_stat["varY"].append(meth_yey_sum / i)
            else:
                meth_stat["varX"].append(meth_xex_sum)# just to be nicely plotable :))
                meth_stat["varY"].append(meth_yey_sum)
            cov_sum += ((res[0]-mex)*(res[1]-mey))
            meth_stat["covXY"].append(cov_sum * division)
            
        ax_x = range(size)
        for k in meth_stat:
            d_row = meth_stat[k]
            plt.title(k)
            plt.plot(ax_x, [theoretical_stat[k]]*size, 'r')
            plt.scatter(ax_x, d_row)
            plt.show()
            
    else:
        for i in range(size):
            decisive = meth2_subs(fun, c, x, y, U[i], V[i], W[i])
            if decisive:
                xy.append((U[i], V[i]))
    
    xy = pd.DataFrame(xy)
    plt.scatter(xy[:][0], xy[:][1])
    plt.show()

def meth1(F_x, x, u, F_y, y, v, fun):
    res_x_fun = simp.solve([x >= 0, x <= 1, F_y - u], x)
    x_i = simp.solve(res_x_fun, x)[0]
    
    ff = simp.integrate(fun/F_y, (y, 0, y))
    
    fun_xi = ff.subs(x, x_i)
    res_y_fun = simp.solve([y >= 0, y <= 1, fun_xi - v], y)
    y_i = simp.solve(res_y_fun, y)[0]
    return (x_i, y_i)

def meth2_subs(fun, c, x, y, u, v, w):
    """
    return: decision whether the point x=u, y=v has 
    """
    if u+v > 1:
        return False
    res = fun.subs(((x, u), (y, v)))
    if w > res*c:
        return False
    return True

if __name__ == "__main__":
    main()
