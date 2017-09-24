class SearchRequest:
    def __init__(self, user, index, query):
        self.user = user
        self.index = index
        self.query_string = query
