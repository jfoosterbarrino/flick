# from . import bp as api
# from app.blueprints.auth.authy import token_auth
# from flask import request, make_response, g, abort
# from app.models import *
# from helpers import require_admin

# @api.get('/genre')
# def get_genres():
#     genres = Genre.query.all()
#     if not genres:
#         abort(404)
#     genres_dicts = [genre.to_dict() for genre in genres]
#     return make_response({"genres":genres_dicts}, 200)

# @api.get('/genre/<int:id>')
# def get_genre(id):
#     genre = Genre.query.get(id)
#     if not genre:
#         abort(404)
#     genre_dict = genre.to_dict()
#     return make_response(genre_dict, 200)

# @api.post('/genre')
# @token_auth.login_required()
# @require_admin
# def post_genre():
#     genre_name =request.get_json().get("name")
#     genre = Genre(name=genre_name)
#     genre.save()
#     return make_response(f"A genre was made with the name {genre.name} and the id of {genre.id}.", 200)

# @api.put('/genre/<int:id>')
# @token_auth.login_required
# @require_admin
# def put_genre(id):
#     genre = Genre.query.get(id)
#     if not genre:
#         abort(404)
#     genre_name = request.get_json().get("name")
#     genre.name = genre_name
#     genre.save()
#     return make_response(f"Genre {genre.id} has a new name: {genre.name}", 200)

# @api.delete('/genre/<int:id>')
# @token_auth.login_required
# @require_admin
# def delete_genre(id):
#     genre = Genre.query.get(id)
#     if not genre:
#         abort(404)
#     genre.delete()
#     return make_response(f"Genre {id} has been deleted", 200)
