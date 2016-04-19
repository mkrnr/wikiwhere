import sys
from main.article_extraction import ArticleExtraction
import collections
import os
import json


#create NamedTuple type for loading the world factbook data set
#load pickled data
Country = collections.namedtuple('Country', 'name, gec, iso2c, iso3c, isonum, stanag, tld')

if __name__ == "__main__":
    # get article url
    article_url =  sys.argv[1]

    base_dir=os.path.dirname(os.path.realpath(__file__))
    sys.path.append(base_dir)

    data_path = os.path.join(base_dir,"data")
    database_path = os.path.join(data_path,"databases")
    geodatabase_path =os.path.join(database_path,"GeoLite2-Country.mmdb")
    ianadatabase_path =os.path.join(database_path,"iana.p")
    wfbdatabase_path =os.path.join(database_path,"wfb.p")

    model_data_path = os.path.join(data_path,"models")

    languages = ["de", "en","es","fr","general","it","nl","sv","uk"]
    article_extraction = ArticleExtraction(geodatabase_path,ianadatabase_path,wfbdatabase_path,model_data_path,languages)

    language,title = article_extraction.parse_url(article_url)

    #print language

    article_path = os.path.join("data","articles",language,title+".json")
    if os.path.isfile(article_path):
        with open(article_path) as data_file:
            data = json.load(data_file)
        print json.dumps(data)

    #else:
    #    print "file not found"
    #
    #print article_path






