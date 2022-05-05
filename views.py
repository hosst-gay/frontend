from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

views = Blueprint('views', __name__, template_folder='templates')

@views.route("/", methods=['GET'])
def home():
    return render_template("home/home.html")

@views.route('/domains', methods=['GET'])
def domains():
    return render_template("etc/domains.html")

