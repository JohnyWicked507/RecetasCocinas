from mod1 import a

# from mod2 import a
# from mod3 import a
# from mod4 import a


def main() -> None:
    a.iniciar()
    while True:
        print(
            "\n--- Menu Libro de Recetas ---"
            "1. Agregar nueva receta"
            "2. Actualizar receta existente"
            "3. Eliminar receta existente"
            "4. Ver listado de recetas"
            "5. Buscar ingredientes y pasos de receta"
            "6. Salir"
        )

        opcion = input("Selecciona una opcion (1-6): ")
        match opcion:
            case "1":
                a.agregar_receta()
            case "2":
                a.actualizar_receta()
            case "3":
                a.eliminar_receta()
            case "4":
                a.ver_recetas()
            case "5":
                a.buscar_receta()
            case "6":
                break
            case _:
                print("Opcion no válida. Intenta de nuevo.")


if __name__ == "__main__":
    main()
