'''
Created on Jan 29, 2016

@author: Martin Koerner <info@mkoerner.de>
'''

# https://github.com/Mimino666/langdetect
from langdetect import detect 
from bs4 import BeautifulSoup
import urllib

url = 'http://bund.de'
html = urllib.urlopen(url).read()
soup = BeautifulSoup(html)
html_body = soup.body.get_text(" ")


print detect(html_body)
