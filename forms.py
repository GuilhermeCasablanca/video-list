from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, PasswordField, EmailField, SelectField
from wtforms.validators import DataRequired

# Stream

class StreamForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Nome', validators=[DataRequired()])
    video_src = StringField('Local', validators=[DataRequired()])
    submit = SubmitField('Enviar')

# Orientação

class OrientacaoForm(FlaskForm):
    id = HiddenField('id')
    orientacao = StringField('Orientação', validators=[DataRequired()])
    submit = SubmitField('Enviar')

# Tamanho

class SizeForm(FlaskForm):
    id = HiddenField('id')
    width = StringField('Width', validators=[DataRequired()])
    height = StringField('Height', validators=[DataRequired()])
    submit = SubmitField('Enviar')

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

