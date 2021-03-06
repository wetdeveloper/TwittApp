from app import *


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(64), unique=True,nullable=False)
    password= db.Column(db.String(64),nullable=False)
    email=db.Column(db.String(100),nullable=False,unique=True)
    dtime=db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow())
    __tablename__='user'
    def __init__(self,username,password,email):
        self.username=username
        self.password=password
        self.email=email

    @classmethod
    def create(cls):
        cls.__table__.create(engine)
    
    @classmethod
    def remove(cls):
        cls.__table__.drop(engine)
        
    def __repr__(self):
        return '<User {}>'.format(self.username)


class Following(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    userid = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    following_userid=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    dtime=db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow())
    fk_userid=db.relationship('User',foreign_keys=[userid])
    fk_following_userid=db.relationship('User',foreign_keys=[following_userid])
    __tablename__='following'
    def __init__(self,userid,following_userid):
        self.userid=userid
        self.following_userid=following_userid

    @classmethod
    def create(cls):
        cls.__table__.create(engine)
    
    @classmethod
    def remove(cls):
        cls.__table__.drop(engine)
        
    def __repr__(self):
        return '<User {}>'.format(self.username)




class Twitts(UserMixin, db.Model):
    __tablename__='twitts'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    userid = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    twitt=db.Column(db.String(100),nullable=False)
    dtime=db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow())
    fk=db.relationship('User',foreign_keys=[userid])
    
   
    def __init__(self,userid,twitt):
        self.userid=userid
        self.twitt=twitt

    @classmethod
    def create(cls):
        cls.__table__.create(engine)
    
    @classmethod
    def remove(cls):
        cls.__table__.drop(engine)
        
    def __repr__(self):
        return '<Twitt {} ---- id={}>'.format(self.twitt,self.id) 




class Retwitts(UserMixin, db.Model):
    __tablename__='retwitts'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    userid= db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    twittid=db.Column(db.Integer,db.ForeignKey('twitts.id',ondelete='CASCADE'),nullable=False)
    dtime=db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow())
    fk_userid=db.relationship('User',foreign_keys=[userid])
    fk_twittid=db.relationship('Twitts',foreign_keys=[twittid])
    
   
    def __init__(self,userid,twittid):
        self.userid=userid
        self.twittid=twittid

    @classmethod
    def create(cls):
        cls.__table__.create(engine)
    
    @classmethod
    def remove(cls):
        cls.__table__.drop(engine)
        
    def __repr__(self):
        return '<ReTwitt {}>'.format(self.id) 




class Comments(UserMixin, db.Model):
    __tablename__='comments'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    userid = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    twittid=db.Column(db.Integer,db.ForeignKey('twitts.id',ondelete='CASCADE'),nullable=False)
    comment=db.Column(db.String(100),nullable=False)
    dtime=db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow())
    fk_userid=db.relationship('User',foreign_keys=[userid])
    fk_twittid=db.relationship('Twitts',foreign_keys=[twittid])
    
   
    def __init__(self,twittid,userid,comment):
        self.userid=userid
        self.twittid=twittid
        self.comment=comment

    @classmethod
    def create(cls):
        cls.__table__.create(engine)
    
    @classmethod
    def remove(cls):
        cls.__table__.drop(engine)
        
    def __repr__(self):
        return '<Comments {}>'.format(self.id) 


class CommentLike(UserMixin, db.Model):
    __tablename__='commentlike'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    userid = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    twittid=db.Column(db.Integer,db.ForeignKey('twitts.id',ondelete='CASCADE'),nullable=False)
    commentid=db.Column(db.Integer,db.ForeignKey('comments.id',ondelete='CASCADE'),nullable=False)
    dtime=db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow())
    fk_userid=db.relationship('User',foreign_keys=[userid])
    fk_twittid=db.relationship('Twitts',foreign_keys=[twittid])
    fk_commentid=db.relationship('Comments',foreign_keys=[commentid])
    
   
    def __init__(self,twittid,userid,commentid):
        self.userid=userid
        self.twittid=twittid
        self.commentid=commentid

    @classmethod
    def create(cls):
        cls.__table__.create(engine)
    
    @classmethod
    def remove(cls):
        cls.__table__.drop(engine)
        
    def __repr__(self):
        return '<Comment {}>'.format(self.id)






