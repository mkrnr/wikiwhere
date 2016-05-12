'''
Created on Feb 4, 2016

@author: Martin Koerner <info@mkoerner.de>
'''

def language_to_dbpedia_url(argument):
    known_languages=['ar', 'eu','cs','nl','eo','fr','de','el','id','it','ja','ko','pl','pt','ru','es','sv','uk']
    if argument in known_languages:
        url = 'http://{0}.dbpedia.org/sparql'.format(argument)
    else:
        url= 'http://dbpedia.org/sparql'    
    return url
