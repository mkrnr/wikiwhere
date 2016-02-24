'''
Created on Jan 29, 2016

@author: Martin Koerner <info@mkoerner.de>
'''

# https://github.com/Mimino666/langdetect
from langdetect import detect 
from bs4 import BeautifulSoup

import json
import urllib
import argparse

# generate help text for arguments
parser = argparse.ArgumentParser(description='Extracts languages from the content of URLs given in a JSON file that contains Wikipedia articles and their referenced URLs')
parser.add_argument('input',
                   help='a file path to the JSON input file', required=True)
parser.add_argument("--output", dest="output", metavar='output path', type=str, required=True)
args = parser.parse_args()

inputfile_path=args.input
outputfile_path=args.output

url_language_dictionary = {}

for line in open(inputfile_path,'r'):
    url=line.rstrip('\n')

    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)
    html_body = soup.body.get_text(" ")
    language=detect(html_body)
    print line+" --> "+language


    url_language_dictionary[url] = language


# write results to a JSON file
with open(outputfile_path, 'w') as f:
    json.dump(url_language_dictionary, f, indent=4, sort_keys=True)
    print "File was stored successfully"