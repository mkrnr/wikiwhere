'''
Created on Jan 29, 2016

@author: Martin Koerner <info@mkoerner.de>
'''

# https://github.com/Mimino666/langdetect
from langdetect import detect 
from bs4 import BeautifulSoup

import json
import urllib
import argparse
import langdetect
import html2text
from markdown import markdown
import signal
import HTMLParser
from httplib import InvalidURL
from utils import json_writer



class WebsiteLanguageExtraction(object):
    

    def get_website_languages(self,json_data):
        url_language_dictionary = {}
        
        url_count = 0
        for article in json_data:
            for url in json_data[article]:
                url_count += 1
                # print url_count
        
                if url in url_language_dictionary:
                    continue
        
                # start a timeout counter
                signal.alarm(10) 
        
                try:
                    html = urllib.urlopen(url).read()
                    decoded_html = html.decode(errors='ignore')
                    markup_text =  html2text.html2text(decoded_html)
                    html_from_markup = markdown(markup_text)
                    text = ''.join(BeautifulSoup(html_from_markup,"lxml").findAll(text=True))
        
                    language = detect(text)
        
                    url_language_dictionary[url] = language
        
                except AttributeError:
                    print "language not detected: " + url
                    continue
                except langdetect.lang_detect_exception.LangDetectException:
                    print "no features in text: " + url
                    continue
                except IOError:
                    print "URL not found: " + url
                    continue
                except ValueError:
                    print "ValueError for: " + url
                    continue
                except TypeError:
                    print "TypeError for: " + url
                    continue
                except RuntimeError:
                    print "RuntimeError for: " + url
                    continue
                except HTMLParser.HTMLParseError:
                    print "HTMLParseError for: " + url
                    continue
                except InvalidURL:
                    print "InvalidURL for: " + url
                    continue
                except TimeoutException:
                    print "timeout for: " + url
                    continue

        return url_language_dictionary

    def timeout_handler(self,signum, frame):   # Custom signal handler
        raise TimeoutException
    
    # Change the behavior of SIGALRM
    signal.signal(signal.SIGALRM, timeout_handler)

if __name__ == '__main__':
    # generate help text for arguments
    parser = argparse.ArgumentParser(description='Extracts languages from the content of URLs given in a JSON file that contains Wikipedia articles and their referenced URLs')
    parser.add_argument('input',
                       help='a file path to the JSON input file')
    parser.add_argument("--output", dest="output", metavar='output path', type=str, required=True)
    args = parser.parse_args()
    
    inputfile_path=args.input
    outputfile_path=args.output
    
    print "running website_language_extraction"

    # load json input
    with open(inputfile_path) as json_input:    
        json_data = json.load(json_input)
    
    website_language_extraction = WebsiteLanguageExtraction()
    url_language_dictionary = website_language_extraction.get_website_languages(json_data)
    json_writer.write_json_file(url_language_dictionary, outputfile_path)
    

# timeout handling from: http://stackoverflow.com/a/25027182/2174538
class TimeoutException(Exception):   # Custom exception class
    pass