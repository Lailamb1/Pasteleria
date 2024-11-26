from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pasteleria.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Formularios con Flask-WTF
class RecetaForm(FlaskForm):
    nombre_receta = StringField('Nombre de la Receta', validators=[DataRequired()])
    ingredientes = TextAreaField('Ingredientes', validators=[DataRequired()])
    instrucciones = TextAreaField('Instrucciones', validators=[DataRequired()])

    # Base de datos simple en memoria (puedes conectarlo a una base de datos real más tarde)
recetas = []
ingredientes = []

# Modelo para los ingredientes
class Ingrediente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    unidad = db.Column(db.String(50), nullable=False)

# Crear las tablas
with app.app_context():
    db.create_all()

# Ruta para la raíz
@app.route('/')
def home():
    return render_template('home.html')

# Ruta para agregar ingredientes
@app.route('/ingredientes', methods=['GET', 'POST'])
def gestionar_ingredientes():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        unidad = request.form['unidad']
        nuevo_ingrediente = Ingrediente(nombre=nombre, precio=precio, unidad=unidad)
        db.session.add(nuevo_ingrediente)
        db.session.commit()
        return redirect(url_for('ver_ingredientes'))
    return render_template('ingredientes.html')

# Ruta para agregar ingredientes

@app.route('/agregar_ingrediente', methods=['GET', 'POST'])
def agregar_ingrediente():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']

        # Crear un nuevo ingrediente con un ID único
        nuevo_ingrediente = Ingrediente(nombre=nombre, precio=0.0, unidad='unidad')  # Asumimos precio y unidad por defecto
        db.session.add(nuevo_ingrediente)
        db.session.commit()

        # Redirigir a la página donde se muestran los ingredientes
        return redirect(url_for('ver_ingredientes'))

    # Si es un GET, simplemente mostramos el formulario
    return render_template('agregar_ingrediente.html')
    # Si es un GET, simplemente mostramos el formulario
    return render_template('agregar_ingrediente.html')


# Ruta para ver los ingredientes
@app.route('/ver_ingredientes')
def ver_ingredientes():
    ingredientes = Ingrediente.query.all()  # Obtener todos los ingredientes desde la base de datos
    return render_template('ver_ingredientes.html', ingredientes=ingredientes)

@app.route('/gestionar_recetas', methods=['GET', 'POST'])
def gestionar_recetas():
    if request.method == 'POST':
        # Obtener los datos del formulario
        titulo = request.form['titulo']
        ingredientes = request.form['ingredientes']
        instrucciones = request.form['instrucciones']
        
        # Crear un diccionario para la receta
        nueva_receta = {
            'titulo': titulo,
            'ingredientes': ingredientes,
            'instrucciones': instrucciones
        }
        
        # Agregar la receta a la lista (en una base de datos esto sería un insert)
        recetas.append(nueva_receta)
        
        # Redirigir a la misma página para mostrar la receta agregada
        return redirect(url_for('gestionar_recetas'))
    
    # Si es un GET, simplemente renderizamos la página con la lista de recetas
    return render_template('gestionar_recetas.html', recetas=recetas)

@app.route('/editar_receta/<int:id>', methods=['GET', 'POST'])
def editar_receta(id):
    receta = obtener_receta_por_id(id)  # Aquí debería ir la función que recupera la receta por ID
    if request.method == 'POST':
        # Recoger los datos del formulario
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        # Aquí actualizas los datos de la receta
        actualizar_receta(id, nombre, descripcion)  # Función que guarda los cambios
        return redirect(url_for('gestionar_recetas'))  # Redirige a la lista de recetas gestionadas

    return render_template('editar_receta.html', receta=receta)  # Pasar la receta a la plantilla para mostrarla

# Función ficticia para obtener receta
def obtener_receta_por_id(id):
    # Aquí deberías hacer la consulta a la base de datos o utilizar una lista de recetas
    return {'id': id, 'nombre': 'Receta de prueba', 'descripcion': 'Descripción de la receta'}

# Función ficticia para actualizar receta
def actualizar_receta(id, nombre, descripcion):
    # Aquí deberías actualizar la receta en la base de datos o en la lista
    pass

@app.route('/eliminar_ingrediente/<int:id>', methods=['POST'])
def eliminar_ingrediente(id):
    ingrediente = Ingrediente.query.get(id)  # Obtener el ingrediente de la base de datos
    if ingrediente:
        db.session.delete(ingrediente)  # Eliminar el ingrediente de la base de datos
        db.session.commit()  # Confirmar la eliminación
    return redirect(url_for('ver_ingredientes'))


@app.route('/gestionar_categorias')
def gestionar_categorias():
    return render_template('gestionar_categorias.html')

if __name__ == '__main__':
    app.run(debug=True)

