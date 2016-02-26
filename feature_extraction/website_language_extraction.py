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

# generate help text for arguments
parser = argparse.ArgumentParser(description='Extracts languages from the content of URLs given in a JSON file that contains Wikipedia articles and their referenced URLs')
parser.add_argument('input',
                   help='a file path to the JSON input file')
parser.add_argument("--output", dest="output", metavar='output path', type=str, required=True)
args = parser.parse_args()

inputfile_path=args.input
outputfile_path=args.output


# timeout handling from: http://stackoverflow.com/a/25027182/2174538
class TimeoutException(Exception):   # Custom exception class
    pass

def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException

# Change the behavior of SIGALRM
signal.signal(signal.SIGALRM, timeout_handler)


url_language_dictionary = {}


# load json input
with open(inputfile_path) as json_input:    
    json_data = json.load(json_input)


url_count = 0
for article in json_data:
    for url in json_data[article]:

        if url in url_language_dictionary:
            continue

        # start a timeout counter
        signal.alarm(10) 

        try:
            html = urllib.urlopen(url).read()
            decoded_html = html.decode(errors='ignore')
            markup_text =  html2text.html2text(decoded_html)
            html_from_markup = markdown(markup_text)
            text = ''.join(BeautifulSoup(html_from_markup).findAll(text=True))

            language = detect(text)

            url_language_dictionary[url] = language

            url_count += 1
            print url_count
        except AttributeError:
            print "language not detected: " + url
            continue
        except langdetect.lang_detect_exception.LangDetectException:
            print "no features in text: " + url
            continue
        except IOError:
            print "URL not found: " + url
            continue
        except TimeoutException:
            print "timeout for: " + url
            continue

            


# write results to a JSON file
with open(outputfile_path, 'w') as f:
    json.dump(url_language_dictionary, f, indent=4, sort_keys=True)
    print "File was stored successfully"