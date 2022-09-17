from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, PasswordField, EmailField, SelectField
from wtforms.validators import DataRequired

# Admin
class UserForm(FlaskForm):
    id = HiddenField('id')
    username = StringField('Usuário', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    isadmin = SelectField('É administrador?', choices=[('0', 'Não'), ('1', 'Sim')])
    submit = SubmitField('Enviar')

class EmailForm(FlaskForm):
    id = HiddenField('id')
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Enviar')

class PasswordForm(FlaskForm):
    id = HiddenField('id')
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Enviar')

# Login

class LoginForm(FlaskForm):
    id = HiddenField('id')
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    isadmin = HiddenField('0')
    submit = SubmitField('Login')
