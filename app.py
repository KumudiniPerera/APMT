from flask import Flask, render_template,request, redirect, url_for, session, flash, abort

#Flask Login
from flask_login import login_manager, UserMixin, login_user, login_required, logout_user, current_user, LoginManager 

#Mysql DB 
from flask_mysqldb import MySQL, MySQLdb

#Email  
from flask_mail import Mail,Message

#Role based authentication flask-user
from flask_user import roles_required

from itsdangerous import URLSafeTimedSerializer

import bcrypt
import sys
import yaml
from smtplib import SMTP
import re

from user import User

#Forms
from forms import SignupForm, LoginForm, TaskForm, ProjectForm, PasswordForm, EmailForm

#Import flask-admin
#from flask_admin import Admin

app = Flask(__name__)

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
    return render_template('dashboard.html')

# ------------------------------ Signup ---------------------------------------------------- #

@app.route('/signup', methods= ['GET','POST'])
def signup():

    form = SignupForm(request.form)
    
    if request.method  == 'POST'and form.validate():
        #Fetch data
        userDetails = request.form

        username = userDetails['username']
        email = userDetails['email']
        password = userDetails['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        
        cur = mysql.connection.cursor()
        cur.execute ("INSERT INTO `user`(`UserName`, `Email`, `Password`) VALUES (%s, %s, %s)",(username ,email, hash_password ))
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
@login_required
def logout():
    session.clear()

    flash('User logout successfully!')
    return redirect(url_for('login'))

# ------------------------------ User Profile ---------------------------------------------------- #

@app.route('/user')
def user():
    return render_template('user.html')

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
@roles_required('Admin')
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
        print("that")
        
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
#@roles_required('Admin')
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

        return redirect(url_for('tableList'))
    else:
        return render_template('task.html', form=form)

# ------------------------------ Delete Task ---------------------------------------------------- #  

@app.route('/delete-task/<string:id>')
#@login_required
#@roles_required('Admin')
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
@login_required
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

        search = request.form['search']
    
        cur = mysql.connection.cursor()
        result = cur.execute (" SELECT * FROM `task` WHERE `Task_Name` LIKE '%%%s%%' OR `Task_description` LIKE '%%%s%%' OR `Project_Name` LIKE '%%%s%%' OR `Assignee` LIKE '%%%s%%' ",(search, search, search, search))
        
        #cur = mysql.connection.cursor()
        #result1 = cur.execute (" SELECT * FROM `user` WHERE `userName` LIKE '%%%s%%' OR `Email` LIKE '%%%s%%' ", (search, search))
        
        #cur = mysql.connection.cursor()
        #result2 = cur.execute (" SELECT * FROM `project` WHERE `Project` LIKE '%%%s%%' OR `Project` LIKE '%%%s%%' OR `Technology` LIKE '%%%s%%'", (search, search, search))
 
        if result>0:
            searchresult = cur.fetchall()
            cur.close()

        else:
            return "No Results Found"
    
    return render_template('search.html', searchresult = searchresult)
        
# ----------------------------- Mail ----------------------------------------------------- #

@app.route("/mail")
#@login_required
def Email():

    msg = Message('Hello', sender = 'dinlanka123@gmail.com', recipients = ['kumudiniaccura@gmail.com'])
    msg.body = "This is the email body"
    mail.send(msg)
    
    return "Sent"

# ----------------------------- Reset password ----------------------------------------------------- #

@app.route('/reset')
def send_password_reset_email(user_email):
    password_reset_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
 
    password_reset_url = url_for(
        'users.reset_with_token',
        token = password_reset_serializer.dumps(user_email, salt='password-reset-salt'),
        _external=True)
 
    html = render_template(
        'email_password_reset.html',
        password_reset_url=password_reset_url)
 
    send_email('Password Reset Requested', [user_email], html)

@app.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        abort(404)
 
    form = PasswordForm()
 
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first_or_404()
 
        user.password = form.password.data
 
        db.session.add(user)
        db.session.commit()
 
        return redirect(url_for('signin'))
 
    return render_template('reset_with_token.html', form=form, token=token)

# ------------------------------ Main ---------------------------------------------------- #

if __name__ == "__main__":
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    ts = URLSafeTimedSerializer(app.secret_key)
    app.run(debug=True)
