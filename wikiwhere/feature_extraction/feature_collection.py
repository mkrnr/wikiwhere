'''
Created on Apr 4, 2016

@author: martin
'''
from wikiwhere.feature_extraction.ip_location_extraction import IPLocationExtraction
from wikiwhere.feature_extraction.tld_location_extraction import TLDLocationExtraction
from wikiwhere.feature_extraction.website_language_extraction import WebsiteLanguageExtraction
import json
import argparse
import collections


#create NamedTuple type for loading the world factbook data set
#load pickled data
Country = collections.namedtuple('Country', 'name, gec, iso2c, iso3c, isonum, stanag, tld')

class FeatureCollection(object):

    def __init__(self,geodatabase_path,ianadatabase_path,wfbdatabase_path):
        self.ip_location_extraction = IPLocationExtraction(geodatabase_path)
        self.tld_location_extraction = TLDLocationExtraction(ianadatabase_path, wfbdatabase_path)
        self.website_language_extraction = WebsiteLanguageExtraction()
        

    def get_features(self, article_name, url):

        #generate json from article_name and url
        article_url_dictionary = {}
        urls = []
        urls.append(url)
        article_url_dictionary[article_name] = urls
        json_data = json.loads(json.dumps(article_url_dictionary))

        features = {}
        try:
            ip_locations = self.ip_location_extraction.get_ip_locations(json_data)
            tld_locations = self.tld_location_extraction.get_tld_locations(json_data)
            website_languages = self.website_language_extraction.get_website_languages(json_data)

            if url in ip_locations:
                features["ip-location"] = ip_locations[url]
            if url in tld_locations:
                features["tld-location"] = tld_locations[url]
            if url in website_languages:
                features["website-language"] = website_languages[url]
        except Exception as exception:
            print "Continue after " + exception.__class__.__name__ + " for URL: " + url
        return features
    
if __name__ == '__main__':
    # generate help text for arguments
    parser = argparse.ArgumentParser(description='Calls the feature collection functions for a given URL')
    parser.add_argument('url',
                       help='an URL for which the features are calculated')
    parser.add_argument("--geodatabase", dest="geodatabase", help='path to mmdb country database', type=str, required=True)
    parser.add_argument("--world_fact_book_database", dest="world_fact_book_database", help='path to world fact book database', type=str, required=True)
    parser.add_argument("--IANA_database", dest="iana_database", help='path to IANA database', type=str, required=True)
    args = parser.parse_args()
    
    geodatabase_path=args.geodatabase
    wfbdatabase_path=args.world_fact_book_database
    ianadatabase_path=args.iana_database
    
    url = args.url

    feature_collection = FeatureCollection(geodatabase_path,ianadatabase_path,wfbdatabase_path)
    features = feature_collection.get_features("test", url)
    print features



