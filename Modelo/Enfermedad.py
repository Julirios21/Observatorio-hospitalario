from peewee import *
from Modelo.Gravedad import *
from Modelo.Duracion import *
from Modelo.Codigo_CIE import *

db = SqliteDatabase("DB_Hospital.db")

class Enfermedad(Model):
    ID = AutoField()
    NombreCientifico = TextField()
    Descripcion = TextField()
    Sintomas = TextField()
    Causas = TextField()
    Prevencion = TextField()
    Tratamiento = TextField()
    TasaMortalidad = FloatField()
    Transmision = TextField()
    RegionPrevalente  = TextField()
    Complicaciones = TextField()

    Gravedad = ForeignKeyField(Gravedad, db_column='Gravedad', backref = 'Enfermedad', on_delete = 'CASCADE')

    Duracion = ForeignKeyField(Duracion, db_column='Duracion', backref = 'Enfermedad', on_delete = 'CASCADE')

    Codigo_CIE = ForeignKeyField(Codigo_CIE, db_column='Codigo_CIE', backref = 'Enfermedad', on_delete = 'CASCADE')

    class Meta:
        database = db