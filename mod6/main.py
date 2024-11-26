from flask import Flask, render_template, request, redirect, url_for, flash
import redis
import json

# Inicializar Flask y KeyDB
app = Flask(__name__)
app.secret_key = "secrets"
client = redis.Redis(host="localhost", port=6379, decode_responses=True)


@app.route("/")
def home():
    keys = client.keys()
    return render_template("index.html", recetas=keys)


@app.route("/receta/<nombre>")
def ver_receta(nombre):
    receta = client.get(nombre)
    if receta:
        receta = json.loads(receta)
        return render_template("receta.html", nombre=nombre, receta=receta)
    flash("Receta no encontrada.", "error")
    return redirect(url_for("home"))


@app.route("/nueva", methods=["GET", "POST"])
def agregar_receta():
    if request.method == "POST":
        nombre = request.form["nombre"]
        ingredientes = request.form["ingredientes"]
        pasos = request.form["pasos"]

        if client.exists(nombre):
            flash(f"Ya existe una receta con el nombre '{nombre}'.", "error")
            return redirect(url_for("home"))

        nueva_receta = {"ingredientes": ingredientes, "pasos": pasos}
        client.set(nombre, json.dumps(nueva_receta))
        flash(f"Receta '{nombre}' agregada con éxito.", "success")
        return redirect(url_for("home"))
    return render_template("nueva.html")


@app.route("/editar/<nombre>", methods=["GET", "POST"])
def editar_receta(nombre):
    receta = client.get(nombre)
    if not receta:
        flash("Receta no encontrada.", "error")
        return redirect(url_for("home"))

    receta = json.loads(receta)
    if request.method == "POST":
        ingredientes = request.form["ingredientes"] or receta["ingredientes"]
        pasos = request.form["pasos"] or receta["pasos"]

        receta_actualizada = {"ingredientes": ingredientes, "pasos": pasos}
        client.set(nombre, json.dumps(receta_actualizada))
        flash(f"Receta '{nombre}' actualizada con éxito.", "success")
        return redirect(url_for("ver_receta", nombre=nombre))
    return render_template("editar.html", nombre=nombre, receta=receta)


@app.route("/eliminar/<nombre>", methods=["POST"])
def eliminar_receta(nombre):
    if client.delete(nombre):
        flash(f"Receta '{nombre}' eliminada con éxito.", "success")
    else:
        flash("Receta no encontrada.", "error")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
