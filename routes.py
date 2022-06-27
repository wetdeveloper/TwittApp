from app import *
from Model import *
from tools import MessedTwittList,MessedRetwittList
from Forms import *
from forgetpassVerification import *


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)




@app.route('/userpage/<string:username>/',methods=["GET"])
@app.route('/userpage/',methods=["GET"])
def userPage(username=None):
    if username==None:
        if "username" in request.args:
            user=User.query.filter_by(username=request.args["username"]).first()
        else:
            return redirect(url_for("twitts"))
    else:
        user=User.query.filter_by(username=username).first()
    if user:
        twitts=Twitts.query.filter_by(userid=user.id).all()
        retwitts=[Twitts.query.filter_by(id=retwitt.twittid).first() for retwitt in Retwitts.query.filter_by(userid=user.id).all()]
        ################## Unread messages notification
        if current_user.is_authenticated:
            unread_messages_senders=[dm.sender_id for dm in DirectMessages.query.filter_by(reciever_id=current_user.id).filter_by(unread=True).all()]
            unread_messages_number=DirectMessages.query.filter_by(reciever_id=current_user.id).filter_by(unread=True).count()
        else:
            unread_messages=False
            unread_messages_senders=False
            unread_messages_number=False
        #######################End unread messages notification
        ####################### followings and followers id
        following_users_number=len([user.following_userid for user in Following.query.filter_by(userid=user.id).all()]) #users that you followed
        followed_users_number=len([user.following_userid for user in Following.query.filter_by(following_userid=user.id).all()])#users that  followed you
        #######################End
        return render_template("user_page.html",user=user,twitts=twitts,unread_messages_senders=unread_messages_senders,unread_messages_number=unread_messages_number,DirectMessages=DirectMessages,
        followed_users_number=followed_users_number,following_users_number=following_users_number,TwittLike=TwittLike,len=len,Following=Following,retwitts=retwitts,User=User)
    else:
        return "There isn't any user by this username."

@app.route('/home/twitts/twitt_it/',methods=['POST','GET'])
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
                "url":url_for('twitts'),'html':'twitts.html',
                'message':"twitted:)"
                }
                )


