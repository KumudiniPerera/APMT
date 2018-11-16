from flask_table import Table, Col
 
class Task(Table):
    id = Col('Id', show=False)
    task = Col('task_name')
    assignee = Col('assignee')
    project = Col('project')
    due_date = Col('due_date')
    status = Col('status')
    task_description = Col('task_description')
    
