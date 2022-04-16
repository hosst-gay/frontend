
from flask import Flask, request, json, send_from_directory, render_template, redirect, render_template_string, abort, Response, url_for
from io import BytesIO
from werkzeug.middleware.proxy_fix import ProxyFix
import os
from os.path import splitext
import secrets
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import json
from pathlib import Path


from utils import size, uptime, userid, folder
from utils.sxcu import sharex


secret_key = 'SawshaIsCute'
admin = ["sawsha"]
allowed_extension = ['.png', '.jpeg', '.jpg', '.gif', '.webm', '.mp4']
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
storage_folder = '/mnt/volume_nyc1_02/imgs/'


app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config["SECRET_KEY"] = "SawshaIsCute"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_BINDS'] = {
    'embed':'sqlite:///embed.db'
}
app.config['SQLALCHEMY_ECHO'] = True
app.wsgi_app = ProxyFix(app.wsgi_app)
uptime = uptime.uptime()
folder_size = size.get_folder_size("/mnt/volume_nyc1_02/imgs")
port = 5001

ip_ban_list = []
allowed_ips = [f'http://localhost:{port}', f'localhost:{port}', f'127.0.0.1:{port}']






def block_method():
    ip = request.environ.get('REMOTE_ADDR')
    if ip in ip_ban_list:
        return abort(Response(render_template("errors/403.html"), 403))

@app.before_request
def block_method():
    ip = request.environ.get('REMOTE_ADDR')
    if ip in ip_ban_list:
        return abort(Response(render_template("errors/403.html"), 403))


@app.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('errors/405.html'), 405


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):

    id = User.query.get(int(user_id))
    print(id)
    return id


def create_uuid():
    return userid.user_id()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.String(50), nullable=False, unique=True)
    ip = db.Integer()




class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=50)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()

        if existing_user_username:
            raise ValidationError(
                "That username already exists! please choose another one.")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")


@app.route("/", methods=["GET", "POST"])
def gfg():
    return render_template("home/home.html")


@app.route("/dashboard")
@login_required
def dash():
    for user in db.session.query(User.username).distinct():
        print(user)
    list = os.listdir(storage_folder)  # dir is your directory path
    number_files = len(list)

    return render_template("dashboard/dash.html", uptime=uptime, files=number_files, size=folder_size)

@app.route('/dashboard/embed')
@login_required
def embed_stuff():
    pass


@app.route('/users', methods=['GET', 'POST'])
def user_search():
    users = db.session.query(User.username).all()

    result = '<br>'.join(u.username for u in users)

    return render_template('users/user.html', result=result)


@app.route('/users/<int:id>', methods=['GET', 'POST'])
def users(id):
    info = User.query.filter_by(id=id).first()
    if info is None:
        return abort(404)
    else:

        return render_template('users/users.html', info=info)






@app.route("/sxcu")
@login_required
def sxcu():
    secret = str(current_user.user_id)
    username = current_user.username

    sharex.sharex(secret=secret, username=username)

    path = f'sxcu/{username}/'

    return send_from_directory(path, "hosst.gay.sxcu")


@app.route("/sharenix")
def share():
    secret = str(current_user.user_id)
    username = current_user.username

    sharex.sharenix(secret=secret, username=username)

    path = f'sxcu/{username}/'

    return send_from_directory(path, ".sharenix.json")


@app.route("/source")
def source():
    return redirect(location="https://github.com/SawshaDev/hosst")

@app.route('/upload')
def upload_file():
    return render_template('upload/upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        ip = request.environ.get('REMOTE_ADDR')
        if ip in ip_ban_list:
            return 'Blacklist IP!', 403

        '''Get file object from POST request, extract and define needed variables for future use.'''
        file = request.files['image']
        extension = splitext(file.filename)[1]
        file.flush()
        size = os.fstat(file.fileno()).st_size
        '''Check for file extension and file size.'''
        if extension not in allowed_extension:
            return 'File type is not supported', 415

        elif size > 6000000:
            return 'File size too large', 400


        filename = secrets.token_urlsafe(5)
        file.save(os.path.join(f"{storage_folder+current_user.username}", filename + extension))
        

        return json.dumps({"filename": filename, "extension": extension}) 

        
@app.route('/imgs/<filename>')
def sendfile(filename=None):
    return send_from_directory(storage_folder, filename)
    

@app.route("/<filename>")
def embed(filename=None):
    extensions = ['.mp4', '.webm', '.mov']
    url = request.root_url
    folder = os.path.join('./', storage_folder+f'/{filename}')

    if filename.endswith(tuple(extensions)):
        return render_template("images/embed2.html", folder=storage_folder)
    else:

        return render_template("images/embed.html", filename=filename, url=url)


@app.route('/login', methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dash'))
    return render_template('login/login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('gfg'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user_id = userid.user_id()

        hashed_password = bcrypt.generate_password_hash(form.password.data)

        user = User.query.filter_by(username=form.username.data).first()
        ip = request.environ.get('REMOTE_ADDR')

        if len(form.password.data) >= 45:
            raise ValidationError("Password is too long!")

        if user:
            raise ValidationError("This username already exists!")
        else:

            new_user = User(username=form.username.data,
                            password=hashed_password, user_id=str(user_id), ip=ip)
            db.session.add(new_user)
            db.session.commit()
            folder.create_folder.folder(username=form.username.data)


            print(os.path.join('/' + storage_folder, f"{form.username.data}"))

            return redirect(url_for('login'))

    return render_template('register/register.html', form=form)


if __name__ == '__main__':
    app.run(port=port, debug=True)
