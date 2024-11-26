from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pasteleria.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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

@app.route('/gestionar_recetas')
def gestionar_recetas():
    return render_template('gestionar_recetas.html')

@app.route('/gestionar_categorias')
def gestionar_categorias():
    return render_template('gestionar_categorias.html')


if __name__ == '__main__':
    app.run(debug=True)

