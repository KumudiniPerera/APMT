from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, DateField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_wysiwyg.wysiwyg import WysiwygField

class SignupForm(Form):
    username = StringField('User Name' , validators= [DataRequired(), Length(min =3)])
    email = StringField('Email' , validators=[DataRequired(), Email(), Length(min = 9)])
    password = PasswordField('Password' , validators=[DataRequired(), Length(min = 8)])

######################################################################################################################################################################
   
class LoginForm(Form):
    email = StringField('Email' , validators=[DataRequired, Email(), Length(min = 9, max= 50)])
    password = PasswordField('Password' , validators=[DataRequired, Length(min = 8)])

######################################################################################################################################################################

class TaskForm(Form):
    task_name = StringField('User Name' , validators= [DataRequired(), Length(min =3)])
    assignee = StringField('Assignee Name', validators= [DataRequired(), Length(min =3)])
    project = StringField('Project', validators= [DataRequired(), Length(min =3)])
    due_date = DateField('Due Date' ,format="%M/%D/%Y")
    status = SelectField(u'Status', choices=[('-- --','None' ), ('In Progress','In Progress' ), ('Completed', 'Completed'), ('Hold', 'Hold')])
    task_description =TextAreaField ('Task Description' , validators= [DataRequired(), Length(max =200)])
#WysiwygField

######################################################################################################################################################################

class ProjectForm(Form):
    projectName = StringField('Project Name' , validators= [DataRequired(), Length(min =3)])
    clientName = StringField('Client Name', validators= [DataRequired(), Length(min =3)])
    technology = StringField('Technology', validators= [DataRequired(), Length(min =3)])

#######################################################################################################################################################################

class PasswordForm(Form):
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=40)])
    
#########################################################################################################################################################################

