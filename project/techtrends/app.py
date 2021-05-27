import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
import logging
import datetime
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


# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


# Define the main route of the web application

def hits_count():
    connection = get_db_connection()
    total = len(connection.execute('SELECT * FROM posts').fetchall())
    totalToString = str(total+1)
    ts = datetime.datetime.now().timestamp()
    connection.execute('INSERT INTO connections (created, total) VALUES (?, ?)',
                       (ts, totalToString))
    connection.commit()
    connection.close()


def get_total_count():
    connection = get_db_connection()
    total = connection.execute('SELECT * FROM connections').fetchall()
    connection.close()
    return len(total)


@ app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)


@ app.route('/healthz')
def healthcheck():
    response = app.response_class(
        response=json.dumps({"result": "OK - healthy"}),
        status=200,
        mimetype='application/json'
    )

    app.logger.info('Status request successfull')
    return response


@ app.route('/metrics')
def metrics():
    # Total amount of posts in the database
    connection = get_db_connection()
    count = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    counter = get_total_count()
    response = app.response_class(
        response=json.dumps(
            {"db_connection_count": counter, "post_count": str(len(count))}),
        status=200,
        mimetype='application/json'
    )
    app.logger.info('Metrics request successfull')
    return response

# Define how each individual article is rendered
# If the post ID is not found a 404 page is shown


@ app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)

    if post is None:
        app.logger.info('No article could be found')
        return render_template('404.html'), 404
    else:
        hits_count()
        postTitle = tuple(post)[2]
        app.logger.info('Article \"%s" retrieved!', postTitle)

        return render_template('post.html', post=post)

# Define the About Us page


@ app.route('/about')
def about():
    app.logger.info('About page successfully retrieved!')
    return render_template('about.html')

# Define the post creation functionality


@ app.route('/create', methods=('GET', 'POST'))
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

            app.logger.info('Article \"%s" successfully created!', title)

            return redirect(url_for('index'))

    return render_template('create.html')


# start the application on port 3111
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(host='0.0.0.0', port='3111')
