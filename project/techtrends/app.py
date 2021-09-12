import sqlite3
from wsgiref.simple_server import WSGIServer

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
import logging

# Declare variables
DbConnectionCount = 0
postsCounts = 0

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global DbConnectionCount
    connection = sqlite3.connect('D:\\Udacity\\Nanodegree\\project\\techtrends\\database.db')
    DbConnectionCount +=1
    connection.row_factory = sqlite3.Row
    return connection


# Function to get a post using its ID
def get_post(post_id):
    global postsCounts
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                              (post_id,)).fetchone()
    postsCounts += 1
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


# Define the main route of the web application
@app.route('/')
def index():
    global postsCounts
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
        return render_template('404.html'), 404
    else:
        # Log Message
        app.logger.info('Article "{0}" successfull'.format(post['title']))
        return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    # Log Message
    app.logger.info('About page successfull')
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

            return redirect(url_for('index'))

    return render_template('create.html')


# Healthcheck endpoint
# Build the /healthz endpoint for the TechTrends application. The endpoint should return the following response:
# An HTTP 200 status code
# A JSON response containing the result: OK - healthy message
@app.route('/healthz')
def healthcheck():
    response = app.response_class(
        response=json.dumps({"result": "OK - healthy"}),
        status=200,
        mimetype='application/json'
    )

    # Log Message
    app.logger.info('Status request successfull')
    return response


# Metrics endpoint
# Build a /metrics endpoint that would return the following:
# An HTTP 200 status code
# A JSON response with the following metrics:
# Total amount of posts in the database
# Total amount of connections to the database.
# For example, accessing an article will query the database, hence will count as a connection.
# Example output: {"db_connection_count": 1, "post_count": 7}
# Tips: The /metrics endpoint response should NOT be hardcoded.

@app.route('/metrics')
def metrics():
    # Get db connection status
    response = app.response_class(
        response=json.dumps({"status": "success", "code": 0,
                             "data": {"db_connection_count": DbConnectionCount, "post_count": postsCounts}}),
        status=200,
        mimetype='application/json'
    )

    ## log line
    app.logger.info('Metrics request successful')
    return response


# start the application on port 3111
if __name__ == "__main__":
    ## stream logs to a file
    logging.basicConfig(filename='D:\\Udacity\\Nanodegree\\project\\techtrends\\app.log', level=logging.DEBUG)
    app.logger.info('Inicio')
    app.run(host='0.0.0.0', port='3111')
