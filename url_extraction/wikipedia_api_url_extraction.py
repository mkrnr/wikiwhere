'''
Created on Apr 8, 2016

@author: Tania
'''

from wikitools import wiki, api
import wikipedia
    

def parse_url(link):
    language = link.rstrip().split('.')[0]
    title= link.rstrip().split('/')
    return language, title[-1]   

def extlinks_extraction(lang, title):
    linkdict = {}
    article_links = {}
    links=[]
    linklist=[]
    
    site = wiki.Wiki(language+".wikipedia.org/w/api.php")
    #urllib2.quote(title.encode("utf8"))
    #title = title.encode("utf-8")
    params = {'action':'query', 'titles':title, 'prop':'extlinks', 'ellimit':500}
    req = api.APIRequest(site, params)
    
    for res in req.queryGen():
        #pprint.pprint(res)
        for pidkey  in res['query']['pages']:
            #print res['query']['pages']
            if 'extlinks' in res['query']['pages'][pidkey]:
                linklist = res['query']['pages'][pidkey]['extlinks']+linklist
        links=links+linklist
        linklist=[]
#    print links
    return links

def clean_list(links):
    url_list=[]
    for link in links:
        url=link.values()
        if url[0].startswith("http"):
            url_list.append(url[0])
    return url_list


url="https://en.wikipedia.org/wiki/United_States"
language, title=parse_url(url)
links=extlinks_extraction(language, title)
url_list=clean_list(links)
print url_list