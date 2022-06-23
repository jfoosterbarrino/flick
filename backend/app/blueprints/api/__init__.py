from flask import Blueprint

bp = Blueprint('api', __name__,url_prefix='/api')

from .import movie_routes, genre_routes, user_routes, auth_routes