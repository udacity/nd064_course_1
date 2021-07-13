from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'dhara'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Codembinga$'
app.config['MYSQL_DATABASE_DB'] = 'AutoCatalog'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


