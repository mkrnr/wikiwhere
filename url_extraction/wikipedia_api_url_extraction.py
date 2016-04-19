'''
Created on Apr 8, 2016

@author: Tania
'''

from wikitools import wiki, api
    

class WikipediaApiUrlExtraction(object):

    def parse_url(self,link):
        language = link.rstrip().split('.')[0].split("//")[1]
        title= link.rstrip().split('/')
        return language, title[-1]   
    
    def extlinks_extraction(self,lang, title):
        links=[]
        linklist=[]

        site = wiki.Wiki("https://"+lang+".wikipedia.org/w/api.php")
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
    
    def clean_list(self,links):
        url_list=[]
        for link in links:
            url=link.values()
            if url[0].startswith("http"):
                url_list.append(url[0])
        return url_list


    def extract_urls(self,url):
        language, title=self.parse_url(url)
        links=self.extlinks_extraction(language, title)
        url_list=self.clean_list(links)
        return url_list


if __name__ == '__main__':

    wikipedia_api_url_extraction = WikipediaApiUrlExtraction()
    url="https://en.wikipedia.org/wiki/United_States"
    extracted_urls = wikipedia_api_url_extraction.extract_urls(url)
    print extracted_urls
    