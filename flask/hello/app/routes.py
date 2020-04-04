from app import app
from flask import Flask
from flask import request, render_template, redirect, flash
import pprint
from app.forms import LoginForm

@app.route('/hello', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        print(pprint.pformat(request.__dict__, depth=5))
        print('rqdataraw=', request.data)
        request.data = request.get_data().strip()
        json = request.get_json()
        print('request=', request)
        print('json=', json)
        print('rqdata=', request.get_data() )
        return 'Post Cereal, Hello! form is %s ' % (request.json)
        # return 'Post Cereal, Hello! %s and %s ' % (json['data'], request.form)
    else:
        return 'Hello, World!'

@app.route('/projects/')
def projects():
    return 'The projection page'

@app.route('/about')
def about():
    return 'The about page'

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user %s, remember_me=%s'
              % (form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)
