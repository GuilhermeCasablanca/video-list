from flask import Flask, redirect, render_template, url_for
from flask import render_template, Flask, send_from_directory, request
from flask_login import login_required
from forms import OrientacaoForm, SizeForm, StreamForm
from models import ConfigModel, db
from blueprints.login.login_bp import login_bp, login_manager
from blueprints.admin.admin_bp import admin_bp
from crud import Crud
from models import StreamModel

app = Flask(__name__)

# videos
@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/videos/<string:stream>/<string:master>')
@login_required
def stream(stream,master):
    video_dir = '/DATA/opt/STREAMS/'+stream
    print(video_dir)
    print(master)
    return send_from_directory(directory=video_dir, path=master, as_attachment=True)

# Configuração
app.config['SECRET_KEY'] = '&nV=A8-xza?LDgd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicia app
db.init_app(app)
login_manager.init_app(app)

# Inicia database
with app.app_context():
    db.create_all()

# Inicia blueprints
app.register_blueprint(login_bp)
app.register_blueprint(admin_bp)

@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('login_bp.login'))

@app.route('/video')
@login_required
def video():
    crud = Crud()
    data = crud.retrieve_all(StreamModel)
    data2 = crud.retrieve_one(1, ConfigModel)
    return render_template('video.html', data=data, data2=data2)

@app.route('/config', methods=['GET', 'POST'])
@login_required
def config():
    crud = Crud()
    data = crud.retrieve_all(StreamModel)
    data2 = crud.retrieve_one(1, ConfigModel)
    return render_template('config.html', data=data, data2=data2)

@app.route('/config_edit', methods=['GET', 'POST'])
@login_required
def config_edit():
    crud = Crud()
    id=request.args.get('id')
    stream = crud.retrieve_one(id, StreamModel)
    form = StreamForm(name=stream.name, video_src=stream.video_src)
    if form.validate_on_submit():
        stream.set_name(form.name.data)
        stream.set_video_src(form.video_src.data)
        crud.update('')
        return redirect(url_for('config'))
    return render_template('config_edit.html', form=form)

@app.route('/config_edit_orientacao', methods=['GET', 'POST'])
@login_required
def config_edit_orientacao():
    crud = Crud()
    id=request.args.get('id')
    config = crud.retrieve_one(id, ConfigModel)
    form = OrientacaoForm(orientacao=config.orientacao)
    if form.validate_on_submit():
        config.set_orientacao(form.orientacao.data)
        crud.update('')
        return redirect(url_for('config'))
    return render_template('config_edit_orientacao.html', form=form)

@app.route('/config_edit_size', methods=['GET', 'POST'])
@login_required
def config_edit_size():
    crud = Crud()
    id=request.args.get('id')
    config = crud.retrieve_one(id, ConfigModel)
    form = SizeForm(width=config.width, height=config.height)
    if form.validate_on_submit():
        config.set_width(form.width.data)
        config.set_height(form.height.data)
        crud.update('')
        return redirect(url_for('config'))
    return render_template('config_edit_size.html', form=form)

@app.route('/config_delete', methods=['GET', 'POST'])
@login_required
def config_delete():
    crud = Crud()
    return render_template('config_delete.html', data=crud.retrieve_all(StreamModel))

# Main
if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=5000)

# * python -m flask
# flask run
# pip freeze > requirements.txt
# pip install -r requirements.txt

# sqlite3 auction.db
# sqlite> .read create.sql
