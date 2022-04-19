
import logger
from flask import Flask, request, json, send_from_directory, render_template, redirect, render_template_string, abort, Response, url_for, flash
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
from werkzeug.datastructures import ImmutableMultiDict


from utils import size, uptime, userid, folder
from utils.sxcu import sharex


secret_key = 'SawshaIsCute'
admin = ["sawsha"]
allowed_extension = ['.png', '.jpeg', '.jpg', '.gif', '.webm', '.mp4']
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
storage_folder = '/mnt/volume_nyc1_02/imgs'
path_to_save = '/mnt/volume_nyc1_02/imgs/'

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config["SECRET_KEY"] = "SawshaIsCute"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_BINDS'] = {
    'embed':'sqlite:///embed.db',
    'image':'sqlite:///image.db'
}
app.wsgi_app = ProxyFix(app.wsgi_app)
uptime = uptime.uptime()
folder_size = size.get_folder_size("/mnt/volume_nyc1_02/imgs")
port = 5001

ip_ban_list = []
allowed_ips = [f'http://localhost:{port}', f'localhost:{port}', f'127.0.0.1:{port}'] #not in use rn but will be soon for some ip only shit



def folder_shit(username):
    return size.get_folder_size(f"/mnt/volume_nyc1_02/imgs/{username}")
def folder_shit2(username):
    return os.listdir(os.path.join(path_to_save, username)) 


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
    return render_template('errors/https://discord.com/api/webhooks/965468843306811432/6qvc-V2gwoxg7REXS3uGtErgqgPczydjFM_rfXnIZfW9_q-VDK59lDpJgv_CtQQc7Tur403.html'), 403


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
    ip = db.Column(db.Integer)

class Embed(db.Model):
    __bind_key__ = 'embed'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    color = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(30), nullable=False)

class image(db.Model):
    __bind_key__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    filename = db.Column(db.String(10), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    secret = db.Column(db.String(50), nullable=False)



class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=50)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Register")
    basepath = f"static/{username}/Images"
    dir = os.walk(basepath)
    file_list = []

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


@app.route("/", methods=["GET"])
def gfg():
    return render_template("home/home.html")


@app.route("/dashboard")
@login_required
def dash():
    for user in db.session.query(User.username).distinct():
        print(user)
    list = folder_shit2(username=current_user.username)  # dir is your directory path
    number_files = len(list)

    return render_template("dashboard/dash.html", uptime=uptime, files=number_files, size=folder_shit(username=current_user.username))


@app.route('/dashboard/embed')
@login_required
def embed_stuff():
    return render_template('dashboard/embed.html')

@app.route('/dashboard/embed', methods=['POST'])
def embed_processing():
    if request.method == 'POST':
        req = request.form['color']
        username = current_user.username
        
        if Embed.query.filter_by(username=username) is not None:
            embed = Embed.query.filter_by(username=username).first()
            embed.color = req
            db.session.commit() 
        else:
            embed_stuff = Embed(color=req, username=username) #this just puts the data into the fucking colums n shit :)))) 
            db.session.add(embed_stuff)
            db.session.commit()

        flash("Succesfully updated your color!")
        return render_template("dashboard/embed.html")


@app.route("/gallery")
@login_required
def gallery():
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

    sharex.sxcu(secret=secret, username=username)

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
@login_required
def upload_file():
    host = request.root_url

    return render_template('upload/upload.html', host=host)

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        pernis = request.form.to_dict(flat=False)['secret_key'][0]
        result = User.query.filter_by(user_id=pernis).first()
        print(pernis)
        remember=request.form.get('secret_key')      

        if result is not None:
            secret = result.user_id
        else:
            secret = remember


        ip = request.environ.get('REMOTE_ADDR')
        if ip in ip_ban_list:
            return 'Blacklist IP!', 403
        

        
        elif request.form.to_dict(flat=False)['secret_key'][0] ==  secret:

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
            file.save(os.path.join(path_to_save+result.username, filename + extension))
            location = os.path.join(path_to_save+result.username, filename+extension)
        
            try:
                file_info = image(username=result.username,filename=filename+extension, location=location, secret=result.user_id)
        
                db.session.add(file_info)
        
                db.session.commit()
            except Exception as e:
                print(e)


            return json.dumps({"filename": filename, "extension": extension})
        else:
            return 'Unauthorized use', 401
    
        

        
@app.route('/imgs/<filename>')
def sendfile(filename=None):
    imageshit = image.query.filter_by(filename=filename).first()
    username = imageshit.username
    return send_from_directory(path_to_save+username, filename)
    

@app.route("/<filename>")
def embed(filename=None):
    extensions = ['.mp4', '.webm', '.mov']
    url = request.root_url
    folder = os.path.join('./', storage_folder+f'/{filename}')
    
    imageshit = image.query.filter_by(filename=filename).first()


    if imageshit is None:
        return abort(404)
    
    username = imageshit.username


    color1 = Embed.query.filter_by(username=username).first()

    if color1 is not None:
        color = color1.color
    else:
        color = "#b15141"

        

    
    print(color)

    if filename.endswith(tuple(extensions)):
        return render_template("images/embed2.html", folder=storage_folder, url=url, filename=filename, color=color)
    else:

        return render_template("images/embed.html", folder=storage_folder, url=url, filename=filename, color=color, username=username)


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

            embed_shit = Embed(username=form.username.data, color="#b15141", title="false")
            db.session.add(embed_shit)


            db.session.commit()
            db.session.commit()
            folder.create_folder.folder(username=form.username.data)

            return redirect(url_for('login'))

    return render_template('register/register.html', form=form)


if __name__ == '__main__':
    app.run(port=port, debug=True)
