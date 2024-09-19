import sqlite3
from db import conexion as cbd
from Modelo.VO.UsuarioVO import Usuario

class UsuarioDAO:
    
    def __init__(self):
        self.getUsuario