class CommentReplays(UserMixin, db.Model):
    __tablename__='commentreplays'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    userid = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    twittid=db.Column(db.Integer,db.ForeignKey('twitts.id',ondelete='CASCADE'),nullable=False)
    commentid=db.Column(db.Integer,db.ForeignKey('comments.id',ondelete='CASCADE'))
    replay=db.Column(db.String(100),nullable=False)
    dtime=db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow())
    fk_userid=db.relationship('User',foreign_keys=[userid])
    fk_twittid=db.relationship('Twitts',foreign_keys=[twittid])
    fk_commentid=db.relationship('Comments',foreign_keys=[commentid])

    
   
    def __init__(self,userid,twittid,commentid,replay):
        self.userid=userid
        self.twittid=twittid
        self.commentid=commentid
        self.replay=replay

    @classmethod
    def create(cls):
        cls.__table__.create(engine)
    
    @classmethod
    def remove(cls):
        cls.__table__.drop(engine)
        
    def __repr__(self):
        return '<CommentReplays {}>'.format(self.id) 




class CommentReplaysLike(UserMixin, db.Model):
    __tablename__='commentreplayslike'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    userid = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    twittid=db.Column(db.Integer,db.ForeignKey('twitts.id',ondelete='CASCADE'),nullable=False)
    commentid=db.Column(db.Integer,db.ForeignKey('comments.id',ondelete='CASCADE'))
    comment_replay_id=db.Column(db.Integer,db.ForeignKey('commentreplays.id',ondelete='CASCADE'))
    dtime=db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow())
    fk_userid=db.relationship('User',foreign_keys=[userid])
    fk_twittid=db.relationship('Twitts',foreign_keys=[twittid])
    fk_commentid=db.relationship('Comments',foreign_keys=[commentid])
    fk_comment_replay_id=db.relationship('CommentReplays',foreign_keys=[comment_replay_id])

    
   
    def __init__(self,userid,twittid,commentid,comment_replay_id):
        self.userid=userid
        self.twittid=twittid
        self.commentid=commentid
        self.comment_replay_id=comment_replay_id

    @classmethod
    def create(cls):
        cls.__table__.create(engine)
    
    @classmethod
    def remove(cls):
        cls.__table__.drop(engine)
        
    def __repr__(self):
        return '<CommentReplays {}>'.format(self.id) 










class ReplayOnReplays(UserMixin, db.Model):
    __tablename__='replayonreplays'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    twittid=db.Column(db.Integer,db.ForeignKey('twitts.id',ondelete='CASCADE'),nullable=False)
    replayid=db.Column(db.Integer,nullable=False)#id of replay which is replayed on
    comment_replay_id=db.Column(db.Integer,db.ForeignKey('commentreplays.id',ondelete='CASCADE'),nullable=False)
    replay=db.Column(db.String(100),nullable=False)
    dtime=db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow())
    replaytable=db.Column('replaytable',db.Boolean,nullable=False,default=True)
    fk_userid=db.relationship('User',foreign_keys=[userid])
    fk_twittid=db.relationship('Twitts',foreign_keys=[twittid])
    fk_comment_replay_id=db.relationship('CommentReplays',foreign_keys=[comment_replay_id])
    def __init__(self,Id,userid,twittid,replayid,comment_replay_id,replaytable,replay):
        self.userid=userid
        self.twittid=twittid
        self.replayid=replayid
        self.replay=replay
        self.comment_replay_id=comment_replay_id
        self.id=Id
        self.replaytable=replaytable

    @classmethod
    def create(cls):
        cls.__table__.create(engine)
    
    @classmethod
    def remove(cls):
        cls.__table__.drop(engine)
        
    def __repr__(self):
        return '<ReplayOnReplays {}>'.format(self.id)




