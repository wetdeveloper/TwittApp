from flask import Blueprint


main_bp = Blueprint("main", __name__)
auth_bp = Blueprint("auth", __name__)

from . import auth
from . import main
