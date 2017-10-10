# YouELP 
_Personalized Yelp with zero-query recommendations_

The vision of this project is to build an end-to-end search and recommendation system for POI data, just like
Yelp, but personalized for users using history of searches and clicks. Here's a mock of the product in vision.

[vision]: https://github.com/pariban/YouELP/raw/master/images/vision.png "Vision"
![Vision][vision]

In this project, the scope of the work is limited to showing recommendations based on interests of similar users. Yelp provides
datasets comprising of businesses and reviews along with users data. Using the affinity of users towards category pairs
the system recommends relevant POIs when user searches for a particular category. For example, users who
reviewed _Bars_ also reviewed POIs of category _Nightlife_, when a user searches for _Bars_, the system will show
recommended businesses of type _Nightlife_. This is explained using the following.

[demo]: https://github.com/pariban/YouELP/raw/master/images/demo.png "Demo"
![Demo][demo]

### Install

You may use pip to install requirements as:
```
pip install -r requirements.txt
```

This project used publicly available [Yelp dataset](https://www.yelp.com/dataset).
Data needs to be extracted and stored in s3 at ```s3://yelp-raw-data/```.

AWS auth information needs to be provided in ```configs/aws.json```.

The service needs to be provisioned with apache2 and _mod_wsgi_. Please look at this
[guide](http://flask.pocoo.org/docs/0.12/deploying/mod_wsgi/). Alternatively, you may run
the Flask dev server by running ```server.py```.

### Preparing Datasets

The system relies on two datasets: 
1. Search data
2. Category-correlation data

#### Search dataset

The search dataset is an amalgamation of _business_ and _review_ records. These two streams are joined to form records
containing both business info and reviews, and indexed in elasticsearch.

[ingestion-flow]: https://github.com/pariban/YouELP/raw/master/images/ingest.png "Ingestion Flow"
![Ingesting search dataset][ingestion-flow]

### Category-correlations data

We extract the category correlations using a Markov model of users reviewing category _C2_ given that they also reviewed
category _C1_. We extract this information using the following pipeline.

[analysis-flow]: https://github.com/pariban/YouELP/raw/master/images/analysis.png "Analysis Flow"
![Analyzing dataset][analysis-flow]

In the following diagram the correlation between categories is explained with a heatmap, where the color of the dots
indicate the affinity between categories. In a zoomed in view, the affinity of category _Indian_ is shown towards other
categories.

[category-correlation]: https://github.com/pariban/YouELP/raw/master/images/correlation.png "Category Correlation"
![Category Correlations][category-correlation]
