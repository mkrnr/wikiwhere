'''
Created on 03 Feb. 2016

@author: Tania Sennikova
'''

import urllib, json
import re
import pprint
import mwparserfromhell
#import xml.etree.ElementTree as ET
import urllib, json
import lxml.etree as ET
from langdetect import detect 

file_path="Data/enwiki-20131001-pages-articles-first-500-articles.xml"
dump={}

def get_namespace(file_path):
    input_file = open(file_path, 'r') 
    for line in input_file:
        # add closing tag or lxml would complain 
        mediawiki_tag = ET.fromstring(line + "</mediawiki>")
        # get xmlns definition
        xmlns = mediawiki_tag.nsmap.get(None)
        break;
    return "{" + xmlns + "}"

def get_language(text):
    filtered_text=re.sub('\{.*?\}\}', '', text)
    filtered_text=re.sub('\[.*?\]\]', '', filtered_text)
    filtered_text=re.sub('<.*?>', '', filtered_text) 
    lang=detect(filtered_text)
    return lang


# get the correct namespace from the xml file
mediawiki_namespace = get_namespace(file_path) 

page_tag = mediawiki_namespace + "page"
title_tag = mediawiki_namespace + "title"
revision_tag = mediawiki_namespace + "revision"
text_tag = mediawiki_namespace + "text"
lang=""

with open(file_path,'r') as xml_file:
    context = ET.iterparse(xml_file, tag=page_tag)

    # iterate over the content of the page tags
    for action, elem in context:
        tree = ET.ElementTree(elem)
        page = tree.getroot()
    
        # iterate over the childs of page
        for child_of_page in page:
    
            # get title
            if child_of_page.tag == title_tag:
                key=child_of_page.text
    
            # handle revision case 
            if child_of_page.tag == revision_tag:
    
                # iterate over childs of revision
                for child_of_revision in child_of_page:
                    if child_of_revision.tag == text_tag: 
    
                        # extract external links from the text of the child
                        lang=get_language(child_of_revision.text)

        dump.update({key:lang})
        #print dump
        key=""
        lang=""
print dump
