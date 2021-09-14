import sqlite3
import sys

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash, render_template_string
import logging
from werkzeug.exceptions import abort
app = Flask(__name__)

connection_count = 0
posts_count = 0
# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global connection_count
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    connection_count += 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    global posts_count
    posts_count = len(posts)
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    title = post[2]
    if post is None:
      app.logger.info("Article non existing")
      return render_template('404.html'), 404
    else:
      app.logger.info("Article %s retrieved!", title)
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info("About paged accessed")
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
            app.logger.info("Article %s successfully created", title)
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route("/healthz")
def healthcheck():
    health = {
        "result": "OK - healthy"
    }
    response = app.response_class(
        response=json.dumps(health),
        status=200,
        mimetype='application/json'
    )
    app.logger.info("Status request successful")
    return response

@app.route("/metrics")
def metrics():
    global posts_count
    data = {
        "db_connection_count": connection_count,
        "post_count": posts_count,
    }
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    app.logger.info("Metrics request successful")
    return response

# start the application on port 3111
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG)
    app.run(host='0.0.0.0', port='3111')
