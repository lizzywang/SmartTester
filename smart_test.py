# -*- coding: utf-8 -*-
_author_ = 'xin'

from flask import Flask,render_template,session,redirect,url_for,flash, request
import MySQLdb as mysql

from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask.ext.redis import FlaskRedis
from graphpath import findGraphPath


app = Flask(__name__)
app.config['SECRET_KEY'] = 'haha'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:1234@localhost:3306/test' #这里登陆的是root用户，要填上自己的密码，MySQL的默认端口是3306，填上之前创建的数据库名text1
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True #设置这一项是每次请求结束后都会自动提交数据库中的变动
app.config['REDIS_URL'] = 'redis://localhost:6379/0'


bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app) #实例化
redis_store = FlaskRedis(app)


class State(db.Model):
    __tablename__ = 'states'
    id = db.Column(db.Integer, primary_key=True)
    componentId = db.Column(db.String(64), index=True)
    action = db.Column(db.String(64))
    type = db.Column(db.String(64))

    def __repr__(self):
        return '<State %r>' % self.id


class Pair(db.Model):
    __tablename__ = 'pairs'
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.Integer, db.ForeignKey('states.id'))
    end = db.Column(db.Integer, db.ForeignKey('states.id'))

    def __repr__(self):
        return '<Pair %r, %r>'


def generate_code(links, start, end):
    paths = findGraphPath(links, start, end)
    states = State.query.all()
    dict = {}
    for state in states:
        dict[state.id] = state
    i = 1
    codes = ""

    for path in paths:
        line = "Test Plan " + str(i) + "\n"
        codes = codes + line
        for node in path:
            line = generate_line(dict.get(node))
            codes = codes + line
        i = i + 1
    result = codes
    return result


def generate_line(state):
    return "    Then I " + state.action + " " + state.type + " with ID " + state.componentId + "\n"


@app.route('/generate_test_plan', methods=['POST'])
def generate_test_plan():
    # TODO links and start and end are read from requests
    links = [1,2,1,3,1,4]
    start = 1
    end = -1
    return generate_code(links, start, end)


@app.route('/')
def home():
    states = State.query.all()
    return render_template('home.html', states=states)


@app.route('/addnew')
def new_student():
    return render_template('state.html')


@app.route('/saveMyModel', methods=['POST'])
def my_save_model():
    if request.method == 'POST':
        saved_models = request.form.get('mySaveModel')
        redis_store.set("test111", saved_models)
    return render_template("home.html", msg="success")
    # TODO


@app.route('/loadMyModel/<modelID>')
def load_my_model(modelID):
    model = redis_store.get(modelID)
    return render_template(home.html, savedModel=model)


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            print("$$$$")
            cid = request.form.get('cid')
            action = request.form.get('action')
            type = request.form.get('type')
            print cid
            print action
            state = State(componentId=cid, action=action,type=type)
            print cid
            db.session.add(state)
            db.session.commit()
            msg = "Record successfully added"
        except:
            msg = "error in insert operation"
        finally:
            states = State.query.all()
            return render_template('home.html', msg=msg, states=states)


@app.route('/list')
def list():
    states = State.query.all()
    return render_template('list.html', states=states)


if __name__ == "__main__":
    app.run(debug=True)
