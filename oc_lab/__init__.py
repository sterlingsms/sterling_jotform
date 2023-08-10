from flask import Blueprint, current_app

oclab_bp = Blueprint('oclab', __name__, url_prefix='/sterling/api/oclab')

from . import views
