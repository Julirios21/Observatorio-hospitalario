from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime, timedelta
from Modelo.Usuario import Usuario
from Modelo.Tipo import Tipo
from Modelo.Enfermedad import Enfermedad
from Modelo.Genero import Genero
import os

# Especificar la ruta a la carpeta de plantillas "Vista"
template_dir = os.path.abspath('Vista')

app = Flask(__name__, template_folder=template_dir)

app.secret_key = 'ra'



# --------------------------------------------------------
# --------------------------------------------------------
# -------------------Rutas principales------------------
# --------------------------------------------------------
# --------------------------------------------------------

# Por defecto entra al login
@app.route('/')
def home():
    return redirect(url_for('login')) 

# Este es el login
@app.route('/login', methods=['GET', 'POST'])
def login():
 
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        # Verifica si el usuario existe
        usuario = Usuario.get_or_none(Usuario.Correo == correo)
        
         
        if usuario and usuario.Contrasena == contrasena:
            
            # Usa metodo session de flask
            session['usuario_id'] = usuario.id
            session['correo'] = usuario.Correo
            session['tipo_usuario'] = usuario.Tipo.id
        
            # Verifica el tipo de usuario
            if usuario.Tipo.id == 3:  # 3 es usuario externo
                return redirect(url_for('info_usuario_externo', usuario_id=usuario.id))  
            
            elif session['tipo_usuario'] == 2:
                return redirect(url_for('info_usuario_interno', usuario_id=session['usuario_id']))
            
            else:
                return redirect(url_for('info_usuario', usuario_id=usuario.id)) 
            
        else:
            flash ('Usuario o contraseña incorrectos', 'error')   # Manejo de errores

    return render_template('login.html') # redirige a LOGIN.HTML

# no cunfundir con sing_up, este verifica si es usuario interno o externo pá mostrarle la informacion dependiendo del tipo
@app.route('/registrao', methods=['GET', 'POST'])
def registrao():
    if session['tipo_usuario'] == 3:  # Si es usuario externo
        return redirect(url_for('info_usuario_externo', usuario_id=session['usuario_id']))  # INFO_USUARIO_EXTERNO
    elif session['tipo_usuario'] == 2:
        return redirect(url_for('info_usuario_interno', usuario_id=session['usuario_id']))
    else:
        return redirect(url_for('info_usuario', usuario_id=session['usuario_id'])) # INFO_USUARIO
    
    

# Dentro de login.html se redirige al sign_up
# Este registra nuevos usuarios
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():

    # Recoge del front(Vista.sign_up.html)
    if request.method == 'POST':
        # Obtén los datos del html
        cedula = request.form['Cedula']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        edad = request.form['edad']
        genero = request.form['genero']
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        tipo_usuario = request.form['tipo_usuario']
        municipio = request.form['municipio']
        departamento = request.form['departamento']

        # Obtiene usuarios de backend(Modelo.Usuario)
        nuevo_usuario = Usuario(
            CC = cedula,
            Nombres=nombres,
            Apellidos=apellidos,
            Edad=edad,
            Genero=genero,
            Correo=correo,
            Contrasena=contrasena,
            Tipo=tipo_usuario,
            Municipio=municipio,
            Departamento=departamento,
            Estado=1  # Toca ver la tabla de estados
        )
        nuevo_usuario.save() #Guarda el usuario

        # Redirigir después de guardar
        return redirect(url_for('login'))  # Redirige a la página de login después del registro

    return render_template('sign_up.html')  # Muestra el formulario de registro en el método GET


# --------------------------------------------------------
# --------------------------------------------------------
# ----------------------Usuarios------------------------
# --------------------------------------------------------
# --------------------------------------------------------
# Usuario externo
@app.route('/info_usuario_externo/<int:usuario_id>', methods=['GET'])
def info_usuario_externo(usuario_id):
    usuario = Usuario.get_or_none(Usuario.id == usuario_id)
    return render_template('info_usuarioexterno.html', usuario=usuario)

