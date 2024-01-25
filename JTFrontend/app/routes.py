from flask import render_template
from JTFrontend.flaskApp import app

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/<selectedNav>')
def selected(selectedNav="home.html"):
    return render_template(f'{selectedNav}')

