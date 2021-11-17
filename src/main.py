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
from models import db, Planets, PlanetsProperties, Login
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_KEY')  # Change this!
jwt = JWTManager(app)

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

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

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
