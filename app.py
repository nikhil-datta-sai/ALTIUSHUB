from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class Post(db.Model):
    postId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"Post('{self.postId}','{self.title}', '{self.content}', '{self.tags}')"

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        postId = request.form['postId']  # Assuming postId is provided in your HTML form initially
        title = request.form['title']
        content = request.form['content']
        tags = request.form['tags']
        new_post = Post(postId=postId, title=title, content=content, tags=tags)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('newpost.html')

@app.route('/manage')
def manage():
    posts = Post.query.all()
    return render_template('manage.html', posts=posts)

@app.route('/delete')
def delete():
    return render_template('delete.html')

@app.route('/drafts')
def drafts():
    return render_template('drafts.html')

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=True)
