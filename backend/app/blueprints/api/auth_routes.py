from .import bp as api
from app.blueprints.auth.authy import basic_auth
from flask import make_response, g

@api.get('/login')
@basic_auth.login_required
def get_login():
    user = g.current_user
    token = user.get_token()
    return make_response({"token": token, **user.to_dict()}, 200)