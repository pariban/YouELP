import json
from elasticsearch import Elasticsearch

class Elastic:
    def __init__(self):
        self.client = Elasticsearch(http_auth=('elastic', 'changeme'))

    def index(self, index_name, key, doc):
        res = self.client.index(index=index_name, doc_type='yelp', id=key, body=doc)

    def search(self, index_name, query):
        return self.client.search(index_name=index_name, q=query)