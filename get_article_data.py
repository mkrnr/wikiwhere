import sys
from wikiwhere.main.article_extraction import ArticleExtraction
import collections
import os
import json
from wikiwhere.utils import json_writer
from wikiwhere.main.count_generation import CountGeneration


#create NamedTuple type for loading the world factbook data set
#load pickled data
Country = collections.namedtuple('Country', 'name, gec, iso2c, iso3c, isonum, stanag, tld')

if __name__ == "__main__":
    # get article url
    article_url =  sys.argv[1]

    new_crawl = False
    if len(sys.argv)>2:
        if  sys.argv[2] == "true":
            new_crawl = True

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
    count_generation = CountGeneration()

    language,title = article_extraction.parse_url(article_url)

    #print language

    language_path = os.path.join("data","articles",language)
    article_feature_path = os.path.join(language_path,title+".json")

    # TODO change name
    article_count_path = os.path.join(language_path,title+"-counts-classification-general.json")

    if new_crawl or not os.path.isfile(article_feature_path):
        # generate new article
        collected_features = article_extraction.collect_features(article_url)
        collected_features_with_prediction = article_extraction.add_predictions(language,collected_features)
        collected_features_array = article_extraction.get_as_array(collected_features_with_prediction)
        
        
        classification_general_counts = count_generation.generate_counts(collected_features_array, "classification-general")
        classification_general_counts_array = count_generation.get_as_array(classification_general_counts)
        #generated_counts_arra = co

        # generate directory if it doesn't exist
        if not os.path.exists(language_path):
            os.makedirs(language_path)

        # write generated file
        json_writer.write_json_file(collected_features_array, article_feature_path)
        json_writer.write_json_file(classification_general_counts_array, article_count_path)
    
    # load existing article from JSON
    #with open(article_path) as data_file:
    #    data = json.load(data_file)

    print article_feature_path

