# -*- coding: utf-8 -*-
"""
@author: parika
"""

import json
from collections import Counter
from operator import add
from pyspark import SparkConf, SparkContext, SQLContext
from pyspark.sql.functions import collect_list, struct


def emit_user_category_tuple(entry):
    """
    Emits all tuples of (category, user_id)
    sample entry:
    {
        business_id: id1,
        categories: [c1, c2],
        reviews: [
            {
                stars: 2,
                user_id: u1,
            },
            {
                stars: 1,
                user_id: u2,
            }
        ]
    }
    """
    entry = json.loads(entry)
    results = []
    if 'categories' in entry and 'reviews' in entry:
        for cat in filter(None, entry['categories']):
            for rev in filter(None, entry['reviews']):
                if 'user_id' in rev:
                    results.append((rev['user_id'], cat))
    return results


def emit_category_markov_distribution(categories):
    """
    Emits the probability of edge transitions based on frequency of occurrences
    """
    counter = Counter(categories)
    sum_of_vals = sum(counter.values())
    results = []
    for key1 in counter.keys():
        for key2 in counter.keys():
            results.append(((key1, key2),
                            counter[key2] * 1.0 * counter[key1] /
                            sum_of_vals /
                            sum_of_vals))
    return results


def main(sc):
    """
    Reads from s3 and posts to elastic search

    It does an outer join of business.json with
    review.json (grouped by 'business_id') on 'business_id'
    and adds an additional column 'reviews'.
    :param sc: spark context
    :return: None
    """
    s3_root = "s3n://yelp-raw-data/"

    sqlContext = SQLContext(sc)
    review_df = sqlContext.read.json(s3_root + 'review.json')
    review_df.rdd.checkpoint
    grouped_reviews = review_df.groupBy(
        'business_id'
    ).agg(
        collect_list(
            struct(
                "stars",
                "user_id"
            )
        ).alias(
            "reviews"
        )
    )
    business_df = sqlContext.read.json(s3_root + 'business.json')
    business_df.rdd.checkpoint
    joined_df = business_df.join(grouped_reviews, 'business_id')
    joined_df.toJSON(
    ).flatMap( # [[(u1, c1), (u2, c2)],[())], ...] --> [(u1, c1), (u2, c2), (), ...]
        emit_user_category_tuple
    ).groupByKey( # group by user
    ).flatMap(
        lambda x: emit_category_markov_distribution(x[1])
    ).reduceByKey( #key = pair of categories
        add
    ).foreach( # (c1, c2): score
        lambda x: "{}\t{}\t{}".format(x[0][0], x[0][1], x[1])
    ).saveAsTextFile(
        s3_root + 'output/correlation.tsv'
    )


if __name__ == "__main__":
    """Reads aws secrets and sets up spark context"""
    conf = SparkConf().setAppName("yelp-analyze")
    sc = SparkContext(conf=conf)
    with open('configs/aws.json') as aws_fp:
        aws_cfg = json.load(aws_fp)
    sc._jsc.hadoopConfiguration().set("fs.s3n.awsAccessKeyId",
                                      str(aws_cfg["awsAccessKeyId"]))
    sc._jsc.hadoopConfiguration().set("fs.s3n.awsSecretAccessKey",
                                      str(aws_cfg["awsSecretAccessKey"]))
    main(sc)
