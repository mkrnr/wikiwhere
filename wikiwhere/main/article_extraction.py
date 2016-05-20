'''
Created on Apr 15, 2016

@author: Martin Koerner <info@mkoerner.de>
'''
from wikiwhere.feature_extraction.feature_collection import FeatureCollection
import argparse
from wikiwhere.url_extraction.wikipedia_api_url_extraction import WikipediaApiUrlExtraction
import collections
from wikiwhere.utils import json_writer
from wikiwhere.machine_learning.instance_classification import InstanceClassification

#create NamedTuple type for loading the world factbook data set
#load pickled data
Country = collections.namedtuple('Country', 'name, gec, iso2c, iso3c, isonum, stanag, tld')

class ArticleExtraction(object):

    def __init__(self,geodatabase_path,ianadatabase_path,wfbdatabase_path,model_data_path,languages):
        self.wikipedia_api_url_extraction=WikipediaApiUrlExtraction()
        self.feature_collection = FeatureCollection(geodatabase_path,ianadatabase_path,wfbdatabase_path)
        self.instance_classification = InstanceClassification(model_data_path,languages)
        self.languages = languages
    
    def parse_url(self,link):
        return self.wikipedia_api_url_extraction.parse_url(link)
    
    def collect_features(self,wikipedia_url):
        extracted_urls=self.wikipedia_api_url_extraction.extract_urls(wikipedia_url)
        collected_featues = {}
        extracted_urls_len = len(extracted_urls)
        extracted_urls_count = 0
        
        id_count = 0
        for extracted_url in extracted_urls:
            extracted_urls_count += 1
            print "extract URL " + str(extracted_urls_count)+" of "+str(extracted_urls_len)

            current_features = self.feature_collection.get_features("", extracted_url)
            current_features["url"] = extracted_url
            collected_featues[id_count] = current_features
            id_count += 1
        return collected_featues

    def add_predictions(self,language,collected_features):
        
        ids_to_be_removed = []
        for url_id in collected_features:
            observation = []
            
            if "ip-location" in collected_features[url_id]:
                observation.append(collected_features[url_id]["ip-location"])
            else:
                observation.append("NaN")

            if "tld-location" in collected_features[url_id]:
                observation.append(collected_features[url_id]["tld-location"])
            else:
                observation.append("NaN")

            if "website-language" in collected_features[url_id]:
                observation.append(collected_features[url_id]["website-language"].upper())
            else:
                observation.append("NaN")

            if language in self.languages:
                classification = self.instance_classification.classify(language, observation)
                if classification is None:
                    if url_id not in ids_to_be_removed:
                        ids_to_be_removed.append(url_id) 
                else:
                    collected_features[url_id]["classification"] = classification
                    
            classification_general = self.instance_classification.classify("general",observation)
            if classification_general is None:
                if url_id not in ids_to_be_removed:
                    ids_to_be_removed.append(url_id) 
            else:
                collected_features[url_id]["classification-general"] = classification_general

            collected_features[url_id]["wikipedia-language"] = language

        for url_to_be_removed in ids_to_be_removed:
            del collected_features[url_to_be_removed]

        return collected_features
    
    def fix_outliers(self, url_feature_dict, classification_id, fixed_classification_id, features):
        for feature_id in url_feature_dict:
            if classification_id in url_feature_dict[feature_id]:
                classification = url_feature_dict[feature_id][classification_id]
            else:
                continue

            feature_values = {}
            for feature in features:
                if feature in url_feature_dict[feature_id]:
                    feature_values[feature] = url_feature_dict[feature_id][feature]
                
            classification_in_features = False
            for feature_name in feature_values:
                if classification.lower() == feature_values[feature_name].lower():
                    classification_in_features = True

            if not classification_in_features:
                # take first element in feature list and use it
                if features[0] in feature_values:
                    url_feature_dict[feature_id][fixed_classification_id] = feature_values[features[0]]

            if fixed_classification_id not in url_feature_dict[feature_id]:
                url_feature_dict[feature_id][fixed_classification_id] = classification

        return url_feature_dict
                
             
                        
                 
        
    def get_as_array(self,url_feature_dict):
        url_feature_array = []
        
        for feature_id in url_feature_dict:
            dict_for_feature_id = {}

            for feature_name in url_feature_dict[feature_id]:
                dict_for_feature_id[feature_name] = url_feature_dict[feature_id][feature_name]
            
            url_feature_array.append(dict_for_feature_id)
        
        return url_feature_array

        
    

if __name__ == '__main__':
    # generate help text for arguments
    parser = argparse.ArgumentParser(description='Extracts URLs from a given wikipedia url and calls the feature collection functions for the urls')
    parser.add_argument('url',
                       help='a Wikipedia URL for which the features are calculated')
    parser.add_argument("--geodatabase", dest="geodatabase", help='path to mmdb country database', type=str, required=True)
    parser.add_argument("--world_fact_book_database", dest="world_fact_book_database", help='path to world fact book database', type=str, required=True)
    parser.add_argument("--IANA_database", dest="iana_database", help='path to IANA database', type=str, required=True)
    parser.add_argument("--model-data", dest="model_data", metavar='path to model-data-directory', type=str, required=True)
    parser.add_argument("--output", dest="output", help='output folder', type=str, required=True)
    args = parser.parse_args()
    
    geodatabase_path=args.geodatabase
    wfbdatabase_path=args.world_fact_book_database
    ianadatabase_path=args.iana_database
    model_data_path = args.model_data
    outputfile_path=args.output
    
    url = args.url

    languages = ["de", "en","es","fr","general","it","nl","sv","uk"]

    article_extraction = ArticleExtraction(geodatabase_path,ianadatabase_path,wfbdatabase_path,model_data_path,languages)
    
    language,title = article_extraction.parse_url(url)

    collected_features = article_extraction.collect_features(url)
    #collected_features_with_prediction = article_extraction.add_predictions(language,collected_features)
    #json_writer.write_json_file(collected_features_with_prediction, outputfile_path+"/"+language+"-"+title+".json")
    json_writer.write_json_file(collected_features, outputfile_path+"/"+language+"-"+title+".json")

