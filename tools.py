# tools.py
from app import db
from Model import Twitts, Retwitts, User, Following
from sqlalchemy.orm import joinedload
from sqlalchemy import desc


def get_messed_twitts(following_usersid=None, limit=None, offset=0):
    if following_usersid is None:
        following_usersid = [user.id for user in User.query.all()]
    
    query = Twitts.query.filter(Twitts.userid.in_(following_usersid)) \
        .options(joinedload(Twitts.fk)) \
        .order_by(desc(Twitts.dtime))
    
    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)
    
    return query.all()


def get_messed_retwitts(following_usersid=None, limit=None, offset=0):
    if following_usersid is None:
        following_usersid = [user.id for user in User.query.all()]
    
    query = Retwitts.query.filter(Retwitts.userid.in_(following_usersid)) \
        .options(joinedload(Retwitts.fk_userid), joinedload(Retwitts.fk_twittid)) \
        .order_by(desc(Retwitts.dtime))
    
    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)
    
    return query.all()
