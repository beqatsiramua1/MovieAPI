from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager


app = Flask(__name__)
api = Api(app)
db_name = 'mydib.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "superhard-secret-key"
jwt = JWTManager(app)
db = SQLAlchemy(app)

resource_register = {
    'email': fields.String,
    'password': fields.String
}

resource_users = {
    'id': fields.Integer,
    'email': fields.String,
    'password': fields.String
}

resource_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "imdb": fields.Float,
    "release_date": fields.Integer,
    "director": fields.String,
    "link": fields.String
}


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return f"email - {self.email}"


class MovieModel(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(), nullable=True)
    imdb = db.Column(db.Float, nullable=True)
    release_date = db.Column(db.Integer, unique=False, nullable=True)
    director = db.Column(db.String(), unique=False, nullable=True)
    link = db.Column(db.String(), nullable=True)

    def __init__(self, title, imdb, release_date, director, link):
        self.title = title
        self.imdb = imdb
        self.release_date = release_date
        self.director = director
        self.link = link


    def __repr__(self):
        return f"movie - {self.title}, {self.imdb}, {self.release_date}, {self.director}, {self.link}"


userParser = reqparse.RequestParser()
userParser.add_argument('email', type=str, help='Email should be string')
userParser.add_argument('password', type=str, help='Password should be string')

registerParser = reqparse.RequestParser()
registerParser.add_argument('email', type=str, required=True, help='This should be string type')
registerParser.add_argument('password', type=str, required=True, help='This should be string type')

movieParser = reqparse.RequestParser()
movieParser.add_argument("title", type=str, help="This type should be string")
movieParser.add_argument("imdb", type=float, help="This should be integer type")
movieParser.add_argument("release_date", type=int, help="THis type should be integer")
movieParser.add_argument("director", type=str, help="THis type should be string")
movieParser.add_argument("link", type=str, help="This type should be string")


class Register(Resource):
    # @marshal_with(resource_register)
    def post(self):
        args = registerParser.parse_args()
        user = UserModel(email=args['email'], password=generate_password_hash(args['password']))
        db.session.add(user)
        db.session.commit()
        return 'You are registered!', 201


class Auth(Resource):
    def post(self):
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        user = UserModel.query.filter_by(email=email).first()
        if user == None:
            return "{'msg': 'Email was not found'}"
        if email != user.email and check_password_hash(user.password, password) == False:
            return jsonify({'msg': 'Bad email or password'}), 401
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token)


class User(Resource):
    @marshal_with(resource_users)
    @jwt_required()
    def get(self, user_id):
        if user_id == 000:
            return UserModel.query.all()
        user = UserModel.query.filter_by(id=user_id).first()
        return user

    # @marshal_with(resource_users)
    @jwt_required()
    def post(self, user_id):
        args = userParser.parse_args()
        password = generate_password_hash(args['password'])
        user = UserModel(email=args['email'], password=password)
        db.session.add(user)
        db.session.commit()
        return f'Created user with id {user_id}'

    # @marshal_with(resource_users)
    @jwt_required()
    def put(self, user_id):
        args = userParser.parse_args()
        user = UserModel.query.filter_by(id=user_id).first()
        password = generate_password_hash(args['password'])
        if user == None:
            user = UserModel(email=args['email'], password=password)
        else:
            user.email = args['email']
            user.password = password
        db.session.add(user)
        db.session.commit()
        return f'Edited user with id {user_id}'

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        return f'Deleted user with id {user_id}'


class Movie(Resource):
    @marshal_with(resource_fields)
    @jwt_required()
    def get(self, movie_id):
        if movie_id == 777:
            return MovieModel.query.all()
        vaccine = MovieModel.query.filter_by(id=movie_id).first()
        return vaccine

    # @marshal_with(resource_fields)
    @jwt_required()
    def post(self, movie_id):
        args = movieParser.parse_args()
        movie = MovieModel(title=args['title'], imdb=args['imdb'], release_date=args['release_date'], director=args['director'],
                                      link=args['link'])
        db.session.add(movie)
        db.session.commit()
        return f'Created new movie with id {movie_id}'

    # @marshal_with(resource_fields)
    @jwt_required()
    def put(self, movie_id):
        args = movieParser.parse_args()
        movie = MovieModel.query.filter_by(id=movie_id).first()
        if movie == None:
            movie = MovieModel(title=args['title'], imdb=args['imdb'], release_date=args['release_date'], director=args['director'],
                                      link=args['link'])
        else:
            movie.title = args['title']
            movie.imdb = args['imdb']
            movie.release_date = args['release_date']
            movie.director = args['director']
            movie.link =args['link']
        db.session.add(movie)
        db.session.commit()
        return f'Edited movie with id {movie_id}'

    @jwt_required()
    def delete(self, movie_id):
        movie = MovieModel.query.filter_by(id=movie_id).first()
        db.session.delete(movie)
        db.session.commit()
        return f'Deleted movie with id {movie_id}'



api.add_resource(Register, '/register')
api.add_resource(Auth, '/login')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(Movie, '/movie/<int:movie_id>')


@app.before_first_request
def create_table():
    import data
    data.create_database()


if __name__ == "__main__":
    app.run(debug=True, port=5000)