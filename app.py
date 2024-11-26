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

# Ruta para ver los ingredientes
@app.route('/ver_ingredientes')
def ver_ingredientes():
    ingredientes = Ingrediente.query.all()
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


@app.route('/eliminar_receta/<int:receta_id>', methods=['GET'])
def eliminar_receta(receta_id):
    del recetas[receta_id]  # Eliminamos la receta por índice
    return redirect(url_for('gestionar_recetas'))

@app.route('/gestionar_categorias')
def gestionar_categorias():
    return render_template('gestionar_categorias.html')

if __name__ == '__main__':
    app.run(debug=True)

