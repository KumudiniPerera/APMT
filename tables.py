from flask_table import Table, Col, LinkCol
 
class User(Table):
    userId = Col('ID', show=True)
    userName = Col('Name')
    Email = Col('Email')
    delete = LinkCol('Delete', 'delete_user', url_kwargs=dict(userId='userId'))
    edit = LinkCol('Edit', 'edit_view', url_kwargs=dict(id='userId'))
    


    
