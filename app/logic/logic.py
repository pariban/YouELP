from ..clients.elastic import Elastic

es_client = Elastic()

def handle_search(query):
    try:
	# format:
	# { user: Name, query_string: Query }
        return {
                "error": None,
                "results": es_client.search("business_name", query["query_string"])
                }
    except Exception as e:
        return { "error": str(e), "results": [] }

