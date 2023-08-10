from flask import Blueprint, current_app

medi_bp = Blueprint('medi', __name__, url_prefix='/sterling/api/medi')

from . import views
