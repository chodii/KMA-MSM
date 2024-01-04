# -*- coding: utf-8 -*-
#programmingwarcrimes
"""
Created on Fri Nov 10 19:28:24 2023

@author: chodora
"""
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Parameters:
file_path = './Rocks.xls'
headers = ("RMCS", "PAOA", "CDLT")# for specified features
p_signif = 0.05# significant value


df = pd.read_excel(file_path, sheet_name="Data")
# loaded as pd.DataFrame

rocks = {}
# load data into rocks ... to be accessible/grouped by the "Class"
rocks_classes = df["Class"]
for i in range(len(rocks_classes)):
    class_rock = rocks_classes[i]
    class_rock = str.replace(class_rock, " ", "")# >:(
    if class_rock not in rocks:
        rocks[class_rock] = {k:[] for k in df}
    for k in df:
        rocks[class_rock][k].append(df[k][i])


statistics = {}
# Calculate statistics:
keys = []
for k in rocks:# for each "Class"
    keys.append(k)
    statistics[k] = {"EX":{}, "varX":{}, "std":{}, "stand_error":{}, "Q1":{}, "Q3":{}, "normality":{}}
    for f in headers:# no need for most of this, but I'll keep it here for myself :)
        statistics[k]["EX"][f] = np.mean(rocks[k][f])
        statistics[k]["varX"][f] = np.var(rocks[k][f])
        statistics[k]["std"][f] = np.std(rocks[k][f])
        statistics[k]["stand_error"][f] = (np.std(rocks[k][f]/np.sqrt(np.size(rocks[k][f]))))
        statistics[k]["Q1"][f] = np.percentile(rocks[k][f], 25)
        statistics[k]["Q3"][f] = np.percentile(rocks[k][f], 75)
        statistics[k]["normality"][f] = True if stats.kstest(rocks[k][f], 'norm')[1] < p_signif else False 
print("Normality of the data", {k:statistics[k]["normality"] for k in keys})# testing normality of the data, seems normal

# Scattter plots:
for fi in range(len(headers)):
    f = headers[fi]
    for finito in range(fi+1, len(headers), 1):
        f2 = headers[finito]
        for k in keys:
            plt.scatter(rocks[k][f], rocks[k][f2], label=k)
        plt.legend()
        plt.xlabel(f)
        plt.ylabel(f2)
        plt.show()
        

# Tests:
t_tests = {}
f_tests = {}
anova = {}
for f in headers:# for each dimension
    f_stones = [rocks[k][f] for k in keys]
    # Box plots
    plt.boxplot(f_stones, labels=keys)
    plt.title(f)
    plt.show()
    t_tests[f] = []
    f_tests[f] = []
    anova[f]   = []
    for i in range(len(keys)):
        k1 = keys[i]
        for j in range(i+1, len(keys), 1):
            k2 = keys[j]
            rocks1 = rocks[k1][f]
            rocks2 = rocks[k2][f]
            
            # T-TEST
            tt_stat, tp_value = stats.ttest_ind(rocks1, rocks2)
            tr = 1# H0: they are similar
            if tp_value <  p_signif:# refusing H0-> they are different
                tr = 0
            t_tests[f].append((k1+" - "+k2, tt_stat, tp_value, tr))
            
            # ANOVA
            at_stat, ap_value = stats.f_oneway(rocks1, rocks2)# for ANOVA
            ar = 1# H0: they are similar
            if ap_value < p_signif:# refusing H0-> they are different
                ar = 0
            anova[f].append((k1+" - "+k2, at_stat, ap_value, ar))
            
            # F-TEST
            f_value = statistics[k1]["varX"][f] / statistics[k2]["varX"][f]# press F
            fp_value = stats.f.cdf(f_value, len(rocks1)-1, len(rocks2)-1)
            fr = 1# H0: they are similar
            if fp_value < p_signif:# refusing H0-> they are different
                fr = 0
            f_tests[f].append((k1+" - "+k2, f_value, fp_value, fr))


# Results:
print("\nTesting similarity of two rocks with p-value:", p_signif)
for d in range(len(headers)):# (d+1)-dimensional test = test resulted in p-value being: p_value < p_significant_value for d+1 dimensions (d=0..2) 
    print("\nsuccessful ",str(d+1)+"-dimensional tests:")
    for pair in range(len(t_tests[headers[0]])):
        if sum(t_tests[headers[i]][pair][3] for i in range(len(headers))) > d:# passed the test for d+1 features/dimensions
            print(t_tests[headers[0]][pair][0] + " \t t-test ", {h: (True if t_tests[h][pair][3] == 1 else False) for h in headers})
            
        if sum(f_tests[headers[i]][pair][3] for i in range(len(headers))) > d:
            print(f_tests[headers[0]][pair][0] + "  \t f-test ", {h: (True if f_tests[h][pair][3] == 1 else False) for h in headers})
        
        if sum(anova[headers[i]][pair][3] for i in range(len(headers))) > d:
            print(f_tests[headers[0]][pair][0] + " \t ANOVA ", {h: (True if anova[h][pair][3] == 1 else False) for h in headers})