@app.route('/home/twitts/<int:start>',methods=['GET'])
@app.route('/home/twitts/',defaults={'start':0},methods=['GET'])
def twitts(start):
    login_message=''
    if 'login_message' in request.args:
        login_message=request.args['login_message']
    start=int(start)
    ##############################TwittsNumber and Twitts List
    if current_user.is_authenticated:
        following_usersid=[user.following_userid for user in Following.query.filter_by(userid=current_user.id).all()]+[current_user.id] #users that you followed them # we add the current_user too cuz we will output the current_user twitts too.
        followed_usersid=[user.following_userid for user in Following.query.filter_by(following_userid=current_user.id).all()]#users that  followed you
        try:
            twittslist=MessedTwittList(following_usersid)
        except BaseException as e:
            return str(e)
        retwittslist=MessedRetwittList(following_usersid)
        TwittsNumber=len(twittslist)+len(retwittslist)
        following_usersid.remove(current_user.id) 
        
        followersid=[follower.userid for follower in Following.query.filter_by(following_userid=current_user.id).all()]#using for followers list
        followersfollowedid=[followerid for followerid in followersid if Following.query.filter_by(userid=current_user.id).filter_by(following_userid=followerid).first()]#using for followers list
        followingsid=[following.following_userid for following in Following.query.filter_by(userid=current_user.id).all()] #using for followinglist
    else:
        twittslist=MessedTwittList()
        retwittslist=MessedRetwittList()
        TwittsNumber=len(twittslist)+len(retwittslist)
        followersid=None
        followersfollowedid=None
        followingsid=None
    ############################# end TwittsNumber and Twitts List
    flag=False
    ButtonsNum=2 
    if 'TwittsNumber' and 'ButtonsNum' in app.config:
        if app.config['TwittsNumber']!=TwittsNumber:
            for i in range(1,10):
                if TwittsNumber>=i:
                    if TwittsNumber%i==0:
                        ButtonsNum=i
                        flag=True
            if flag==False:
                for i in range(10,TwittsNumber+1):
                    if TwittsNumber%i==0:
                        flag=True
                        ButtonsNum=i
            app.config['TwittsNumber']=TwittsNumber
            app.config['ButtonsNum']=ButtonsNum
        elif app.config['TwittsNumber']==TwittsNumber:
            TwittsNumber=app.config['TwittsNumber']
            ButtonsNum=app.config['ButtonsNum']
    elif not('TwittsNumber' and 'ButtonsNum' in app.config):
        for i in range(1,10):
            if TwittsNumber>=i:
                if TwittsNumber%i==0:
                    ButtonsNum=i
                    flag=True
            if flag==False:
                for i in range(10,TwittsNumber+1):
                    if TwittsNumber%i==0:
                        flag=True
                        ButtonsNum=i
    #end ButtonsNum
    Twitts_perPage=int(TwittsNumber/ButtonsNum) #TwittsNumber=len(twittlist)+len(retwittslist)
    if Twitts_perPage==0:#when CommentsNumber=1 and ButtonsNumber=2(by default)
        Twitts_perPage=1
    Retwitts_perPage=Twitts_perPage
    Step=2
    if start==ButtonsNum:
        twittslist=twittslist[start*Twitts_perPage:]
        retwittslist=retwittslist[start*Retwitts_perPage:]
    else:
        twittslist=twittslist[start*Twitts_perPage:(start+1)*Twitts_perPage]
        retwittslist=retwittslist[start*Retwitts_perPage:(start+1)*Retwitts_perPage]
    return render_template('twitts.html',twittslist=twittslist,start=start,ButtonsNum=ButtonsNum,login_message=login_message,
   Step=Step,TwittLike=TwittLike,DirectMessages=DirectMessages,
   Twitts_perPage=Twitts_perPage,TwittsNumber=TwittsNumber,following_users_number=len(following_usersid) if current_user.is_authenticated else None
   ,followed_users_number=len(followed_usersid ) if current_user.is_authenticated else None , retwittslist=retwittslist,Twitts=Twitts,abs=abs,datetime=datetime,
   followingsid=followingsid,followersfollowedid=followersfollowedid,followersid=followersid,User=User)



@app.route("/home/twitts/retwitt/",methods=['POST'])
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




@app.route('/home/twitts/like_twitt/',methods=['POST'])
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

@app.route("/home/twitts/twitt/<int:twittid>/likers/<string:username>/",methods=["GET"])
@app.route("/userpage/twitt/<int:twittid>/likers/<string:username>/",methods=["GET"])
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
        
        

    



@app.route('/home/twitts/see_comments/<int:twittid>/<int:start>',methods=['GET'])
@app.route('/home/twitts/see_comments/',methods=['GET'],defaults={'twittid':1,'start':0})
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


@app.route('/home/twitts/like_comment/',methods=['POST'])
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


@app.route('/home/twitts/see_comments/Likers/<int:twittid>/<int:commentid>',methods=['GET'])
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


@app.route('/home/twitts/leave_comments/',methods=['POST'])
def LeaveComment():
    comment=Comments(request.form['twittid'],current_user.id,request.form['comment'])
    db.session.add(comment)
    db.session.commit()
    return jsonify(
        {'message':'commented'}
    )

@app.route('/home/twitts/see_comment_replays/<int:commentid>',methods=['GET'])
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

@app.route('/home/twitts/leave_comment_replay/',methods=['POST'])
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


@app.route('/home/twitts/see_comments/like_comment_replays/',methods=['POST'])
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





@app.route('/home/twitts/see_replay_on_replays/<int:twittid>/<int:id>/<int:comment_replay_id>/<int:request_from>',methods=['GET'])
@app.route('/home/twitts/see_replay_on_replays/',methods=['GET'],defaults={'twittid':1,'id':1,'comment_replay_id':1})
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


@app.route('/home/twitts/see_replay_on_replays/likereplaysonreplay/',methods=['POST'])
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
    #------------------------------------------
    #id=id is the id of the replay that the liked replay is replayed on
   
        


@app.route('/home/twitts/leave_replay_on_replays/',methods=['POST'])
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


