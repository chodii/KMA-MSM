# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 22:53:28 2023

@author: chodo
"""

import numpy as np

import matplotlib.pyplot as plt
# Define the constants and PDFs for x and y (you'll need to specify these)
c = 32/3.0  # Adjust as needed
mean_x = 1.0
variance_x = 0.5

mean_y = 2.0
variance_y = 1.0

# Number of realizations
num_realizations = 1000

# Generate realizations
realizations = []
x_values = []
y_values = []
for _ in range(num_realizations):
    #x = np.random.normal(mean_x, np.sqrt(variance_x))
    #y = np.random.normal(mean_y, np.sqrt(variance_y))
    y = (np.random.randint(0, 1000)/1000.0) * 2
    x = (np.random.randint(0, 1000)/1000.0) * (4-2*y)
    fxy = c * (x + y**2 + x * y)
    realizations.append(fxy)
    x_values.append(x)
    y_values.append(y)
# Calculate the mean and variance of the realizations
mean_realizations = np.mean(realizations)
variance_realizations = np.var(realizations)

print("Mean of Realizations:", mean_realizations)
print("Variance of Realizations:", variance_realizations)

# Histogram
plt.hist(realizations, bins=30, density=True, alpha=0.6, color='b', label='Histogram')
plt.title('Histogram of Realizations')
plt.xlabel('f(x, y)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)
plt.show()

# Context
plt.figure(figsize=(10, 6))

#plt.scatter(y_values, realizations, c=x_values, cmap='viridis', marker='o', s=50)
#plt.scatter(x_values, realizations, c=y_values, cmap='viridis', marker='o', s=50)
plt.scatter(x_values, y_values, c=realizations, cmap='viridis', marker='o', s=50)
plt.colorbar(label='f(x, y)')
plt.title('Scatter Plot of Realizations')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.show()