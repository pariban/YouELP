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

