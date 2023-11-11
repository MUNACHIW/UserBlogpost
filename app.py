from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate

import random 


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog1.db"
app.secret_key = "89iudh8789f7bd89789f7d9yf787d97f987d897f9"

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)





# stores information in a file 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=True)
    password = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True, )
    

    def __str__(self):
        return self.username


# user a
# user b 

# a = post = post a = a id  
# b = post = post b = aid grts post 

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    user_id = db.Column(db.Integer)
    likes = db.relationship('PostLike', backref='post', lazy=True)

    def __str__(self):
        return self.title

class PostLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __str__(self):
        return self.post_id
      


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    post_id = db.Column(db.Integer) # rel to post
    user_id = db.Column(db.Integer) # rel to user
    
    def __str__(self):
        return self.title
    
    
    
# migrations: update the content of the database without losing our data 


@app.get("/")
def home_page():
    if not session.get("user"):
        return redirect("/signin")
    
    logged_in_user = session.get("user")
    user = User.query.filter_by(username=logged_in_user['username']).first()
    posts = Post.query.filter_by(user_id=user.id).all()
   
    return render_template("index.html", data=posts) 


@app.route("/blog")
def blog():
    if not session.get("user"):
        return redirect("/signin")
    
    logged_in_user = session.get("user")
    user = User.query.filter_by(username=logged_in_user['username']).first()
    posts = Post.query.filter_by(user_id=user.id).all()
    return render_template("blog.html", data = posts)

@app.route("/post", methods=["GET","POST"])
def handle_post():  
    if not session.get("user"):
        return redirect('/signin')
    
    if request.method == "GET":
        return render_template("post.html")
   
    
    if request.method == "POST":
        data = request.form
        logged_in_user = session.get("user")
        user = User.query.filter_by(username=logged_in_user['username']).first() # information of the user that is logged in
        title = data.get("title")
        content = data.get("content")
        post = Post(title=title, content=content, user_id=user.id)   
        db.session.add(post)
        db.session.commit()
        
        return redirect("/")
@app.get("/post/<int:id>")
def get_post_detail(id):
    if not session.get("user"):
        return redirect('/signin')
    
    logged_in_user = session.get("user")
    user = User.query.filter_by(username=logged_in_user['username']).first()
    post = Post.query.filter_by(id=id, user_id=user.id).first()
    comments = Comments.query.filter_by(post_id=id).all()
    likes = PostLike.query.filter_by(post_id=post.id).count()
    return render_template("detail.html", post=post,comments=comments, likes = likes )

@app.post("/post/<int:id>/comment")
def make_comment_handler(id):
    if not session.get("user"):
        return redirect('/signin')
    
    logged_in_user = session.get("user")
    user = User.query.filter_by(username=logged_in_user['username']).first()
    content = request.form.get("content")
    commennt = Comments(content=content, post_id=id, user_id=user.id)
    db.session.add(commennt)
    db.session.commit()
    return redirect(url_for('get_post_detail', id=id))


 
    
@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    user_id = request.form['user_id']
    post_like = PostLike.query.filter_by(user_id=user_id, post_id=post_id).first()
    if post_like:
        db.session.delete(post_like)
    else:
        post_like = PostLike(user_id=user_id, post_id=post_id)   
        db.session.add(post_like)
    db.session.commit()
    return redirect(url_for('get_post_detail', id=post_id))






@app.route('/like_count/<int:post_id>')
def like_count(post_id):
    count = PostLike.query.filter_by(post_id=post_id).count()
    return str(count)

    

@app.get("/comment/<int:id>/delete")
def delete_comment_detail(id):
    if not session.get("user"):
        return redirect('/signin')
    
    logged_in_user = session.get("user")
    user = User.query.filter_by(username=logged_in_user['username']).first()
    comment = Comments.query.filter_by(id=id, user_id=user.id).first()
    
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('get_post_detail' , id = id))


@app.route("/signup", methods=['GET',"POST"])
def handle_signup():
    if request.method == "GET":
        return render_template("signup.html")
    
    
    if request.method == "POST":
        data = request.form
        
        username = data['username']
        password = data['password']
        hash_password = generate_password_hash(password)
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "User already has an account  go back to signup and move to sigin"  # Redrect to the signup page
        
        user = User(username=username, password=hash_password)
     
        db.session.add(user)
        db.session.commit()
        return redirect("/")

@app.route("/signin", methods=['GET',"POST"])
def handle_signin():
    
    if request.method == "GET":
        return render_template("signin.html")
    
    if request.method == "POST":
        data = request.form
        username = data['username']
        password = data['password']
        user = User.query.filter_by(username=username).first()
        if user is None:
            # Redirect the user back to the signup page
            return redirect("/signup")
        if check_password_hash(user.password, password):
            session['user'] = {
                "username": user.username
            }
            print(user.email, user.username)
            return redirect("/")    
        
        return redirect("/signin")
    
    
@app.route("/home")
def home_page2():
    return redirect("/")

@app.route("/logoutpage", methods=['GET',"POST"] )
def takepage():
 if request.method == "GET":
    return render_template('logout.html')

@app.get("/logout")
def handles_logout():
    if session.get("user"):
        session.pop("user")
        return redirect("/signin")

if __name__ == "__main__":
    app.run(port=3000, debug=True)
    