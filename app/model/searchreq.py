class SearchRequest:
    def __init__(self, user, index, query):
        self.user = user
        self.index = index
        self.query_string = query

    def __str__(self):
        return "{} | {} | {}".format(self.user, self.index, self.query_string)

    def __repr__(self):
        return self.__str__()
