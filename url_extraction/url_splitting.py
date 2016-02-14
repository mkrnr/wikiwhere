'''
Created on 22.01.2016

@@author: Florian
'''
import tldextract
import re
import io
import argparse


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Enter file containing wiki article name TAB number of sources TAB number of links TAB link TAB* and get the url split into subdomain, domain and suffix')
    parser.add_argument('input', nargs=1, type=str,  help='name of the inputfile with .txt ending')
    parser.add_argument('output', nargs=1, type=str, help='name of the outputfile with .txt ending')
    args = parser.parse_args()
    
    file_path = args.input[0]
    tldfile = io.open (file_path,'rb') #open file)
    
    out_name = args.output[0]
    tldout = open (out_name,"wb") #create output as of now the .txt will always be added
    
    lc = sum(1 for line in io.open(file_path,'rb'))#count lines for loop
    i=0 #initial index
    while (i<lc):   
        tldline = tldfile.readline()
        results = re.split(r'\t+', tldline) #split at tab using regular expression
        for l in range(len(results)):
            if (l < 3): #first three split parts article name & numbers
                tldout.write(results[l])  
                tldout.write("\n")
            else:
                #print(tldextract.extract(results[l])) #for control
                tldout.write(str(tldextract.extract(results[l]))) #cast to string ExtractResult object
                tldout.write("\n")
        i+=1 #increase index
    tldout.close()
    tldfile.close()