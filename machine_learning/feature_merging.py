'''
Created on Feb 24, 2016

@author: Martin Koerner
'''

import argparse
import json
from utils import country_lookup

# generate help text for arguments
parser = argparse.ArgumentParser(description='Merges results from feature extraction JSON files into one CSV file')
parser.add_argument('--ip-location', dest='ip_location'
                   , help='JSON file containing URLs as keys and tuples with (lat,long) as values', type=str)
parser.add_argument('--website-language', dest='website_language'
                   , help='JSON file containing URLs as keys and language iso codes as values', type=str)
parser.add_argument('--wikipedia-language', dest='wikipedia_language'
                   , help='JSON file containing Wikipedia article names as keys and language iso codes as values', type=str)
parser.add_argument('--wikipedia-location', dest='wikipedia_location'
                   , help='JSON file containing URLs as keys and tuples with (lat,long) as values', type=str)
parser.add_argument('--sparql-location', dest='sparql_location'
                   , help='JSON file containing URLs as keys and tuples with (lat,long) as values', type=str)
parser.add_argument('--article-to-url', dest='article_to_urls', metavar='JSON file containing Wikipedia articles as key and references URLs as values', type=str, required=True)
parser.add_argument('--output', dest='output', metavar='output path for the merged CSV file', type=str, required=True)

args = parser.parse_args()

url_features_dictionary={}


def add_feature(url, feature_name, feature_value):
    if url not in url_features_dictionary:
        url_features_dictionary[url] = {}
    url_features_dictionary[url][feature_name] = feature_value


with open(args.article_to_urls) as json_input:    
    article_urls_dictionary = json.load(json_input)

if args.ip_location is not None:
    print "Merging ip-location"
    with open(args.ip_location) as json_input:    
        json_data = json.load(json_input)
    
    for url in json_data:
        add_feature(url, "ip-location", json_data[url])
    
    
if args.website_language is not None:
    print "Merging website-language"
    with open(args.website_language) as json_input:    
        json_data = json.load(json_input)
    
    for url in json_data:
        add_feature(url, "website-language", json_data[url])
    

if args.wikipedia_language is not None:
    print "Merging wikipedia-language"
    with open(args.wikipedia_language) as json_input:    
        json_data = json.load(json_input)
    
    for article in json_data:
        urls = article_urls_dictionary[article]
        if urls is None:
            print "article not found: " +  article
        else:
            for url in urls:
                add_feature(url, "wikipedia-language", json_data[article])
        
    
if args.sparql_location is not None:
    print "Merging sparql-location"
    with open(args.sparql_location) as json_input:    
        json_data = json.load(json_input)
    
    for url in json_data:
        country = country_lookup.get_country(json_data[url][0], json_data[url][1])
        add_feature(url, "sparql-location", country)

    
#for url in url_features_dictionary:
#    for feature in url_features_dictionary[url]:
#        print url + " -- "+ feature + " --> " + url_features_dictionary[url][feature]


#country = country_lookup.get_country("52.509669","13.376294")
#country_iso=pycountry.countries.get(name=country)
#print country.lower()