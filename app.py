from flask import Flask, redirect, render_template, url_for, send_from_directory, request
from flask_login import login_required
from models import VideoModel, db
from blueprints.login.login_bp import login_bp, login_manager
from blueprints.admin.admin_bp import admin_bp

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
    video_dir = '/var/www/html/'+stream
    print(video_dir)
    print(master)
    return send_from_directory(directory=video_dir, path=master, as_attachment=True)

# Configuração
app.config['SECRET_KEY'] = '&nV=A8-xza?LDgd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicia database e login
db.init_app(app)
login_manager.init_app(app)

# Inicia blueprints
app.register_blueprint(login_bp)
app.register_blueprint(admin_bp)

# Inicia database

with app.app_context():
    db.create_all()

    db.session.query(VideoModel).delete()

    db.session.add(VideoModel('Jogo 01 - Sinal Internacional', 'stream1', '/videos/stream1/master.m3u8'))
    db.session.add(VideoModel('Jogo 02 - Sinal Internacional', 'stream2', '/videos/stream2/master.m3u8'))
    db.session.add(VideoModel('Jogo 03 - Sinal Internacional', 'stream3', '/videos/stream3/master.m3u8'))
    db.session.add(VideoModel('Jogo 04 - Sinal Internacional', 'stream4', '/videos/stream4/master.m3u8'))
    db.session.add(VideoModel('Jogo 05 - Youtube', 'stream5', '/videos/stream5/master.m3u8'))
    db.session.add(VideoModel('Jogo 06 - Centauro', 'stream6', '/videos/stream6/master.m3u8'))

    db.session.commit()

@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('login_bp.login'))

@app.route('/video')
@login_required
def video():
    return render_template('video.html', data=VideoModel.query.all())

@app.route('/play', methods=['POST', 'GET'])
@login_required
def play():
    if request.method == "POST":
        stream = request.form.get('video')

        query = VideoModel.query.filter_by(stream=stream).first()
        query.isactive = 1
        db.session.commit()

    return redirect(url_for('video'))

@app.route('/stop', methods=['POST', 'GET'])
@login_required
def stop():
    if request.method == "POST":
        stream = request.form.get('video')

        query = VideoModel.query.filter_by(stream=stream).first()
        query.isactive = 0
        db.session.commit()

    return redirect(url_for('video'))

@app.route('/restart', methods=['POST', 'GET'])
@login_required
def restart():
    if request.method == "POST":
        stream = request.form.get('video')
        
        query = VideoModel.query.filter_by(stream=stream).first()
        query.isactive = 1
        db.session.commit()

    return redirect(url_for('video'))

@app.route('/estatisticas', methods=['POST', 'GET'])
@login_required
def estatisticas():
    if request.method == "POST":
        stream = request.form.get('video')
        
    return redirect(url_for('video'))


# Main
if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=5000)


# * python -m flask
# flask run
# pip freeze > requirements.txt
# pip install -r requirements.txt

# sqlite3 auction.db
# sqlite> .read create.sql