@app.route('/myip',methods=['GET'])
def MyIp():
    
    return request.remote_addr,200


@app.route('/logout')
def Logout():
    logout_user()
    return redirect(url_for('twitts'))



@app.route('/signup',methods=['POST','GET'])
def Signup():
    form=SignupForm()
    if request.method=='POST':
        if form.validate_on_submit():
            username=form.username.data
            # password=form.password.data
            password=generate_password_hash(form.password.data)
            email=form.email.data
            user=User.query.filter_by(username=form.username.data).first()
            if not(user):
                try:
                    user=User(username,password,email)
                    db.session.add(user)
                    db.session.commit()
                    login_user(user)
                except BaseException as e:
                    return str(e)
                else:
                    return redirect(url_for('twitts'))
            return "This username is already taken.try another."
        else:
            return str(form.errors)
    elif request.method=='GET':
        return render_template('signup.html',form=form)

        

@app.route('/home/login',methods=['POST','GET'])
def Login():
    form=LoginForm()
    if request.method=='POST':
        if form.validate_on_submit():
            username=form.username.data
            password=form.password.data
            # user=User.query.filter_by(username=username).filter_by(password=password).first()
            user=User.query.filter_by(username=username).first()
            if user:
                if check_password_hash(user.password,password):
                    login_user(user)
                    return redirect(url_for('twitts'))
                return "Wrong Password"
            else:
                return redirect(url_for('Login',message='No user matches taken username and password. \n try again. '))
        return str(form.errors)
    elif request.method=='GET':
        message=''
        if current_user.is_authenticated:
            return redirect(url_for('twitts',login_message="You're already logged in.first logout then try to login via other account"))
        if 'message' in request.args:
            message=request.args['message']
        return render_template('login.html',message=message,form=form)


@app.route('/home/login/forgetpassword/',methods=["GET","POST"])
def ForgetPassword():
    form=ForgetPasswordForm()
    if request.method=="GET":
        if current_user.is_authenticated:
            return jsonify({
                "message":"You are already a user.log out to login twice!"
            })
        return render_template("forgetpassword.html",form=form)
    elif request.method=="POST":
        if form.validate_on_submit():
            username=form.username.data
            user=User.query.filter_by(username=username).first()
            if user:
                emailAddress=user.email
                session["verification"]={}
                session["verification"]["verificationCode"]=[str(random.randint(0,9)) for i in range(4)]
                session["verification"]["verificationCode"]="".join(session["verification"]["verificationCode"])
                session["verification"]["emailAddress"]=emailAddress
                mailVerCode(emailAddress,session["verification"]["verificationCode"])
                return redirect(url_for("ResetPassword"))
            else:
                return jsonify({
                    "message":"User is not found"
                })
        else:
            return str(form.errors)
@app.route('/home/login/forgetpassword/resetpassword',methods=['GET','POST'])
def ResetPassword():
    form=ResetPasswordForm()
    if request.method=='GET':
        if current_user.is_authenticated:
            return jsonify({
                "message":"You are already a user.log out to login twice!"
            })
        else:
            if not("verification" in session):
                return redirect(url_for('ForgetPassword'))
            else:
                return render_template('reset-password.html',form=form)
    elif request.method=='POST':
        if form.validate_on_submit():
            if session["verification"]["verificationCode"]==form.verificationCode.data:
                User.query.filter_by(email=session["verification"]["emailAddress"]).first().password=form.newPassword.data
                del session["verification"]
                return jsonify({
                    "message":"Password is Changed!"
                })
            else:
                del session["verification"]
                return redirect(url_for("ForgetPassword"))


