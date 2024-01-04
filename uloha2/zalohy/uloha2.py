# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 17:31:05 2023

@author: chodo
"""

"""
    7. Attribute Information:
       1. sepal length in cm
       2. sepal width in cm
       3. petal length in cm
       4. petal width in cm
       5. class: 
          -- Iris Setosa
          -- Iris Versicolour
          -- Iris Virginica
    
    Summary Statistics:
            	         Min  Max   Mean    SD Class  Correlation
       sepal length: 4.3  7.9   5.84    0.83      0.7826   
        sepal width: 2.0  4.4   3.05    0.43      -0.4194
       petal length: 1.0  6.9   3.76    1.76      0.9490  (high!)
        petal width: 0.1  2.5   1.20    0.76      0.9565  (high!)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import sqrtm
from scipy.stats import chi2
import random
import math

# read iris
fname = "iris.data"
fil = open(fname)
lines = fil.readlines()
iris = {}
for lin in lines:
    pars = lin.split(",")
    name = pars[-1].replace("\n", "")
    if name == "":
        continue
    if name not in iris.keys():
        iris[name] = []
        for i in range(len(pars)-1):
            iris[name].append([])
    for i in range(len(pars)-1):
        iris[name][i].append(float(pars[i]))
# print(iris)

statistics = {}
for k in iris.keys():
    statistics[k] = {}
    for i in range(len(iris[k])):
        EX = np.mean(iris[k][i])#sum(iris[k][i]) / len(iris[k][i])
        statistics[k]["E"+str(i)] = EX
        varX = 0
        for j in range(len(iris[k][i])):
            varX += (iris[k][i][j] - EX)**2
        varX /= len(iris[k][i])
        statistics[k]["var"+str(i)] = varX
    plt.scatter(iris[k][0], iris[k][1])
plt.show()


k = "Iris-setosa"
data = [iris[k][0], iris[k][1]]
transformed_data = [[],[]]
cov_mat = np.cov(data)
cov_mat_root = sqrtm(cov_mat)#**(1/2)
cov_mat_root_inv = np.linalg.inv(cov_mat_root)
for j in range(len(iris[k][i])):
    row = []# [x_i - EX, y_i - EY]
    for i in range(2):#len(iris[k])
        xx = iris[k][i][j] - statistics[k]["E"+str(i)]
        row.append(xx)
    
    res_i = np.matmul(cov_mat_root_inv, row)
    transformed_data[0].append(res_i[0])
    transformed_data[1].append(res_i[1])

plt.scatter(transformed_data[0], transformed_data[1])
plt.show()

# KROUŽKUJU
df = 2
alpha = 5e-2
x = []
y = []
for i in range(0, 1000):
    angle = random.uniform(0, 1) * (np.pi * 2)
    r = np.sqrt(chi2.ppf(1 - alpha, df))
    x.append(r*math.cos(angle));
    y.append(r*math.sin(angle));
plt.scatter(x, y, color='blue')
plt.scatter(transformed_data[0], transformed_data[1])
plt.show()


back_data = [[],[]]
for j in range(len(x)):
    back_data[0].append(x[j])# + statistics[k]["E"+str(0)]
    back_data[1].append(y[j])#res_i[1] + statistics[k]["E"+str(1)]
res_back = np.matmul(cov_mat_root, back_data)
#plt.scatter(x, y, color='blue')
for i in range(len(res_back)):
    for j in range(len(res_back[i])):
        res_back[i,j] += statistics[k]["E"+str(i)]
plt.scatter(res_back[0], res_back[1])
plt.scatter(iris[k][0], iris[k][1])
plt.show()



for k in statistics.keys():
    mu = np.array([statistics[k]["E"+str(i)] for i in range(len(iris[k]))])

