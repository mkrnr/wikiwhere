'''
Created on May 16, 2016

@author: Martin Koerner <info@mkoerner.de>
'''
from wikiwhere.plot_data_generation.count_generation import CountGeneration
import pycountry
import math




class MapDataGeneration(object):
    
    
    def __init__(self):
        self.color = "235"
        self.lightness = "60%"
        self.count_generation = CountGeneration()
    
    def generate_map_data_array(self,collected_features_array,feature_name):
        feature_counts = self.count_generation.generate_counts(collected_features_array, feature_name) 

        max_count = self.get_max_count(feature_counts)
        print max_count
        map_data_array = []

        for label in feature_counts:
            feature_dir = {}
            saturation = int(math.log(feature_counts[label]) / math.log(max_count) *100)

            feature_dir["color"] = "hsl(" + self.color+", "+ str(saturation)+"%, "+self.lightness+")"
            feature_dir["count"] = str(feature_counts[label])
            feature_dir["label"] = str(pycountry.countries.get(alpha2=label).alpha3)
            
            map_data_array.append(feature_dir)

        return map_data_array

    def get_max_count(self,feature_counts):
        max_count = 0

        for label in feature_counts:
            if feature_counts[label] > max_count:
                max_count = feature_counts[label]

        return max_count
