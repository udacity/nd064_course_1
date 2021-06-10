import sqlite3
import logging

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
from datetime import datetime
from datetime import date


# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    now = datetime.now()
    today = date.today()       
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()   
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
logging.basicConfig(level=logging.DEBUG)


# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    now = datetime.now()
    today = date.today()       
    app.logger.info(today.strftime("%d/%m/%Y")+", "+now.strftime("%H:%M:%S")+" From @app.route('/'): All artices displayed!")        
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    now = datetime.now()
    today = date.today()
    if post is None:
      app.logger.error(today.strftime("%d/%m/%Y")+", "+now.strftime("%H:%M:%S")+" From @app.route('/<int:post_id>'): Artice with id: "+str(post_id)+" cannot be retrieved!")        
      return render_template('404.html'), 404
    else:
      post = get_post(post_id)
      app.logger.info(today.strftime("%d/%m/%Y")+", "+now.strftime("%H:%M:%S")+" From @app.route('/<int:post_id>'): Artice "+post[2]+" retrieved!")
      #app.logger.info(now.strftime("%H:%M:%S"))
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    now = datetime.now()
    today = date.today()    
    app.logger.info(today.strftime("%d/%m/%Y")+", "+now.strftime("%H:%M:%S")+" From @app.route('/about'): About Us retrieved!")
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
            now = datetime.now()
            today = date.today()               
            app.logger.error(today.strftime("%d/%m/%Y")+", "+now.strftime("%H:%M:%S")+" From @app.route('/create', methods=('GET', 'POST')): No title specified for new article!")
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            now = datetime.now()
            today = date.today()  
            app.logger.info(today.strftime("%d/%m/%Y")+", "+now.strftime("%H:%M:%S")+" From @app.route('/create', methods=('GET', 'POST')): Article with title "+title+" added to database")

            return redirect(url_for('index'))

    return render_template('create.html')
	
# Define the healthcheck functionality 
@app.route('/healthz')
def status():
    data = {"OK": "healthy"}
    return jsonify(data), 200

# Define the metrics functionality 
@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    posts = connection.execute('SELECT COUNT(*) FROM posts AS CNT').fetchone()
    
    connection.close()
    
    data = {"db_connection_count": 1, "post_count": posts[0]}
    return jsonify(data), 200	

# start the application on port 3111
if __name__ == "__main__":
   app.run(host='0.0.0.0', port='3111')
