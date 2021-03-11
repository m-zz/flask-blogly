"""Blogly application."""

from flask import Flask, request, redirect, flash, render_template
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route("/")
def home():

    a = User(first_name='John', last_name='Smith')
    db.session.add(a)
    b = User(first_name='Mickey', last_name='Mouse')
    db.session.add(b)
    db.session.commit()
    return redirect('/users')


@app.route("/users")
def userlist():

    users = User.query.all()
    return render_template('user_list.html', users=users)


@app.route("/users/new", methods = ['POST','GET'])
def new_user():

    if request.method == 'GET':
        return render_template('user_form.html')
    # f_name, l_name, img_url = request.form -- can we destructure?
    if request.form['img_url']:
        new_user = User(
            first_name=request.form['f_name'],
            last_name=request.form['l_name'],
            image_url=request.form['img_url'])
    else:
        new_user = User(
            first_name=request.form['f_name'],
            last_name=request.form['l_name'])


    
    
    # f_name = request.form['f_name']
    # l_name = request.form['l_name']
    # img_url = request.form['img_url']
    # user = User(first_name=f_name, last_name=l_name, image_url=img_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>')
def display_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_detail.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):

    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        # make changes
        user.first_name = request.form['f_name']
        user.last_name = request.form['l_name']
        user.image_url = request.form['img_url'] or "https://t4.ftcdn.net/jpg/03/46/93/61/360_F_346936114_RaxE6OQogebgAWTalE1myseY1Hbb5qPM.jpg"
        db.session.commit()
        # redirect to the user page
        return redirect(f'/users/{user.id}')
    return render_template('user_edit.html', user=user)
    

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    
    Post.query.filter(Post.user_id == user_id).delete()
    User.query.filter(User.id == user_id).delete()
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new', methods = ['POST', 'GET'])
def post_form_for_user(user_id):
    
    user = User.query.get_or_404(user_id)
    if request.method == 'GET':
        return render_template('post_form.html', user = user)

    p_title = request.form['p_title']
    p_content = request.form['p_content']

    post = Post(title = p_title, content = p_content, user_id = user_id)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def get_post(post_id):

    post = Post.query.get_or_404(post_id)

    return render_template('post_detail.html', post = post)


@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):

    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        # make changes
        post.title = request.form['p_title']
        post.content = request.form['p_content']
        
        db.session.commit()
        # redirect to the user page
        return redirect(f'/users/{post.user.id}')
    
    return render_template('post_edit.html', post = post)


@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    user_id = Post.query.get_or_404(post_id).user_id
    Post.query.filter(Post.id == post_id).delete()
    
    db.session.commit()
    return redirect(f'/users/{user_id}')