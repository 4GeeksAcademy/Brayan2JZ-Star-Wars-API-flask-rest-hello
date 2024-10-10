"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorites, Character, Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
        
    response_body = {
    "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/user/all', methods=['GET'])
def get_all_users():
    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))

    return jsonify(all_users), 200

@app.route('/', methods=['GET'])
def get_people():
    people=Character.query.all()
    serialized_people=[person.serialize() for person in people]

    return jsonify(serialized_people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person=Character.query.get(people_id)
    if person is None:
        raise APIException("Dudeman not found", status_code=404)
    return jsonify(person.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets=Planet.query.all()
    serialized_planets=[planet.serialize() for planet in planets]

    return jsonify(serialized_planets), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet=Planet.query.get(planet_id)
    if planet is None:
        raise APIException("Planet not found", status_code=404)
    return jsonify(planet.serialize()), 200

@app.route('/users/favorites', methods=['GET'])
def list_user_favorites():
    user_id=request.args.get("user_id")
    if user_id is None:
        raise APIException("Please provide User ID", status_code=404)
    user=User.query.get(user_id)
    if user is None:
        raise APIException("User not found", status_code=404)
    

    favorites=Favorites.query.filter_by(user_id=user_id).all()
    serialized_favorites=[favorite.serialize() for favorite in favorites]

    return jsonify(serialized_favorites), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_fav_character(people_id):
    user_id=request.args.get("user_id")
    if user_id is None:
        raise APIException("Please provide User ID", status_code=404)
    user=User.query.get(user_id)
    if user is None:
        raise APIException("User not found", status_code=404)
    
    character=Character.query.get(people_id)
    if character is None:
        raise APIException("Character Not Found", status_code=404)
    
    favorite=Favorites(name=character.name, user_id=user_id, character_id=people_id, category="Character")
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"Message": "Favorite character added successfully"}), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_fav_planet(planet_id):
    user_id=request.args.get("user_id")
    if user_id is None:
        raise APIException("Please provide User ID", status_code=404)
    user=User.query.get(user_id)
    if user is None:
        raise APIException("User not found", status_code=404)
    
    planet=Planet.query.get(planet_id)
    if planet is None:
        raise APIException("planet Not Found", status_code=404)
    
    favorite=Favorites(name=planet.name, user_id=user_id, planet_id=planet_id, category="Planet")
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"Message": "Favorite planet added successfully"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_fav_character(people_id):
    user_id=request.args.get("user_id")
    if user_id is None:
        raise APIException("Please provide User ID", status_code=404)
    
    favorite=Favorites.query.filter_by(user_id=user_id, character_id=people_id).first()
    if favorite is None:
        raise APIException("Person not found", status_code=404)
    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"Message": "Favorite character deleted successfully"}), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(planet_id):
    user_id=request.args.get("user_id")
    if user_id is None:
        raise APIException("Please provide User ID", status_code=404)
    
    favorite=Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite is None:
        raise APIException("Planet not found", status_code=404)
    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"Message": "Favorite planet deleted successfully"}), 200

# @app.route('/user', methods=['POST'])
# def create_user():
#     username = request.json["username"]
#     password = request.json["password"]

#     user1 = User(username=username, password=password)
#     db.session.add(user1)
#     db.session.commit()
        
#     response_body = {
#     "msg": "Hello, created user " + username
#     }
#     return jsonify(response_body), 200

# @app.route('/favorites', methods=['POST'])
# def create_fav():
        
#     if request.json["category"] == "character":
#         char = Character(
#             name=request.json["name"],
#             gender=request.json["gender"],
#             birth_year=request.json["birth_year"],
#             height=request.json["height"],
#             mass=request.json["mass"]
#         )

#         fave = Favorites(
#             name=request.json["name"],
#             category=request.json["category"],
#             user_id=request.json["user_id"],
#             character_id=request.json["entity_id"]
#         )
#     elif request.json["category"] == "planet":
#         planet = Planet(
#             name=request.json["name"],
#             climate=request.json["climate"],
#             gravity=request.json["gravity"],
#             population=request.json["population"],
#             terrain=request.json["terrain"]
#         )
#         fave = Favorites(
#             name=request.json["name"],
#             category=request.json["category"],
#             user_id=request.json["user_id"],
#             planet_id=request.json["entity_id"]
#         )

    # db.session.add(user1)
    # db.session.commit()

    # return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
