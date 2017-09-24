# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 18:27:30 2017

@author: parika
"""

# This script reads from s3 and posts parallaly to Elasticsearch
import json
from elasticsearch import Elasticsearch
from pyspark import SparkConf, SparkContext, SQLContext
from pyspark.sql.functions import collect_list

es = Elasticsearch(http_auth=('elastic','changeme'))

def postToElasticSearch(index_name, primary_key, doc):
    """
    Posts record to Elastic search using the provided elastic search client
    """
    global es
    pk = doc.get("primary_key")
    res = es.index(index=index_name, doc_type='yelp', id=pk, body=doc)
   # print(res['created'])


def main(sc):
    # reads from s3 and posts to elastic search
    s3_root = "s3n://yelp-raw-data/"

    sqlContext = SQLContext(sc)
    business_df = sqlContext.read.json(s3_root + 'business.json')
    review_df = sqlContext.read.json(s3_root + 'review.json')

    grouped_reviews = review_df.groupBy('business_id').agg(collect_list("reviews").alias("reviews"))
    joined_df = business_df.join(grouped_reviews, 'left_outer')
    joined_df.foreach(lambda x: postToElasticSearch('business_review_joined', 'business_id', x)).collect()

if __name__ == "__main__":
        # Configure OPTIONS
    with open('configs/aws.json') as aws_fp:
        aws_cfg = json.load(aws_fp)
    conf = SparkConf().setAppName("yelp-ingest")
    sc   = SparkContext(conf=conf)
    sc._jsc.hadoopConfiguration().set("fs.s3n.awsAccessKeyId", str(aws_cfg["awsAccessKeyId"]))
    sc._jsc.hadoopConfiguration().set("fs.s3n.awsSecretAccessKey", str(aws_cfg["awsSecretAccessKey"]))
    main(sc)
