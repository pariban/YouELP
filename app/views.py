
from flask import render_template
from app import app
from logic import logic
from .forms import SearchForm
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
    form = SearchForm()
    if request.method == 'GET':
        return render_template("search.html",
                               title="Search",
                               user="Parika", # FIXME
                               form=form)
    else:
        render_template("search.html",
                        title="Search Results",
                        user="Parika", # FIXME
                        form = form,
                        results=logic.handle_search({
                            "user": "Parika",
                            "query_string": form.query_string.data,
                        })
                )
