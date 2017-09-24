class SearchResponse:
    def __init__(self, error, results):
        self.error = error
        self.results = results['hits']['hits'] if results else None
