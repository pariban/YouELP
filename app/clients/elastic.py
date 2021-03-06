import json
from elasticsearch import Elasticsearch

class Elastic:
    def __init__(self):
        self.client = Elasticsearch(http_auth=('elastic', 'changeme'))

    def index(self, index_name, key, doc):
        res = self.client.index(index=index_name, doc_type='yelp', id=key, body=doc)

    def search(self, index_name, query):
        return self.client.search(index=index_name, q=query)

    def get(self, index_name, doc_id):
        return self.client.get(index=index_name, doc_type='yelp', id=doc_id)
