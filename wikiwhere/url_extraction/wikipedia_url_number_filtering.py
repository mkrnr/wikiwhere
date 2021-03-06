'''
Created on Mar 7, 2016

@author: Martin Koerner <info@mkoerner.de>
'''

import json

import argparse
from random import shuffle

# generate help text for arguments
parser = argparse.ArgumentParser(description='Extracts a predefined number of URLs from a JSON file containing wikipedia article names as key and urls as value')
parser.add_argument('input',
                   help='a file path to the output file generated by this program')
parser.add_argument("--output", dest="output", help='output path', type=str, required=True)
parser.add_argument("--number", dest="number", help='articles to filter out', type=int, required=True)
args = parser.parse_args()

inputfile_path = args.input
outputfile_path = args.output
number_of_urls = args.number


print "running wikipedia_url_number_filtering"

# load json input
with open(inputfile_path) as json_input:    
    json_data = json.load(json_input)

article_url_tuples = []
# get list of wikipedia article names
for article in json_data:
    for url in json_data[article]:
        article_url_tuples.append((article,url))

shuffle(article_url_tuples)

sliced_article_url_tuples=article_url_tuples[:number_of_urls]

article_url_dictionary = {}

for tup in sliced_article_url_tuples:
    if tup[0] in article_url_dictionary:
        article_url_dictionary[tup[0]].append(tup[1])
    else:
        urls = []
        urls.append(tup[1])
        article_url_dictionary[tup[0]] = urls

# write dictionary with key = Wikipedia article and value = URLs to JSON file
with open(outputfile_path, 'w') as f:
    json.dump(article_url_dictionary, f, indent=4, sort_keys=True)
    print "JSON file was stored successfully"


