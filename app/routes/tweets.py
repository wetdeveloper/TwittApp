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

from . import tweets_bp

from . import tweets_bp

@tweets_bp.route('/home/twitts/twitt_it/',methods=['POST','GET'])
def TwittIt():
    if request.method=='POST':
        twitt=Twitts(current_user.id,request.form['twitt_text'])
        try:
            db.session.add(twitt)
            db.session.commit()
        except BaseException as e:
            return str(e)
        else:
            return jsonify({
                "url":url_for('tweets.twitts'),'html':'twitts.html',
                'message':"twitted:)"
                }
                )

@tweets_bp.route('/home/twitts/', defaults={'start': 0}, methods=['GET'])
def twitts(start):
    login_message = request.args.get('login_message', '')
    start = int(start)
    Step = 2                    # تعداد دکمه‌های صفحه‌بندی که نمایش داده می‌شه
    per_page = 10               # تعداد توییت در هر صفحه (قابل تنظیم)

    if current_user.is_authenticated:
        # لیست ID کاربران فالو شده + خود کاربر
        following_query = Following.query.filter_by(userid=current_user.id)
        following_usersid = [f.following_userid for f in following_query] + [current_user.id]

        # شمارش کل توییت‌ها (بهینه)
        twitts_count = Twitts.query.filter(Twitts.userid.in_(following_usersid)).count()
        retwitts_count = Retwitts.query.filter(Retwitts.userid.in_(following_usersid)).count()
        TwittsNumber = twitts_count + retwitts_count

        # دریافت توییت‌ها با joinedload برای جلوگیری از N+1
        twittslist = Twitts.query.filter(Twitts.userid.in_(following_usersid)) \
            .options(joinedload(Twitts.fk)) \
            .order_by(desc(Twitts.dtime)) \
            .offset(start * per_page).limit(per_page).all()

        retwittslist = Retwitts.query.filter(Retwitts.userid.in_(following_usersid)) \
            .options(joinedload(Retwitts.fk_userid), joinedload(Retwitts.fk_twittid)) \
            .order_by(desc(Retwitts.dtime)) \
            .offset(start * per_page).limit(per_page).all()

        # اطلاعات فالو برای نمایش در صفحه
        followersid = [f.userid for f in Following.query.filter_by(following_userid=current_user.id).all()]
        followersfollowedid = [fid for fid in followersid 
                              if Following.query.filter_by(userid=current_user.id, following_userid=fid).first()]
        followingsid = [f.following_userid for f in Following.query.filter_by(userid=current_user.id).all()]

    else:
        # حالت بدون لاگین (همه توییت‌ها)
        TwittsNumber = Twitts.query.count() + Retwitts.query.count()

        twittslist = Twitts.query.options(joinedload(Twitts.fk)) \
            .order_by(desc(Twitts.dtime)) \
            .offset(start * per_page).limit(per_page).all()

        retwittslist = Retwitts.query.options(joinedload(Retwitts.fk_userid), 
                                            joinedload(Retwitts.fk_twittid)) \
            .order_by(desc(Retwitts.dtime)) \
            .offset(start * per_page).limit(per_page).all()

        followersid = followersfollowedid = followingsid = None

    # محاسبه تعداد صفحات
    ButtonsNum = (TwittsNumber + per_page - 1) // per_page if TwittsNumber > 0 else 1

    return render_template('twitts.html',
                           twittslist=twittslist,
                           retwittslist=retwittslist,
                           start=start,
                           ButtonsNum=ButtonsNum,
                           Step=Step,
                           TwittsNumber=TwittsNumber,
                           TwittLike=TwittLike,
                           Twitts=Twitts,
                           User=User,
                           datetime=datetime,
                           login_message=login_message,
                           following_users_number=len(following_usersid)-1 if current_user.is_authenticated else None,
                           followed_users_number=len([f.following_userid for f in Following.query.filter_by(following_userid=current_user.id).all()]) if current_user.is_authenticated else None,
                           followersid=followersid,
                           followersfollowedid=followersfollowedid,
                           followingsid=followingsid,
                           abs=abs)

@tweets_bp.route("/home/twitts/retwitt/",methods=['POST'])
def ReTwitt():
    retwitter_userid=current_user.id
    twittid=request.form['twittid']
    print("function is running..........................")
    if (Retwitts.query.filter_by(userid=current_user.id)
    .filter_by(twittid=twittid).first()):
        message="You already retwitted this twitt.you can not retwitt a twitt twice. "
        return jsonify({
            'message':message
        }) 
    else:
        retwitt=Retwitts(retwitter_userid,twittid)
        try:
            db.session.add(retwitt)
            db.session.commit()
        except BaseException as e:
            return str(e)
        else:
            message='Retwitted for you XD'
            return jsonify({
                "message":message
                
            })

@tweets_bp.route('/home/twitts/like_twitt/',methods=['POST'])
def LikeTwitt():
    if request.method=='POST':
        userid=current_user.id
        twittid=request.form['twittid']
        twitt_likes_number=TwittLike.query.filter_by(twittid=twittid).count()
        print(f'type of twittid is {type(twittid)}')
        if TwittLike.query.filter_by(userid=current_user.id).filter_by(twittid=twittid).first():
            twitt_unlike=TwittLike.query.filter_by(userid=current_user.id).filter_by(twittid=twittid).first()
            try:
                db.session.delete(twitt_unlike)
                db.session.commit()
            except BaseException as e:
                return str(e)
            else:
                return jsonify({
                    'message':"You  unliked this twitt","twitt_likes_number":twitt_likes_number-1,
                    "twittid":twittid,
                    'unliked':True,
                    })
        else:
            twitt_like=TwittLike(userid, twittid)
            try:
                db.session.add(twitt_like)
                db.session.commit()
            except BaseException as e:
                return str(e)
            else:
                return jsonify(
                        {
                        'message':"twitt Liked","twitt_likes_number":twitt_likes_number+1,
                        "twittid":twittid,
                        'unliked':False
                        }
                    )

@tweets_bp.route("/userpage/twitt/<int:twittid>/likers/<string:username>/",methods=["GET"])
def TwittLikers(twittid=None,username=None):
    if "twittid" in request.args and "username" in request.args:
        twittid=request.args("twittid")
        username=request.args("username")
    elif twittid==None or username==None:
        return jsonify({
            "message":"twittid or username is empty"
        })
    user=User.query.filter_by(username=username).first()
    twitt=Twitts.query.filter_by(id=twittid).first()
    if not(user):
        return jsonify({
            "message":"User is not found by this username"
        })
    if not(twitt):
        return jsonify({
            "message":"User and Twitt is not matched"
        })
    TwLikers=TwittLike.query.filter_by(twittid=twitt.id).all()
    if TwLikers:
        TwLikers=[User.query.filter_by(id=twliker.userid).first() for twliker in TwLikers]
        return render_template("TwittLikers.html",TwLikers=TwLikers)
    return jsonify({
        "message":"No one Liked this Twitt yet"
    })
