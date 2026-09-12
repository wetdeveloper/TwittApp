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

from . import messages_bp

from . import messages_bp

@messages_bp.route('/home/twitts/direct',methods=['POST'])
def Direct(reciever_id=None): #Need to be None to handle Post method otherwise we got positional argument error
    if current_user.is_authenticated:
        if request.method=='POST':
            reciever_id=request.form['reciever_id']
            message=request.form['message']
            dm=DirectMessages(current_user.id, reciever_id, message)
           # return reciever_id
            try:
                db.session.add(dm)
                db.session.commit()
            except BaseException as e:
                return str(e)
            else:
                return redirect(url_for('Direct',reciever_id=reciever_id))
        elif request.method == 'GET':
            if reciever_id is None:
                if 'reciever_id' in request.args:
                    reciever_id = request.args['reciever_id']
                else:
                    return redirect(url_for('tweets.twitts'))
            # elif reciever_id==current_user.id:
            #         return "You  can not send message to yourself! this option will be comming  soon."
            ############ set unread=False
            unread_messages = DirectMessages.query.filter_by(
        reciever_id=current_user.id, 
        sender_id=reciever_id
    ).filter_by(unread=True).all()
    
        for unmsg in unread_messages:
            unmsg.unread = False
            db.session.commit()

    # دریافت پیام‌ها
        dms = DirectMessages.query.filter(
            ((DirectMessages.reciever_id == reciever_id) & (DirectMessages.sender_id == current_user.id)) |
            ((DirectMessages.reciever_id == current_user.id) & (DirectMessages.sender_id == reciever_id))
        ).order_by(DirectMessages.dtime).all()

        return render_template('directpage.html', 
                               reciever_id=reciever_id, 
                               dms=dms, 
                               User=User)
    return 'You should login first.'
