import csv
from logic import handle_search

class Recommender():
    def __init__(self):
        self.correlation_map = {}
        with open('resources/correlation.tsv') as infile:
            reader = csv.reader(infile, delimiter='\t')
            for row in reader:
                self.correlation_map[row[0]] = row[1]

    def get_recommendations(self, query):
        tgt_category = self._get(query.query_string)
        if tgt_category:
            recommendation_query = query
            recommendation_query.query_string = tgt_category
            return handle_search(recommendation_query)


    def _get(self, source_category):
        if source_category in self.correlation_map:
            return self.correlation_map[source_category].lower()
        return None
