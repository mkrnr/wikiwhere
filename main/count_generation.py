'''
Created on May 3, 2016

@author: Martin Koerner <info@mkoerner.de>
'''


class CountGeneration(object):
    def generate_counts(self,collected_features_array,feature_name):
        feature_counts = {}
        for instance in collected_features_array:
            feature = instance[feature_name]
            if feature in feature_counts:
                feature_counts[feature] += 1
            else:
                feature_counts[feature] = 1 
        
        return feature_counts

    def get_as_array(self,feature_counts):
        feature_count_array = []
        
        for label in feature_counts:
            dict_for_label = {}

            dict_for_label["label"] = label
            dict_for_label["count"] = feature_counts[label]
        
            feature_count_array.append(dict_for_label)
        
        return feature_count_array