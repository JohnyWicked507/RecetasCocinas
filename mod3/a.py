from pymongo import MongoClient

# Conexion inicial
client = MongoClient("mongodb://localhost:27017/")
db = client.recetas_db
recetas_collection = db.recetas


def iniciar_db() -> None:
    # Asegurar que la coleccion exista (MongoDB la crea automáticamente en la primera inserción)
    if "recetas" not in db.list_collection_names():
        print("Base de datos inicializada.")
    else:
        print("Base de datos ya existe.")


def agregar_receta() -> None:
    nombre = input("Nombre de la receta: ")
    ingredientes = input("Ingredientes: ")
    pasos = input("Pasos de la receta: ")

    nueva_receta = {
        "nombre": nombre,
        "ingredientes": ingredientes,
        "pasos": pasos,
    }

    try:
        recetas_collection.insert_one(nueva_receta)
        print(f"Receta '{nombre}' agregada con exito.")
    except Exception as e:
        print(f"Error al agregar receta: {e}")


def actualizar_receta() -> None:
    nombre = input("Nombre de la receta a actualizar: ")
    receta = recetas_collection.find_one({"nombre": nombre})

    if not receta:
        print("Receta no encontrada.")
        return

    nuevos_ingredientes = input("Nuevos ingredientes: ") or receta["ingredientes"]
    nuevos_pasos = input("Nuevos pasos: ") or receta["pasos"]

    try:
        recetas_collection.update_one(
            {"nombre": nombre},
            {"$set": {"ingredientes": nuevos_ingredientes, "pasos": nuevos_pasos}},
        )
        print(f"Receta '{nombre}' actualizada con exito.")
    except Exception as e:
        print(f"Error al actualizar receta: {e}")


def eliminar_receta() -> None:
    nombre = input("Nombre de la receta a eliminar: ")
    result = recetas_collection.delete_one({"nombre": nombre})

    if result.deleted_count > 0:
        print(f"Receta '{nombre}' eliminada con exito.")
    else:
        print("Receta no encontrada.")


def ver_recetas() -> None:
    recetas = recetas_collection.find({}, {"_id": 0, "nombre": 1})

    if recetas.count() > 0:
        print("Recetas disponibles:")
        for receta in recetas:
            print(f"- {receta['nombre']}")
    else:
        print("No hay recetas guardadas.")


def buscar_receta() -> None:
    nombre = input("Nombre de la receta a buscar: ")
    receta = recetas_collection.find_one({"nombre": nombre}, {"_id": 0})

    if receta:
        print(
            f"Nombre: {receta['nombre']}\nIngredientes: {receta['ingredientes']}\nPasos: {receta['pasos']}"
        )
    else:
        print("Receta no encontrada.")
