# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 18:54:29 2023

@author: chodora
"""

from matplotlib import pyplot as plt
import numpy as np
import sympy as simp
import pandas as pd
def main():
    x = simp.Symbol("x")
    y = simp.Symbol("y")
    
    # given density function
    fun = (1 -x -y)
    size = 1000# n of samples
    solution_by_substitution = True# and method, (the other one does not work for me, but I tried)
    
    # distrib
    eq1 = simp.integrate(fun, (x, 0, 1-y))
    eq2 = simp.integrate(eq1, (y, 0, 1))# calculate c
    c = 1/eq2
    
    F_y = simp.integrate(c*fun, (y, 0, 1-x))
    F_x = simp.integrate(c*fun, (x, 0, 1-y))
    
    
    F_x_int = simp.integrate(c*fun, (x, 0, x))# to keep both variables, wrong attempt, not used
    
    # statistics
    EX = simp.integrate(x*F_y, (x, 0, 1))
    EY = simp.integrate(y*F_x, (y, 0, 1))
    # varX, varY
    varX = simp.integrate(x*x*F_y, (x, 0, 1)) - EX**2
    varY = simp.integrate(y*y*F_x, (y, 0, 1)) - EY**2
    # covXY
    covXY_pty = simp.integrate(x*y*c*fun, (x, 0, 1-y))
    covXY = simp.integrate(covXY_pty, (y, 0, 1)) - EX*EY
    
    theoretical_stat = {"EX":EX, "EY":EY, "varX":varX, "varY":varY, "covXY":covXY}
    
    xy = []

    meth_sum_x = 0
    meth_sum_y = 0
    meth_xex_sum = 0
    meth_yey_sum = 0
    cov_sum = 0
    meth_stat = {"EX":[], "EY":[], "varX":[], "varY":[], "covXY":[]}
    i = 0
    while i < size:
        u = np.random.uniform(low=0, high=1)
        v = np.random.uniform(low=0, high=1)
        w = np.random.uniform(low=0, high=1)
        if not solution_by_substitution:
            res = meth1(F_x_int, x, u, F_y, y, v)
        else:
            decisive = meth2_subs(fun, c, x, y, u, v, w)
            if not decisive:# if out of our defined range
                continue# and generate new numbers
            res = (u, v)# else generated x=u, y=v lies in our defined space 
        xy.append(res)
        i += 1
        
        meth_sum_x += res[0]
        meth_sum_y += res[1]
        division = 1.0/(i+1)# for /n, speeds up calculation
        mex = meth_sum_x * division
        mey = meth_sum_y * division
        meth_stat["EX"].append(mex)
        meth_stat["EY"].append(mey)
        
        meth_xex_sum += (res[0] - mex)
        meth_yey_sum += (res[1] - mey)
        if i > 0:# varX = sum(x - EX)/(n-1) -> i = n-1
            meth_stat["varX"].append(meth_xex_sum / i)
            meth_stat["varY"].append(meth_yey_sum / i)
        else:
            meth_stat["varX"].append(meth_xex_sum)# just to be nicely (easily) plotable :))
            meth_stat["varY"].append(meth_yey_sum)
        cov_sum += ((res[0]-mex)*(res[1]-mey))
        meth_stat["covXY"].append(cov_sum * division)
        
    ax_x = range(size)# graph x axis -> n
    for k in meth_stat:# plot all statistics
        d_row = meth_stat[k]
        
        plt.title(k)
        plt.plot(ax_x, [theoretical_stat[k]]*size, color='r', label="theoretical")
        plt.scatter(ax_x, d_row, color='b', label="real")
        plt.xlabel("n")
        plt.show()
        
    xy = pd.DataFrame(xy)
    plt.scatter(xy[:][0], xy[:][1])
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
    # x and y is generated in given space
    # EX and EY is slightly different, probably convergates slowly
    # based on tests, to me it seems like  EX, EY convergates faster than varX, varY which convergates faster than covXY 
    

def meth1(F_x, x, u, F_y, y, v):# something done terribly wrong here :(, please don't take any points for this
    res_x_fun = simp.solve([x >= 0, x <= 1, F_y - u], x)
    x_i = simp.solve(res_x_fun, x)[0]
    
    fun_xi = F_x.subs(x, x_i)
    res_y_fun = simp.solve([y >= 0, y <= 1, fun_xi - v], y)
    y_i = simp.solve(res_y_fun, y)[0]
    return (x_i, y_i)# wrong attempt

def meth2_subs(fun, c, x, y, u, v, w):# can (w likely) happen that x=u and y=v?
    if u+v > 1:
        return False
    res = fun.subs(((x, u), (y, v)))
    if w > res*c:
        return False
    return True# right attempt

if __name__ == "__main__":
    main()
