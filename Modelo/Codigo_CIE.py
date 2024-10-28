from peewee import *

db = SqliteDatabase("DB_Hospital.db")

class Codigo_CIE(Model):
    id = AutoField() 
    Codigo = CharField()
    Nombre = CharField()
    Categoria = CharField()

    class Meta:
        database = db
