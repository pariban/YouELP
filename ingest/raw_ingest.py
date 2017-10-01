# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 18:27:30 2017

@author: parika
"""

# This script reads from s3 and posts parallaly to Elasticsearch
import json

import sys
from elasticsearch import Elasticsearch
from pyspark import SparkConf, SparkContext


def postToElasticSearch(index_name, primary_key, record):
    """
    Posts record to Elastic search using the provided elastic search client
    """
    doc = json.loads(record)
    pk = doc.get("primary_key")
    es = getESClient()
    res = es.index(index=index_name, doc_type='yelp', id=pk, body=doc)
   # print(res['created'])


def getESClient():
    """Creates and returns an elastic search client"""
    es = Elasticsearch(http_auth=('elastic','changeme'))
    return es


def populateESWithJsonFile(sc, index_name, index_attrib):
    file_name = index_attrib["file_name"]
    primary_key = index_attrib["primary_key"]
    """reads s3 file and populates elastic search"""
    rdd = sc.textFile(file_name)
    rdd.map(lambda x : postToElasticSearch(index_name, primary_key, x)).collect()
    

def main(sc):
    # reads from s3 and posts to elastic search
    s3_root = "s3n://yelp-raw-data/"
    index_info = {
            "business": {
                    "file_name": s3_root + "business.json",
                    "primary_key": "busniness_id",
                    },
            "user": {
                    "file_name": s3_root + "user.json",
                    "primary_key": "user_id"
                    },
            }
    for index_name, index_attrib in index_info.items():
        populateESWithJsonFile(sc, index_name, index_attrib)


if __name__ == "__main__":
    raise Exception("Deprecated: please use ingest.py")

    # Configure OPTIONS
    with open('configs/aws.json') as aws_fp:
        aws_cfg = json.load(aws_fp)
    conf = SparkConf().setAppName("yelp-ingest")
    sc   = SparkContext(conf=conf)
    sc._jsc.hadoopConfiguration().set("fs.s3n.awsAccessKeyId", str(aws_cfg["awsAccessKeyId"]))
    sc._jsc.hadoopConfiguration().set("fs.s3n.awsSecretAccessKey", str(aws_fp["awsSecretAccessKey"]))
    main(sc)
