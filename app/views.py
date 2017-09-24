
from flask import render_template
from app import app
from logic import logic
from .forms import SearchForm
from .model.searchreq import SearchRequest
from .model.searchresp import SearchResponse
from flask import request

@app.route('/')
@app.route('/index')
def index():
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


@app.route('/search', methods=['GET', 'POST'])
def search():
    user = "Parika" # FIXME
    form = SearchForm()
    if request.method == 'GET':
        return render_template("search.html",
                               title="Search",
                               user=user,
                               form=form)
    else:
        return render_template("search.html",
                               title="Search Results",
                               user=user,
                               form = form,
                               results=logic.handle_search(SearchRequest(user, form.query_string.data))
                               )
