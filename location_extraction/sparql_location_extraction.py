'''
Created on Jan 11, 2016

@author: Martin Koerner <info@mkoerner.de>
'''


from SPARQLWrapper import SPARQLWrapper, JSON
from SPARQLWrapper.SPARQLExceptions import QueryBadFormed

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
# sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
# sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")

match_out = open("/home/martin/rl/data/dbpedia-all.txt", "wb")  # open output

match_count = 0
domain_matches = {}

location_query = """
        { SELECT * WHERE {
      ?match dbo:locationCity ?locationCity .
      ?locationCity dbp:latitude ?lat .
      ?locationCity dbp:longitude ?long
        } }
      UNION
        { SELECT * WHERE {
      ?match dbo:locationCity ?locationCity .
    ?locationCity geo:lat ?lat .
    ?locationCity geo:long ?long
  } }

  UNION
        { SELECT * WHERE {
      ?match dbp:parentAgency ?parentAgency .
    ?parentAgency geo:lat ?lat .
    ?parentAgency geo:long ?long
  } }
  UNION
        { SELECT * WHERE {
    ?match geo:lat ?lat .
    ?match geo:long ?long
  } }
  UNION
        { SELECT * WHERE {
      ?match dbo:location ?location .
    ?location geo:lat ?lat .
    ?location geo:long ?long
  } }
  """
query_string = """
    select * where {
        { SELECT * WHERE {
      ?match foaf:homepage  ?url .
       """ + location_query + """
        }
         }
      UNION
        { SELECT * WHERE {
      ?match dbp:url  ?url .
       """ + location_query + """
        } }
   }
    """
limit = 5000
offset = 0
while True:
    print offset
    query_string_with_offset = query_string + " LIMIT " + str(limit) + " OFFSET " + str(offset)

    sparql.setQuery(query_string_with_offset)
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
    except QueryBadFormed:
        print "SPARQL query bad formed: " + query_string_with_offset
    
    
    if len(results["results"]["bindings"]) > 0:
        for result in results["results"]["bindings"]:
            match_string = result["url"]["value"] + "\t" + result["match"]["value"] + "\t" + result["lat"]["value"] + "\t" + result["long"]["value"]
            # print match_string
            match_out.write(match_string.encode('utf8') + "\n")
            print match_string.encode('utf8')
        offset += limit
    else:
        break;

match_out.close()
