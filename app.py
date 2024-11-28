import json
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recetas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Filtro personalizado para convertir JSON a lista
@app.template_filter('from_json')
def from_json(value):
    return json.loads(value) if value else []

# Modelo de Receta
class Receta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(500), nullable=False)
    ingredientes = db.Column(db.String(500), nullable=False)  # Guardaremos la lista de ingredientes como un string JSON
    preparacion = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return f'<Receta {self.nombre}>'

# Crear la base de datos (solo si no existe)
with app.app_context():
    db.create_all()

# Ruta para la página principal
@app.route('/')
def home():
    return render_template('home.html')

# Ruta para gestionar recetas
@app.route('/gestionar_recetas')
def gestionar_recetas():
    recetas = Receta.query.all()
    return render_template('gestionar_recetas.html', recetas=recetas)

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

# Ruta para eliminar receta
@app.route('/eliminar_receta/<int:id>')
def eliminar_receta(id):
    receta = Receta.query.get_or_404(id)
    db.session.delete(receta)
    db.session.commit()
    return redirect(url_for('gestionar_recetas'))

if __name__ == '__main__':
    app.run(debug=True)
