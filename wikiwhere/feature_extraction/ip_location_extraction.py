'''
Created on Feb 21, 2016

@author: Martin Koerner <info@mkoerner.de>
'''

import geoip2.database
import socket
from urlparse import urlsplit
import json 

import argparse
from wikiwhere.utils import json_writer

class IPLocationExtraction(object):

    def __init__(self,database_path):
        # This creates a Reader object. You should use the same object
        # across multiple requests as creation of it is expensive.
        self.db_reader = geoip2.database.Reader(database_path)

    def get_ip_locations(self,json_data):
        url_location_dictionary = {}
        
        url_count = 0
        for article in json_data:
            for url in json_data[article]:
                url_count += 1
                if url in url_location_dictionary:
                    continue
                try:
                    ip = socket.gethostbyname(urlsplit(url).netloc)
        
                    response = self.db_reader.country(ip)
            
                    if response.country.iso_code is not None:
                        url_location_dictionary[url] = response.country.iso_code
                except socket.gaierror:
                    print "URL not found: " + url
                except geoip2.errors.AddressNotFoundError:
                    print "IP location not found: " + ip

        return url_location_dictionary
    

if __name__ == '__main__':
    # generate help text for arguments
    parser = argparse.ArgumentParser(description='Extracts locations (country ISO code) from the IP-address of URLs given a JSON file containing Wikipedia articles and URLs referenced by them')
    parser.add_argument('input',
                       help='a file path to the input JSON file')
    parser.add_argument("--output", dest="output", metavar='output path', type=str, required=True)
    parser.add_argument("--database", dest="database", metavar='path to mmdb country database', type=str, required=True)
    args = parser.parse_args()
    
    inputfile_path=args.input
    outputfile_path=args.output
    databse_path=args.database
    
    print "running ip_location_extraction"
    
    # load json input
    with open(inputfile_path) as json_input:    
        json_data = json.load(json_input)
    
    ip_location_extraction=IPLocationExtraction(databse_path)
    url_location_dictionary=ip_location_extraction.get_ip_locations(json_data)
    json_writer.write_json_file(url_location_dictionary, outputfile_path)
