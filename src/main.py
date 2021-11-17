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
from models import db, Starships, DetailsStarship
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
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

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
