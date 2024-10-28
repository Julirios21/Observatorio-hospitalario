from peewee import *

db = SqliteDatabase("DB_Hospital.db")

class Genero(Model):
    id = AutoField()
    Nombre = CharField()

    class Meta:
        database = db