from flask import Flask, render_template, request
from search import search

app = Flask(__name__)


@app.route("/", methods=["GET"])
def get_home():
    return render_template('index.html')


@app.route("/", methods=["POST"])
def post_home():
    if request.form['search']:
        search_req = request.form['search']
        res = search(search_req)
    return render_template('index.html', data = res)