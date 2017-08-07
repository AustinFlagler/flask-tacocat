import datetime

from flask.ext.login import UserMixin
from flask.ext.bcrypt import generate_password_hash
from peewee import *

DATABASE = SqliteDatabase('tacos.db')

class User(UserMixin, Model):
    email = CharField(unique = True)
    password = CharField(max_length = 100)

    class Meta:
        database = DATABASE

    def get_tacos(self):
        return Taco.select().where(Taco.user == self)

    @classmethod
    def create_user(cls, email, password):
        try:
            with DATABASE.transaction():
                cls.create(
                    email = email,
                    password = generate_password_hash(password)
                )
        except IntegrityError:
            raise ValueError("Sorry, that user already exists.")

class Taco(Model):
    user = ForeignKeyField(rel_model = User, related_name = "tacos")
    protein = CharField()
    shell = CharField()
    cheese = BooleanField()
    extras = TextField()

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Taco], safe=True)
    DATABASE.close()
