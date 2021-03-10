"""Blogly application."""

from flask import Flask, request, redirect, flash, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route("/")
def home():
    return redirect('/users')

@app.route("/users")
def userlist():

    a = User(first_name = 'John', last_name = 'Smith')
    db.session.add(a)
    db.session.commit()

    users = User.query.all()
    return render_template('list.html', users = users)

@app.route("/users/new")
def new_user():

    return render_template('user_form.html')

@app.route("/users/new/add", methods = ['POST'])
def add_user():

    # f_name, l_name, img_url = request.form -- can we destructure?
    f_name = request.form['f_name']
    l_name = request.form['l_name']
    img_url = request.form['img_url']


    user = User(first_name = f_name, last_name = l_name, image_url = img_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')