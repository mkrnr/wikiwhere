'''
Created on Mar 31, 2016

@author: Tania Sennikova
'''
import pandas as pd
import csv
import numpy as np
from numpy import recfromcsv
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm, cross_validation
from sklearn.preprocessing import Imputer
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import ShuffleSplit
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.externals import joblib

# Read Dataset
dataset = pd.read_csv('data/preproc/dewiki-preproc.csv')
y = dataset['sparql-location']
X = dataset
del X['sparql-location']
#del X['website-language']

# NaN Handling
imputer = Imputer(missing_values='NaN', strategy='most_frequent', axis=1)
X=imputer.fit_transform(X, y)

print 'NaN in X: ', np.any(np.isnan(X))
print 'NaN in Y: ',np.any(np.isnan(y))

# Splitting
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

# SVM
estimator = svm.SVC(decision_function_shape='ovo')
svm_model=estimator.fit(X,y)
#joblib.dump(estimator, 'data/models/dewiki/dewiki.pkl') 
print 'SVM = ',svm_model.score(X, y)
# For testing
#pred_decision=estimator.predict(X_test)
#print 'SVM classes true',y_test
#print 'SVM classes predicted',pred_decision

# Cross validation
# cv = ShuffleSplit(X_train.shape[0], n_iter=10, test_size=0.2, random_state=0)
# gammas = np.logspace(-6, -1, 10)
# classifier = GridSearchCV(estimator=estimator, cv=cv, param_grid=dict(gamma=gammas))
# classifier.fit(X_train, y_train)
# print 'SVM = ', classifier.score(X_test, y_test) 



# Regression
model = LogisticRegression(solver='lbfgs', multi_class='multinomial')
lr_model = model.fit(X_train, y_train)
print 'LR = ', lr_model.score(X,y)

# K-NN
neigh = KNeighborsClassifier(n_neighbors=3, weights='distance')
knn_model=neigh.fit(X_train, y_train)
print 'KNN = ',knn_model.score(X,y)

