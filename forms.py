from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class SignupForm(FlaskForm):
    username = StringField('User Name' , validators= [DataRequired(), Length(min =3)], render_kw={"placeholder": "Your Name"})
    email = StringField('Email' , validators=[DataRequired(), Email(), Length(min = 9)], render_kw={"placeholder": "Your Email"})
    password = PasswordField('Password' , validators=[DataRequired(), Length(min = 8)], render_kw={"placeholder": "Password"})

######################################################################################################################################################################
   
class LoginForm(FlaskForm):
    email = StringField('Email' , validators=[DataRequired, Email(), Length(min = 9, max= 50)], render_kw={"placeholder": "Email"})
    password = PasswordField('Password' , validators=[DataRequired, Length(min = 8)], render_kw={"placeholder": "Password"})

######################################################################################################################################################################

class TaskForm(FlaskForm):
    task_name = StringField('User Name' , validators= [DataRequired(), Length(min =3)], render_kw={"placeholder": "Task Name"})
    projectname = StringField('Project Name', validators= [DataRequired(), Length(min =3)],render_kw={"placeholder": "Project Name"})
    assignee = StringField('Assignee Name', validators= [DataRequired(), Length(min =3)],render_kw={"placeholder": "Assignee Name"})
    due_date = DateField('Due Date' ,render_kw={"placeholder": "Due Date"})
    status = SelectField(u'Status', choices=[('In Progress','In Progress' ), ('Completed', 'Completed'), ('Hold', 'Hold')])
    task_description = TextAreaField('Task Description' , validators= [DataRequired(), Length(max =200)], render_kw={"placeholder": "Task Description"})

######################################################################################################################################################################

class ProjectForm(FlaskForm):
    project_name = StringField('Project Name' , validators= [DataRequired(), Length(min =3)], render_kw={"placeholder": "Project Name"})
    client_name = StringField('Client Name', validators= [DataRequired(), Length(min =3)],render_kw={"placeholder": "Client Name"})
    technology = StringField('Technology', validators= [DataRequired(), Length(min =3)],render_kw={"placeholder": "Technolgy"})
    