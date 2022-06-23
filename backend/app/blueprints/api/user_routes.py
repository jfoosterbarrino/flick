from . import bp as api
from app.blueprints.auth.authy import token_auth
from flask import request, make_response, g, abort
from app.models import *
from helpers import require_admin


#ADMIN ROUTES (ADMIN REQUIRED)
## GET ALL USERS
## GET USER BY ID
## PUT USER BY ID
## DELETE USER BY ID

@api.get('/user')
@token_auth.login_required()
def get_users():
    users = User.query.all()
    users_dicts = [user.to_dict() for user in users]
    return make_response({"users":users_dicts}, 200)

@api.get('/user/<int:id>')
@token_auth.login_required()
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(404)
    user_dict = user.to_dict()
    return make_response(user_dict, 200)

@api.put('/user/<int:id>')
@token_auth.login_required()
@require_admin
def put_user_by_id(id):
    user = User.query.get(id)
    if not user:
        abort(404)
    user_dict = request.get_json()
    user.from_dict(user_dict)
    user.save()
    return make_response(f"User {user.first_name} {user.last_name} with Id {user.id} has been updated.", 200)

@api.delete('/user/<int:id>')
@token_auth.login_required()
@require_admin
def delete_user_by_id(id):
    user = User.query.get(id)
    if not user:
        abort(404)
    user.delete()
    return make_response(f"User of Id {id} has been deleted", 200)


# USER ROUTES
## LOGIN BASIC AUTH
## POST USER NO AUTH
## PUT USER TOKEN AUTH
## DELETE USER TOKEN AUTH

@api.post('/user')
def post_user():
    user_dict = request.get_json()
    if not User.query.filter_by(email=user_dict.get('email')).first():
        user = User()
        user.register(user_dict)
        user.save()
        return make_response("success",200)
    else:
        abort(409)

@api.put('/user')
@token_auth.login_required()
def put_user():
    user_dict = request.get_json()
    user = User.query.filter_by(email=user_dict.get('email')).first()
    if not user:
        make_response("Not Found, please input correct email", 404)
    user.from_dict(user_dict)
    db.session.commit()
    return make_response("success",200)

@api.delete('/user')
@token_auth.login_required()
def delete_user():
    g.current_user.delete()
    return make_response("success",200)




