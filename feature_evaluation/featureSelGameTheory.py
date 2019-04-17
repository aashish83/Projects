
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 17:23:00 2018

@author: aashi
"""
import random
import pandas as pd
import numpy as np
import gcmi
import entropy_estimators as ee
from matplotlib import pyplot as plt
from sklearn import cross_validation, svm
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold, cross_val_score
from sklearn.ensemble import ExtraTreesClassifier
from sklearn import feature_selection

##loading data and preprocessing
data_raw = pd.read_csv("C:/Ash/Game_theory/clean1.data",sep=',',header=None)

xvals = []
yvals = []
for i in range(len(data_raw)):
    xvals.append(data_raw.values[i][2:168])
    yvals.append(data_raw.values[i][168])


xdf = pd.DataFrame(xvals)



col_names = []
for i in range(0,np.shape(xvals)[1]): 
    
    col_names.append(i)
    
col_names1 = list(col_names)

col_namesb = list(col_names)

col_namestree = list(col_names)

col_namesp = list(col_names)

xdf.columns = col_names    
 


### Shapley value analysis contribution function:

def contribution(flist , test):
    col = xdf[flist]    ### with f
    col2 = xdf[test]    ##without f  
    x_train, x_test, y_train, y_test = train_test_split(col, yvals)
    clf = GaussianNB()
    #clf = tree.DecisionTreeClassifier()

    clf.fit(x_train, y_train)
    scoref = clf.score(x_test,y_test)
    x_train1, x_test1, y_train1, y_test1 = train_test_split(col2, yvals)
    clf2 = GaussianNB()
    #clf2 = tree.DecisionTreeClassifier()
    clf2.fit(x_train1, y_train1)
    score = clf2.score(x_test1,y_test1)
    
    f_contri = scoref - score
    
    return f_contri
    

t = 20    # number of random coalitions  
d = 10   # size of the permutation    

e = 4
epochs = 10
iteration = 0
type(col_names)
while(iteration<=epochs):
    vals = list(np.zeros(len(col_names1)))
    #print(len(col_names))
    for f in col_names:
       # print(vals[f])
        feat = list(col_names)
        feat.remove(f)
        
        for j in range(1,t):
            
            
            flist = random.sample(feat, d)
            
            test = list(flist)
            
            
            flist.append(f)
        
            vals[f] = vals[f] + contribution(flist , test) + random.uniform(0.000000001, 0.0000001)

        vals[f] = vals[f] / t
       
    for k in range(0,e):
        el = vals.index(sorted(vals)[k])
        #print("The removed feature is", el,"its value is ",sorted(vals)[k] )
       # print(np.unique(col_names).size == len(col_names))
        col_names.remove(el)
   
    iteration +=1
    print("end of iteration number", iteration)

### banzhaf power index

def mutualinfo(x,y): 
    minfo = gcmi.mi_gg(x,y)
    return minfo

def cminf(x,y,z):  ### I(x,y/z)
    cminfo = gcmi.cmi_ggg(x,y,z)
    return cminfo


t=5
d=15
iteration1 = 0
epochs1 = 1
p=list(np.zeros(len(col_namesb)))
dep = 0
indep =1
while(iteration1<epochs1):

    vals = list(np.zeros(len(col_names1)))
   
    for f in col_namesb:
       # print(vals[f])
        feat1 = list(col_namesb)
        feat1.remove(f)
        for j in range(1,t):
           
            flist1 = random.sample(feat1, d)
            
            coal = list(flist1)
            
            for e in coal:
                #print("e is",e)
                x1 = xdf[e]
                x2 = xdf[f]
                m = mutualinfo(x1,yvals)
                c = cminf(x1,yvals,x2)
                if(c-m > 0):
                    #print("at dependancy for feature", f)
                    dep+=1   ### number of dependant in a coalition
                if(c-m <= 0):
                    #print("at indep for feature", f)
                    indep +=1  ##number of redundant or independant in a coalition.
            delta = dep/indep   ## p value 
            #print(delta)
            if(delta >= 0.5):
                p[f] = p[f] + 1
            dep = 0
            indep = 1
        p[f] = p[f]/t
        p[f] = p[f] + random.uniform(0.00000001, 0.0000001)
    iteration1+=1
    print("end of the iteration")


banz = [float(i)/max(p) for i in p]
iteration2 = 0
epoch2 = 40
e2 = 4
theta = 0.6

banz2 = list(banz)


for i in range(len(banz)):
    if(banz[i] < theta):
        #print(banz[i] ,"for i value", i)
        ind = banz2.index(banz[i])
        #print(ind)
        col_namesb.remove(ind)


######function for getting performance using 10 fold cross validation.
def performance(feat, target):
    x = xdf[feat]
    x_trainb, x_testb, y_trainb, y_testb = train_test_split(x, target)
    clf1 = GaussianNB()
    #clf1 = svm.SVC(gamma='scale')
    #clf1 = tree.DecisionTreeClassifier()
    clf1.fit(x_trainb, y_trainb)
    score = clf1.score(x_testb, y_testb)
    return score

def crossvalperf(feat, target):
    x = xdf[feat]
    k_fold =cross_validation.KFold(len(target), n_folds = 10, shuffle=True, random_state=0)
    clf = GaussianNB()
    #clf = svm.SVC(kernel ='linear' , C=1)
    #clf = tree.DecisionTreeClassifier()
    accuracy = cross_val_score(clf, x , target, cv=k_fold, n_jobs=1)
    return accuracy


###code for 
kb= crossvalperf(col_namesb,yvals).mean()
ks = crossvalperf(col_names,yvals).mean()
kn = crossvalperf(col_names1,yvals).mean()

### including other feature selection algo:

######Feature sel using extra trees classifier
r2 = 60
model = ExtraTreesClassifier()
model.fit(xdf, yvals)
fe = list(model.feature_importances_)

fef = [x+random.uniform(0.000000001, 0.0000001) for x in fe ]

for k in range(0,r2):
    el = fef.index(sorted(fef)[k])
    #print("The removed feature is", el,"its value is ",sorted(vals)[k] )
    # print(np.unique(col_names).size == len(col_names))
    
    col_namestree.remove(el)


####### Filter methods
ll = feature_selection.f_regression(xdf, yvals, center=True)
new = list(ll[0])
r = 60
for k in range(0,r):
    ell = new.index(sorted(new)[k])

    col_namesp.remove(ell)
    

final = list(np.zeros(len(col_names1)))

for i in range(len(col_names1)):
    final[i] = col_names.count(i) + col_namesb.count(i) + col_namestree.count(i) + col_namesp.count(i)

final1 = np.array(final)    
feat_list = []

feature_set = np.argsort(-final1)

feat_list.append(feature_set)

ff = feat_list[0]
f = list(ff[0:110])
kv=sorted(crossvalperf(f, yvals))[6]
Feat = xdf[f]

crossvalperf(col_namesb, yvals).mean()


performance(f,yvals)

shap = crossvalperf(col_names, yvals)



####### Plot The graph of accuracy
print("The classification accuracy without any feature selection model is", kn*100,"%" )
print("The classification accuracy using shapely value analysis model is", ks*100,"%" )
print("The classification accuracy using Banzhaf power index model is", kb*100,"%" )
print("The classification accuracy using voting of models", kv*100,"%" )
acc = []
acc.append(kn*100)
acc.append(ks*100)
acc.append(kb*100)
acc.append(kv*100)


pos = [0,1,2,3] 
x = np.arange(len(acc))
labels = ["NO FS" , 'Shapley Value', "Banzhaf" , 'Voting']
fig = plt.figure()
width = .35
plot = plt.bar(x,acc, width)
plot[0].set_color('r')
plot[2].set_color('y')
plot[3].set_color('g')
plt.xticks(pos, labels)
plt.ylabel("Accuracy")
plt.title("Classification Accuracies for different models")
fig.autofmt_xdate()
plt.show()
