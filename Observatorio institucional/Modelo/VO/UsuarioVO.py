class Usuario:

    def __init__(self,cc, nombre, apellido, direccion, tipo, departamento, ciudad, edad, categoria, correo, contraseña):
        self.__cc = cc
        self.__nombre = nombre
        self.__appellido = apellido
        self.__direccion = direccion
        self.__tipo = tipo
        self.__ciudad = ciudad
        self.__edad = edad
        self.__categoria = categoria
        self.__correo = correo
        self.__contraseña = contraseña
        self.__departamento = departamento

    def __str__(self) -> str:
        return (f"la cedula es: {self.__cc} y de nombre: {self.__nombre}")
    
    @property
    def cc(self):
        return self.__cc
    
    @property
    def nombre(self):
        return self.__nombre
    
    def setnombre(self,Nnombre):
        self.__nombre = Nnombre