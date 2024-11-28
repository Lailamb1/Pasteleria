from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import json

# Configuración de la aplicación
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recetas.db'  # Base de datos SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de la receta
class Receta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(500), nullable=False)
    ingredientes = db.Column(db.Text, nullable=False)  # Ingredientes en formato JSON
    preparacion = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Receta {self.nombre}>'
    
    

# Ruta para agregar o editar recetas
@app.route('/agregar_receta', methods=['GET', 'POST'])
@app.route('/editar_receta/<int:id>', methods=['GET', 'POST'])
def agregar_receta(id=None):
    if id:
        receta = Receta.query.get_or_404(id)
    else:
        receta = None

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        ingredientes = request.form['ingredientes']
        preparacion = request.form['preparacion']

        # Convertir los ingredientes en una lista JSON
        ingredientes_list = ingredientes.split('\n')  # Separamos por saltos de línea
        ingredientes_json = json.dumps(ingredientes_list)

        if receta:
            receta.nombre = nombre
            receta.descripcion = descripcion
            receta.ingredientes = ingredientes_json
            receta.preparacion = preparacion
        else:
            nueva_receta = Receta(
                nombre=nombre,
                descripcion=descripcion,
                ingredientes=ingredientes_json,
                preparacion=preparacion
            )
            db.session.add(nueva_receta)

        db.session.commit()
        return redirect(url_for('gestionar_recetas'))

    return render_template('agregar_receta.html', receta=receta)

# Ruta para gestionar las recetas (mostrar lista de recetas)
@app.route('/gestionar_recetas')
def gestionar_recetas():
    recetas = Receta.query.all()  # Obtener todas las recetas de la base de datos
    return render_template('gestionar_recetas.html', recetas=recetas)

@app.route('/')
def home():
    return render_template('home.html')

# Inicializar la base de datos
@app.before_request
def create_tables():
    db.create_all()

@app.route('/eliminar_receta/<int:id>', methods=['POST'])
def eliminar_receta(id):
    receta = Receta.query.get_or_404(id)
    db.session.delete(receta)
    db.session.commit()
    return redirect(url_for('gestionar_recetas'))




if __name__ == '__main__':
    with app.app_context():  # Crear un contexto de la aplicación
        db.create_all()  # Crear las tablas de la base de datos
    app.run(debug=True)
