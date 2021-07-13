from flask_table import Table, Col, LinkCol
 
class Results(Table):
    model_id = Col('Id', show=False)
    model_code = Col('Code')
    model_year = Col('Year')
    model_name_za = Col('Model')
    make_name = Col('Make')
    created=Col('Created')
    modified=Col('Modified')
    edit = LinkCol('Edit', 'edit_view', url_kwargs=dict(id='model_id'))
    delete = LinkCol('Delete ', 'delete_user', url_kwargs=dict(id='model_id'))

class BodyType(Table):
    body_id = Col('Id', show=False)
    body_type = Col('Body')
    doors = Col('Doors')
    created = Col('Created')
    modified = Col('Modified')
    edit = LinkCol('Edit','edit_view',url_kwargs=dict(id='body_id'))
    delete = LinkCol('Delete','delete_boy',url_kwargs=dict(id='body_id'))