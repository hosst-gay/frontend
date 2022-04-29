from flask import Flask, request, json, send_from_directory, render_template, redirect, render_template_string, abort, Response, url_for, flash
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


from utils import size, userid, folder
from utils.sxcu import sharex
from utils.uptime import uptime as uptimea

allowed_extension = ['.png', '.jpeg', '.jpg', '.gif', '.webm', '.mp4']
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
storage_folder = '/mnt/volume_nyc1_02/imgs'
path_to_save = '/mnt/volume_nyc1_02/imgs/'

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config["SECRET_KEY"] = "SawshaIsCute"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schema/database.db'
app.config['SQLALCHEMY_BINDS'] = {
    'embed':'sqlite:///schema/embed.db',
    'image':'sqlite:///schema/image.db',
    'profile':'sqlite:///schema/profile.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.wsgi_app = ProxyFix(app.wsgi_app)
folder_size = size.get_folder_size("/mnt/volume_nyc1_02/imgs")
port = 5001

ip_ban_list = []
allowed_ips = [f'http://localhost:{port}', f'localhost:{port}', f'127.0.0.1:{port}'] #not in use rn but will be soon for some ip only shit



