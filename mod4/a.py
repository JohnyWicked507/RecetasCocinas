import json
import redis

# Conexion inicial a KeyDB
client = redis.Redis(decode_responses=True)


def iniciar() -> None:
    pass


def agregar_receta() -> None:
    nombre = input("Nombre de la receta: ")
    ingredientes = input("Ingredientes: ")
    pasos = input("Pasos de la receta: ")

    if client.exists(nombre):
        print(f"Ya existe una receta con el nombre '{nombre}'.")
        return

    nueva_receta = {
        "ingredientes": ingredientes,
        "pasos": pasos,
    }

    try:
        client.set(nombre, json.dumps(nueva_receta))
        print(f"Receta '{nombre}' agregada con exito.")
    except Exception as e:
        print(f"Error al agregar receta: {e}")


def actualizar_receta() -> None:
    nombre = input("Nombre de la receta a actualizar: ")
    receta = client.get(nombre)

    if not receta:
        print("Receta no encontrada.")
        return

    receta = json.loads(receta)
    nuevos_ingredientes = input("Nuevos ingredientes: ") or receta["ingredientes"]
    nuevos_pasos = input("Nuevos pasos: ") or receta["pasos"]

    receta_actualizada = {
        "ingredientes": nuevos_ingredientes,
        "pasos": nuevos_pasos,
    }

    try:
        client.set(nombre, json.dumps(receta_actualizada))
        print(f"Receta '{nombre}' actualizada con exito.")
    except Exception as e:
        print(f"Error al actualizar receta: {e}")


def eliminar_receta() -> None:
    nombre = input("Nombre de la receta a eliminar: ")

    if client.delete(nombre):
        print(f"Receta '{nombre}' eliminada con exito.")
    else:
        print("Receta no encontrada.")


def ver_recetas() -> None:
    keys = client.keys()

    if keys:
        print("Recetas disponibles:")
        for key in keys:
            print(f"- {key}")
    else:
        print("No hay recetas guardadas.")


def buscar_receta() -> None:
    nombre = input("Nombre de la receta a buscar: ")
    receta = client.get(nombre)

    if receta:
        receta = json.loads(receta)
        print(
            f"Nombre: {nombre}\nIngredientes: {receta['ingredientes']}\nPasos: {receta['pasos']}"
        )
    else:
        print("Receta no encontrada.")
