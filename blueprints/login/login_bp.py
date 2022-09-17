from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, LoginManager, logout_user
from urllib.parse import urlparse, urljoin
from models import UserModel
from forms import LoginForm

login_bp = Blueprint('login_bp', __name__,
                     template_folder='templates')

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(user_id)


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Does not allow logged in user to navigate to /login URL of your application
    if current_user.is_authenticated:
        flash('Logged in successfully.')
        return redirect(url_for('video'))
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        user = UserModel.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Usuário ou senha inválidos')
            return redirect(url_for('login_bp.login'))

        login_user(user)

        flash('Logged in successfully.')

        next = request.args.get('next')

        # is_safe_url should check if the url is safe for redirects.
        if not is_safe_url(next):
            return abort(400)

        return redirect(next or url_for('video'))
    return render_template('login/login.html', form=form)


@login_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_bp.login'))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login_bp.login'))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc
