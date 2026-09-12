from werkzeug.security import check_password_hash, generate_password_hash
from ..Model import *
from ..tools import get_messed_twitts, get_messed_retwitts   
from ..Forms import *
from ..forgetpassVerification import *
from flask_admin.contrib.sqla import ModelView
from flask import (
    request,
    render_template,
    redirect,
    url_for,
    flash,
    session,
    jsonify,
    abort,
)

from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required
)

from sqlalchemy.orm import joinedload

from . import misc_bp

from . import misc_bp

@misc_bp.route('/myip',methods=['GET'])
def MyIp():
    
    return request.remote_addr,200
