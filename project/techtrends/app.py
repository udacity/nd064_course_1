import sqlite3
import logging
from datetime import datetime

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

# Count DB connections
db_connections_count = 0

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global db_connections_count
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    db_connections_count += 1
    return connection



# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Function to log messages
def log_msg(message, code = 0):
    '''
    This function logs messages. 
    message: text of the message
    code:    differentiates info log and error log. Defaults to 0
        0: info log
        1: error log
    '''
    time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    if code == 0:
        app.logger.info('{time} | {message}'.format(time=time, message=message))
    else:
        app.logger.error('{time} | {message}'.format(time=time, message=message))

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
        log_msg('Article id number "{id}" does not exist'.format(id = post_id), 1)
        return render_template('404.html'), 404
    else:
        title = post['title']
        log_msg('Article "{title}" retrieved'.format(title=title))
        return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    log_msg('About us page retrieved')
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

            log_msg('A new article "{title}" created'.format(title=title))
            return redirect(url_for('index'))

    return render_template('create.html')

# Healthcheck endpoint
@app.route('/healthz')
def healthcheck():
    response = ''
    try:
        connection = get_db_connection()
        connection.cursor()
        connection.execute("SELECT * FROM posts")
        connection.close()

        response = app.response_class(
            response = json.dumps({'result':'OK - healthy'}),
            status = 200,
            mimetype = 'application/json'
        )
        log_msg('Healthcheck request: OK')

    except:
        response = app.response_class(
            response = json.dumps({'result':'ERROR - unhealthy'}),
            status = 500,
            mimetype = 'application/json'
        )
        log_msg('Healthcheck request: not OK', 1)
    return response

# Metrics endpoint 
@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    posts_count = connection.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    connection.close()

    response = app.response_class(
        response = json.dumps({"db_connection_count": db_connections_count, "post_count": posts_count}),
        status = 200,
        mimetype = 'application/json')

    log_msg('Metrics request: OK')
    return response

# start the application on port 3111
if __name__ == "__main__":
    # stream logs to a console
    logging.basicConfig(level=logging.DEBUG)
    
    app.run(host='0.0.0.0', port='3111')
