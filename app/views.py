import os

from flask import render_template
from app import app
from .logic import logic, recommend
from .forms import SearchForm
from .model import searchreq
from flask import request

def root_dir():
    return os.path.abspath(os.path.dirname(__file__))

recommender = recommend.Recommender(os.path.join(root_dir(), 'resources/correlation.tsv'))

@app.route('/deprecated_index')
def deprecated_index():
    user = {'nickname': 'Miguel'}  # fake user
    posts = [  # fake array of posts
            {
                'author': {'nickname': 'John'},
                'body': 'Beautiful day in Portland!'
                },
            {
                'author': {'nickname': 'Susan'},
                'body': 'The Avengers movie was so cool!'
                }
            ]
    return render_template("index.html",
            title='Home',
            user=user,
            posts=posts)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def search():
    user = "Parika" # FIXME
    form = SearchForm()
    global recommender
    if request.method == 'GET':
        return render_template("index.html",
                               title="Home",
                               user=user,
                               form=form)
    else:
        query_string = form.query_string.data
        return render_template("index.html",
                               title="Search Results",
                               user=user,
                               form = form,
                               results=logic.handle_search(
                                   searchreq.SearchRequest(
                                       user,
                                       'business_review_joined',
                                       query_string)
                               ),
                               recommendations=recommender.get_recommendations(
                                   searchreq.SearchRequest(
                                       user,
                                       'business_review_joined',
                                       query_string)
                               )
                               )

@app.route('/details/<id>', methods=['GET'])
def details(id):
    user = "Parika" # FIXME
    form = SearchForm()
    return render_template("details.html",
                           title="Details",
                           user=user,
                           form = form,
                           doc=logic.handle_details(
                               searchreq.SearchRequest(
                                   user,
                                   'business_review_joined',
                                   ''
                               ), id
                           ))
