import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
from flask import current_app
import logging

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    increment_counter()
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Count posts
def total_posts():
    connection = get_db_connection()
    total = connection.execute('SELECT count(id) FROM posts').fetchone()[0]
    connection.close()
    return total

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
with app.app_context():
    current_app.config["counter"] = 0 

def get_counter() -> int:
    with app.app_context():
        return current_app.config["counter"] 

def increment_counter():
    with app.app_context():
        current_app.config["counter"] += 1

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        app.logger.error(f"Post [{post_id}] not found.'")
        return render_template('404.html'), 404
    else:
        app.logger.info(f"Post '{post['title']} fetched.'")
        return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info(f"About page is retrieved")
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            app.logger.info(f"New Post created, with title: '{title}'")
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/healthz')
def health():
    response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
    )
    return response

def get_metrics():
    return {
        "db_connection_count": get_counter(),
        "post_count": total_posts() 
    }

@app.route('/metrics')
def metrics():
    response = app.response_class(
            response=json.dumps(get_metrics()),
            status=200,
            mimetype='application/json'
    )
    return response


# start the application on port 3111
if __name__ == "__main__":
    #logging.basicConfig(format='%(asctime)s %(message)s',

    #datefmt='%Y-%m-%d,%H:%M:%S:%f', level=logging.INFO)
    logging.basicConfig(
        level=logging.DEBUG, \
        format='%(levelname)s:%(module)s:%(asctime)s, %(message)s', \
        datefmt='%d/%m/%Y, %H:%M:%S'
    )
    app.run(host='0.0.0.0', port='3111')
