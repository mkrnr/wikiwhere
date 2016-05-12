'''
Created on Feb 24, 2016

@author: Martin Koerner <info@mkoerner.de>
'''

import operator

def vote(coordinates_array, absolute_threshold):

    location_vote_dictionary = {}
    for new_location in coordinates_array:

        match = None

        # search for match
        for saved_location in location_vote_dictionary:
            # consider locations to be the same if the absolute difference is smaller than absolute_threshold
            if abs(saved_location[0] - new_location[0]) < absolute_threshold and abs(saved_location[1] - new_location[1]) < absolute_threshold :
                match = saved_location
                break;

        if match:
            # vote for match
            location_vote_dictionary[match] += 1
        else:
            # vote for new_location
            location_vote_dictionary[new_location] = 1
    
    # get location with the highest number of votes
    location_max_votes = max(location_vote_dictionary.iteritems(), key=operator.itemgetter(1))[0] 
    return location_max_votes
            