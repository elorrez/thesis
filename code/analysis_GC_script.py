# -*- coding: utf-8 -*-
"""

@author: Christina Papagiannopoulou
@purpose: Example script which calculates the linear and non-linear Granger causality quantification for one pixel on the globe.
@reference: Papagiannopoulou et al., 2017. A non-linear Granger-causality framework to investigate
		climate–vegetation dynamics. Geoscentific Model Development, 10, 1–16. DOI: 10.5194/gmd-10-1-2017.

@input: test.csv

@arguments:     1) Input file
		2) linear OR non-linear

@execute:   python GC_script.py test.csv linear
	    python GC_script.py test.csv non-linear

"""
import numpy as np
# from sklearn.preprocessing import Imputer, This module does not exist anymore (is from 0.16, now: 0.23)
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from numpy import genfromtxt #Load data from a text file, with missing values handled as specified.
import time
import sys # This module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter.
# from sklearn.cross_validation import KFold, his module does not exist anymore (is from 0.17, now: 0.23)
from sklearn.model_selection import KFold
from sklearn.metrics import r2_score #R^2 (coefficient of determination) regression score function.
from sklearn.linear_model import Ridge #Linear least squares with l2 regularization.
# from sklearn.grid_search import GridSearchCV, This module does not exist anymore
from sklearn.model_selection import GridSearchCV
import os


#%%functions

#parameters: vector 'arr' and an integer 'num'
#returns: a 'num'-times shifted vector
def shift2(arr,num):
    arr=np.roll(arr,num) #Roll array elements along a given axis.
    if num < 0:
         np.put(arr,range(len(arr)+num,len(arr)),np.nan) #np.put: Replaces specified elements of an array with given values.
    elif num > 0:
         np.put(arr,range(num),np.nan)
    return arr

#parameters: string 'inpath' = the path of the .csv dataset
#returns: the dataset in a numpy array
def readFile(inpath):
    if os.path.isfile(inpath):
        dataset = genfromtxt(open(inpath,'r'), delimiter=',', dtype='f8')[0:]
        for col in range(dataset.shape[1]):
            ipos = np.where(np.isposinf(dataset[:, col]))
            dataset[ipos, col] = np.max(np.ma.masked_invalid(dataset[:, col]))
            ineg = np.where(np.isneginf(dataset[:, col]))
            dataset[ineg, col] = np.min(np.ma.masked_invalid(dataset[:, col]))
        imp = SimpleImputer(missing_values=np.nan, strategy='mean')# fill in the missing values with the mean of each column
        # !SimpleImputer will throw ValueError if the array passed in contains np.inf, which is not the case in the old imputer!
        transformedData = imp.fit_transform(dataset)
        # rmvedCols = imp.statistics_, Weird error--> says that this attribute does not exist, while sklearn says it does?
        #replace by taking the mean of every column ignoring nan values
        rmvedCols = np.nanmean(dataset, axis=0)
        idxRmved = np.where(np.isnan(rmvedCols))#take the indices of the nan columns
        nanTarget = dataset.shape[1]-1 in idxRmved[0]#check if the target is a nan column
        if nanTarget:
            raise ValueError("The target variable contains only nan values or inf")
    else:
        raise ValueError("File does not exist")
    return (transformedData)

#parameters: vector 'target' which is the target variable
#returns: the dataset which includes the previous values of the target
def createAuto(target):
    win=13 # window size, how many previous values we take of the target (here 12 because the range goes from 1-12 without the 13) 12 months
    dataAuto = np.empty((len(target),win-1))
    for i in range(1,win):
        dataAuto[:,i-1] = shift2(target, i)
    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    transformedDataAuto = imp.fit_transform(dataAuto)
    X_auto = transformedDataAuto
    return X_auto

