import csv
import sys
from logic import handle_search

class Recommender():
    def __init__(self, resources):
        self.correlation_map = {}
        with open(resources) as infile:
            reader = csv.reader(infile, delimiter='\t')
            for row in reader:
                self.correlation_map[row[0].lower()] = row[1].lower()
            print >>sys.stderr, "loaded categories", len(self.correlation_map)

    def get_recommendations(self, query):
        # print >>sys.stderr, "getting recommendations for", query
        tgt_category = self._get(query.query_string.lower())
        # print >>sys.stderr, "tgt:", tgt_category
        if tgt_category:
            query.query_string = tgt_category
            return handle_search(query)


    def _get(self, source_category):
        if source_category in self.correlation_map:
            return self.correlation_map[source_category]
        return None
