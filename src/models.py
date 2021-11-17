from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Login(db.Model):
    __tablename__ = 'login'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique= True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    _is_active = db.Column(db.Boolean, nullable=False)
    


    def __repr__(self):
        return f'id:{seld.id}, username: {self.username}'

    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username, 
        }
    
    @classmethod
    def get_user_by_email(cls, email_user):
        user = cls.query.filter_by(email = email_user).one_or_none()
    

    def create(self):
        db.session.add(self)
        db.session.commit()




class DetailsStarship(db.Model):
    __tablename__ = 'detailsStarship'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    manufacturer = db.Column(db.String(250), nullable=False) 
    model = db.Column(db.String(250), nullable=False)
    cost_in_credits = db.Column(db.FLOAT, nullable=False)
    max_atmosphering_speed = db.Column(db.FLOAT, nullable=False)

    starship = db.relationship("Starships", back_populates="details")

    def __repr__(self):
        return f'Starship name is: {self.name}, its manufactured by {self.manufacturer}, model {self.model}, it costs {self.cost} credits, and has a max atmospheric speed of {self.max_atmosphering_speed} km/h.'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "manufacturer": self.manufacturer,
            "model" : self.model,
            "cost_in_credits": self.cost_in_credits,
            "max_atmosphering_speed": self.max_atmosphering_speed  
        } 


    @classmethod
    def get_id(cls, id_details):
        detail = cls.query.get(id_details)
        return detail




class Starships(db.Model):
    __tablename__ = 'starships'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    id_details = db.Column(db.Integer, db.ForeignKey("detailsStarship.id"), unique = True)

    details = db.relationship("DetailsStarship", back_populates="starship")
    

    def __repr__(self):
        return f'Starship name is: {self.name} and its properties are {self.properties}'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "id_details": self.details.to_dict()
            # do not serialize the password, its a security breach
        }

    @classmethod
    def get_all_starships(cls):
        all_starships = cls.query.all()
        return all_starships
    
    @classmethod
    def get_starship_id(cls, id):
        starship = cls.query.filter_by(id=id).one_or_none()
        return starship

    def create_new_starship(self):
        db.session.add(self)
        db.session.commit()
        return self 




