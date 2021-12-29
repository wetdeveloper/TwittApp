from app import *
from Model import *
from tools import MessedTwittList,MessedRetwittList
from Forms import *


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



@app.route('/home/twitts/twitt_it/',methods=['POST','GET'])
def TwittIt():
    if request.method=='POST':
        twitt=Twitts(current_user.username,request.form['twitt_text'])
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
    ################## Unread messages notification
    if current_user.is_authenticated:
        unread_messages_senders=[dm.sender for dm in DirectMessages.query.filter_by(reciever=current_user.username).filter_by(unread=True).all()]
        unread_messages_number=DirectMessages.query.filter_by(reciever=current_user.username).filter_by(unread=True).count()
    else:
        unread_messages=False
        unread_messages_senders=False
        unread_messages_number=False
        
    #######################End unread messages notification
    login_message=''
    if 'login_message' in request.args:
        login_message=request.args['login_message']
    start=int(start)
    ##############################TwittsNumber and Twitts List
    if current_user.is_authenticated:
        following_users=[user.following_user for user in Following.query.filter_by(username=current_user.username).all()]+[current_user.username] #users that you followed them # we add the current_user too cuz we will output the current_user twitts too.
        followed_users=[user.following_user for user in Following.query.filter_by(following_user=current_user.username).all()]#users that  followed you
        try:
            twittslist=MessedTwittList(following_users)
        except BaseException as e:
            return str(e)
        retwittslist=MessedRetwittList(following_users)
        TwittsNumber=len(twittslist)+len(retwittslist)
        following_users.remove(current_user.username) 
        
        followers=[follower.username for follower in Following.query.filter_by(following_user=current_user.username).all()]#using for followers list
        followersfollowed=[follower for follower in followers if Following.query.filter_by(username=current_user.username).filter_by(following_user=follower).first()]#using for followers list
        followings=[following.following_user for following in Following.query.filter_by(username=current_user.username).all()] #using for followinglist
    else:
        twittslist=MessedTwittList()
        retwittslist=MessedRetwittList()
        TwittsNumber=len(twittslist)+len(retwittslist)
        followers=None
        followersfollowed=None
        followings=None
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
   Step=Step,TwittLike=TwittLike,unread_messages_senders=unread_messages_senders,unread_messages_number=unread_messages_number,DirectMessages=DirectMessages,
   Twitts_perPage=Twitts_perPage,TwittsNumber=TwittsNumber,following_users_number=len(following_users) if current_user.is_authenticated else None
   ,followed_users_number=len(followed_users ) if current_user.is_authenticated else None , retwittslist=retwittslist,Twitts=Twitts,abs=abs,datetime=datetime,
   followings=followings,followersfollowed=followersfollowed,followers=followers)



@app.route("/home/twitts/retwitt/",methods=['POST'])
def ReTwitt():
    retwitter_username=current_user.username
    twittid=request.form['twittid']
    if (Retwitts.query.filter_by(username=current_user.username)
    .filter_by(twittid=twittid).first()):
        message="You already retwitted this twitt.you can not retwitt a twitt twice. "
        return jsonify({
            'message':message
        }) 
    else:
        retwitt=Retwitts(retwitter_username,twittid)
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
        username=current_user.username
        twittid=request.form['twittid']
        twitt_likes_number=TwittLike.query.filter_by(twittid=twittid).count()
        print(f'type of twittid is {type(twittid)}')
        if TwittLike.query.filter_by(username=current_user.username).filter_by(twittid=twittid).first(): #twit's likes number aren't canged
            return jsonify({
                'message':"You already liked this twitt-don't try to like a twitt twice","twitt_likes_number":twitt_likes_number,
                "twittid":twittid
                }
                )
        twitt_like=TwittLike(username, twittid)
        try:
            db.session.add(twitt_like)
            db.session.commit()
        except BaseException as e:
            return str(e)
    return jsonify(
                    {
                    "url":url_for('twitts'),'html':'twitts.html'
                    ,'message':"twitt Liked","twitt_likes_number":twitt_likes_number+1,
                    "twittid":twittid
                    }
                )
    



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
    CommentLike=CommentLike,CommentsNumber=CommentsNumber)


@app.route('/home/twitts/like_comment/',methods=['POST'])
def LikeComment():
    if request.method=='POST':
        username=current_user.username
        twittid=request.form['twittid'] 
        commentid=request.form['commentid']
        comment_likes_number=CommentLike.query.filter_by(twittid=twittid).filter_by(commentid=commentid).count()
        if CommentLike.query.filter_by(username=current_user.username).filter_by(commentid=commentid).first():
            return jsonify(
                {
                    'message':'U already liked this Comment .dont attempt to like again'
                    ,'comment_likes_number':comment_likes_number
                }
            )
        comment_like=CommentLike(twittid,username,commentid)
        try:
            db.session.add(comment_like)
            db.session.commit()
        except BaseException as e:
            return str(e)
        else:
            return jsonify(
                {
                    'message':'comment is liked:)',
                    'comment_likes_number':comment_likes_number+1
                }
            )
        


