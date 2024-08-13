"""

from newapi.wd_sparql import get_query_result, get_query_data

"""
import traceback
import pywikibot
import sys
from SPARQLWrapper import SPARQLWrapper, JSON


def get_query_data(query):
    endpoint_url = "https://query.wikidata.org/sparql"
    # ---
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # ---
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    # ---
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    # ---
    data = {}
    # ---
    try:
        data = sparql.query().convert()
    except Exception as e:
        pywikibot.output("Traceback (most recent call last):")
        pywikibot.output(traceback.format_exc())
        pywikibot.output(f"API/tools.py quoteurl: Exception: {e}")
        pywikibot.output(" CRITICAL:")
    # ---
    return data


def get_query_result(query):
    # ---
    data = get_query_data(query)
    # ---
    lista = [x for x in data["results"]["bindings"]]
    # ---
    return lista
