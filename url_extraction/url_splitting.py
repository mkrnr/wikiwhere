'''
Created on 22.01.2016

@author: Florian, Martin Koerner <info@mkoerner.de>
'''
from urlparse import urlparse
import argparse
import json


# generate help text for arguments
parser = argparse.ArgumentParser(description='Extracts domains from a file containing the URLs of Wikipedia articles.')
parser.add_argument('input',
                   help='a file path to the output file generated by this program', required=True)
parser.add_argument("--output", dest="output", metavar='output path', type=str, required=True)
args = parser.parse_args()

inputfile_path = args.input
outputfile_path = args.output

article_domain_dictionary = {}

# load json input
with open(inputfile_path) as json_input:    
    json_data = json.load(json_input)

article_url_dictionary = {}

# iterate over Wikipedia articles
for article in json_data:
    urls = []
    for url in json_data[article]:
        parsed_url = urlparse(url)
        stripped_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)
        urls.append(stripped_url)
    article_url_dictionary[article] = urls

# write dictionary with key = Wikipedia article and value = URLs to JSON file
with open(outputfile_path, 'w') as f:
    json.dump(article_url_dictionary, f, indent=4, sort_keys=True)
    print "JSON file was stored successfully"
