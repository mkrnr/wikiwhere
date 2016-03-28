'''
Created on 08.02.2016

@author: Florian
'''


import re
import collections
import pickle
from tld import get_tld
import json 
import argparse
from tld.exceptions import TldDomainNotFound

#create NamedTuple type for loading the world factbook data set
Country = collections.namedtuple('Country', 'name, gec, iso2c, iso3c, isonum, stanag, tld')

# generate help text for arguments
parser = argparse.ArgumentParser(description='Extracts locations (country ISO code) from the top-level domains of URLs given a JSON file containing Wikipedia articles and URLs referenced by them')
parser.add_argument('input', help='a file path to the input JSON file')
parser.add_argument("--output", dest="output", metavar='output path', type=str, required=True)
parser.add_argument("--world_fact_book_database", dest="world_fact_book_database", metavar='path to world fact book database', type=str, required=True)
parser.add_argument("--IANA_database", dest="iana_database", metavar='path to IANA database', type=str, required=True)
args = parser.parse_args()

inputfile_path=args.input
outputfile_path=args.output
wfbdatabse_path=args.world_fact_book_database
ianadatabse_path=args.iana_database

print "running tld_location_extraction"

# load json input
with open(inputfile_path) as json_input:    
    json_data = json.load(json_input)
#load pickled data
iana = pickle.load(open(ianadatabse_path, "rb"))
wfb = pickle.load(open(wfbdatabse_path, "rb" ))

tld_location_dictionary = {}

url_count = 0
for article in json_data:
    for url in json_data[article]:
        url_count += 1
        #split url and get suffix
        try:
            res = get_tld(url, as_object=True)
        except TldDomainNotFound:
            print "tld not found: "+ str(res)
        tld = res.suffix
        #check suffix for combination and get only last part if necessary, after the dot needs to be added in front for
        if (tld.count(".") > 0):
            results = re.split(r'\.', tld)
            tld = results[len(results)-1]
        tld ="."+tld
        
        #print tld
        try:
            if (iana[tld] == 'country-code'):
                for w in wfb:
                    if w.tld == tld:
                        tld_location_dictionary[url]= w.iso2c
            else:
                tld_location_dictionary[url]= tld.replace(".",'').upper() 
        except KeyError:
            print "no entry found for: "+ str(tld)
# write results to a JSON file
with open(outputfile_path, 'w') as f:
    json.dump(tld_location_dictionary, f, indent=4, sort_keys=True)
    print "File was stored successfully"
                    