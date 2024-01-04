# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 17:31:05 2023

@author: chodora
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
"""
    First I read the data
"""
fname = "iris.data"
fil = open(fname)
lines = fil.readlines()
iris = {}
for lin in lines:
    pars = lin.split(",")
    name = pars[-1].replace("\n", "")
    if name == "":
        continue
    n_of_features = 2#len(pars)-1
    if name not in iris.keys():
        iris[name] = []
        for i in range(n_of_features):
            iris[name].append([])
    for i in range(n_of_features):
        iris[name][i].append(float(pars[len(pars)-2-i]))# for petal width/length in cm


"""
    Calculate statistics
"""
plt.title(fname)
statistics = {}
for k in iris.keys():
    statistics[k] = {}
    for i in range(len(iris[k])):
        EX = np.mean(iris[k][i])
        statistics[k]["E"+str(i)] = EX
    plt.scatter(iris[k][0], iris[k][1], label=k)
plt.legend()
plt.show()


#k = "Iris-setosa"
"""
    Then transform the data in order to draw circle around the confidence group
"""
#plt.title("Transforming the data")
transformed_data = {}
inv_COV_mtx = {}
for k in iris.keys():
    data = iris[k]
    transformed_data[k] = [[] for i in range(len(iris[k]))]
    cov_mat = np.cov(data)# kovarianční matice
    cov_mat_root = sqrtm(cov_mat)# COV**(1/2)
    cov_mat_root_inv = np.linalg.inv(cov_mat_root)# COV**(-1)
    inv_COV_mtx[k] = cov_mat_root_inv
    for j in range(len(iris[k][i])):
        row = []# [x_i - EX, y_i - EY]
        for i in range(len(iris[k])):#
            xx = iris[k][i][j] - statistics[k]["E"+str(i)]
            row.append(xx)
        
        res_i = np.matmul(cov_mat_root_inv, row)# COV**(-1/2) * entry-wise mean deviation
        for f in range(len(res_i)):
            transformed_data[k][f].append(res_i[f])# append transformed entry
        #transformed_data[1].append(res_i[1])
    
#    plt.scatter(transformed_data[k][0], transformed_data[k][1], label=k)
#plt.legend()
#plt.show()


"""
    draw circles
"""
plt.title("Transforming the data and marking confidence group")
circles = {}
for k in iris.keys():
    # KROUŽKUJU
    df = 2
    alpha = 5e-2
    x = []
    y = []
    for i in range(0, 100):
        angle = random.uniform(0, 1) * (np.pi * 2)
        r = np.sqrt(chi2.ppf(1 - alpha, df))
        x.append(r*math.cos(angle));
        y.append(r*math.sin(angle));
    circles[k] = [x, y]
    plt.scatter(x, y, label="cg "+k)#, color='blue'
    plt.scatter(transformed_data[k][0], transformed_data[k][1], label=k)
plt.legend()
plt.show()
    
"""
    transform circles back
"""
plt.title("Transform back")
transformed_circles = {}
for k in iris.keys():
    back_data = [[],[]]
    x = circles[k][0]
    y = circles[k][1]
    for j in range(len(x)):
        back_data[0].append(x[j])# + statistics[k]["E"+str(0)]
        back_data[1].append(y[j])#res_i[1] + statistics[k]["E"+str(1)]
    res_back = np.matmul(cov_mat_root, back_data)
    for i in range(len(res_back)):
        for j in range(len(res_back[i])):
            res_back[i,j] += statistics[k]["E"+str(i)]
    transformed_circles[k] = res_back
    plt.scatter(res_back[0], res_back[1], label="cg "+k)
    plt.scatter(iris[k][0], iris[k][1], label=k)
plt.legend()
plt.show()


""" After the circles have been drawn and data has been transformed back """
plt.title("Identify outliers")
outliers = [[],[]]
for k in iris.keys():
    threshold = None
    outliers_distance = []
    for t in range(2):
        for i in range(len(iris[k][0])):
            for j in range(len(iris[k])):
                if threshold is None:# count all mahalanobis distances in order to be able to find optimal threshold
                    mahalanobis_distance = np.sqrt(abs(transformed_data[k][j][i]))
                    outliers_distance.append(mahalanobis_distance)
                    continue
                if outliers_distance[i*(len(iris[k])) + j] > threshold:# mark all outliers
                    outliers[0].append(iris[k][0][i])
                    outliers[1].append(iris[k][1][i])
        if threshold is None:
            threshold = np.percentile(outliers_distance, 95)# finding 0.95 quartil and using it as threshold

for k in iris.keys():
    plt.scatter(transformed_circles[k][0], transformed_circles[k][1], label="cg "+k, color="grey")
    plt.scatter(iris[k][0], iris[k][1], label=k)
plt.scatter(outliers[0], outliers[1], color='red', label="Outliers")
plt.legend()
plt.show()

# 
