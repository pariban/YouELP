import traceback

from app.model.searchresp import SearchResponse
from ..clients.elastic import Elastic

es_client = Elastic()

def handle_search(query):
    """
    Handles a query
    :param query: SearchQuery
    :return: SearchResponse
    """
    try:
        matches = es_client.search(query.index, query.query_string)
        return SearchResponse(None, matches)
    except Exception as e:
        traceback.print_exc()
        return SearchResponse(str(e), None)

def handle_details(query, doc_id):
    """
    Returns details of a business
    :param doc_id:
    :return:
    """
    try:
        matches = es_client.get(index=query.index, id=doc_id)
        return {
            "details": matches['_source'],
            "error": None
        }
    except Exception as e:
        traceback.print_exc()
        return {
            "details": None,
            "error": str(e)
        }
