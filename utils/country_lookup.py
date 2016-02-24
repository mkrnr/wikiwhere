'''
Created on Feb 23, 2016

@author: Tatiana Sennikova, Martin Koerner <info@mkoerner.de>
'''

from urllib2 import urlopen
import json

# Get place using GoogleMaps API
def get_country(lat, lon):
    country=""
    # town=""
    url = "http://maps.googleapis.com/maps/api/geocode/json?"
    url += "latlng=%s,%s&sensor=false" % (lat, lon)
    #print url
    v = urlopen(url).read()
    j = json.loads(v)
    #print j
    if j['status']!=u'ZERO_RESULTS':
        components = j['results'][0]['address_components']
        country = None
        # town = None
        for c in components:
            if "country" in c['types']:
                country = c['short_name']
            #if "postal_town" in c['types']:
            #    town = c['long_name']
    #print country
    return country
