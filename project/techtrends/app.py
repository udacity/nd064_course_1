from gc import collect
from poplib import POP3_SSL_PORT
import sqlite3
import logging
from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
from flask import has_request_context, request
from datetime import date, datetime

# https://flask.palletsprojects.com/en/2.0.x/logging/
from logging.config import dictConfig

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hit me baby, one more time!'

# set and initialize collections object to track metric information
collections_obj = {
        'db_connection_count': 0,
        'post_count': 0
}



# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post


# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    collections_obj['db_connection_count'] += 1
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.info(f'Article {post_id} non-existent, unable to retrieve.')
      return render_template('404.html'), 404
    else:
      app.logger.info('Article "{}" retrieved'.format(post['title']))
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info(f'About Us page retreived.')
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
            collections_obj['db_connection_count'] += 1
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            app.logger.info(f'Article "{title}" created.')
            return redirect(url_for('index'))

    return render_template('create.html')

# Define the post creation functionality 
@app.route('/healthz')
def healthcheck():
    response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
    )
    return response

def get_posts_metrics(collections_obj):
    """
    Gather posts metrics into the collection_obj
    Parameters:
    collection_obj: metric information
    """
    connection = get_db_connection()
    collections_obj['db_connection_count'] += 1
    posts_count = connection.execute('SELECT count(*) FROM posts').fetchone()
    connection.close()
    collections_obj['post_count'] = posts_count[0]

def metrics():
    """
    Display metrics gathered within the collection_obj
    """
    get_posts_metrics(collections_obj)
    response = app.response_class(
        response=json.dumps(collections_obj),
        status=200,
        mimetype='application/json')
    app.logger.info(f'/metrics route handler called. db_connections: {collections_obj["db_connection_count"]}, {collections_obj["post_count"]}')
    return response
app.add_url_rule('/metrics', 'metrics', metrics)

# start the application on port 3111
if __name__ == "__main__":

    # INFO:werkzeug:127.0.0.1 - - [08/Jan/2021 22:40:06] "GET /metrics HTTP/1.1" 200 -
    # INFO:werkzeug:127.0.0.1 - - [08/Jan/2021 22:40:09] "GET / HTTP/1.1" 200 -
    # INFO:app:01/08/2021, 22:40:10, Article "2020 CNCF Annual Report" retrieved!
    logging.basicConfig(level=logging.DEBUG,format='%(levelname)s:%(name)s:%(asctime)s, %(message)s')

    # add a customer handler to app logger https://docs.python.org/3/howto/logging-cookbook.html#logging-to-multiple-destinations
    logger = logging.getLogger('app')
    logger.setLevel(logging.DEBUG)
    app_file_handler = logging.FileHandler('app.log')
    formatter = logging.Formatter('%(levelname)s:%(name)s:%(asctime)s, %(message)s',datefmt='%d/%m/%Y, %H:%H:%S')
    app_file_handler.setFormatter(formatter)
    app_file_handler.setLevel(logging.DEBUG)
    logger.addHandler(app_file_handler)
    
    app.run(host='0.0.0.0', port='3111')
