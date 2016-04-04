'''
Created on Apr 4, 2016

@author: Tania Sennikova
'''
from sklearn.externals import joblib
from numpy import loadtxt

class DoClassificcation:
    
    def __init__(self):
        self.models = {}
        self.mappings = {}
        languages = ["de", "fr"]
        for language in languages:
            self.models[language] = joblib.load('data/models/'+language+'wiki/'+language+'wiki.pkl') 
            text_file = open('data/preproc/'+language+'wiki-mapping.txt')
            self.mappings[language] = text_file.read().split()
    
    def classify(self, language, observation):
        clf = self.models[language]
        mapping = self.mappings[language]
        for i in range(0,len(observation)):
            observation[i]=mapping.index(observation[i])
        res=clf.predict(observation)
        return mapping[res]
        
if __name__ == '__main__':
    
    observation=['DE','AT','DE']
    do_classification = DoClassificcation()
    
    print do_classification.classify("de", observation)