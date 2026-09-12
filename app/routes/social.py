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

from . import social_bp

from . import social_bp

@social_bp.route('/home/twitts/follow/',methods=['POST'])
def Follow():
    if request.method=='POST':
        if current_user.is_authenticated:
            followingtarget_id=request.form['followingtarget_id']
            follower_id=request.form['follower_id']
            if followingtarget_id==current_user.id:
                return jsonify({
                    'message':'You can not follow yourself'
                })
            if Following.query.filter_by(userid=follower_id).filter_by(following_userid=followingtarget_id).first():
                return jsonify({
                    'message':"you've followed this user before.",
                })
            else:
                follow=Following(follower_id,followingtarget_id)
                if follow:
                    try:
                        db.session.add(follow)
                        db.session.commit()
                    except BaseException as e:
                        return jsonify({
                            'message':f'error:{e}'
                        })
                    else:
                        if "followersOrfollowingsPage" in request.args:
                            if request.args["followersOrfollowingsPage"]=="Followers":
                                return redirect(url_for("users.Followers",userid=current_user.id))
                            elif request.args["followersOrfollowingsPage"]=="Followings":
                                return redirect(url_for("users.Followings",userid=current_user.id))
                        else:
                            return redirect(url_for("users.userPage",username=User.query.filter_by(id=followingtarget_id).first().username))
                return jsonify({
                    'message':f'Something Went Wrong'
                })

@social_bp.route('/home/twitts/unfollow/',methods=['POST'])
def UnFollow():
    if request.method=='POST':
        if current_user.is_authenticated:
            unfollowingtarget_id=request.form['unfollowingtarget_id']
            unfollower_id=request.form['unfollower_id']
            unfollow=Following.query.filter_by(userid=unfollower_id).filter_by(following_userid=unfollowingtarget_id).first()
            if unfollow:
                try:
                    db.session.delete(unfollow)
                    db.session.commit()
                except BaseException as e:
                    return jsonify({
                        'message':f'error:{e}'
                    })
                else:
                    if "followersOrfollowingsPage" in request.args:
                        if request.args["followersOrfollowingsPage"]=="Followers":
                            return redirect(url_for("users.Followers",username=current_user.username))
                        elif request.args["followersOrfollowingsPage"]=="Followings":
                            return redirect(url_for("users.Followings",username=current_user.username))
                    else:
                        return redirect(url_for("users.userPage",username=User.query.filter_by(id=unfollowingtarget_id).first().username))
            else:
                return jsonify({
                    'message':f'Something Went Wrong'
                })
