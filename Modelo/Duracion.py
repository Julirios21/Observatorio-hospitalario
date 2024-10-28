from peewee import *

db = SqliteDatabase("DB_Hospital.db")

class Duracion(Model):
    ID = AutoField() 
    Nombre = CharField()

    class Meta:
        database = db
