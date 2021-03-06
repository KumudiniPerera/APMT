from flask import Flask, render_template,request, redirect, url_for, session, flash, abort, g

#Flask Login
from flask_login import login_manager, UserMixin, login_user, login_required, logout_user, current_user, LoginManager 

#Mysql DB 
from flask_mysqldb import MySQL, MySQLdb

#Email  
from flask_mail import Mail,Message

#Role based authentication flask-user
from flask_user import roles_required

from itsdangerous import URLSafeTimedSerializer

# SoceketIO for chat tool
#from flask_socketio import SocketIO

#Commenting system
from flask_disqus import Disqus

import bcrypt
import sys
import yaml
from smtplib import SMTP
import re

#from user import User

#role based authentication
from functools import wraps
#from flask_user import roles_required

#Forms
from forms import SignupForm, LoginForm, TaskForm, ProjectForm, PasswordForm, RegisterForm

#Import flask-admin
#from flask_admin import Admin

app = Flask(__name__)
#socketio = SocketIO(app)
disq = Disqus(app)

#Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# ------------------------------ Configure DB ------------------------------------------------ #

db = yaml.load (open('db.yaml'))
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# ------------------------------ Configure Mail ------------------------------------------------ #

email = yaml.load(open('email.yaml'))
app.config['MAIL_SERVER'] = email['mail_server']
app.config['MAIL_PORT'] = email['mail_port']
app.config['MAIL_USERNAME'] = email['mail_username']
app.config['MAIL_PASSWORD'] = email['mail_password']
#app.config['MAIL_USE_TLS'] = email['mail_use_tls']
app.config['MAIL_USE_SSL'] = email['mail_use_ssl']

mail = Mail(app)

# ------------------------------ Dashboard ---------------------------------------------------- #

@app.route('/index')
def main():
    if(checkIFAuthenticated()):
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))

# ------------------------------ Signup ---------------------------------------------------- #

