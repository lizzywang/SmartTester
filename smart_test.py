# -*- coding: utf-8 -*-
_author_ = 'xin'

from flask import Flask,render_template,session,redirect,url_for,flash, request
import MySQLdb as mysql

from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'haha'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:1234@localhost:3306/test' #这里登陆的是root用户，要填上自己的密码，MySQL的默认端口是3306，填上之前创建的数据库名text1
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True #设置这一项是每次请求结束后都会自动提交数据库中的变动


bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app) #实例化


class State(db.Model):
    __tablename__ = 'states'
    id = db.Column(db.Integer, primary_key=True)
    componentId = db.Column(db.String(64), unique=True, index=True)
    action = db.Column(db.String(64))

    def __repr__(self):
        return '<State %r, %r>' % self.componentId, self.action


class Pair(db.Model):
    __tablename__ = 'pairs'
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.Integer, db.ForeignKey('states.id'))
    end = db.Column(db.Integer, db.ForeignKey('states.id'))

    def __repr__(self):
        return '<Pair %r, %r>'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/addnew')
def new_student():
    return render_template('state.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            print("$$$$")
            cid = request.form.get('cid')
            action = request.form.get('action')
            print cid
            print action
            state = State(componentId=cid, action=action)
            print cid
            db.session.add(state)
            db.session.commit()
            msg = "Record successfully added"
        except:
            msg = "error in insert operation"
        finally:
            return render_template('result.html', msg=msg)


@app.route('/list')
def list():
    states = State.query.all()
    return render_template('list.html', states=states)


if __name__ == "__main__":
    app.run(debug=True)
