'''
Created on Jan 11, 2016

@author: Martin Koerner, Tatiana Sennikova
'''


from SPARQLWrapper import SPARQLWrapper, JSON
from SPARQLWrapper.SPARQLExceptions import QueryBadFormed
import json
import argparse
from wikiwhere.utils import dbpedia_mapping, country_lookup, majority_voting, json_writer
import urllib2
import socket


class WikipediaLocationExtraction(object):

    def __init__(self,language):
        # initialize sparql querier
        # get mapping from two-letter country code to dbpedia endpoint URL
        dbpedia_url = dbpedia_mapping.language_to_dbpedia_url(language) 
        self.sparql = SPARQLWrapper(dbpedia_url)
        self.sparql.setTimeout(1000)
        self.sparql.setReturnFormat(JSON)

    # Convert coordinates to decimals
    def dms2dd(self,degrees, minutes, seconds, direction):
        dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
        if direction == 'S' or direction == 'W':
            dd *= -1
        return dd
    
    def query_location(self,article):
        
        article_url = '<http://'+ language + '.wikipedia.org/wiki/'+article + '>'
        location = None
            
            
        # SPARQL query that 
        namespaces = """
        PREFIX dbo: <http://dbpedia.org/resource/classes#>
        PREFIX dbp: <http://dbpedia.org/property/>
        """
            
        location_query = """        
        {
            SELECT * WHERE {
                ?match dbp:latitude ?lat .
                ?match dbp:longitude ?long
            }
        }
        UNION
        {
            SELECT * WHERE {
                ?match geo:lat ?lat .
                ?match geo:long ?long
            }
        }
        UNION
        {
            SELECT * WHERE {
                ?match dbp:latDeg ?latDeg .
                ?match dbp:latMin ?latMin .
                ?match dbp:latSec ?latSec .
                ?match dbp:lonDeg ?lonDeg .
                ?match dbp:lonMin ?lonMin .
                ?match dbp:lonSec ?lonSec
            }
        }
        UNION
        {
            SELECT * WHERE {
                ?match dbp:latDeg ?latDeg .
                ?match dbp:latMin ?latMin .
                ?match dbp:latSec ?latSec .
                ?match dbp:lonDeg ?lonDeg .
                ?match dbp:lonMin ?lonMin .
                ?match dbp:lonSec ?lonSec .
                ?match dbp:latDir ?latDir .
                ?match dbp:lonDir ?lonDir
            }
        }
        UNION
        {
            SELECT * WHERE {
                ?match dbp:latDegrees ?latDeg .
                ?match dbp:latMinutes ?latMin .
                ?match dbp:latSeconds ?latSec .
                ?match dbp:longDegrees ?lonDeg .
                ?match dbp:longMinutes ?lonMin .
                ?match dbp:longSeconds ?lonSec .
                ?match dbp:latDirection ?latDir .
                ?match dbp:longDirection ?lonDir
    
            }
        }
    
    
        UNION
        {
            SELECT * WHERE {
                ?match dbp:latd ?lat .
                ?match dbp:longd ?long
            }
        }
                
        """
        query_string = namespaces + """
        SELECT * WHERE {
            ?match foaf:isPrimaryTopicOf """+article_url+""" .
            """+location_query+"""
        }
        """
                
        query_string_with_offset = query_string 
            
        self.sparql.setQuery(query_string_with_offset)
    
        try:
            results = self.sparql.query().convert()
        except QueryBadFormed:
            print "SPARQL query bad formed: " + query_string_with_offset
            return None
        except urllib2.HTTPError:
            print "HTTP Error 502: " + article
            return None
        except urllib2.URLError:
            print "Network is unreachable while working on: " + article
            return None
        except socket.timeout:
            print "Query timed out for: " + article
            return None
            
            
        if len(results["results"]["bindings"]) > 0:
            coordinates_array = []
            for result in results["results"]["bindings"]:
                if  "lat" in result:
                    latitude = result["lat"]["value"]
                    longitude = result["long"]["value"]
                else:
                    lat_dir=0
                    if "latDir" in result:
                        lat_dir = result["latDir"]["value"]
                    
                    latitude = self.dms2dd(result["latDeg"]["value"], result["latMin"]["value"], result["latSec"]["value"], lat_dir)
                    longitude = self.dms2dd(result["lonDeg"]["value"], result["lonMin"]["value"], result["lonSec"]["value"], lat_dir)
    
                latitude = float(latitude)
                longitude = float(longitude)
                coordinates_array.append((latitude,longitude))
    
            majority_vote =  majority_voting.vote(coordinates_array,threshold)
            location = country_lookup.get_country(majority_vote[0],majority_vote[1])
            
        return location

    def get_wikipedia_languages(self,json_data):
        article_language_dictionary={}        
        
        article_count = 0
        # Main loop
        for article in json_data:
            article_with_underscores = article.replace(' ', '_')
            location = self.query_location(article_with_underscores)
            if location is not None:
                # print article + " --> " +location
                article_language_dictionary[article] = location
            
            article_count += 1
            
            # print article_count

if __name__ == '__main__':
    # generate help text for arguments
    parser = argparse.ArgumentParser(description='Extracts geo locations from a list of wikipedia articles given in JSON.')
    parser.add_argument('input',
                               help='a file path to a JSON file containing wikipedia article names')
    parser.add_argument("--output", dest="output", metavar='output path', type=str)
    parser.add_argument("--language", dest="language", metavar='two-letter country code', type=str, help="on of the language editions of dbpedia (default: en):", required=True)
    parser.add_argument("--threshold", dest="threshold", metavar='threshold for majority voting', type=float, help="absolute threshold for majority voting on coordinates (default: 0.1)", required=True)
            
    args = parser.parse_args()
            
    inputfile_path=args.input
    outputfile_path=args.output
    language = args.language
    threshold = args.threshold
    
    # load json input
    with open(inputfile_path) as json_input:    
        json_data = json.load(json_input)

    print "running wikipedia_location_extraction"

    wikipedia_location_extraction = WikipediaLocationExtraction(language)
    article_url_dictionary = wikipedia_location_extraction.get_wikipedia_languages(json_data)
    json_writer.write_json_file(article_url_dictionary, outputfile_path)