@app.route('/home/twitts/leave_comments/',methods=['POST'])
def LeaveComment():
    comment=Comments(request.form['twittid'],current_user.username,request.form['comment'])
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
        return render_template('CommentReplays.html',commentreplays=commentreplays,CommentReplaysLike=CommentReplaysLike,CommentReplayLiked_message=CommentReplayLiked_message)
    return 'No replays on this comment'

@app.route('/home/twitts/leave_comment_replay/',methods=['POST'])
def LeaveCommentReplay():
    commentreplays=CommentReplays(current_user.username, request.form['twittid'],request.form['commentid'],request.form['replay'])
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
    if CommentReplaysLike.query.filter_by(username=current_user.username).filter_by(commentid=commentid).filter_by(comment_replay_id=comment_replay_id).first():
        return jsonify(
            {
               "message":"U already liked this replay.don't attempt to like again",
               "comment_replay_id":comment_replay_id,
               "comment_replay_likes_number":comment_replay_likes_number

            }
        )
    commentreplayslike=CommentReplaysLike(current_user.username,
    twittid,commentid,comment_replay_id)
    try:
        db.session.add(commentreplayslike)
        db.session.commit()
    except BaseException as e:
        return str(e)
    else:
        return jsonify(
            {
               "message":"U already liked this replay.don't attempt to like again",
               "comment_replay_id":comment_replay_id,
               "comment_replay_likes_number":comment_replay_likes_number+1
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
        return render_template('SeeReplayOnReplays.html',replayonreplays=replayonreplays,ReplaysOnReplayLikes=ReplaysOnReplayLikes)
    return "No replays!"


@app.route('/home/twitts/see_replay_on_replays/likereplaysonreplay/',methods=['POST'])
def LikeReplaysOnReplay():
    replaysonreplaylikesnumber=ReplaysOnReplayLikes.query.filter_by(liked_replay_id=int(request.form['id'])).filter_by(comment_replay_id=
    request.form['comment_replay_id']).filter_by(replaytable=bool(int(request.form['replaytable']))).count()

    if ReplaysOnReplayLikes.query.filter_by(username=current_user.username).filter_by(liked_replay_id=int(request.form['id'])).filter_by(comment_replay_id=
    request.form['comment_replay_id']).filter_by(replaytable=bool(int(request.form['replaytable']))).first():
        return jsonify({
            "message":"U already liked this replay.don't attempt to like again",
            'replaysonreplaylikesnumber':replaysonreplaylikesnumber,
            'id':request.form['id']
        })
    
    likereplaysonreplay=ReplaysOnReplayLikes(current_user.username,int(request.form['twittid']),int(request.form['id']),request.form['comment_replay_id'],bool(int(request.form['replaytable'])))
    try:
        db.session.add(likereplaysonreplay)
        db.session.commit()
    except BaseException as e:
        return str(e)

    return jsonify({
            "message":"Liked XD:)",
            'replaysonreplaylikesnumber':replaysonreplaylikesnumber+1,
            'id':request.form['id']
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
        replayonreplays=ReplayOnReplays(Id,current_user.username,request.form['twittid'],request.form['id'],request.form['comment_replay_id'],True,request.form['replay'])
    elif request.form['replaytable']=='0':
        replayonreplays=ReplayOnReplays(Id,current_user.username,request.form['twittid'],request.form['id'],request.form['comment_replay_id'],False,request.form['replay'])
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
            password=form.password.data
            try:
                user=User(username,password)
                db.session.add(user)
                db.session.commit()
                login_user(user)
            except BaseException as e:
                return str(e)
            else:
                return redirect(url_for('twitts'))
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
            user=User.query.filter_by(username=username).filter_by(password=password).first()
            if user:
                login_user(user)
                return redirect(url_for('twitts'))
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


@app.route('/home/twitts/direct/<string:reciever_username>',methods=['GET'])
@app.route('/home/twitts/direct',methods=['GET'],defaults={'reciever_username':False})
@app.route('/home/twitts/direct',methods=['POST'])
def Direct(reciever_username=None):
    if current_user.is_authenticated:
        
        if request.method=='POST':
            reciever_username=request.form['reciever_username']
            message=request.form['message']
            dm=DirectMessages(current_user.username, reciever_username, message)
            try:
                db.session.add(dm)
                db.session.commit()
            except BaseException as e:
                return str(e)
            else:
                return redirect(url_for('Direct',reciever_username=reciever_username))
        elif request.method=='GET':
            if reciever_username==False:
                if 'reciever_username' in request.args:
                    reciever_username=request.args['reciever_username']
                else:
                    return redirect(url_for('twitts'))
            elif reciever_username==current_user.username:
                    return "You not send message to yourself! this option will be able soon."
            ############ set unread=False
            unread_messages=DirectMessages.query.filter_by(reciever=current_user.username).filter_by(sender=reciever_username).filter_by(unread=True).all()
            for unmsg in unread_messages:
                unmsg.unread=False
                db.session.commit()
            ############ end set unread=False
            dms=DirectMessages.query.filter(or_(DirectMessages.reciever==reciever_username,DirectMessages.reciever==current_user.username)).filter(or_(DirectMessages.sender==reciever_username,DirectMessages.sender==current_user.username)).order_by(desc(DirectMessages.dtime)).all()
            return render_template('directpage.html',reciever_username=reciever_username,dms=dms)
    
    return 'You should login first.'


@app.route('/home/twitts/followers/',methods=['POST'])
def Followers():
    if request.method=='POST':
        if current_user.is_authenticated:
            followers=[follower.username for follower in Following.query.filter_by(following_user=current_user.username).all()]
            followersfollowed=[follower for follower in followers if Following.query.filter_by(username=current_user.username).filter_by(following_user=follower).first()]
            return jsonify({
                'followers':followers,
                'followersfollowed':followersfollowed,
                'message':'followers list is ready'
            })
           
@app.route('/home/twitts/followings/',methods=['POST'])
def Followings():
    if request.method=="POST":
        if current_user.is_authenticated:
            followings=[following.following_user for following in Following.query.filter_by(username=current_user.username).all()]
            return jsonify({
                'followings':followings,
                'message':'followings list is ready'
            })

@app.route('/home/twitts/follow/',methods=['POST'])
def Follow():
    if request.method=='POST':
        if current_user.is_authenticated:
            followingtarget=request.form['followingtarget']
            if followingtarget==current_user.username:
                return jsonify({
                    'message':'You can not follow yourself'
                })
            follow=Following(current_user.username,followingtarget)
            if Following.query.filter_by(username=current_user.username).filter_by(following_user=followingtarget).first():
                return jsonify({
                    'message':"you've followed this user before.",
                    
                })
            else:
                try:
                    db.session.add(follow)
                    db.session.commit()
                except BaseException as e:
                    return jsonify({
                        'message':f'error:{e}'
                    })
                else:
                    return jsonify({
                        'message':f"you are following {request.form['followingtarget']} now",
                    })

@app.route('/home/twitts/unfollow/',methods=['POST'])
def UnFollow():
    if request.method=='POST':
        if current_user.is_authenticated:
            unfollowingtarget=request.form['unfollowingtarget']
            unfollower=request.form['unfollower']
            unfollow=Following.query.filter_by(username=unfollower).filter_by(following_user=unfollowingtarget).first()
            if unfollow:
                try:
                    db.session.delete(unfollow)
                    db.session.commit()
                except BaseException as e:
                    return jsonify({
                        'message':f'error:{e}'
                    })
                else:
                    return jsonify({
                        'message':f"you unfollowed user: {unfollowingtarget}",
                    })
            else:
                return jsonify({
                    'message':f'you unfollowed user:{unfollowingtarget} before'
                })


@app.route('/home/twitts/search-user/',methods=['GET'])
def Search():
    username=request.args.get('searcheduser')
    user=User.query.filter_by(username=username).first()
    if not(user):
        return "Not found any user"
    return render_template('searched_users.html',user=user,Following=Following)

# admin.add_view(ModelView(User, db.session))
# admin.add_view(ModelView(Twitts, db.session))
# admin.add_view(ModelView(Comments,db.session))
# admin.add_view(ModelView(CommentReplays,db.session))
# admin.add_view(ModelView(ReplayOnReplays,db.session))
# admin.add_view(ModelView(TwittLike,db.session))
# admin.add_view(ModelView(DirectMessages,db.session))
# admin.add_view(ModelView(CommentLike,db.session))
# admin.add_view(ModelView(Following,db.session))
# admin.add_view(ModelView(Retwitts,db.session))
# admin.add_view(ModelView(CommentReplaysLike,db.session))
# admin.add_view(ModelView(ReplaysOnReplayLikes,db.session))
app.run(debug='True')