@app.route('/signup', methods= ['GET','POST'])
def signup():

    form = SignupForm(request.form)
    
    if request.method  == 'POST':
        #Fetch data
        userDetails = request.form

        username = userDetails['username']
        email = userDetails['email']
        password = userDetails['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        
        cur = mysql.connection.cursor()
        cur.execute ("INSERT INTO `user`(`userName`, `Email`, `Password`, `userrole_id`) VALUES (%s, %s, %s, 1)",(username ,email, hash_password ))
        mysql.connection.commit()

        session['name'] = username
        session['email'] = email

        cur.close()

        return redirect(url_for('main'))
        
    else:
        #use the below function to see the errors in validation
        print(form.errors)
        return render_template('signup.html' , form = form )

# ------------------------------ Login ---------------------------------------------------- #   

@app.route('/', methods= ['GET','POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':

        loginDetails = request.form

        email =loginDetails['email']
        password = loginDetails['password'].encode('utf-8')

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute ("SELECT * FROM `user` WHERE Email= %s",(email,))
        user = cur.fetchone()
        cur.close() 
        
        if (user):
            if(bcrypt.hashpw(password,user['Password'].encode('utf-8'))== user['Password'].encode('utf-8')):
                session['auth_level'] = user['userrole_id']
                
                return redirect(url_for('main'))
                
            else:
                flash('Invalid Email or Password !')
                return redirect(url_for('login'))

        else:
            flash('Invalid Email or Password !')
            return redirect(url_for('login'))     

    else:
        return render_template('login.html', form = form)

# ------------------------------ Logout ---------------------------------------------------- #

@app.route('/logout')
# @login_required
def logout():
    session.clear()

    flash('User logout successfully!')
    return redirect(url_for('login'))

# ------------------------------ User Profile ---------------------------------------------------- #

@app.route('/user')
def user():
    return render_template('user.html')

# ------------------------------ Register Developers ---------------------------------------------------- #

@app.route('/register', methods= ['GET','POST'])
# @required_roles('Admin')
def register():

    form = RegisterForm(request.form)
    
    if request.method  == 'POST':
        #Fetch data
        userDetails = request.form

        username = userDetails['username']
        email = userDetails['email']
        password = userDetails['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        
        cur = mysql.connection.cursor()
        cur.execute ("INSERT INTO `user`(`userName`, `Email`, `Password`, `userrole_id`) VALUES (%s, %s, %s, 2)",(username ,email, hash_password ))
        mysql.connection.commit()

        session['name'] = username
        session['email'] = email

        cur.close()

        return redirect(url_for('main'))
        
    else:
        #use the below function to see the errors in validation
        print(form.errors)
        return render_template('reguser.html' , form = form )

# ------------------------------ Table- user ---------------------------------------------------- #

@app.route('/table-list')
#@login_required
def tableList():

    cur = mysql.connection.cursor()
    resultvalue = cur.execute (" SELECT * FROM `user` ")   

    if resultvalue>0:
        userDetails = cur.fetchall()
        cur.close()

    cur = mysql.connection.cursor()
    resultvalue1 = cur.execute (" SELECT * FROM `project` ")   

    if resultvalue1>0:
        projectDetails = cur.fetchall()
        cur.close()

    cur = mysql.connection.cursor()
    resultvalue2 = cur.execute (" SELECT * FROM `task` ")  

    if resultvalue2>0:
        taskDetails = cur.fetchall()
        cur.close()

        return render_template('tables.html' , userDetails = userDetails, projectDetails= projectDetails, taskDetails=taskDetails)

# ------------------------------ Delete user ---------------------------------------------------- #  

@app.route('/delete-user/<string:id>')
@login_required
# @required_roles('admin')
def delete_user(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM `user` WHERE `userId`=%s", (id,))
        mysql.connection.commit()

        flash('User deleted successfully!')
        return redirect('/table-list')
        
    except Exception as e:
        print(e)

    finally:
        cur.close() 

# ------------------------------ Update user ---------------------------------------------------- #

@app.route('/edit-user/', methods= ['GET','POST'])
@login_required
@roles_required('Admin')
def edit_user():
    
    if request.method == 'POST':

        user_details = request.form

        userid = user_details['id']
        username = user_details['username']
        email = user_details['email']

        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE user
               SET userName=%s, Email=%s
               WHERE userId=%s
            """, (username, email, userid) )

        flash("Data Updated Successfully")
        mysql.connection.commit()
        cur.close()
        
        return redirect (url_for('tableList'))
                 
# ------------------------------ Add Tasks ---------------------------------------------------- #

@app.route('/task', methods= ['GET','POST'])
#@login_required
# @roles_required('Admin')
def tasks():
    form =TaskForm()
    
    if request.method == 'POST':
        
        task_details = request.form
        
        task_name = task_details['task_name']
        project = task_details['project']
        assignee = task_details['assignee']
        due_date = task_details['due_date']
        status = task_details['status']
        task_description = task_details['task_description']
        notag = re.sub("<.*?>", " ", task_description)
        
        cur = mysql.connection.cursor()
        cur.execute ("INSERT INTO `task`(`Task_Name`, `Task_description`, `Due_Date`, `Status`, `Project_Name`, `Assignee`) VALUES (%s, %s, %s, %s, %s, %s)",(task_name, notag, due_date, status, project, assignee  ))
        mysql.connection.commit()

        flash('Task added successfully!')
        cur.close()

        assignee = "%" + request.form['assignee'] + "%"
    
        cur = mysql.connection.cursor()
        cur.execute (f"SELECT `Email` FROM `user` WHERE `userName` LIKE '{assignee}'")
        recipient= cur.fetchone()
        cur.close()

        cur = mysql.connection.cursor()
        resultvalue = cur.execute (" SELECT * FROM `task` WHERE `Task_Name` = %s", (task_name,))  

        if resultvalue>0:
            taskDetail = cur.fetchall()
            cur.close()
            
            msg = Message('APMT', sender = 'dinlanka123@gmail.com', recipients = [recipient['Email']])
            #msg.body = "Hi,\n.\n\n"
            msg.html = render_template('mail.html', taskDetail=taskDetail)
            mail.send(msg)

        return redirect(url_for('tableList'))
    else:
        return render_template('task.html', form=form)
    
    
# ------------------------------ Delete Task ---------------------------------------------------- #  

@app.route('/delete-task/<string:id>')
#@login_required
@roles_required('Admin')
def delete_task(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM `task` WHERE `Task_ID`=%s", (id,))
        mysql.connection.commit()

        flash('Task deleted successfully!')
        return redirect('/table-list')
        
    except Exception as e:
        print(e)

    finally:
        cur.close() 

# ------------------------------ Update Task---------------------------------------------------- #

@app.route('/edit-task/', methods= ['GET','POST'])
#@login_required
@roles_required('Admin')
def edit_task():
    
    if request.method == 'POST':
        
        task_details = request.form

        taskid = task_details['id']
        task = task_details['task']
        project = task_details['project']
        assignee = task_details['assignee']
        due_date = task_details['due_date']
        status = task_details['status']
        description = task_details['description']

        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE `task` SET 
              `Task_Name`=%s,`Task_description`=%s,`Due_Date`=%s,`Status`=%s,`Project_Name`=%s,`Assignee`= %s
               WHERE `Task_ID`=%s
            """, (task, description, due_date, status, project, assignee, taskid) )

        mysql.connection.commit()

        flash("Data Updated Successfully")
        cur.close()
        
        return redirect (url_for('tableList'))


# ------------------------------ Add Projects ---------------------------------------------------- #

@app.route('/project', methods= ['GET','POST'])
@login_required
@roles_required('Admin')
def project():

    form =ProjectForm()

    if request.method == 'POST':
        
        project_details = request.form
        
        projectName = project_details['projectName']
        clientName = project_details['clientName']
        technology = project_details['technology']

        cur = mysql.connection.cursor()
        cur.execute ("INSERT INTO `project`(`Project`, `Client_Name`, `Technology`) VALUES (%s, %s, %s)",(projectName ,clientName, technology ))
        flash('Project added successfully!')
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('tableList'))

    return render_template('project.html', form=form)

# ------------------------------ Delete Project ---------------------------------------------------- #  

@app.route('/delete-project/<string:id>')
@login_required
@roles_required('Admin')
def delete_project(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM `project` WHERE `Project_ID`=%s", (id,))
        mysql.connection.commit()

        flash('Project deleted successfully!')
        return redirect('/table-list')
        
    except Exception as e:
        print(e)

    finally:
        cur.close() 

# ------------------------------ Update Project ---------------------------------------------------- #

@app.route('/edit-project/', methods= ['GET','POST'])
@login_required
@roles_required('Admin')
def edit_project():
    
    if request.method == 'POST':
        
        project_details = request.form

        projectid = project_details['id']
        project = project_details['project']
        client  = project_details['client']
        technology  = project_details['technology']

        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE `project` SET 
               `Project`=%s,`Client_Name`=%s,`Technology`=%s 
               WHERE Project_ID=%s
            """, (project, client, technology, projectid) )

        flash("Data Updated Successfully")
        mysql.connection.commit()
        cur.close()
        
        return redirect (url_for('tableList'))

# ------------------------------ Notifications ---------------------------------------------------- #

@app.route('/notifications')
@login_required
def notifications():
    return render_template('notifications.html')

# ------------------------------ Search ---------------------------------------------------- #

@app.route("/search", methods=['GET', 'POST'])
#@login_required
def search():

    if request.method == 'POST':

        search = "%" + request.form['search'] + "%"
    
        cur = mysql.connection.cursor()
        result = cur.execute (f"SELECT * FROM task WHERE Task_Name LIKE '{search}' OR Task_description LIKE '{search}' OR Project_Name LIKE '{search}' OR Assignee LIKE '{search}'")
        
        #cur = mysql.connection.cursor()
        #result1 = cur.execute (f"SELECT * FROM `user` WHERE `userName` LIKE '{search}' OR `Email` LIKE '{search}' ")
        
        #cur = mysql.connection.cursor()
        #result2 = cur.execute (f" SELECT * FROM `project` WHERE `Project` LIKE '{search}' OR `Project` LIKE '{search}' OR `Technology` LIKE '{search}'")
        
        if result>0:
            searchresultTask= cur.fetchall()
            cur.close()

        #if result1>0:
            #searchUser = cur.fetchall()
            #cur.close()

        #if result2>0:
            #searchProject = cur.fetchall()
            #cur.close()

            return render_template('search.html', searchresultTask = searchresultTask)

        else:
            return "No Results Found"

    return render_template('search.html', searchresult = [])
    
# ----------------------------- Reset password ----------------------------------------------------- #

@app.route('/reset' , methods= ['GET','POST'])
def reset_password():

    form = PasswordForm()

    if request.method == 'POST':
        
        user_details = request.form
        
        email =user_details['email']
        password = user_details['password'].encode('utf-8')
        
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute ("SELECT * FROM `user` WHERE Email= %s",(email,))
        user = cur.fetchone()
        cur.close()

        print(user)
        
        if (user):
            
            hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        
                
            cur = mysql.connection.cursor()
            cur.execute (" UPDATE `user` SET `Password`= %s  WHERE `Email`=%s", (hash_password, email))
            mysql.connection.commit()


            return render_template('reset_password.html', form = form)

        else:

            flash('User does not exist !')
            return redirect(url_for('reset_password'))     

    else:
        return render_template('email_password_reset.html', form = form)
        
# ------------------------------ Task Descriptions ---------------------------------------------------- #

@app.route('/task-details/<string:id>')
def task_details(id):

    cur = mysql.connection.cursor()
    resultvalue = cur.execute (" SELECT * FROM `task` WHERE `Task_ID`=%s", (id,))

    if resultvalue>0:
        taskDetails = cur.fetchall()
        cur.close()
    
    return render_template('Description.html', taskDetails=taskDetails)
    
# ------------------------------ Kanban Board ---------------------------------------------------- #

@app.route('/kanban')
def kanban_chart():

    cur = mysql.connection.cursor()
    resultvalue2 = cur.execute (" SELECT * FROM `task` ")  

    if resultvalue2>0:
        taskDetails = cur.fetchall()
        cur.close()

    return render_template ('kanban.html', taskDetails=taskDetails)



def checkIFAuthenticated():
    if('auth_level' in session):
        return True
    else:
        return False 

def returnAuthLevel():
    return session['auth_level']


# ------------------------------ Role based authentication ---------------------------------------------------- #

# def required_roles(*roles):
#     def wrapper(f):
#         @wraps(f)
#         def wrapped(*args, **kwargs):
#             if get_current_user_role() not in roles:
#                 flash('Authentication error, please check your details and try again','error')
#                 return redirect(url_for('index'))
#             return f(*args, **kwargs)
#         return wrapped
#     return wrapper
 
# def get_current_user_role():
#     return g.user.role


# ------------------------------ Main ---------------------------------------------------- #

if __name__ == "__main__":
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    ts = URLSafeTimedSerializer(app.secret_key)
    #socketio.run(app, debug=True)
    app.run(debug=True)
