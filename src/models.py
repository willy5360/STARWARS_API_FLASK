from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Login(db.Model):
    __tablename__ = "login"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)
    _is_active = db.Column(db.Boolean, nullable=False)

    def __repr__ (self):
        return f'this is {self.id} and username: {self.username}'

    
    def to_dict(self):
        return{
            "id":self.id,
            "username":self.username
        }
    


class PlanetsProperties (db.Model):
    __tablename__ = 'planets_properties'

    id = db.Column(db.Integer, primary_key =True)
    diameter = db.Column(db.FLOAT, nullable=False)
    rotation = db.Column(db.FLOAT, nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    population = db.Column(db.Integer, nullable=False)

    planets = db.relationship("Planets" , back_populates="properties")

    def __repr__ (self):
        return f'This is the id {self.id}, diameter is {self.diameter} kms, rotation is {self.rotation} kms/s, climate is {self.climate}, terrain is {self.terrain} and population is {self.population} aliens'


    def to_dict(self):
        return{
            "id": self.id,
            "diameter": self.diameter,
            "rotation": self.rotation,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population
        }
    @classmethod
    def get_id(cls, id_properties):
        propertie = cls.query.get(id_properties)
        return propertie


class Planets(db.Model):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    id_properties = db.Column(db.Integer,db.ForeignKey("planets_properties.id"), unique=True)

    properties = db.relationship( "PlanetsProperties", back_populates = "planets")

    def __repr__(self):
        return f'Planets is {self.name} and its properties {self.properties} with the id {self.id}'


    def to_dict(self):
        print("aqui esta las id properties", self.properties)
        return {
            "id": self.id,
            "name": self.name,
            "properties": self.properties.to_dict()
        }
    
    @classmethod
    def get_planet_id(cls, id_planet):
        planet = cls.query.get(id_planet)
        return planet

    @classmethod
    def get_planets(cls):
        all_planets = cls.query.all()
        return all_planets

    
    def create_new(self):
        db.session.add(self)
        db.session.commit()
        return self

