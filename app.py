from flask import Flask, render_template,request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb

import bcrypt

from user import User

from forms import SignupForm, LoginForm, TaskForm

import yaml

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

    if form.validate_on_submit():  

        #Fetch data
        #userDetails = request.form

        #username = (userDetails['username'])
        #email = (userDetails['email'])
        #password = (userDetails['pass'].encode('utf-8'))
        #hash_password = (bcrypt.hashpw(password, bcrypt.gensalt()))

        username = form.username.data
        email = form.email.data
        password = (form.password.data).encode('utf-8')
        hash_password = (bcrypt.hashpw(password, bcrypt.gensalt()))
    
        cur = mysql.connection.cursor()
        cur.execute ("INSERT INTO `user`(`UserName`, `Email`, `Password`) VALUES (%s, %s, %s)",(username ,email, hash_password ))
        mysql.connection.commit()

        session['name'] = username
        session['email'] = email

        cur.close()

        return redirect(url_for('main' )) 

    return render_template('signup.html' , form = form )
        
@app.route('/', methods= ['GET','POST'])
def login():

    form = LoginForm()

    if request.method == 'POST':

        #userDetails1 = request.form

        email = form.email.data
        password = (form.password.data).encode('utf-8')
        #userDetails1['email']
        #password = userDetails1['pass'].encode('utf-8')

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
    resultValue = cur.execute ("SELECT `userId`, `UserName`, `email` FROM `user`")
    if resultValue > 0:
        userDetails = cur.fetchall()
        print(userDetails)
    return render_template('tables.html' , userDetails=userDetails)

@app.route('/notifications')
def notifications():
    return render_template('notifications.html')

@app.route('/task')
def tasks():
    form =TaskForm()
    return render_template('task.html', form=form)

if __name__ == "__main__":
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.run(debug=True)
