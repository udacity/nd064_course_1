from os import cpu_count
import logging
import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

# Global Variable
conn_counter = 0

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global conn_counter
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    conn_counter+=1
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
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        app.logger.info("Article with post ID '%s' not found!", post_id)
        return render_template('404.html'), 404
    else:
        app.logger.info("Article '%s' retrieved!", post['title'])
        return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info("About article accessed")
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
            app.logger.info("Created new article!")
            return redirect(url_for('index'))
    return render_template('create.html')

# Define the healthz endpoint
@app.route('/healthz')
def return_healthz():
    return jsonify({"status": "OK - healthy"})

# Define the metrics endpoint
@app.route('/metrics')
def return_metrics():
    connection = get_db_connection()
    posts_count = connection.execute('SELECT COUNT(*) FROM posts').fetchone()
    connection.close()
    return jsonify({"posts_count": posts_count['COUNT(*)'], "db_connection_count": conn_counter})




# start the application on port 3111
if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S", 
        level=logging.DEBUG)
    app.run(host='0.0.0.0', port='3111')
