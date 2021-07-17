from typing import NoReturn
import pymysql
from app import app
from tables import BodyType
from tables import Results
from db_config import mysql
from flask import flash, render_template, request, redirect, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

links = [
    {'name': 'Home', 'url': ''},
    {'name': 'View Models', 'url': '/models'},
    {'name': 'Create Models', 'url': '/create'}
]


@app.route('/')
def home():
    """KS Auto Parts Catalog"""

    return render_template('home.html',
                           title="Catalog",
                           description="Catalog System",
                           links=links
                           )


@app.route('/models')
def models():
    conn = None
    cursor = None
    _select = "SELECT main.model_id, main.model_code, main.model_year, main.model_name_za, main.created, main.modified,  minor.make_name"
    _from = " FROM model AS main"
    _join = " INNER JOIN  make AS minor ON main.key_make = minor.make_id"
    _order = " ORDER BY main.modified desc"
    _sql = _select + _from + _join + _order

    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(_sql)
        rows = cursor.fetchall()
        table = Results(rows)
        table.border = True
        return render_template('models.html', table=table, links=links, rows=rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/edit/<int:id>')
def edit_view(id):
    conn = None
    cursor = None
    _select = "SELECT main.model_id,main.model_code,main.model_year,main.model_name_za,main.key_make "
    _from = " FROM model AS main "
    _join = " INNER JOIN make AS minor ON main.key_make = minor.make_id"
    _select2 = "SELECT make_id, make_name,make_abbreviation "
    _from2 = " FROM make"
    _sql = _select + _from + _join
    _sql2 = _select2 + _from2
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(_sql + " WHERE model_id=%s ", id)
        model_row = cursor.fetchone()
        cursor.execute(_sql2)
        make_rows = cursor.fetchall()
        if model_row and make_rows:
            return render_template('edit.html', model_row=model_row, make_rows=make_rows)
        else:
            return 'Record #{id} is missing'.format(id=id)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/new_model')
def add_user_view():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("Select make_id,make_name,make_abbreviation FROM make")
        rows = cursor.fetchall()
        if rows:
            return render_template('add.html',
                                   title="Create New Model",
                                   description="Catalog System add a new model to the system",
                                   field_titles="New Model",
                                   rows=rows)
        else:
            return 'No Makes have been added to the system yet'
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/add_model', methods=['POST'])
def add_model():
    conn = None
    cursor = None
    try:
        _code = request.form['inputModelCode']
        _year = request.form['inputModelYear']
        _name = request.form['inputModelName']
        _make = request.form['inputSelectMake']
        # validate the received values
        if _code and _year and _name and _make and request.method == 'POST':
            # do not save password as a plain text
            # _hashed_password = generate_password_hash(_password)
            # save edits
            sql = "INSERT INTO model( model_code, model_year, model_name_za, key_make) VALUES(%s, %s, %s)"
            data = (_code, _year, _name, _make)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            flash('Model added successfully!')
            return redirect('/models')
        else:
            return 'Error while adding model'
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/body')
def vehicle_body():
    conn = None
    cursor = None
    # _select = "SELECT body_id, body_type, doors, created, modified "
    _select = " SELECT *"
    _from = " FROM body"
    _sql = _select + _from
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(_sql)
        body_rows = cursor.fetchall()
        table = BodyType(body_rows)
        table.border = True
        if body_rows:
            return render_template('body.html',
                                   title="View Body Types",
                                   description="Catalog System view all vehicle body types defined in the system",
                                   field_titles="New Model",
                                   body_rows=body_rows                
			                  )			
        else:
            return 'No body types have been added to the system yet !'
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/new_body')
def create_body():
    return render_template(
        'add_body.html',
        title="Create New Body",
        description="Add new body type to the system",       
	    field_titles="New Body",
    )

@app.route('/save', methods=['POST'])
def save():
	conn = None
	cursor = None

	try:
		_type = request.form['bodyType']	
		_doors = request.form['doors']

		if _type and _doors and request.method == 'POST':
			sql = "INSERT INTO body( body_type, doors) VALUES(%s, %s)"
			data = (_type, _doors)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			return redirect('/body')
		else:
			flash('Error while saving your data')
			return redirect('new_body')
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/update', methods=['POST'])
def update_model():
    conn = None
    cursor = None
    try:
        _code = request.form['inputModelCode']
        _year = request.form['inputModelYear']
        _model = request.form['inputModelName']
        _id = request.form['id']
        _make = request.form['inputSelectMake']
        # validate the received values
        if _code and _year and _model and _id and _make and request.method == 'POST':
            # do not save password as a plain text
            # _hashed_password = generate_password_hash(_password)
            # print(_hashed_password)
            # save edits
            sql = "UPDATE model SET model_code=%s, model_year=%s, model_name_za=%s, key_make=%s WHERE model_id=%s"
            data = (_code, _year, _model, _make, _id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            flash("Model updated successfully!")
            return redirect('/models')
        else:
            return 'Error while updating user'
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/delete/<int:id>')
def delete_user(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM model WHERE model_id=%s", (id,))
        conn.commit()
        flash('Model deleted successfully!')
        return redirect('/models')
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()




if __name__ == "__main__":
    app.run(host='0.0.0.0')
