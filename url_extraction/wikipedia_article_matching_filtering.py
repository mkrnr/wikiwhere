'''
Created on Mar 9, 2016

@author: Martin Koerner <info@mkoerner.de>
'''

import json

from urlparse import urlparse
import argparse

# generate help text for arguments
parser = argparse.ArgumentParser(description='Extracts domains from a file containing the URLs of Wikipedia articles.')
parser.add_argument('input',
                   help='JSON file containing wikipedia articles and their links')
parser.add_argument("--matches", dest="matches", help='JSON file containing matchings if URLs and their location extracted from dbpedia', type=str, required=True)
parser.add_argument("--output", dest="output", help='output path', type=str, required=True)
args = parser.parse_args()

inputfile_path = args.input
matchesfile_path = args.matches
outputfile_path = args.output

print "running wikipedia_article_matching_filtering"

# load json input
with open(inputfile_path) as json_input:    
    wikipedia_data = json.load(json_input)

# load json input
with open(matchesfile_path) as json_matches:    
    matches_data = json.load(json_matches)

# get list of matched urls

matched_urls = []
for url in matches_data:
    matched_urls.append(url)
    
filtered_article_url_dictionary = {}

# iterate over Wikipedia articles and selected the filtered articles
for article in wikipedia_data:
    filtered_urls = []
    for url in wikipedia_data[article]:
        parsed_url = urlparse(url)
        stripped_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)
        if stripped_url in matched_urls:
            filtered_urls.append(url)
    if len(filtered_urls)>0:
        filtered_article_url_dictionary[article] = filtered_urls
        
# write dictionary with key = Wikipedia article and value = URLs to JSON file
with open(outputfile_path, 'w') as f:
    json.dump(filtered_article_url_dictionary, f, indent=4, sort_keys=True)
    print "JSON file was stored successfully"


