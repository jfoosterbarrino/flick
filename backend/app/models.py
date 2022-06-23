from app import db, login
from datetime import datetime as dt, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import secrets


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default = dt.utcnow)
    img = db.Column(db.String)
    is_admin = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, unique = True, index = True)
    token_exp = db.Column(db.DateTime)
    movies = db.relationship('Movie', backref='user', lazy='dynamic', cascade='all, delete', secondary="movie_user")

    def _repr_(self):
        return f'<User: {self.id} | {self.email}>'

    def __str__(self):
        return f'<User: {self.first_name} | {self.last_name} | {self.email}>'

    def hash_password(self,password):
        return generate_password_hash(password)

    def check_password_hash(self,password):
        return check_password_hash(self.password, password)

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])
        self.img = data['img']


    def to_dict(self):
        return{
            'id': self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "created_on": self.created_on,
            "is_admin": self.is_admin,
            "token": self.token,
            "img":self.img
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def add_movie(self, movie):
        self.movies.append(movie)
        db.session.commit()

    def remove_movie(self, movie):
        self.movies.remove(movie)
        db.session.commit()

    def register(self, data):
        self.email = data['email']
        self.password = self.hash_password(data['password'])
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.img = data['img']

    def get_token(self, exp=86400):
        current_time = dt.utcnow()
        if self.token and self.token_exp > current_time + timedelta(seconds=60):
            return self.token
        self.token = secrets.token_urlsafe(32)
        self.token_exp = current_time + timedelta(seconds=exp)
        self.save()
        return self.token

    def revoke_token(self):
        self.token_exp = dt.utcnow() - timedelta(seconds=61)

    @staticmethod
    def check_token(token):
        u = User.query.filter_by(token=token).first()
        if not u or u.token_exp < dt.utcnow():
            return None
        return u

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

        
        
        





# class Genre(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String)
#     movies = db.relationship('Movie', backref = 'genre', lazy='dynamic', cascade = "all, delete-orphan")

#     def __repr__(self):
#         return f'<Genre: {self.id} | {self.name}>'

#     def save(self):
#         db.session.add(self)
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()

#     def to_dict(self):
#         return {
#             "id":self.id,
#             "name":self.name
#         }

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    tmdb_id = db.Column(db.Integer)
    title = db.Column(db.String)
    overview = db.Column(db.Text)
    homepage = db.Column(db.String)
    vote_average = db.Column(db.Float)
    release_date = db.Column(db.String)
    runtime = db.Column(db.Integer)
    poster_path = db.Column(db.String)
    backdrop_path = db.Column(db.String)
    genre_id = db.Column(db.Integer)
    genre_name = db.Column(db.String)

    def __repr__(self):
        return f'<Movie: {self.id} | {self.title}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id, 
            'tmdb_id': self.tmdb_id,
            'title':self.title, 
            'overview' :self.overview, 
            'homepage': self.homepage,
            'vote_average' :self.vote_average, 
            'release_date':self.release_date, 
            'runtime' :self.runtime, 
            'poster_path' :self.poster_path, 
            'backdrop_path':self.backdrop_path,
            'genre_id':self.genre_id,
            'genre_name':self.genre_name

        }

    def register(self, data):
        self.tmdb_id = data['id']
        self.title= data['title']
        self.overview = data['overview']
        self.homepage = data['homepage']
        self.vote_average = data['vote_average']
        self.release_date = data['release_date']
        self.runtime = data['runtime']
        self.poster_path = data['poster_path']
        self.backdrop_path = data['backdrop_path']
        self.genre_id = data['genres'][0]['id']
        self.genre_name = data['genres'][0]['name']


    def from_dict(self, data):
        for category in ['tmdb_id','title','overview','homepage','vote_average','release_date','runtime','poster_path','backdrop_path','genre_id',"genre_name"]:
            if category in data:
                setattr(self, category, data[category])

    



class MovieUser(db.Model):
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)


    


