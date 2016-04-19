'''
Created on Apr 3, 2016

@author: Tania
'''
import pandas as pd
import csv
import numpy as np
def all_same(items):
    return all(x == items[0] for x in items)

# Create some toy data in a Pandas dataframe
with open ('data/dewiki-merge.csv') as csvfile:
    dataset = csv.reader(csvfile)
    first_row = next(dataset)
    num_cols = len(first_row)
    data = list(dataset)

unique_set=[]
new_set=[]
decoded_data=[]
for row in data:
    for i in range(0,num_cols): 
        if row[i] not in unique_set:
            unique_set.append(row[i])
nan_value=unique_set.index("NaN")
print unique_set
for i in data:
    if not all_same(i):
        #print i
        for j in i:
            if j in unique_set:
                if j!="NaN":
                    new_set.append(unique_set.index(j))
                if j=="NaN":
                    new_set.append(np.nan)
        #print new_set
        decoded_data.append(new_set) 
        new_set=[]

with open("data/preproc/dewiki-preproc.csv", "wb") as f:
    writer = csv.writer(f,  delimiter=',')
    writer.writerow(["ip-location", "tld-location", "website-language", "sparql-location"])
    writer.writerows(decoded_data)

text_file=open("data/preproc/dewiki-mapping.txt", "w")
for item in unique_set:
  text_file.write("%s\n" % item)
text_file.close()
