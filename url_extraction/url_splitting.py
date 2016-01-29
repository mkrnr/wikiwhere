'''
Created on 22.01.2016

@@author: Florian
'''
import tldextract
import re
import io
import tkFileDialog as filedialog
if __name__ == '__main__':

    file_path = filedialog.askopenfilename()
    tldfile = io.open (file_path,'rb') #open file)
    out_name = filedialog.asksaveasfilename()
    tldout = open (str(out_name)+".txt","wb") #create output as of now the .txt will always be added
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