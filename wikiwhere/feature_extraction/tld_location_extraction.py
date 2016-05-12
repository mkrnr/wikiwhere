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
from tld.exceptions import TldDomainNotFound, TldBadUrl
from wikiwhere.utils import json_writer


#create NamedTuple type for loading the world factbook data set
#load pickled data
Country = collections.namedtuple('Country', 'name, gec, iso2c, iso3c, isonum, stanag, tld')

class TLDLocationExtraction(object):

    def __init__(self,ianadatabse_path,wfbdatabse_path):
        self.iana = pickle.load(open(ianadatabse_path, "rb"))
        self.wfb = pickle.load(open(wfbdatabse_path, "rb" ))

    def get_tld_locations(self,json_data):
        url_location_dictionary = {}
    
        url_count = 0
        for article in json_data:
            for url in json_data[article]:
                url_count += 1
                #split url and get suffix
                try:
                    res = get_tld(url, as_object=True)
                except TldDomainNotFound:
                    print "tld not found: "+ str(url)
                    continue
                except TldBadUrl:
                    print "bad url: "+ str(url)
                    continue
                tld = res.suffix
                #check suffix for combination and get only last part if necessary, after the dot needs to be added in front for
                if (tld.count(".") > 0):
                    results = re.split(r'\.', tld)
                    tld = results[len(results)-1]
                tld ="."+tld
                
                #print tld
                try:
                    if (self.iana[tld] == 'country-code'):
                        for w in self.wfb:
                            if w.tld == tld:
                                url_location_dictionary[url]= w.iso2c
                    else:
                        url_location_dictionary[url]= tld.replace(".",'').upper() 
                except KeyError:
                    print "no entry found for: "+ str(tld)

        return url_location_dictionary

if __name__ == '__main__':
    # generate help text for arguments
    parser = argparse.ArgumentParser(description='Extracts locations (country ISO code) from the top-level domains of URLs given a JSON file containing Wikipedia articles and URLs referenced by them')
    parser.add_argument('input', help='a file path to the input JSON file')
    parser.add_argument("--output", dest="output", metavar='output path', type=str, required=True)
    parser.add_argument("--world_fact_book_database", dest="world_fact_book_database", metavar='path to world fact book database', type=str, required=True)
    parser.add_argument("--IANA_database", dest="iana_database", metavar='path to IANA database', type=str, required=True)
    args = parser.parse_args()
    
    inputfile_path=args.input
    outputfile_path=args.output
    wfbdatabase_path=args.world_fact_book_database
    ianadatabase_path=args.iana_database
    
    print "running tld_location_extraction"
    
    # load json input
    with open(inputfile_path) as json_input:    
        json_data = json.load(json_input)
    
    tld_location_extraction = TLDLocationExtraction(ianadatabase_path,wfbdatabase_path)
    url_location_dictionary = tld_location_extraction.get_tld_locations(json_data)
    json_writer.write_json_file(url_location_dictionary, outputfile_path)
