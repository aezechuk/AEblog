from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Arielle'}
    posts = [
        {
            'author': {'username': 'Camille'}, 'body': 'Basketball for Beginners!'
        },  
        {
            'author': {'username': 'Zaid'}, 'body': 'Spelling Bee Prep Tips!'
        },
        {
            'author': {'username': 'Pokey'}, 'body': 'The Best foods for Bulking Up!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)