from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

views = Blueprint('views', __name__, template_folder='templates')


@views.route('/domains', methods=['GET'])
def domains():
    return render_template("etc/domains.html")

