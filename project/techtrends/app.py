import sqlite3
# import logging

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort


# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    global connection_counter
    connection_counter += 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Function to get total post count in database
def get_post_count():
    connection = get_db_connection()
    post_count = connection.execute('SELECT count(*) FROM posts').fetchone()[0]
    connection.close()
    app.logger.info("Post count retrieved from database")
    return post_count

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
connection_counter = 0

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
      app.logger.error("no post was found")
      return render_template('404.html'), 404
    else:
      app.logger.info("Article %s retrieved!" % post['title'])
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info("opened about up page.")
    return render_template('about.html')

# Health check endpoint
@app.route('/healthz')
def healthz():
    response = app.response_class(
        response=json.dumps({"result": "OK - healthy"}),
        status=200,
        mimetype='application/json'
    )
    app.logger.debug("health endpoint was called")
    return response

# API metrics endpoint
@app.route('/metrics')
def metrics():
    total_posts = get_post_count()
    response = app.response_class(
        response=json.dumps({"db_connection_count": connection_counter, "post_count": total_posts}),
        status=200,
        mimetype='application/json'
    )
    app.logger.info("Metrics ready to be sent.")
    return response

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            app.logger.error("Title was missing!")
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            app.logger.info("New article was added with title %s" % title)
            return redirect(url_for('index'))

    return render_template('create.html')

# start the application on port 3111
if __name__ == "__main__":
   app.run(host='0.0.0.0', port='3111',debug=True)
