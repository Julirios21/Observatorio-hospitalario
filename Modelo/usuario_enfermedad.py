from peewee import *
from Modelo.Tipo import Tipo
from Modelo.Genero import Genero
from Modelo.Enfermedad import Enfermedad
from Modelo.Usuario import Usuario
db = SqliteDatabase("DB_Hospital.db")

# Definir la tabla intermedia para la relación Many-to-Many
class UsuarioEnfermedad(Model):
    id = AutoField()
    usuario = ForeignKeyField(Usuario, backref='enfermedades', on_delete='CASCADE')
    enfermedad = ForeignKeyField(Enfermedad, backref='usuarios', on_delete='CASCADE')

    class Meta:
        database = db
        table_name = 'usuario_enfermedad'  # Nombre de la tabla intermedia