# Usuario interno
@app.route('/info_usuario_interno/<int:usuario_id>', methods=['GET'])
def info_usuario_interno(usuario_id):
    usuario = Usuario.select()
    if usuario is None:
        return "Usuarios no encontrado", 404  # Manejo de error si el usuario no existe
    return render_template('info_usuariointerno.html', Usuarios=usuario)  # Renderiza la plantilla con el usuario

# Usuario mod
@app.route('/info_usuario/<int:usuario_id>', methods=['GET'])
def info_usuario(usuario_id):
    usuario = Usuario.select()
    if usuario is None:
        return "Usuarios no encontrado", 404  # Manejo de error si el usuario no existe
    return render_template('info_usuario.html', Usuarios=usuario)  # Renderiza la plantilla con el usuario

# Listar usuarios
@app.route('/usuarios', methods=['GET'])
def lista_usuarios():
    return redirect(url_for('info_usuario',  usuario_id=session['usuario_id']))
@app.route('/lista_usuarios_internos')

def lista_usuarios_internos():
    # Aquí puedes obtener los datos necesarios para mostrar en el HTML
    usuarios = Usuario.select()

    # Renderizar el template con los datos
    return render_template('info_usuariointerno.html', usuarios=usuarios)


# Editar usuario
@app.route('/editarusuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = Usuario.get_or_none(Usuario.id == id)
    if not usuario:
        return "Usuario no encontrado", 404
    
    if request.method == 'POST':
        usuario.CC = request.form['Cedula']
        usuario.Nombres = request.form['nombres']
        usuario.Apellidos = request.form['apellidos']
        usuario.Edad = request.form['edad']
        usuario.Genero = request.form['genero']
        usuario.Correo = request.form['correo']
        usuario.Contrasena = request.form['contrasena']
        usuario.Tipo = request.form['tipo_usuario']
        usuario.Municipio = request.form['municipio']
        usuario.Departamento = request.form['departamento']

        # Asignar la enfermedad seleccionada
        enfermedad_id = request.form['enfermedad']
        usuario.Enfermedad = Enfermedad.get(Enfermedad.ID == enfermedad_id)

        usuario.save()

        return redirect(url_for('lista_usuarios'))

    enfermedades = Enfermedad.select()
    return render_template('editar_usuario.html', usuario=usuario, enfermedades=enfermedades)

@app.route('/agregarenfermedadusuario/<int:id>', methods=['GET', 'POST'])
def agregarenfermedadusuario(id):
    usuario = Usuario.get_or_none(Usuario.id == id)
    enfermedades = Enfermedad.select()

    if not usuario:
        return "Usuario no encontrado", 404

    if request.method == 'POST':
        # Obtener el ID de la enfermedad seleccionada
        enfermedad_id = request.form.get('enfermedad_id')
        print("Enfermedad ID:", enfermedad_id)  # Para depuración

        # Recuperar la enfermedad utilizando el ID
        enfermedad = Enfermedad.get_or_none(Enfermedad.ID == enfermedad_id)
        
        if enfermedad:
            # Asignar la enfermedad al usuario y guardar
            usuario.Enfermedad = enfermedad
            usuario.save()
            return redirect(url_for('info_usuario_interno', usuario_id=usuario.id))


    return render_template('agregarenfermedadusuario.html', usuario=usuario, enfermedades=enfermedades)



# Eliminar usuario
@app.route('/eliminarusuario/<int:id>', methods=['GET'])
def eliminar_usuario(id):
    usuario = Usuario.get_or_none(Usuario.id == id)

    # Verificar si el usuario existe
    if not usuario:
        return "Usuario no encontrado", 404

    # Eliminar el usuario de la base de datos
    usuario.delete_instance()

    # Redirigir a la lista de usuarios después de eliminar
    return redirect(url_for('lista_usuarios'))


# --------------------------------------------------------
# --------------------------------------------------------  
# ------------------Enfermedades----------------------
# --------------------------------------------------------
# --------------------------------------------------------
@app.route('/enfermedades_usuario', methods=['GET'])
def enfermedades_usuario():
    enfermedades = Enfermedad.select()
    if enfermedades is None:
        return "Enfermedades no encontradas", 404
    
    # Verifica si es Externo, si es externo manda a enfermedadesExternos.html
    if session['tipo_usuario'] == 3:
        return render_template('enfermedadesExternos.html', Enfermedades=enfermedades)
    else:
        return render_template('enfermedades.html', Enfermedades=enfermedades)


#  Lista de enfermedades
@app.route('/lista_enfermedades', methods=['GET'])
def lista_enfermedades():
    enfermedades = Enfermedad.select()
    return render_template('lista_enfermedades.html', enfermedades=enfermedades)

# ----------------Agregar nueva enfermedad-------------

@app.route('/agregarenfermedad', methods=['GET', 'POST'])
def agregar_enfermedad():
    if request.method == 'POST':
        # Obtener los datos del formulario enviados por el usuario
        nombre_cientifico = request.form['NombreCientifico']
        descripcion = request.form['Descripcion']
        sintomas = request.form['Sintomas']
        causas = request.form['Causas']
        prevencion = request.form['Prevencion']
        tratamiento = request.form['Tratamiento']
        tasa_mortalidad = request.form['TasaMortalidad']
        region_prevalente = request.form['RegionPrevalente']
        complicaciones = request.form['Complicaciones']
        codigo_cie = request.form['Codigo_CIE']

        # Crear una nueva instancia de Enfermedad
        nueva_enfermedad = Enfermedad(
            NombreCientifico=nombre_cientifico,
            Descripcion=descripcion,
            Sintomas=sintomas,
            Causas=causas,
            Prevencion=prevencion,
            Tratamiento=tratamiento,
            TasaMortalidad=tasa_mortalidad,
            RegionPrevalente=region_prevalente,
            Complicaciones=complicaciones,
            Codigo_CIE=codigo_cie
        )

        # Guardar la nueva enfermedad en la base de datos
        nueva_enfermedad.save()

        return redirect(url_for('enfermedades_usuario'))

    return render_template('enfermedadN.html')

# ----------------Editar Enfermedad----------------
@app.route('/editarenfermedad/<int:ID>', methods=['GET', 'POST'])
def editar_enfermedad(ID):

    enfermedad = Enfermedad.get_or_none(Enfermedad.ID == ID)
    
    if not enfermedad:
        return "Enfermedad no encontrada", 404
    
    if request.method == 'POST':
        # Obtener los datos nuevos del formulario
        enfermedad.NombreCientifico = request.form['NombreCientifico']
        enfermedad.Descripcion = request.form['Descripcion']
        enfermedad.Sintomas = request.form['Sintomas']
        enfermedad.Causas = request.form['Causas']
        enfermedad.Prevencion = request.form['Prevencion']
        enfermedad.Tratamiento = request.form['Tratamiento']
        enfermedad.TasaMortalidad = request.form['TasaMortalidad']
        enfermedad.RegionPrevalente = request.form['RegionPrevalente']
        enfermedad.Complicaciones = request.form['Complicaciones']
        
        # Guardar los cambios en la base de datos
        enfermedad.save()
        
        return redirect(url_for('lista_enfermedades'))  # Redirigir a la lista de enfermedades

    # Renderizar la plantilla para editar la enfermedad con los datos actuales
    return render_template('editar_enfermedad.html', enfermedad=enfermedad)

#  ----------------Eliminar Enfermedad----------------
@app.route('/eliminarenfermedad/<int:ID>', methods=['GET'])
def eliminar_enfermedad(ID):
    # Buscar la enfermedad por su id
    enfermedad = Enfermedad.get_or_none(Enfermedad.ID == ID)

    # Verificar si la enfermedad existe
    if not enfermedad:
        return "Enfermedad no encontrada", 404

    # Eliminar la enfermedad de la base de datos
    enfermedad.delete_instance()

    # Redirigir a la lista de enfermedades después de eliminar
    return redirect(url_for('enfermedades_usuario'))



# --------------------------------------------------------
# --------------------------------------------------------
# -----------------------Los graficos-------------------
# --------------------------------------------------------
# --------------------------------------------------------
@app.route('/graficos')
def graficos():
    usuario = Usuario.select()
    if usuario is None:
        return "Usuarios no encontrado", 404
    return render_template('/graficos.html', usuarios = usuario)








if __name__ == '__main__':
    app.run(debug=True)