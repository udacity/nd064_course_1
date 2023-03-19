import sqlite3
import logging
import sys

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

# Function to get a database connection.
# This function connects to database with the name `database.db`


def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    connection.execute(
        'UPDATE DatabaseConnection SET numOfConnection = numOfConnection + 1 WHERE id = 1').fetchone()
    connection.commit()

    return connection

# Function to get a post using its ID


def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ? and title <> "Homepage"',
                              (post_id,)).fetchone()
    connection.close()
    return post

# Function to count the total connection to the database


def count_dbConnection():
    connection = get_db_connection()
    num_of_connection = connection.execute(
        'SELECT numOfConnection FROM DatabaseConnection').fetchone()
    connection.close()
    return num_of_connection[0]

# Function to count the number of posts in the database


def count_post():
    connection = get_db_connection()
    post_count = connection.execute('SELECT COUNT(id) FROM posts').fetchone()
    connection.close()
    return post_count[0] - 1  # -1 of homepage


# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application


@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute(
        'SELECT id, title, created FROM posts WHERE title <> "Homepage"').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered
# If the post ID is not found a 404 page is shown


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        app.logger.debug(
            'A non-existing article is accessed and a 404 page is returned.')
        return render_template('404.html'), 404
    else:
        app.logger.debug('Article "' + post['title'] + '"retrieved!')
        return render_template('post.html', post=post)


@app.route('/healthz')
def healthz():
    try:
        connection = get_db_connection()
        connection.execute('SELECT id FROM posts').fetchall()
        response = app.response_class(
            response=json.dumps({"result": "OK - healthy"}),
            status=200,
            mimetype='application/json'
        )
    except:
        response = app.response_class(
            response=json.dumps({"result": "ERROR - Something went wrong!!!"}),
            status=500,
            mimetype='application/json'
        )

    return response

# Define the metrics endpoint


@app.route('/metrics')
def metrics():
    response = app.response_class(
        response=json.dumps(
            {"db_connection_count": count_dbConnection(), "post_count": count_post()}),
        status=200,
        mimetype='application/json'
    )
    return response

# Define the About Us page


@app.route('/about')
def about():
    app.logger.debug('The "About Us" page is retrieved')
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
            app.logger.debug('A new article "' + title + '"is created!')
            return redirect(url_for('index'))

    return render_template('create.html')


# start the application on port 3111
if __name__ == "__main__":
    logging.basicConfig(
        format='%(levelname)s:%(name)s:%(asctime)s, %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    app.run(host='0.0.0.0', port='3111')
