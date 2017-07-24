#! /usr/local/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/<user>')
def index(user=None):
    return render_template("user.html", user=user)


if __name__ == "__main__":
    app.run(debug=True)