#parameters: 'X' the predictors, 'y' the target, 'cvFolds' number of folds, 'estimator' machine learning algorithm
#returns: the R squared for each fold
def crossValidation(X, y, cvFolds, estimator):
    r2 = np.zeros((cvFolds,1))
    kf = KFold(n_splits=cvFolds, shuffle=True, random_state = 30)
    cv_j=0
    for train_index, test_index in kf.split(X):
        train_X = X[train_index,:]
        test_X = X[test_index,:]
        train_y = y[train_index]
        test_y = y[test_index]
        estimator.fit(train_X,train_y)
        y_true, y_pred = test_y,estimator.predict(test_X)
        r2[cv_j] = r2_score(y_true, y_pred)
        cv_j = cv_j + 1
    return r2

#parameters: 'X' the predictors, 'y' the target, 'cvFolds' number of folds, 'estimator' machine learning algorithm
#returns: the R squared for each fold
def nestedCrossValidation(X, y, cvFolds, estimator):
    kf = KFold(n_splits=cvFolds, shuffle=True, random_state = 30)
    cv_j=0
    param_grid = {'alpha': [0.0000001,0.000001,0.00001,0.0001,0.001,0.01,0.1,1,10,100,1000,10000,100000, 1000000, 10000000,1000000000]}
    r2 = np.zeros((cvFolds,1))
    for train_index, test_index in kf.split(X):
        train_X = X[train_index,:]
        test_X = X[test_index,:]
        train_y = y[train_index]
        test_y = y[test_index]
        grid = GridSearchCV(estimator, param_grid=param_grid, verbose=0, cv=cvFolds, scoring='neg_mean_squared_error')
        grid.fit(train_X,train_y)
        y_true, y_pred = test_y,grid.best_estimator_.predict(test_X)
        r2[cv_j] = r2_score(y_true, y_pred)
        cv_j = cv_j + 1
    return r2

def run_GC_script(inpath, GC_mode):
    data = readFile(inpath)

    X = data[:,2:data.shape[1]-1] #exclude the first column because it is the timestamp column
    y = data[:,data.shape[1]-1] # the target variable is the last column

    X1 = createAuto(y) #take the autocorrelation features
    X = np.concatenate((X,X1), axis=1)
    cvFolds = 5 #number of folds in cross-validation
    if(len(X[0])!=0): #check if there is at least one predictor
        start_time = time.perf_counter()    # as of Python 3.3, the use of time.clock() is deprecated, and it is recommended to use perf_counter() or process_time() instead
        if GC_mode == "non-linear":
            est = RandomForestRegressor(random_state=0, n_estimators=100, max_features='sqrt')
            R_squared_full = crossValidation(X, y, cvFolds, est)
            R_squared_baseline = crossValidation(X1, y, cvFolds, est)

        elif GC_mode == "linear":
            est = Ridge(copy_X=True, fit_intercept=True, max_iter=None, normalize=True, solver='lsqr', tol=0.001)
            R_squared_full = nestedCrossValidation(X, y, cvFolds, est)
            R_squared_baseline = nestedCrossValidation(X1, y, cvFolds, est)

        else:
            raise ValueError("The 2nd argument should be \'non-linear\' or \'linear\'")
    else:
        raise ValueError("Number of predictors is zero!")
    GC_dif = np.mean(R_squared_full) - np.mean(R_squared_baseline)
    return [np.mean(R_squared_baseline), np.mean(R_squared_full), GC_dif]
#   print ('%s Granger causality' %GC_mode)
#   print ("Explained variance of baseline model: %f" %np.mean(R_squared_baseline))
#   print ("Explained variance of full model: %f" %np.mean(R_squared_full))
#   print ("Quantification of Granger causality: %f" %GC_dif)
#   runtime = time.perf_counter() - start_time
#   print ("Total time: %d seconds" %runtime)

if __name__ == '__main__':
    #%% main script
    if len(sys.argv) < 3:
        raise ValueError('Two arguments are needed: inpath \'linear\'(or \'non-linear\')')
    inpath = sys.argv[1] # 1st arg, the file path
    GC_mode = sys.argv[2] #2nd arg, the mode "non-linear" or "linear"
    run_GC_script(inpath, GC_mode)
