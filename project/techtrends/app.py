import sqlite3
import os
from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
from logging.config import dictConfig
debugMode = os.environ.get("DEBUG") == "True"

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '%(levelname)s:%(module)s - [%(asctime)s] %(message)s',
    }},
    'handlers': {
        'stderr': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
            'formatter': 'default'
        },
        'stdout': {
             'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'default'
        }
        },
    'root': {
        'level': ('DEBUG','INFO')[debugMode],
        'handlers': ['stderr','stdout']
    }
})
# Function to get a database connection.
# This function connects to database with the name `database.db`
connections = 0;
  
def get_db_connection():
    global connections
    connections = connections+1
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
app.logger.setLevel
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
      app.logger.info('post id %s not found, rendering 404', post_id)  
      return render_template('404.html'), 404
    else:
      app.logger.info('Article %s retrieved successfully: %s', post_id, post['title'])
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info('rendering about page')
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
            app.logger.info('created a new article with title %s',title)
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/healthz')
def healthz():
    try:
        connection = get_db_connection()
        connection.execute('SELECT * FROM posts').fetchall()
        connection.close()
        response=app.response_class(json.dumps({"result":"OK - healthy"}),
        status=200,
        mimetype='application/json'
        )
    except Exception as e:
        response=app.response_class(json.dumps({"result":"ERROR - unhealthy"}),
        status=500,
        mimetype='application/json'
        )  
    return response

@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    global connections
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    postcount = len(posts)
    response = app.response_class(
        response=json.dumps({"db_connection_count":connections, "post_count": postcount}),
        status=200,
        mimetype='application/json'
    )
    return response

# start the application on port 3111
if __name__ == "__main__":
   app.run(host='0.0.0.0', port='3111',debug=debugMode)