class ReplaysOnReplayLikes(UserMixin, db.Model):
    __tablename__='replaysonreplaylikes'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    twittid=db.Column(db.Integer,db.ForeignKey('twitts.id',ondelete='CASCADE'),nullable=False)
    liked_replay_id=db.Column(db.Integer,db.ForeignKey('replayonreplays.id',ondelete='CASCADE'),nullable=False)
    dtime=db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow())
    comment_replay_id=db.Column(db.Integer,db.ForeignKey('commentreplays.id',ondelete='CASCADE'),nullable=False)
    replaytable=db.Column('replaytable',db.Boolean,nullable=False,default=True)
    fk_username=db.relationship('User',foreign_keys=[userid])
    fk_twittid=db.relationship('Twitts',foreign_keys=[twittid])
    fk_liked_replay_id=db.relationship('ReplayOnReplays',foreign_keys=[liked_replay_id])
    fk_comment_replay_id=db.relationship('CommentReplays',foreign_keys=[comment_replay_id])
    
   
    def __init__(self,userid,twittid,liked_replay_id,comment_replay_id,replaytable):
        self.userid=userid
        self.twittid=twittid
        self.liked_replay_id=liked_replay_id
        self.comment_replay_id=comment_replay_id #id of the commentreplay that replayonreplay is replayed on it.
        self.replaytable=replaytable

    @classmethod
    def create(cls):
        cls.__table__.create(engine)
    
    @classmethod
    def remove(cls):
        cls.__table__.drop(engine)
        
    def __repr__(self):
        return '<ReplaysOnReplayLikes {}>'.format(self.id)






class TwittLike(UserMixin, db.Model):
    __tablename__='twittlike'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    twittid=db.Column(db.Integer,db.ForeignKey('twitts.id',ondelete='CASCADE'),nullable=False)
    dtime=db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow())
    fk_userid=db.relationship('User',foreign_keys=[userid])
    fk_twittid=db.relationship('Twitts',foreign_keys=[twittid])
    def __init__(self,userid,twittid):
        self.userid=userid
        self.twittid=twittid
      

    @classmethod
    def create(cls):
        cls.__table__.create(engine)
    
    @classmethod
    def remove(cls):
        cls.__table__.drop(engine)
        
    def __repr__(self):
        return '<twittid {}>'.format(self.id) 




class DirectMessages(UserMixin, db.Model):
    __tablename__='directmessages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id= db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    reciever_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    message=db.Column(db.String(2000),nullable=False)
    unread= db.Column('unread',db.Boolean, default=True,nullable=False)
    dtime=db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow)
    fk_sender_id=db.relationship('User',foreign_keys=[sender_id])
    fk_reciever_id=db.relationship('User',foreign_keys=[reciever_id])

    
   
    def __init__(self,sender_id,reciver_id,message):
        self.sender_id=sender_id
        self.reciever_id=reciver_id
        self.message=message
      

    @classmethod
    def create(cls):
        cls.__table__.create(engine)
    
    @classmethod
    def remove(cls):
        cls.__table__.drop(engine)
        
    def __repr__(self):
        return '<direct {}>'.format(self.id)

class ProfilePhotos(UserMixin, db.Model):
    __tablename__='profilephotos'
    id = db.Column(db.Integer, primary_key=True)
    userid= db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    dtime=db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow)
    fk_userid=db.relationship('User',foreign_keys=[userid])
    def __init__(self,userid):
        self.userid=userid
    @classmethod
    def create(cls):
        cls.__table__.create(engine)
    
    @classmethod
    def remove(cls):
        cls.__table__.drop(engine)
        
    def __repr__(self):
        return '<profilephoto {}>'.format(self.id)


db.create_all() 


# User.create()
# DirectMessages.create()
# Twitts.create()
# Comments.create()
# CommentReplays.create()
# ReplayOnReplays.create()
# TwittLike.create()
# CommentLike.create()
# Following.create()
# Retwitts.create()
# CommentReplaysLike.create()
# ReplaysOnReplayLikes.create()
# ProfilePhotos.create()



# ProfilePhotos.remove()
# ReplaysOnReplayLikes.remove()
# CommentReplaysLike.remove()
# Retwitts.remove()
# Following.remove()
# CommentLike.remove()
# TwittLike.remove()
# DirectMessages.remove()
# ReplayOnReplays.remove()
# CommentReplays.remove()
# Comments.remove()
# Twitts.remove()
# User.remove()

















