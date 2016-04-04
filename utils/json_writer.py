'''
Created on Apr 4, 2016

@author: martin
'''
import json

def write_json_file(json_object,outputfile_path):
    # write results to a JSON file
    with open(outputfile_path, 'w') as f:
        json.dump(json_object, f, indent=4, sort_keys=True)
        print "File was stored successfully"