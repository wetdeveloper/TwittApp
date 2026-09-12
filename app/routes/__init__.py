from flask import Blueprint


auth_bp = Blueprint("auth", __name__)
users_bp = Blueprint("users", __name__)
tweets_bp = Blueprint("tweets", __name__)
comments_bp = Blueprint("comments", __name__)
social_bp = Blueprint("social", __name__)
messages_bp = Blueprint("messages", __name__)
misc_bp = Blueprint("misc", __name__)


from . import auth
from . import users
from . import tweets
from . import comments
from . import social
from . import messages
from . import misc
