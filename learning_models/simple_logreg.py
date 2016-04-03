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
from astropy.units import liter
from sklearn.preprocessing import Imputer

dataset = pd.read_csv('data/preproc/dewiki-preproc.csv')



y = dataset['sparql-location']
X = dataset
del X['sparql-location']

imputer = Imputer(missing_values='NaN', strategy='most_frequent', axis=1)
X=imputer.fit_transform(X, y)

print np.any(np.isnan(X))
print np.any(np.isnan(y))

model = LogisticRegression()
model = model.fit(X, y)
print model.score(X, y)


# import numpy as np
# import pandas as pd
# import statsmodels as sm
# import matplotlib.pyplot as plt
# import patsy
# from patsy import dmatrices
# from sklearn.linear_model import LogisticRegression
# from sklearn.cross_validation import train_test_split
# from sklearn import metrics
# from sklearn.cross_validation import cross_val_score
# 
# dataset = pd.read_csv('data/dewiki-merge.csv')
# y, X = dmatrices('sparql_location ~ ip_location + tld_location + website_language + sparql_location', dataset, return_type="dataframe")
# print X.columns

