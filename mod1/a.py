import sqlite3

base_de_datos = "recetas.db"


def iniciar() -> None:
    conn = sqlite3.connect(base_de_datos)
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS recetas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        ingredientes TEXT NOT NULL,
        pasos TEXT NOT NULL
    )
    """
    )
    conn.commit()
    conn.close()


def agregar_receta() -> None:
    nombre = input("Nombre de la receta: ")
    ingredientes = input("Ingredientes (separados por comas): ")
    pasos = input("Pasos de la receta: ")

    with sqlite3.connect(base_de_datos) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO recetas (nombre, ingredientes, pasos) VALUES (?, ?, ?)",
                (nombre, ingredientes, pasos),
            )
            conn.commit()
            print(f"Receta '{nombre}' agregada con exito.")
        except sqlite3.IntegrityError:
            print("Ya existe una receta con ese nombre.")


def actualizar_receta() -> None:
    nombre = input("Nombre de la receta a actualizar: ")
    with sqlite3.connect(base_de_datos) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM recetas WHERE nombre = ?", (nombre,))
        receta = cursor.fetchone()

        if not receta:
            print("Receta no encontrada.")
            return

        nuevos_ingredientes = input("Nuevos ingredientes: ")
        nuevos_pasos = input("Nuevos pasos: ")

        nuevos_ingredientes = nuevos_ingredientes or receta[2]
        nuevos_pasos = nuevos_pasos or receta[3]

        cursor.execute(
            "UPDATE recetas SET ingredientes = ?, pasos = ? WHERE nombre = ?",
            (nuevos_ingredientes, nuevos_pasos, nombre),
        )
        conn.commit()
        print(f"Receta '{nombre}' actualizada con exito.")


def eliminar_receta() -> None:
    nombre = input("Nombre de la receta a eliminar: ")
    with sqlite3.connect(base_de_datos) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM recetas WHERE nombre = ?", (nombre,))
        if cursor.rowcount > 0:
            conn.commit()
            print(f"Receta '{nombre}' eliminada con exito.")
        else:
            print("Receta no encontrada.")


def ver_recetas() -> None:
    with sqlite3.connect(base_de_datos) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM recetas")
        recetas = cursor.fetchall()

        if recetas:
            print("Recetas disponibles:")
            for receta in recetas:
                print(f"- {receta[0]}")
        else:
            print("No hay recetas guardadas.")


def buscar_receta() -> None:
    nombre = input("Nombre de la receta a buscar: ")
    with sqlite3.connect(base_de_datos) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM recetas WHERE nombre = ?", (nombre,))
        receta = cursor.fetchone()

        if receta:
            print(f"Nombre: {receta[1]}\nIngredientes: {receta[2]}\nPasos: {receta[3]}")
        else:
            print("Receta no encontrada.")
