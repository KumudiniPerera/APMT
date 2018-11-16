from flask import Flask, render_template,request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb

import bcrypt
import yaml
import sys

from forms import SignupForm, LoginForm, TaskForm, ProjectForm
from tables import User

app = Flask(__name__)

#Configure DB
db = yaml.load (open('db.yaml'))
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/index')
def main():
    return render_template('dashboard.html')

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
        cur.execute("SELECT `UserId` FROM `user`")
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
                return redirect(url_for('login'))

        else:
            return redirect(url_for('login'))     

    else:
        return render_template('login.html', form = form)

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/table-list')
def tableList():

    cur = mysql.connection.cursor()
    resultValue = cur.execute (" SELECT `userId`, `userName`, `Email` FROM `user` ")
    
    if resultValue > 0:
        userDetails = cur.fetchall()
        table = User(userDetails)
        
    return render_template('tables.html' , table= table)

@app.route('/notifications')
def notifications():
    return render_template('notifications.html')

@app.route('/task', methods= ['GET','POST'])
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
        
        cur = mysql.connection.cursor()
        cur.execute ("INSERT INTO `task`(`Task_Name`, `Task_description`, `Due_Date`, `Status`, `Project_Name`, `Assignee`) VALUES (%s, %s, %s, %s, %s, %s)",(task_name, task_description, due_date, status, project, assignee  ))
        mysql.connection.commit()

        cur.close()

        return redirect(url_for('main'))
    else:
        return render_template('task.html', form=form)

@app.route('/project', methods= ['GET','POST'])
def project():

    form =ProjectForm()

    if request.method == 'POST':
        
        project_details = request.form
        
        projectName = project_details['projectName']
        clientName = project_details['clientName']
        technology = project_details['technology']
   
        cur = mysql.connection.cursor()
        cur.execute ("INSERT INTO `project`(`Project`, `Client_Name`, `Technology`) VALUES (%s, %s, %s)",(projectName ,clientName, technology ))
        mysql.connection.commit()

        cur.close()

        return redirect(url_for('main'))

    return render_template('project.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/delete/')
def delete_user(userId):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM `user` WHERE `userId`=%s", (userId,))
        mysql.connection.commit()

        #flash('User deleted successfully!')
        return redirect('/table-list')
        
    except Exception as e:
        print(e)

    finally:
        cur.close() 

@app.route('/edit/')
def edit_view(id):
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM tbl_user WHERE user_id=%s", id)
        row = cur.fetchone()
        
        if row:
            return render_template('edit.html', row=row)

        else:
            return 'Error loading #{id}'.format(id=id)
               
    finally:
        cur.close()

if __name__ == "__main__":
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.run(debug=True)
