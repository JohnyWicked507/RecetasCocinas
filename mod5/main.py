from typing_extensions import LiteralString
from flask import Flask, request, jsonify
import redis
import json

# Inicializar Flask y KeyDB
app = Flask(__name__)
client = redis.Redis(decode_responses=True)


@app.route("/")
def home() -> LiteralString:
    return "Bienvenido a la API de Recetas. Usa los endpoints para interactuar."


@app.route("/recetas", methods=["GET"])
def listar_recetas():
    keys = client.keys()
    if keys:
        return jsonify({"recetas": keys}), 200
    return jsonify({"mensaje": "No hay recetas guardadas"}), 404


@app.route("/recetas/<nombre>", methods=["GET"])
def buscar_receta(nombre):
    receta = client.get(nombre)
    if receta:
        return jsonify({"nombre": nombre, **json.loads(receta)}), 200
    return jsonify({"mensaje": "Receta no encontrada"}), 404


@app.route("/recetas", methods=["POST"])
def agregar_receta():
    datos = request.json
    nombre = datos.get("nombre")
    ingredientes = datos.get("ingredientes")
    pasos = datos.get("pasos")

    if not (nombre and ingredientes and pasos):
        return jsonify({"mensaje": "Faltan campos obligatorios"}), 400

    if client.exists(nombre):
        return (
            jsonify({"mensaje": f"Ya existe una receta con el nombre '{nombre}'"}),
            409,
        )

    nueva_receta = {"ingredientes": ingredientes, "pasos": pasos}
    client.set(nombre, json.dumps(nueva_receta))
    return jsonify({"mensaje": f"Receta '{nombre}' agregada con exito"}), 201


@app.route("/recetas/<nombre>", methods=["PUT"])
def actualizar_receta(nombre):
    receta = client.get(nombre)
    if not receta:
        return jsonify({"mensaje": "Receta no encontrada"}), 404

    datos = request.json
    nuevos_ingredientes = datos.get("ingredientes", json.loads(receta)["ingredientes"])
    nuevos_pasos = datos.get("pasos", json.loads(receta)["pasos"])

    receta_actualizada = {"ingredientes": nuevos_ingredientes, "pasos": nuevos_pasos}
    client.set(nombre, json.dumps(receta_actualizada))
    return jsonify({"mensaje": f"Receta '{nombre}' actualizada con exito"}), 200


@app.route("/recetas/<nombre>", methods=["DELETE"])
def eliminar_receta(nombre):
    if client.delete(nombre):
        return jsonify({"mensaje": f"Receta '{nombre}' eliminada con exito"}), 200
    return jsonify({"mensaje": "Receta no encontrada"}), 404


if __name__ == "__main__":
    app.run(debug=True)
