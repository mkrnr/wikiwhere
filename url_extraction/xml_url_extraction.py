'''
Created on Jan 12, 2016

@author: Martin Koerner <info@mkoerner.de>
'''

import lxml.etree as ET
import mwparserfromhell
from bz2 import BZ2File


def get_namespace(file_path):
    with BZ2File(file_path) as xml_file:
        for line in xml_file:
            # add closing tag or lxml would complain 
            mediawiki_tag = ET.fromstring(line + "</mediawiki>")
            # get xmlns definition
            xmlns = mediawiki_tag.nsmap.get(None)
            break;
    return "{" + xmlns + "}"

def extract_urls(text):
    parsed_text = mwparserfromhell.parse(child_of_revision.text)
    text_tree_split = parsed_text.get_tree().split()
    for element in text_tree_split:
        if element.startswith("http://") or element.startswith("https://"):
            print "\t" + element

file_path = "/home/martin/glm/datasets/wiki/enwiki-20140402-pages-articles.xml.bz2"

# get the correct namespace from the xml file
mediawiki_namespace = get_namespace(file_path) 

page_tag = mediawiki_namespace + "page"
title_tag = mediawiki_namespace + "title"
revision_tag = mediawiki_namespace + "revision"
text_tag = mediawiki_namespace + "text"

# set the context with the page tag

# file_path = "/home/martin/glm/datasets/wiki/barwiki-20150901-pages-articles.xml.bz2"

with BZ2File(file_path) as xml_file:
    context = ET.iterparse(xml_file, tag=page_tag)

    # iterate over the content of the page tags
    for action, elem in context:
        tree = ET.ElementTree(elem)
        page = tree.getroot()
    
        # iterate over the childs of page
        for child_of_page in page:
    
            # get title
            if child_of_page.tag == title_tag:
                print child_of_page.text 
    
            # handle revision case 
            if child_of_page.tag == revision_tag:
    
                # iterate over childs of revision
                for child_of_revision in child_of_page:
                    if child_of_revision.tag == text_tag: 
    
                        # extract external links from the text of the child
                        extract_urls(child_of_revision.text)
                                    
