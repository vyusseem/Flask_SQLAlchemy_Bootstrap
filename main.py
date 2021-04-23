from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# DB/model
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable = False)
    title = db.Column(db.String(100), nullable=False, default="")
    content = db.Column(db.Text, nullable=False, default="")
    author = db.Column(db.String(25), default="N/A")
    date_posted = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return 'Blog Post' + str(self.id)

# Populate DB with test data
@app.before_first_request
def before_first_request_func():
    db.create_all()     
    
    for i in range(10):
        p = Post(
            title='Lorem Ipsum {}'.format(i+1),
            content='Voluptas qui est velit non id cum ut. Eaque asperiores soluta culpa explicabo ducimus molestias commodi  {}'.format(i+1))
        db.session.add(p)
    
    db.session.add(Post(
        title="Dialectics of Nature", 
        content="Their essential character: the grouping of the whole body about the nervous system. Thereby the development of self-consciousness, etc. becomes possible. In all other animals the nervous system is a secondary affair, here it is the basis of the whole organisation.", 
        author="Friedrich"))
    
    db.session.commit()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/posts', methods = ['GET'])
def posts():
    """ Display all Posts """
    all_posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('posts.html', posts = all_posts)


@app.route('/posts/add', methods = ['GET', 'POST'])
def posts_add():
    '''
    GET: Display a form to create Post
    POST: Save new Post
    '''
    if request.method == 'POST':
        post = Post(
                title=request.form['title'], 
                content=request.form['content'], 
                author=request.form['author']
            )
        db.session.add(post) 
        db.session.commit() 
        return redirect('/posts')
    else:
        return render_template('posts_form.html', post=None)


@app.route('/posts/edit/<int:id>', methods = ['POST', 'GET'])
def posts_edit(id):
    '''
    GET: Display a form to edit Post
    POST: Update Post
    '''
    app.logger.info('Post # %s edit', id)
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']  
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('posts_form.html', post = post)


@app.route('/posts/delete/<int:id>', methods = ['GET'])
def posts_delete(id):
    ''' Delete Post '''
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()        
    return redirect('/posts')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

