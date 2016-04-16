'''
Created on Apr 15, 2016

@author: Martin Koerner <info@mkoerner.de>
'''
from feature_extraction.feature_collection import FeatureCollection
import argparse
from url_extraction.wikipedia_api_url_extraction import WikipediaApiUrlExtraction
import collections
from utils import json_writer
from machine_learning.instance_classification import InstanceClassification

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
        for extracted_url in extracted_urls:
            extracted_urls_count += 1
            print "extract URL " + str(extracted_urls_count)+" of "+str(extracted_urls_len)
            if extracted_url not in collected_featues:
                current_features = self.feature_collection.get_features("", extracted_url)
                collected_featues[extracted_url]=current_features
        return collected_featues

    def add_predictions(self,wikipedia_language,collected_features):
        for extracted_url in collected_features:
            observation = []

            if "ip-location" in collected_features[extracted_url]:
                observation.append(collected_features[extracted_url]["ip-location"])
            else:
                observation.append("NaN")

            if "tld-location" in collected_features[extracted_url]:
                observation.append(collected_features[extracted_url]["tld-location"])
            else:
                observation.append("NaN")

            if "website-language" in collected_features[extracted_url]:
                observation.append(collected_features[extracted_url]["website-language"].upper())
            else:
                observation.append("NaN")

            if language in self.languages:
                collected_features[extracted_url]["classification"] = self.instance_classification.classify(language, observation)
            
            collected_features[extracted_url]["classification-general"] = self.instance_classification.classify("general",observation)

            collected_features[extracted_url]["wikipedia-language"] = language

        return collected_features

        
    

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

