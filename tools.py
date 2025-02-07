from app import *
from app import *
from Model import *

def MessedTwittList(following_users=None):
    if current_user.is_authenticated:
        if not(following_users):
            return AssertionError('Empty following user')
        else:
            following_users=following_users
    else:
        following_users=[user.id for user in User.query.all()]
    twittslist=[Twitts.query.filter_by(userid=fuser).all() for fuser in following_users]#مانند یک ماتریس با این لیست رفتار میکنیم ،ستونهای سطر شامل توییت های یک یوزر است یعنی هر سطر متعلق به یک یوزر است
    new_twittlist=list()
    while True:
        count=0
        for i in range(0,len(twittslist)):
            if len(twittslist[i])==0:
                count+=1
                continue
            new_twittlist.append(twittslist[i][0])
            del twittslist[i][0]
        if count==len(twittslist):
            break
    return new_twittlist





def MessedRetwittList(following_usersid=None):
    if current_user.is_authenticated:
        if not(following_usersid):
            return AssertionError('Empty following user')
        else:
            following_usersid=following_usersid
    else:
        following_usersid=[user.id for user in User.query.all()]
    retwittslist=[Retwitts.query.filter_by(userid=fuserid).all() for fuserid in following_usersid]#مانند یک ماتریس با این لیست رفتار میکنیم ،ستونهای سطر شامل توییت های یک یوزر است یعنی هر سطر متعلق به یک یوزر است
    new_retwittslist=list()
    while True:
        count=0
        for i in range(0,len(retwittslist)):
            if len(retwittslist[i])==0:
                count+=1
                continue
            new_retwittslist.append(retwittslist[i][0])
            del retwittslist[i][0]
        if count==len(retwittslist):
            break
    return new_retwittslist



            
  
