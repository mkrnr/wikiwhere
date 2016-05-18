'''
Created on May 16, 2016

@author: Martin Koerner <info@mkoerner.de>
'''
from wikiwhere.plot_data_generation.count_generation import CountGeneration
import pycountry
import math
from wikiwhere.utils import json_writer
from colour import Color




class MapDataGeneration(object):
    
    
    def __init__(self):
        self.color = "235"
        self.lightness = "50%"
        self.saturation = "100%"
        self.count_generation = CountGeneration()
    
    def generate_map_data_array(self,collected_features_array,feature_name):
        feature_counts = self.count_generation.generate_counts(collected_features_array, feature_name) 

        max_count = self.get_max_count(feature_counts)
        map_data_array = []

        # yellow = Color("lime")
        # red = Color("red")
        # color_range = list(yellow.range_to(red, max_count))
        for label in feature_counts:
            feature_dir = {}
            #saturation = int(math.log(feature_counts[label]) / math.log(max_count) *100)

            #color = color_range[feature_counts[label]-1]
            ratio = float(feature_counts[label])/max_count
            color = self.get_color(ratio)
            hue = color.hsl[0] * 360
            feature_dir["color"] = "hsl(" + str(hue)+", "+ self.saturation+", "+self.lightness+")"
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
    
    # calculation based on: http://www.andrewnoske.com/wiki/Code_-_heatmaps_and_color_gradients
    def get_color(self, value):
        # blue rgb
        aR = 0
        aG = 0
        aB = 255
        
        # red rgb
        bR = 255
        bG = 0
        bB = 0
        
        red   = (float(bR - aR) * value + aR)/255
        green = (float(bG - aG) * value + aG)/255
        blue  = (float(bB - aB) * value + aB)/255

        return Color(rgb=(red,green,blue))

#import json
#
#with open("/srv/http/articles/de/Krimkrise/analysis.json") as json_file:
#    json_data = json.load(json_file)
#    print(json_data)
#    
#map_data_generation = MapDataGeneration()
#
#map_data_array = map_data_generation.generate_map_data_array(json_data, "classification-general")
#
#json_writer.write_json_file(map_data_array, "/srv/http/articles/de/Krimkrise/map-data.json")