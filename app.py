from flask import Flask, render_template,request, redirect, url_for, session, flash
from flask_mysqldb import MySQL, MySQLdb
from flask_datepicker import datepicker

import bcrypt
import sys
import yaml

from user import User
from forms import SignupForm, LoginForm, TaskForm, ProjectForm

app = Flask(__name__)

# ------------------------------ Configure DB ------------------------------------------------ #

db = yaml.load (open('db.yaml'))
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
datepicker(app)

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
                return redirect(url_for('login'))

        else:
            return redirect(url_for('login'))     

    else:
        return render_template('login.html', form = form)

# ------------------------------ Logout ---------------------------------------------------- #

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ------------------------------ User Profile ---------------------------------------------------- #

@app.route('/user')
def user():
    return render_template('user.html')

# ------------------------------ Table- user ---------------------------------------------------- #

@app.route('/table-list')
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


        return render_template('tables.html' , userDetails = userDetails, projectDetails= projectDetails)

# ------------------------------ Delete user ---------------------------------------------------- #  

@app.route('/delete-user/<string:id>')
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

# ------------------------------ Update- user ---------------------------------------------------- #

@app.route('/edit-user/', methods= ['GET','POST'])
def edit_user(id):
    
    if request.method == 'POST':
        
        user_details = request.form

        userid = user_details['id']
        print(userid)
        username = user_details['username']
        print(username)
        email = user_details['email']
        print(email)

        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE user
               SET name=%s, email=%s
               WHERE userId=%s
            """, (username, email, userid) )

        flash("Data Updated Successfully")

        cur.commit()
        
        return redirect (url_for('tableList'))
                      
# ------------------------------ Add Tasks ---------------------------------------------------- #

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

# ------------------------------ Add Projects ---------------------------------------------------- #

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

# ------------------------------ Delete Projecr ---------------------------------------------------- #  

@app.route('/delete-project/<string:id>')
def delete_project(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM `project` WHERE `Project_ID`=%s", (id,))
        mysql.connection.commit()

        flash('User deleted successfully!')
        return redirect('/table-list')
        
    except Exception as e:
        print(e)

    finally:
        cur.close() 
# ------------------------------ Notifications ---------------------------------------------------- #

@app.route('/notifications')
def notifications():
    return render_template('notifications.html')

# ------------------------------ Main ---------------------------------------------------- #

if __name__ == "__main__":
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.run(debug=True)