@app.route('/home/twitts/direct/<string:reciever_id>',methods=['GET'])
@app.route('/home/twitts/direct',methods=['GET'],defaults={'reciever_id':None})
@app.route('/home/twitts/direct',methods=['POST'])
def Direct(reciever_id=None): #Need to be None to handle Post method otherwise we got positional argument error
    if current_user.is_authenticated:
        if request.method=='POST':
            reciever_id=request.form['reciever_id']
            message=request.form['message']
            dm=DirectMessages(current_user.id, reciever_id, message)
            try:
                db.session.add(dm)
                db.session.commit()
            except BaseException as e:
                return str(e)
            else:
                return redirect(url_for('Direct',reciever_id=reciever_id))
        elif request.method=='GET':
            if reciever_id==None:
                if 'reciever_id' in request.args:
                    reciever_username=request.args['reciever_id']
                else:
                    return redirect(url_for('twitts'))
            elif reciever_id==current_user.id:
                    return "You  can not send message to yourself! this option will be able soon."
            ############ set unread=False
            unread_messages=DirectMessages.query.filter_by(reciever_id=current_user.id).filter_by(sender_id=reciever_id).filter_by(unread=True).all()
            for unmsg in unread_messages:
                unmsg.unread=False
                db.session.commit()
            ############ end set unread=False
            # dms=DirectMessages.query.filter(or_(DirectMessages.reciever_id==reciever_id,DirectMessages.reciever_id==current_user.id)).filter(or_(DirectMessages.sender_id==reciever_id,DirectMessages.sender_id==current_user.id)).order_by(desc(DirectMessages.dtime)).all()
            if int(reciever_id)!=current_user.id:
                dms=DirectMessages.query.filter_by(reciever_id=reciever_id).filter_by(sender_id=current_user.id).all()+DirectMessages.query.filter_by(reciever_id=current_user.id).filter_by(sender_id=reciever_id).all()
            else:
                dms=DirectMessages.query.filter_by(reciever_id=reciever_id).filter_by(sender_id=current_user.id).all()
            dms=sorted(dms,key=lambda x:x.dtime)
            return render_template('directpage.html',reciever_id=reciever_id,dms=dms,User=User)
    
    return 'You should login first.'


@app.route('/userpage/<string:username>/followers/',methods=['GET'])
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

@app.route('/user/<string:username>/followings/',methods=['GET'])
def Followings(username=None):
        user=User.query.filter_by(username=username).first()
        if user:
            if username==None:
                if "username" in request.args:
                    username=request.args["username"]
            followings_id=[following.following_userid for following in Following.query.filter_by(userid=user.id).all()]
            return render_template("followings_list.html",Following=Following,User=User,user=user,followings_id=followings_id)
        return "User not found"



@app.route('/home/twitts/follow/',methods=['POST'])
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
                                return redirect(url_for("Followers",userid=current_user.id))
                            elif request.args["followersOrfollowingsPage"]=="Followings":
                                return redirect(url_for("Followings",userid=current_user.id))
                        else:
                            return redirect(url_for("userPage",username=User.query.filter_by(id=followingtarget_id).first().username))
                return jsonify({
                    'message':f'Something Went Wrong'
                })

@app.route('/home/twitts/unfollow/',methods=['POST'])
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
                            return redirect(url_for("Followers",username=current_user.username))
                        elif request.args["followersOrfollowingsPage"]=="Followings":
                            return redirect(url_for("Followings",username=current_user.username))
                    else:
                        return redirect(url_for("userPage",username=User.query.filter_by(id=unfollowingtarget_id).first().username))
            else:
                return jsonify({
                    'message':f'Something Went Wrong'
                })





@app.route('/home/twitts/search-user/',methods=['GET'])
def Search():
    username=request.args.get('searcheduser')
    user=User.query.filter_by(username=username).first()
    if not(user):
        return "Not found any user"
    return render_template('searched_users.html',user=user,Following=Following)

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Twitts, db.session))
admin.add_view(ModelView(Comments,db.session))
admin.add_view(ModelView(CommentReplays,db.session))
admin.add_view(ModelView(ReplayOnReplays,db.session))
admin.add_view(ModelView(TwittLike,db.session))
admin.add_view(ModelView(DirectMessages,db.session))
admin.add_view(ModelView(CommentLike,db.session))
admin.add_view(ModelView(Following,db.session))
admin.add_view(ModelView(Retwitts,db.session))
admin.add_view(ModelView(CommentReplaysLike,db.session))
admin.add_view(ModelView(ReplaysOnReplayLikes,db.session))
app.run(debug='True')
