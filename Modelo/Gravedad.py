from peewee import *

db = SqliteDatabase("DB_Hospital.db")

class Gravedad(Model):
    ID = AutoField() 
    Nombre = CharField()

    class Meta:
        database = db
