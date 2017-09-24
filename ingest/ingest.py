# -*- coding: utf-8 -*-
"""
@author: parika

This script reads from s3, joins records and posts parallaly to Elasticsearch

<p>
business.json contains business info and the primary key is 'business_id'
review.json contains reviews for every place and 'business_id' is a field in every record.
The logic is to do a left_join(business, review) on 'business_id' and
store all reviews in business records as a list.
</p>
"""

import json
from elasticsearch import Elasticsearch
from pyspark import SparkConf, SparkContext, SQLContext
from pyspark.sql.functions import collect_list, struct

def postToElasticSearch(index_name, primary_key, rec):
    """
    Posts record to Elastic search using the provided elastic search client

    :param index_name: elastic search index name
    :param primary_key: id of the record
    :param rec: record as a json string
    :return: None
    """
    doc = json.loads(rec.encode('utf8'))
    pk = doc.get("primary_key")
    es = Elasticsearch(http_auth=('elastic','changeme'))
    res = es.index(index=index_name, doc_type='yelp', id=pk, body=doc)
    print(res['created'])


def main(sc):
    """
    reads from s3 and posts to elastic search
    :param sc: spark context
    :return: None
    """
    s3_root = "s3n://yelp-raw-data/"

    sqlContext = SQLContext(sc)
    review_df = sqlContext.read.json(s3_root + 'review.json')
    grouped_reviews = review_df\
        .groupBy('business_id')\
        .agg(collect_list(
        struct("date", "review_id", "stars", "text", "useful", "user_id").alias("reviews")))
    business_df = sqlContext.read.json(s3_root + 'business.json')
    joined_df = business_df.join(grouped_reviews, 'business_id', 'left_outer')
    joined_df\
        .toJSON()\
        .foreach(
        lambda x: postToElasticSearch('business_review_joined', 'business_id', x))\
        .collect()

if __name__ == "__main__":
        # Configure OPTIONS
    with open('configs/aws.json') as aws_fp:
        aws_cfg = json.load(aws_fp)
    conf = SparkConf().setAppName("yelp-ingest")
    sc   = SparkContext(conf=conf)
    sc._jsc.hadoopConfiguration().set("fs.s3n.awsAccessKeyId", str(aws_cfg["awsAccessKeyId"]))
    sc._jsc.hadoopConfiguration().set("fs.s3n.awsSecretAccessKey", str(aws_cfg["awsSecretAccessKey"]))
    main(sc)
