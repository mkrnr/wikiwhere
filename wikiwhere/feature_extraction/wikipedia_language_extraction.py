'''
Created on 03 Feb. 2016

@author: Tania Sennikova
'''

import urllib, json
import re
import pprint
import mwparserfromhell
from bz2 import BZ2File
import lxml.etree as ET
from langdetect import detect 
import argparse
from langdetect.lang_detect_exception import LangDetectException
from wikiwhere.utils import json_writer

class WikipediaLanguageExtraction(object):

    def get_namespace(self,inputfile_path):
        with BZ2File(inputfile_path) as xml_file:
            for line in xml_file:
            # add closing tag or lxml would complain 
                mediawiki_tag = ET.fromstring(line + "</mediawiki>")
                # get xmlns definition
                xmlns = mediawiki_tag.nsmap.get(None)
                break
        return "{" + xmlns + "}"
    
    def get_language(self,text):
        filtered_text = re.sub('\{.*?\}\}', '', text)
        filtered_text = re.sub('\[.*?\]\]', '', filtered_text)
        filtered_text = re.sub('<.*?>', '', filtered_text) 
        language = detect(filtered_text)
        return language
    
    def get_wikipedia_languages(self):
        article_language_dictionary={}
        
        # get the correct namespace from the xml file
        mediawiki_namespace = self.get_namespace(inputfile_path) 
        
        page_tag = mediawiki_namespace + "page"
        title_tag = mediawiki_namespace + "title"
        revision_tag = mediawiki_namespace + "revision"
        text_tag = mediawiki_namespace + "text"
        redirect_tag = mediawiki_namespace + "redirect"
        ns_tag = mediawiki_namespace + "ns"
        language = ""
        
        
        article_count=0
        article_not_detected_count=0
        
        with BZ2File(inputfile_path) as xml_file:
            context = ET.iterparse(xml_file, tag=page_tag)
        
            # iterate over the content of the page tags
            for action, elem in context:
                tree = ET.ElementTree(elem)
                page = tree.getroot()
            
                article_name = None
                namespace = None
                redirect = False
                language = None
        
                # iterate over the childs of page
                for child_of_page in page:
                                
                    # get title
                    if child_of_page.tag == title_tag:
                        article_name = child_of_page.text
        
                    # check namespace
                    if child_of_page.tag == ns_tag:
                        namespace = child_of_page.text
                        if namespace is "0":
                            article_count += 1
                        else:
                            break
        
                    # check if article is a redirect
                    if child_of_page.tag == redirect_tag:
                        redirect = True
                        break
            
                    # handle revision case 
                    if child_of_page.tag == revision_tag:
            
                        # iterate over childs of revision
                        for child_of_revision in child_of_page:
                            if child_of_revision.tag == text_tag: 
                                
                                if child_of_revision.text is not None:
                                    try:
                                        # extract external links from the text of the child
                                        language = self.get_language(child_of_revision.text)
                                    except LangDetectException:
                                        article_not_detected_count += 1
                                        break
        
                if namespace is "0" and redirect is False and article_name is not None and language is not None: 
                    article_language_dictionary[article_name] = language
                    #print article_language_dictionary
                
                # the following code fixes the memory problems with iterparse, see:
                # http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
        
                # It's safe to call clear() here because no descendants will be
                # accessed
                elem.clear()
                # Also eliminate now-empty references from the root node to elem
                for ancestor in elem.xpath('ancestor-or-self::*'):
                    while ancestor.getprevious() is not None:
                        del ancestor.getparent()[0]                         
        
            del context
        
        print "number of articles: " + str(article_count)
        print "number of undetected articles: " + str(article_not_detected_count)

if __name__ == '__main__':
    # generate help text for arguments
    parser = argparse.ArgumentParser(description='Extracts languages from a list of wikipedia articles given in the xml dump format.')
    parser.add_argument('input',
                       help='a file path to bz2 compressed XML dump input')
    parser.add_argument("--output", dest="output", metavar='output path', type=str, required=True)
    
    args = parser.parse_args()
    
    inputfile_path = args.input
    outputfile_path = args.output
    
    print "running wikipedia_language_extraction"
    
    wikipedia_language_extraction = WikipediaLanguageExtraction()
    wikipedia_language_dictionary = wikipedia_language_extraction.get_wikipedia_languages()
    json_writer.write_json_file(wikipedia_language_dictionary, outputfile_path)
