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

from . import users_bp

from . import users_bp

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@users_bp.route('/userpage/', methods=["GET"])
def userPage(username=None):
    ProfPicUpForm = ProfPicUploadForm()

    if not username:
        username = request.args.get("username")
        if not username:
            return redirect(url_for("tweets.twitts"))

    # کوئری اصلی کاربر + اطلاعات پروفایل
    user = User.query.filter_by(username=username).first()
    if not user:
        return "There isn't any user by this username."

    # شمارش‌های بهینه (بدون لوپ اضافی)
    followed_users_number = Following.query.filter_by(following_userid=user.id).count()   # فالوورها
    following_users_number = Following.query.filter_by(userid=user.id).count()          # فالوئینگ‌ها

    # توییت‌های کاربر
    twitts = Twitts.query.filter_by(userid=user.id)\
        .options(joinedload(Twitts.fk))\
        .order_by(desc(Twitts.dtime)).all()

    # ری‌توییت‌ها
    retwitts = db.session.query(Twitts)\
        .join(Retwitts, Twitts.id == Retwitts.twittid)\
        .filter(Retwitts.userid == user.id)\
        .options(joinedload(Twitts.fk))\
        .order_by(desc(Retwitts.dtime)).all()

    # اطلاعات پیام‌های خوانده‌نشده (فقط برای کاربر فعلی)
    unread_messages_number = 0
    unread_messages_senders = []
    if current_user.is_authenticated:
        unread_query = DirectMessages.query.filter_by(
            reciever_id=current_user.id, 
            unread=True
        )
        unread_messages_number = unread_query.count()
        unread_messages_senders = [dm.sender_id for dm in unread_query.all()]

    # آدرس عکس پروفایل
    ProfPhoAdd = f'/ProfilePhotos/{user.id}.jpg' if ProfilePhotos.query.filter_by(userid=user.id).first() else None

    return render_template("user_page.html",
                           user=user,
                           twitts=twitts,
                           retwitts=retwitts,
                           unread_messages_senders=unread_messages_senders,
                           unread_messages_number=unread_messages_number,
                           DirectMessages=DirectMessages,
                           followed_users_number=followed_users_number,
                           following_users_number=following_users_number,
                           TwittLike=TwittLike,
                           Following=Following,
                           User=User,
                           ProfPicUpForm=ProfPicUpForm,
                           ProfPhoAdd=ProfPhoAdd,
                           len=len)

@users_bp.route('/UploadProfilePicture',methods=['POST'])
def UploadProfPic():
    form=ProfPicUploadForm()
    if form.validate_on_submit:
        if current_user.is_authenticated:
            userid=current_user.id
            flag=True #had profile photo
            if ProfilePhotos.query.filter_by(userid=userid).first():#if user already has a profile photo
                os.remove('static/ProfilePhotos/'+str(userid)+'.jpg')
            else:
                flag=False
            try:
                filename = secure_filename(str(userid)+'.jpg')
                form.uploadbox.data.save('static/ProfilePhotos/' + filename)
                if flag:
                    PF=ProfilePhotos.query.filter_by(userid=userid).first()
                    PF.dtime=datetime.datetime.now()
                else:
                    PF=ProfilePhotos(userid)
                    db.session.add(PF)
                db.session.commit()
            except BaseException as e:
                return str(e)
            else:
                return "uploaded"
        return redirect(url_for("users.userPage",username=current_user.username))
    return str(form.errors)

@users_bp.route('/userpage/<string:username>/followers/',methods=['GET'])
def Followers(username=None):
        user=User.query.filter_by(username=username).first()
        if user:
            if username==None:
                if "username" in request.args:
                    username=request.args["username"]
            followers_id=[follower.userid for follower in Following.query.filter_by(following_userid=user.id).all()]
            followersfollowed_id=[followerid for followerid in followers_id if Following.query.filter_by(following_userid=followerid).filter_by(userid=user.id).first()]
            followersnotfollowed_id=list(set(followers_id)-set(followersfollowed_id))
            return render_template("followers_list.html",Following=Following,User=User,user=user,followersfollowed_id=followersfollowed_id,followersnotfollowed_id=followersnotfollowed_id)
        return "User not found"

@users_bp.route('/user/<string:username>/followings/',methods=['GET'])
def Followings(username=None):
        user=User.query.filter_by(username=username).first()
        if user:
            if username==None:
                if "username" in request.args:
                    username=request.args["username"]
            followings_id=[following.following_userid for following in Following.query.filter_by(userid=user.id).all()]
            return render_template("followings_list.html",Following=Following,User=User,user=user,followings_id=followings_id)
        return "User not found"

@users_bp.route('/home/twitts/search-user/',methods=['GET'])
def Search():
    username=request.args.get('searcheduser')
    user=User.query.filter_by(username=username).first()
    if not(user):
        return "Not found any user"
    return render_template('searched_users.html',user=user,Following=Following)
