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

from . import comments_bp

from . import comments_bp

@comments_bp.route('/home/twitts/see_comments/<int:twittid>/<int:start>', methods=['GET'])
@comments_bp.route('/home/twitts/see_comments/', methods=['GET'], defaults={'twittid': 1, 'start': 0})
def SeeComments(start,twittid):
    start=int(start)
    twittid=int(twittid)
    CommentsNumber=Comments.query.filter_by(twittid=twittid).count() #Y
    # ButtonsNum
    flag=False 
    ButtonsNum=2 
    for i in range(1,10):
        if CommentsNumber>1:
            if CommentsNumber%i==0:
                ButtonsNum=i
                flag=True
    if flag==False:
        for i in range(10,CommentsNumber+1):
            if CommentsNumber%i==0:
                flag=True
                ButtonsNum=i
    #end ButtonsNum
    print(f'CommentsNum={CommentsNumber} , ButtonsNum={ButtonsNum}')
    Comments_perPage=int(CommentsNumber/ButtonsNum)
    if Comments_perPage==0:#when CommentsNumber=1 and ButtonsNumber=2(by default)
        Comments_perPage=1
    Step=2
    if start==ButtonsNum:
        commentslist=Comments.query.filter_by(twittid=int(twittid)).all()[start*Comments_perPage:]
    else:
        commentslist=Comments.query.filter_by(twittid=twittid).all()[start*Comments_perPage:(start+1)*Comments_perPage]
    
    return render_template('comments.html',commentslist=commentslist,start=start,ButtonsNum=ButtonsNum,Step=Step,twittid=twittid,Comments_perPage=Comments_perPage,
    CommentLike=CommentLike,CommentsNumber=CommentsNumber,User=User)

@comments_bp.route('/home/twitts/like_comment/',methods=['POST'])
def LikeComment():
    if request.method=='POST':
        userid=current_user.id
        twittid=request.form['twittid'] 
        commentid=request.form['commentid']
        comment_likes_number=CommentLike.query.filter_by(twittid=twittid).filter_by(commentid=commentid).count()
        if CommentLike.query.filter_by(userid=userid).filter_by(commentid=commentid).first():
            commentunlike=CommentLike.query.filter_by(userid=userid).filter_by(commentid=commentid).first()
            try:
                db.session.delete(commentunlike)
                db.session.commit()
            except BaseException as e:
                return str(e)
            else:
                return jsonify(
                    {
                        'message':'u unliked this comment!',
                        'comment_likes_number':comment_likes_number-1,
                        'unliked':True
                    }
                )
        comment_like=CommentLike(twittid,userid,commentid)
        try:
            db.session.add(comment_like)
            db.session.commit()
        except BaseException as e:
            return str(e)
        else:
            return jsonify(
                {
                    'message':'you liked this comment!',
                    'comment_likes_number':comment_likes_number+1,
                    'unliked':False
                }
            )

@comments_bp.route('/home/twitts/see_comments/Likers/<int:twittid>/<int:commentid>',methods=['GET'])
def CommentLikers(twittid=None,commentid=None):
    if "twittid" in request.args and "commentid" in request.args:
            twittid=request.args("twittid")
            commentid=request.args("commentid")
    elif twittid==None or commentid==None:
        return jsonify({
            "message":"twittid or commentid is missed."
        })
    twitt=Twitts.query.filter_by(id=twittid).first()
    user=User.query.filter_by(id=twitt.userid).first()
    comment=Comments.query.filter_by(id=commentid).first()
    if not(user):
        return jsonify({
            "message":"User is not found"
        })
    if not(twitt):
        return jsonify({
            "message":"Twitt is not found"
        })
    if not(comment):
        return jsonify({
            "message":"Comment  is not found"
        })
        
    ComLikers=CommentLike.query.filter_by(twittid=twitt.id).filter_by(commentid=commentid).all()
    if ComLikers:
        ComLikers=[User.query.filter_by(id=comliker.userid).first() for comliker in ComLikers]
        return render_template("CommentLikers.html",ComLikers=ComLikers)
    return jsonify({
        "message":"No one liked this comment"
    })

@comments_bp.route('/home/twitts/leave_comments/',methods=['POST'])
def LeaveComment():
    comment=Comments(request.form['twittid'],current_user.id,request.form['comment'])
    db.session.add(comment)
    db.session.commit()
    return jsonify(
        {'message':'commented'}
    )

@comments_bp.route('/home/twitts/see_comment_replays/<int:commentid>',methods=['GET'])
def SeeCommentReplays(commentid):
    if "CommentReplayLiked_message" in request.args:
        CommentReplayLiked_message=request.args['CommentReplayLiked_message']
    else:
        CommentReplayLiked_message=""
    print(f'commentid={ commentid}')
    commentreplays=CommentReplays.query.filter_by(commentid=commentid).all()
    if commentreplays:
        return render_template('CommentReplays.html',commentreplays=commentreplays,CommentReplaysLike=CommentReplaysLike,CommentReplayLiked_message=CommentReplayLiked_message,User=User)
    return 'No replays on this comment'

@comments_bp.route('/home/twitts/leave_comment_replay/',methods=['POST'])
def LeaveCommentReplay():
    commentreplays=CommentReplays(current_user.id, request.form['twittid'],request.form['commentid'],request.form['replay'])
    try:
        db.session.add(commentreplays)
        db.session.commit()
    except BaseException as e:
        return jsonify(
        {
            "message":str(e)
        }
        )
    else:
        return jsonify(
            {
                "message":"Replayed successfully:)"
            }
        )

