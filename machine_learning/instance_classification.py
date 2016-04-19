'''
Created on Apr 4, 2016

@author: Tania Sennikova
'''
from sklearn.externals import joblib
import argparse
import copy

class InstanceClassification:
    
    def __init__(self,model_data_path,languages):
        self.models = {}
        self.mappings = {}
        for language in languages:
            self.models[language] = joblib.load(model_data_path+'/models/'+language+'wiki/'+language+'wiki.pkl') 
            text_file = open(model_data_path+'/preproc/'+language+'wiki-mapping.txt')
            self.mappings[language] = text_file.read().split()
    
    def classify(self, language, observation):
        #print observation
        clf = self.models[language]
        mapping = self.mappings[language]
        mapped_observation = []
        for i in range(0,len(observation)):
            if observation[i] in mapping:
                mapped_observation.append(mapping.index(observation[i]))
            else:
                mapped_observation.append(mapping.index("NaN"))
        #print mapped_observation
        res=clf.predict(mapped_observation)
        return mapping[res[0]]
        
if __name__ == '__main__':
        # generate help text for arguments
    parser = argparse.ArgumentParser(description='Classifies a given observation using the trained models')
    # TODO change input
    parser.add_argument('input',
                       help='a file path to the input JSON file')
    parser.add_argument("--model-data", dest="model_data", metavar='path to model-data-directory', type=str, required=True)
    args = parser.parse_args()
    
    model_data_path = args.model_data

    observation=['RU','RU','SL']
    #observation=['DE','AT','DE']

    languages = ["de", "en","es","fr","general","it","nl","sv","uk"]
    instance_classification = InstanceClassification(model_data_path,languages)
    
    print instance_classification.classify("general", observation)
    #print instance_classification.classify("de", observation)