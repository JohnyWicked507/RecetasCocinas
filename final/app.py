from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Configuracion basica de Flask
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"  # Base de datos local
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializar la base de datos
db = SQLAlchemy(app)


# Modelo para Donante
class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    blood_type = db.Column(db.String(10), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "blood_type": self.blood_type}


# Ruta para la pagina principal
@app.route("/")
def index():
    return render_template("index.html")


# Ruta para obtener todos los donantes
@app.route("/donors", methods=["GET"])
def get_donors():
    donors = Donor.query.all()
    return jsonify([donor.to_dict() for donor in donors])


# Ruta para agregar un donante
@app.route("/donors", methods=["POST"])
def add_donor():
    data = request.get_json()
    if not data or "name" not in data or "blood_type" not in data:
        return jsonify({"error": "Datos invalidos"}), 400

    new_donor = Donor(name=data["name"], blood_type=data["blood_type"])
    db.session.add(new_donor)
    db.session.commit()
    return jsonify(new_donor.to_dict()), 201


# Ruta para eliminar un donante
@app.route("/donors/<int:donor_id>", methods=["DELETE"])
def delete_donor(donor_id):
    donor = Donor.query.get_or_404(donor_id)
    db.session.delete(donor)
    db.session.commit()
    return jsonify({"message": "Donante eliminado"}), 200


# Crear las tablas en la base de datos antes de la primera solicitud
def create_tables():
    with app.app_context():
        db.create_all()


# Ejecutar la aplicacion
if __name__ == "__main__":
    app.run(debug=True)
