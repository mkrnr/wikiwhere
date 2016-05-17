'''
Created on May 3, 2016

@author: Martin Koerner <info@mkoerner.de>
'''

import operator

class CountGeneration(object):
    def generate_counts(self,collected_features_array,feature_name):
        feature_counts = {}
        for instance in collected_features_array:
            if feature_name in instance:
                feature = instance[feature_name]
                if feature in feature_counts:
                    feature_counts[feature] += 1
                else:
                    feature_counts[feature] = 1 
        
        return feature_counts

    def get_as_array(self,feature_counts):
        feature_count_array = []

        sorted_feature_counts = sorted(feature_counts.items(), key=operator.itemgetter(1),reverse=True)

        for feature_count_tuple in sorted_feature_counts:
            dict_for_label = {}

            dict_for_label["label"] = feature_count_tuple[0]
            dict_for_label["count"] = feature_count_tuple[1]
        
            feature_count_array.append(dict_for_label)
        
        return feature_count_array
