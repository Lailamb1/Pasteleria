from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pasteleria.db'  # Usamos SQLite
db = SQLAlchemy(app)

# Definir el modelo para los ingredientes
class Ingrediente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    costo_unitario = db.Column(db.Float, nullable=False)
    unidad = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Ingrediente {self.nombre}>'

# Crear la base de datos (solo si no existe)
with app.app_context():
    db.create_all()

# Página principal
@app.route('/')
def home():
    return render_template('home.html')

# Iniciar la aplicación en localhost:5000
if __name__ == '__main__':
    app.run(debug=True)
