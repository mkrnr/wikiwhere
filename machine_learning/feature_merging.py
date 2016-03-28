'''
Created on Feb 24, 2016

@author: Martin Koerner
'''

import argparse
import json
from utils import countries
from urlparse import urlparse

# generate help text for arguments
parser = argparse.ArgumentParser(description='Merges results from feature extraction JSON files into one CSV file')
parser.add_argument('--ip-location', dest='ip_location'
                   , help='JSON file containing URLs as keys and tuples with (lat,long) as values', type=str)
parser.add_argument('--tld-location', dest='tld_location'
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
parser.add_argument('--world-borders', dest='world_borders', type=str, required=True)
parser.add_argument('--empty-marker', dest='empty_marker', type=str, required=True)
parser.add_argument('--csv-delimiter', dest='csv_delimiter', type=str, required=True)

args = parser.parse_args()

csv_delimiter = args.csv_delimiter
empty_feature_marker = args.empty_marker

print "running feature_merging"

url_features_dictionary={}


def add_feature(url, feature_name, feature_value):
    if url not in url_features_dictionary:
        url_features_dictionary[url] = {}
    url_features_dictionary[url][feature_name] = feature_value


with open(args.article_to_urls) as json_input:    
    article_urls_dictionary = json.load(json_input)
    
# string for the header containing the feature names

used_features = []

if args.ip_location is not None:
    print "Merging ip-location"
    used_features.append("ip-location")
    with open(args.ip_location) as json_input:    
        json_data = json.load(json_input)
    
    for url in json_data:
        add_feature(url, "ip-location", json_data[url])

if args.tld_location is not None:
    print "merging tld-location"
    used_features.append("tld-location")
    with open(args.tld_location) as json_input:    
        json_data = json.load(json_input)
    
    for url in json_data:
        add_feature(url, "tld-location", json_data[url])
    
    
if args.website_language is not None:
    print "merging website-language"
    used_features.append("website-language")
    with open(args.website_language) as json_input:    
        json_data = json.load(json_input)
    
    for url in json_data:
        add_feature(url, "website-language", json_data[url])

    

if args.wikipedia_language is not None:
    print "merging wikipedia-language"
    used_features.append("wikipedia-language")
    with open(args.wikipedia_language) as json_input:    
        json_data = json.load(json_input)
    
    for article in json_data:
        if article in article_urls_dictionary:
            urls = article_urls_dictionary[article]
            for url in urls:
                add_feature(url, "wikipedia-language", json_data[article])
        
if args.wikipedia_location is not None:
    print "merging wikipedia-location"
    used_features.append("wikipedia-location")
    with open(args.wikipedia_location) as json_input:    
        json_data = json.load(json_input)
    
    for article in json_data:
        urls = article_urls_dictionary[article]
        if urls is None:
            print "article not found: " +  article
        else:
            for url in urls:
                add_feature(url, "wikipedia-location", json_data[article])
count_not_found = 0    
count_found = 0
if args.sparql_location is not None:
    print "merging sparql-location"
    used_features.append("sparql-location")
    with open(args.sparql_location) as json_input:    
        json_data = json.load(json_input)
    
    country_checker = countries.CountryChecker(args.world_borders)
    for url in url_features_dictionary:
        parsed_url = urlparse(str(url))
        stripped_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)
        if stripped_url in json_data:
            #country = country_lookup.get_country(json_data[stripped_url][0], json_data[stripped_url][1])
            country = country_checker.getCountry(countries.Point(json_data[stripped_url][0], json_data[stripped_url][1]))
            if (country is None):
                count_not_found += 1
                add_feature(url, "sparql-location", empty_feature_marker)
            else:
                count_found += 1
                add_feature(url, "sparql-location", country.iso)
        else:
            print "url not in dictionary: " + stripped_url

print "countries not found: "+ str(count_not_found)
print "countries found: "+ str(count_found)



# generate header string
header_string = "url" + csv_delimiter

for feature in used_features:
    header_string = header_string + feature + csv_delimiter

if header_string.endswith(csv_delimiter):
    header_string = header_string[:-1]

output_file = open(args.output,'w')
output_file.write(header_string+"\n") 

print "merging header: " + header_string

for url in url_features_dictionary:
    url_feature_string = url+csv_delimiter

    for feature in used_features:
        if feature in url_features_dictionary[url]:
            url_feature_string = url_feature_string+url_features_dictionary[url][feature]+csv_delimiter
        else:
            url_feature_string = url_feature_string+empty_feature_marker+csv_delimiter
    if url_feature_string.endswith(csv_delimiter):
        url_feature_string = url_feature_string[:-1]

    output_file.write(url_feature_string+"\n")


output_file.close() # you can omit in most cases as the destructor will call it

print "CSV file was stored successfully"