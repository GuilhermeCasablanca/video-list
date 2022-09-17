from flask import Blueprint, current_app, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from forms import UserForm, EmailForm, PasswordForm
from models import UserModel
from crud import Crud


admin_bp = Blueprint('admin_bp', __name__,
                    template_folder='templates')


# Roteamento web do admin

@admin_bp.route('/admin/index')
@login_required
def admin():
    if not current_user.isadmin:
        return current_app.login_manager.unauthorized()
    return render_template('admin/index.html')


@admin_bp.route('/admin/create/user', methods=["GET", "POST"])
@login_required
def create_user():
    if not current_user.isadmin:
        return current_app.login_manager.unauthorized()

    crud = Crud()
    form = UserForm()
    form.submit.label.text = "Cadastrar"
    if form.validate_on_submit():
        user = UserModel()
        user.set_username(form.username.data)
        user.set_email(form.email.data)
        user.set_password(form.password.data)
        user.set_isadmin(form.isadmin.data)

        error = 'Erro! O usuário ou email já existem'
        if crud.create(user, error):
            return redirect(url_for('admin_bp.retrieve_user'))
    return render_template('admin/create_user.html', form=form)

@admin_bp.route('/admin/retrieve/user', methods=['GET', 'POST'])
@login_required
def retrieve_user():
    if not current_user.isadmin:
        return current_app.login_manager.unauthorized()

    crud = Crud()
    return render_template('admin/retrieve_user.html', data=crud.retrieve_all(UserModel))


@admin_bp.route('/admin/update/email', methods=['GET', 'POST'])
@login_required
def update_email():
    if not current_user.isadmin:
        return current_app.login_manager.unauthorized()

    crud = Crud()
    id=request.args.get('id')
    form = EmailForm()
    if form.validate_on_submit():
        user = crud.retrieve_one(id, UserModel)
        user.set_email(form.email.data)
        crud.update('Erro! O email já existe')
        return redirect(url_for('admin_bp.retrieve_user'))
    return render_template('admin/update_email.html', form=form)

@admin_bp.route('/admin/update/password', methods=['GET', 'POST'])
@login_required
def update_password():
    if not current_user.isadmin:
        return current_app.login_manager.unauthorized()

    crud=Crud()
    id=request.args.get('id')
    form = PasswordForm()
    if form.validate_on_submit():
        user = crud.retrieve_one(id, UserModel)
        user.set_password(form.password.data)
        crud.update('Erro ao mudar a senha')
        return redirect(url_for('admin_bp.retrieve_user'))
    return render_template('admin/update_password.html', form=form)


@admin_bp.route('/admin/delete/user', methods=['GET', 'POST'])
@login_required
def delete_user():
    if not current_user.isadmin:
        return current_app.login_manager.unauthorized()
        
    crud = Crud()
    id = request.args.get('id')
    if request.method == 'POST':
        user = crud.retrieve_one(id, UserModel)
        error = 'Erro ao deletar'
        crud.delete(user, error)
        return redirect(url_for('admin_bp.retrieve_user'))
    return render_template('admin/delete_user.html')
