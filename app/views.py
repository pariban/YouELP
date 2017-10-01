
from flask import render_template
from app import app
from .logic import logic, recommend
from .forms import SearchForm
from .model import searchreq
from flask import request

recommender = recommend.Recommender()

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
        return render_template("index.html",
                               title="Search Results",
                               user=user,
                               form = form,
                               results=logic.handle_search(
                                   searchreq.SearchRequest(
                                       user,
                                       'business_review_joined',
                                       form.query_string.data)
                               ),
                               recommendations=recommender.get_recommendations(
                                   searchreq.SearchRequest(
                                       user,
                                       'business_review_joined',
                                       form.query_string.data)
                               )
                               )

@app.route('/details/<id>', methods=['GET'])
def details(id):
    user = "Parika" # FIXME
    return render_template("details.html",
                           title="Details",
                           user=user,
                           doc=logic.handle_details(
                               searchreq.SearchRequest(
                                   user,
                                   'business_review_joined',
                                   ''
                               ), id
                           ))
