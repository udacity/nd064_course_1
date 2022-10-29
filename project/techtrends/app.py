from multiprocessing import connection
import sqlite3
import logging
import sys
from tkinter import W
from turtle import screensize

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

logger = None

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
        logger.info("Article for post id \"{}\" does not exist! a 404 page is returned".format(post_id))
        return render_template('404.html')        
    else:        
        logger.info("Article \"{}\" retrieved!".format(post['title']))
        return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    logger.info("The \"About Us\" page is retrieved.")
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

            logger.info("Article \"{}\" is created.".format(title))
            
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/healthz')
def healthz():
    logger.info("healthz called")
    response = app.response_class(
    response = json.dumps({'result' : 'Ok - healthy'}), 
    status = 200,
    mimetype="application/json"
    )
    return response

@app.route('/metrics')
def metrics():
    logger.info("metrics called")   
    
    connection = get_db_connection()
    post_count = connection.execute('SELECT count(*) FROM posts').fetchone()
    tables = connection.execute('SELECT name FROM sqlite_master WHERE type=\'table\'').fetchall()  
    response = app.response_class(
    response = json.dumps({"db_connection_count": 1, "post_count": post_count[0]}), 
    status = 200,
    mimetype="application/json"    
    )

    connection.close()
    return response


def setup_logger():    
    #logging.basicConfig(filename='app.log',level=logging.DEBUG, format='%(levelname)s %(asctime)-8s %(message)s', datefmt='%d/%m/%Y, %H:%M:%S')   
    formatter = logging.Formatter(fmt='%(levelname)s %(asctime)-8s %(message)s', datefmt='%d/%m/%Y, %H:%M:%S')
    handler = logging.FileHandler('tech_trend_log.txt')
    handler.setFormatter(formatter)
    
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)

    logger_temp = logging.getLogger("app")
    logger_temp.setLevel(logging.INFO)    
    logger_temp.addHandler(handler)
    logger_temp.addHandler(screen_handler)
    return logger_temp

# start the application on port 3111
if __name__ == "__main__":
    
   #logging.basicConfig(filename='app.log',level=logging.DEBUG, format='%(levelname)s %(modulename)s %(asctime)-8s %(message)s', datefmt='%d/%m/%Y, %H:%M:%S')   
   #global logger
   logger = setup_logger()
   app.run(host='0.0.0.0', port='3111')