@comments_bp.route('/home/twitts/see_comments/like_comment_replays/',methods=['POST'])
def LikeCommentReplays():
    comment_replay_id=request.form['comment_replay_id']
    twittid=request.form['twittid']
    commentid=request.form['commentid']
    comment_replay_likes_number=CommentReplaysLike.query.filter_by(commentid=commentid).filter_by(comment_replay_id=comment_replay_id).filter_by(twittid=twittid).count()
    if CommentReplaysLike.query.filter_by(userid=current_user.id).filter_by(commentid=commentid).filter_by(comment_replay_id=comment_replay_id).first():
        unlikecomment=CommentReplaysLike.query.filter_by(userid=current_user.id).filter_by(commentid=commentid).filter_by(comment_replay_id=comment_replay_id).first()
        try:
            db.session.delete(unlikecomment)
            db.session.commit()
        except BaseException as e:
            return str(e)
        else:
            return jsonify(
                {
                "message":"u unliked this replay.",
                "comment_replay_id":comment_replay_id,
                "comment_replay_likes_number":comment_replay_likes_number-1,
                'unliked':True

                }
            )
    commentreplayslike=CommentReplaysLike(current_user.id,
    twittid,commentid,comment_replay_id)
    try:
        db.session.add(commentreplayslike)
        db.session.commit()
    except BaseException as e:
        return str(e)
    else:
        return jsonify(
            {
               "message":"liked this replay",
               "comment_replay_id":comment_replay_id,
               "comment_replay_likes_number":comment_replay_likes_number+1,
               'unliked':False
            }
        )

@comments_bp.route('/home/twitts/see_replay_on_replays/',methods=['GET'],defaults={'twittid':1,'id':1,'comment_replay_id':1})
def SeeReplayOnReplays(twittid,id,comment_replay_id,request_from):
    if "replay_liked_message" in request.args:
        replay_liked_message=request.args['replay_liked_message']
    else:
        replay_liked_message=""
    if request_from==1:
        replayonreplays=ReplayOnReplays.query.filter_by(replayid=id).filter_by(twittid=twittid).filter_by(comment_replay_id=comment_replay_id).filter_by(replaytable=True).all()
    elif request_from==0:
         replayonreplays=ReplayOnReplays.query.filter_by(replayid=id).filter_by(twittid=twittid).filter_by(comment_replay_id=comment_replay_id).filter_by(replaytable=False).all()


    if replayonreplays:
        return render_template('SeeReplayOnReplays.html',replayonreplays=replayonreplays,ReplaysOnReplayLikes=ReplaysOnReplayLikes,User=User)
    return "No replays!"

@comments_bp.route('/home/twitts/see_replay_on_replays/likereplaysonreplay/',methods=['POST'])
def LikeReplaysOnReplay():
    comment_replay_id=request.form['comment_replay_id']
    replaytable=bool(int(request.form['replaytable']))
    replaysonreplaylikesnumber=ReplaysOnReplayLikes.query.filter_by(liked_replay_id=int(request.form['id'])).filter_by(comment_replay_id=
    comment_replay_id).filter_by(replaytable=replaytable).count()

    if ReplaysOnReplayLikes.query.filter_by(userid=current_user.id).filter_by(liked_replay_id=request.form['id']).filter_by(comment_replay_id=
    comment_replay_id).filter_by(replaytable=replaytable).first():
        unlikerp=ReplaysOnReplayLikes.query.filter_by(userid=current_user.id).filter_by(liked_replay_id=request.form['id']).filter_by(comment_replay_id=comment_replay_id).filter_by(replaytable=replaytable).first()
        try:
            db.session.delete(unlikerp)
            db.session.commit()
        except BaseException as e:
            return str(e)
        else:
            return jsonify({
                "message":"u unliked this replay!",
                'replaysonreplaylikesnumber':replaysonreplaylikesnumber-1,
                'id':request.form['id'],
                'unliked':True
            })
    
    likereplaysonreplay=ReplaysOnReplayLikes(current_user.id,int(request.form['twittid']),int(request.form['id']),request.form['comment_replay_id'],bool(int(request.form['replaytable'])))
    try:
        db.session.add(likereplaysonreplay)
        db.session.commit()
    except BaseException as e:
        return str(e)

    return jsonify({
            "message":"u liked this replay!",
            'replaysonreplaylikesnumber':replaysonreplaylikesnumber+1,
            'id':request.form['id'],
            'unliked':False
        })

@comments_bp.route('/home/twitts/leave_replay_on_replays/',methods=['POST'])
def Leave_Replay_On_Replays():
    if ReplayOnReplays.query.count()==0:
        Id=2
    else:
        Id=Id=ReplayOnReplays.query.order_by(desc("id")).first().id+1
    if request.form['replaytable']=='1':
        replayonreplays=ReplayOnReplays(Id,current_user.id,request.form['twittid'],request.form['id'],request.form['comment_replay_id'],True,request.form['replay'])
    elif request.form['replaytable']=='0':
        replayonreplays=ReplayOnReplays(Id,current_user.id,request.form['twittid'],request.form['id'],request.form['comment_replay_id'],False,request.form['replay'])
    try:
        db.session.add(replayonreplays)
        db.session.commit()
    except BaseException as e:
        return jsonify({
            'message':str(e)
        })
    else:
        return jsonify({
            'message':'well replied:)',
        })
