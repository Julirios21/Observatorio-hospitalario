from peewee import *
from Modelo.Tipo import Tipo  # Importa correctamente el modelo Tipo
from Modelo.Genero import Genero  # Importa correctamente el modelo Genero
from Modelo.Enfermedad import Enfermedad

db = SqliteDatabase("DB_Hospital.db")

class Usuario(Model):
    id = AutoField()
    CC = IntegerField()
    Nombres = TextField()
    Apellidos = TextField()
    Edad = IntegerField()
    Correo = TextField()
    Contrasena = TextField()
    Municipio = TextField()
    Departamento = TextField()
    Estado = IntegerField()

    # ForeignKeyField para Tipo usando el nombre de columna 'Tipo'
    Tipo = ForeignKeyField(Tipo, db_column='Tipo', backref='usuarios', on_delete='CASCADE')

    # ForeignKeyField para Genero usando el nombre de columna 'Genero'
    Genero = ForeignKeyField(Genero, db_column='Genero', backref='usuarios', on_delete='CASCADE')

    Enfermedad = ManyToManyField(Enfermedad, backref='usuarios')
    class Meta:
        database = db
