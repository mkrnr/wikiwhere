'''
Created on Feb 23, 2016

@author: Martin Koerner <info@mkoerner.de>
'''

import json


# Class for building a dictionary for looking up the Wikipedia article in which a given URL was referenced

class WikipediaURLLookup(object):

    url_article_dictionary = {}

    def __init__(self,json_file_path):
        # load JSON file
        with open(json_file_path) as data_file:    
            wikipedia_json = json.load(data_file)
        
        # populate dictionary
        for article in wikipedia_json:
            for url in wikipedia_json[article]:
                if url in self.url_article_dictionary:
                    self.url_article_dictionary[url].append(article)
                else:
                    articles=[]
                    articles.append(article)
                    self.url_article_dictionary[url]=articles
    
    def lookup(self,url):
        return self.url_article_dictionary[url]
    
