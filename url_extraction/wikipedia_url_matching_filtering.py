'''
Created on Mar 9, 2016

@author: Martin Koerner <info@mkoerner.de>
'''

import json

from urlparse import urlparse
import argparse
import re

# generate help text for arguments
parser = argparse.ArgumentParser(description='Extracts domains from a file containing the URLs of Wikipedia articles.')
parser.add_argument('input',
                   help='CSV file containing wikipedia articles and their links')
parser.add_argument("--matches", dest="matches", help='JSON file containing matchings if URLs and their location extracted from dbpedia', type=str, required=True)
parser.add_argument("--output", dest="output", help='output path', type=str, required=True)
args = parser.parse_args()

inputfile_path = args.input
matchesfile_path = args.matches
outputfile_path = args.output

print "running wikipedia_article_matching_filtering"

# load json input
wikipedia_reader = open(inputfile_path, 'r')

# load json input
with open(matchesfile_path) as json_matches:    
    matches_data = json.load(json_matches)

# get list of matched urls
matched_urls = set()
for url in matches_data:
    matched_urls.add(url)
    
filtered_article_url_dictionary = {}

url_error_count = 0
# iterate over Wikipedia articles and selected the filtered articles
with open(inputfile_path, "r") as ins:
    for line in ins:
        line_split = re.split(r'\t+', line)
        filtered_urls = []
        iter_line = iter(line_split)
        article_name = next(iter_line)
        for url in iter_line:
            # remove trailing new lines
            url=url.rstrip()
            try:
                parsed_url = urlparse(url)
                stripped_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)
                if stripped_url in matched_urls:
                    filtered_urls.append(url)
            except ValueError:
                url_error_count += 1
                print "ValueError while parsing URL for: " + url
                
        if len(filtered_urls)>0:
            filtered_article_url_dictionary[article_name] = filtered_urls

print "URLs with error: " + str(url_error_count)

# write dictionary with key = Wikipedia article and value = URLs to JSON file
with open(outputfile_path, 'w') as f:
    json.dump(filtered_article_url_dictionary, f, indent=4, sort_keys=True)
    print "JSON file was stored successfully"
