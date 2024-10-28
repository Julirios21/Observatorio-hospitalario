from peewee import *

db = SqliteDatabase("DB_Hospital.db")

class Tipo(Model):
    id = AutoField() 
    Nombre = CharField()

    class Meta:
        database = db
