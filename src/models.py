from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Login(db.Model):
    __tablename__='login'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)
    _is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'{self.username}, id: {self.id}'

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            # la clase no se pone aqui!
        }


class People(db.Model):
    __tablename__='people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    id_properties = db.Column(db.Integer, db.ForeignKey("people_properties.id"), unique=True)
    
    properties=db.relationship("PeopleProperties", back_populates= "people")

    def __repr__(self):
        return f' People is :{self.name}, id:{self.id}, properties: {self.id_properties}'


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "properties": self.id_properties
        }

    @classmethod
    def get_all(cls):
        persons= cls.query.all()
        return persons

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def get_people_id(cls,id_people):
        people= cls.query.get(id_people)
        return people


class PeopleProperties(db.Model):
    __tablename__='people_properties'

    id=db.Column(db.Integer, primary_key=True)
    Height=db.Column(db.Integer, nullable=False)
    Mass=db.Column(db.Integer, nullable=False)
    Hair_color=db.Column(db.String(250), nullable=False)
    Birth_year=db.Column(db.DATETIME(timezone=False), nullable=False)

    people=db.relationship("People", back_populates= "properties")

    def __repr__(self):
        return f' Properties are :{self.Height}, id:{self.id}, Hair_color: {self.Hair_color}, Skin_color: {self.Skin_color}, Eyes_color: {self.Eyes_color}, Birth_year: {self.Birth_year}'

    def to_dict(self):
        return {
            "id": self.id,
            "Height": self.Height, 
            "Hair_color": self.Hair_color, 
            "Birth_year": self.Birth_year
        }

    @classmethod
    def get_by_id_propertie(cls, id_properties):
        propertie=cls.query.get(id_properties)
        return propertie