import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

DATABASE_FILE = 'database.db'
PORT = '3111'

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect(DATABASE_FILE)
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
        return render_template('404.html'), 404
    else:
        return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
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


@app.route('/healthz')
def healthz():
    """Validates application health.

    healthz() will check the connection with SQLite database by starting a connection and performing a test query.

    Returns:
        json: a JSON object with 'result' key holding state of the application health and 'reason' key in case the application is unhealthy
    """
    res = dict()
    status_code = 200
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cur = conn.cursor()
        # simple test query
        cur.execute('SELECT 1').fetchone()
    except Exception as e:
        result = 'NOT OK - unhealthy'
        status_code = 500
        res['reason'] = str(e)
    else:
        result = 'OK - healthy'
    finally:
        conn.close()
        res['result'] = result
        return app.response_class(
            response=json.dumps(res),
            status=status_code,
            mimetype='application/json'
        )


# start the application on port 3111
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)
