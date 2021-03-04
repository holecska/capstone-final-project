import os
from sqlalchemy import Table, Column, String, Integer, Date, create_engine
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

def setup_db(app):

    if app.config['ENV'] == 'production':
        app.config.from_object('config.ProductionConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')

    db.app = app
    db.init_app(app)
    db.create_all()


association_table = db.Table('association',
                             db.Column('movie_id', db.Integer,
                                       db.ForeignKey('movies.id')),
                             db.Column('actor_id', db.Integer,
                                       db.ForeignKey('actors.id'))
                             )
'''

MOVIES

'''


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    release_date = Column(Date)
    artists = relationship(
        'Actor', secondary=association_table, backref='actor')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }


'''

ACTORS

'''


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String(10))

    # def __init__(self, title, release_date):
    #   self.title = title
    #   self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
