# app/Model.py
from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import desc, or_
from flask_admin.contrib.sqla import ModelView

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    dtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    __tablename__ = 'user'

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return f'<User {self.username}>'


class Following(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    following_userid = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    dtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    __tablename__ = 'following'

    def __init__(self, userid, following_userid):
        self.userid = userid
        self.following_userid = following_userid

    def __repr__(self):
        return f'<Following {self.id}>'


class Twitts(UserMixin, db.Model):
    __tablename__ = 'twitts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    twitt = db.Column(db.String(100), nullable=False)
    dtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fk = db.relationship('User', foreign_keys=[userid])

    def __init__(self, userid, twitt):
        self.userid = userid
        self.twitt = twitt

    def __repr__(self):
        return f'<Twitt {self.twitt} - id={self.id}>'


class Retwitts(UserMixin, db.Model):
    __tablename__ = 'retwitts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    twittid = db.Column(db.Integer, db.ForeignKey('twitts.id', ondelete='CASCADE'), nullable=False)
    dtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fk_userid = db.relationship("User", foreign_keys=[userid])
    fk_twittid = db.relationship("Twitts", foreign_keys=[twittid])

    def __init__(self, userid, twittid):
        self.userid = userid
        self.twittid = twittid

    def __repr__(self):
        return f'<Retwitt {self.id}>'


class Comments(UserMixin, db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    twittid = db.Column(db.Integer, db.ForeignKey('twitts.id', ondelete='CASCADE'), nullable=False)
    comment = db.Column(db.String(100), nullable=False)
    dtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, twittid, userid, comment):
        self.userid = userid
        self.twittid = twittid
        self.comment = comment

    def __repr__(self):
        return f'<Comments {self.id}>'


class CommentLike(UserMixin, db.Model):
    __tablename__ = 'commentlike'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    twittid = db.Column(db.Integer, db.ForeignKey('twitts.id', ondelete='CASCADE'), nullable=False)
    commentid = db.Column(db.Integer, db.ForeignKey('comments.id', ondelete='CASCADE'), nullable=False)
    dtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, twittid, userid, commentid):
        self.userid = userid
        self.twittid = twittid
        self.commentid = commentid


class CommentReplays(UserMixin, db.Model):
    __tablename__ = 'commentreplays'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    twittid = db.Column(db.Integer, db.ForeignKey('twitts.id', ondelete='CASCADE'), nullable=False)
    commentid = db.Column(db.Integer, db.ForeignKey('comments.id', ondelete='CASCADE'))
    replay = db.Column(db.String(100), nullable=False)
    dtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, userid, twittid, commentid, replay):
        self.userid = userid
        self.twittid = twittid
        self.commentid = commentid
        self.replay = replay


class CommentReplaysLike(UserMixin, db.Model):
    __tablename__ = 'commentreplayslike'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    twittid = db.Column(db.Integer, db.ForeignKey('twitts.id', ondelete='CASCADE'), nullable=False)
    commentid = db.Column(db.Integer, db.ForeignKey('comments.id', ondelete='CASCADE'))
    comment_replay_id = db.Column(db.Integer, db.ForeignKey('commentreplays.id', ondelete='CASCADE'))
    dtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, userid, twittid, commentid, comment_replay_id):
        self.userid = userid
        self.twittid = twittid
        self.commentid = commentid
        self.comment_replay_id = comment_replay_id


class ReplayOnReplays(UserMixin, db.Model):
    __tablename__ = 'replayonreplays'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    twittid = db.Column(db.Integer, db.ForeignKey('twitts.id', ondelete='CASCADE'), nullable=False)
    replayid = db.Column(db.Integer, nullable=False)
    comment_replay_id = db.Column(db.Integer, db.ForeignKey('commentreplays.id', ondelete='CASCADE'), nullable=False)
    replay = db.Column(db.String(100), nullable=False)
    dtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    replaytable = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, Id, userid, twittid, replayid, comment_replay_id, replaytable, replay):
        self.id = Id
        self.userid = userid
        self.twittid = twittid
        self.replayid = replayid
        self.comment_replay_id = comment_replay_id
        self.replay = replay
        self.replaytable = replaytable


class ReplaysOnReplayLikes(UserMixin, db.Model):
    __tablename__ = 'replaysonreplaylikes'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    twittid = db.Column(db.Integer, db.ForeignKey('twitts.id', ondelete='CASCADE'), nullable=False)
    liked_replay_id = db.Column(db.Integer, db.ForeignKey('replayonreplays.id', ondelete='CASCADE'), nullable=False)
    dtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comment_replay_id = db.Column(db.Integer, db.ForeignKey('commentreplays.id', ondelete='CASCADE'), nullable=False)
    replaytable = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, userid, twittid, liked_replay_id, comment_replay_id, replaytable):
        self.userid = userid
        self.twittid = twittid
        self.liked_replay_id = liked_replay_id
        self.comment_replay_id = comment_replay_id
        self.replaytable = replaytable


class TwittLike(UserMixin, db.Model):
    __tablename__ = 'twittlike'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    twittid = db.Column(db.Integer, db.ForeignKey('twitts.id', ondelete='CASCADE'), nullable=False)
    dtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, userid, twittid):
        self.userid = userid
        self.twittid = twittid


class DirectMessages(UserMixin, db.Model):
    __tablename__ = 'directmessages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    reciever_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    message = db.Column(db.String(2000), nullable=False)
    unread = db.Column(db.Boolean, default=True, nullable=False)
    dtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, sender_id, reciever_id, message):
        self.sender_id = sender_id
        self.reciever_id = reciever_id
        self.message = message


class ProfilePhotos(UserMixin, db.Model):
    __tablename__ = 'profilephotos'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    dtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, userid):
        self.userid = userid


# ایجاد جداول
db.create_all()
















