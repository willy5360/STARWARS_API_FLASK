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
from models import db, Planets, PlanetsProperties, People, PeopleProperties, Starships, DetailsStarship, Login
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from sqlalchemy import exc

#from models import Person



app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_KEY')
jwt = JWTManager(app)

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)




@app.route('/starships', methods=['GET'])
def get_starships():
    starships = Starships.get_all_starships()
    all_starships = [starship.to_dict() for starship in starships]
    return jsonify(all_starships), 200


@app.route('/starships/<int:id>', methods=['GET'])
def get_starship_by_id(id):
    starship = Starships.get_starship_id(id)
    return jsonify(starship.to_dict()), 200
    return jsonify({'error': 'Starship not found'}), 400


# @app.route('/starships', methods=['POST'])
# def create_starship():
#     new_starship = request.json.get('name', None)

#     if not new_starship:
#         return jsonify({'error' : 'Missing starship name'}), 400
#     starship = Starships(name=new_starship, properties="")

#     starship_created = starship.create_new_starship()
#     return jsonify(starship_created.to_dict()), 201


@app.route('/starships/<int:id>/details', methods=['GET'])
def select_details(id):
    starship = Starships.get_starship_id(id)
    if starship:
        details = DetailsStarship.get_id(starship.id_details)
    if details:
        return jsonify(details.to_dict()), 200 
    
    return jsonify({'error':'Details not found'}), 400

  



# @app.route("/login", methods=["POST"])
# def login():
#     username = request.json.get("username", None)
#     password = request.json.get("password", None)
#     if username and password :
#         login = Login.get_by_username(username)

#     return jsonify({"error": "invalid data"}), 400

#     access_token = create_access_token(identity=username)
#     return jsonify(access_token=access_token)


@app.route('/planet', methods=['GET'])
def get_all_planets():
    planets = Planets.get_planets()
    all_Planets = [planet.to_dict() for planet in planets]
    return jsonify(all_Planets), 200


@app.route('/planet/<int:id>', methods=['GET'])
def get_planet_by_id(id):
    planet = Planets.get_planet_id(id)
    if planet:
        return jsonify(planet.to_dict()), 200

    return jsonify({'error': 'Planet not found'}), 400



@app.route('/planet/<int:id>/property', methods=['GET'])
def select_properties(id):
    planet = Planets.get_planet_id(id)
    if planet:
        properties = PlanetsProperties.get_id(planet.id_properties)
    if properties:
        return jsonify(properties.to_dict()), 200

    return jsonify({'error': 'properties not found'}), 400


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/people', methods=['GET'])
def get_people():
    persons= People.get_all()
    all_persons=[people.to_dict() for people in persons]
    return jsonify(all_persons), 200



@app.route('/people/<int:id>', methods=['GET'])
def get_people_by_id(id):
    people= People.get_by_id(id)

    if people:
        return jsonify(people.to_dict()), 200

    return jsonify({'error': 'people not found'}), 404



# @app.route('/people', methods=['POST'])
# def create_people():
#     new_people=request.json.get('name',None)

#     if not new_people:
#         return jsonify({'error':'missing people'}), 400

#     people= People(name =new_people)
#     try:
#         people_created=people.create()
#         return jsonify(people_created.to_dict()), 201
#     except exc.IntegrityError:
#         return jsonify({'error': 'fail in data'}), 400


        
@app.route('/people/<int:id>/propertie', methods=['GET'])
def get_properties_by_id(id):
    people=People.get_people_id(id)
    if people:
        properties= PeopleProperties.get_by_id_propertie(people.id_properties)
    if properties:
        return jsonify(properties.to_dict()), 200

    return jsonify({'error': 'propertie not found'}), 404


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
