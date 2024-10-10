from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            # do not serialize the password, its a security breach
        }
    

    
class Character(db.Model):
    __tablename__="character"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(100))
    birth_year = db.Column(db.String(100))
    height = db.Column(db.String(100))
    mass = db.Column(db.String(100))

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "height": self.height,
            "mass": self.mass
            # do not serialize the password, its a security breach
        }
    
class Planet(db.Model):
    __tablename__="planet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    climate = db.Column(db.String(120))
    gravity = db.Column(db.String(120)) 
    terrain = db.Column(db.String(120))
    population = db.Column(db.String(120))
    

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "population": self.population
            # do not serialize the password, its a security breach
        }
    
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(120))
    user_id = db.Column("user_id", db.ForeignKey(User.id))
    user = db.relationship(User)
    character_id = db.Column("character_id", db.ForeignKey(Character.id))
    character = db.relationship(Character)
    planet_id = db.Column("planet_id", db.ForeignKey(Planet.id))
    planet = db.relationship(Planet)

    def __repr__(self):
        return '<Favorites %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "user_id": self.user_id,
            # "character_id": self.character_id,
            "character": self.character.serialize() if self.character else None,
            # "planet_id": self.planet_id
            "planet": self.planet.serialize() if self.planet else None
            # do not serialize the password, its a security breach
        }