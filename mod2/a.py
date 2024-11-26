from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

url = "mysql+pymysql://usuario:contraseña@localhost/recetas_db"

Base = declarative_base()


class Receta(Base):
    __tablename__ = "recetas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)
    ingredientes = Column(String(500), nullable=False)
    pasos = Column(String(1000), nullable=False)


engine = create_engine(url)
Session = sessionmaker(bind=engine)


def iniciar() -> None:
    Base.metadata.create_all(engine)
    print("Base de datos inicializada.")


def agregar_receta() -> None:
    session = Session()
    nombre = input("Nombre de la receta: ")
    ingredientes = input("Ingredientes: ")
    pasos = input("Pasos de la receta: ")
    nueva_receta = Receta(nombre=nombre, ingredientes=ingredientes, pasos=pasos)

    try:
        session.add(nueva_receta)
        session.commit()
        print(f"Receta '{nombre}' agregada con exito.")
    except Exception as e:
        print(f"Error al agregar receta: {e}")
    finally:
        session.close()


def actualizar_receta() -> None:
    session = Session()
    nombre = input("Nombre de la receta a actualizar: ")
    receta = session.query(Receta).filter_by(nombre=nombre).first()

    if not receta:
        print("Receta no encontrada.")
        return

    nuevos_ingredientes = input("Nuevos ingredientes: ") or receta.ingredientes
    nuevos_pasos = input("Nuevos pasos: ") or receta.pasos

    receta.ingredientes = nuevos_ingredientes
    receta.pasos = nuevos_pasos

    try:
        session.commit()
        print(f"Receta '{nombre}' actualizada con exito.")
    except Exception as e:
        print(f"Error al actualizar receta: {e}")
    finally:
        session.close()


def eliminar_receta() -> None:
    session = Session()
    nombre = input("Nombre de la receta a eliminar: ")
    receta = session.query(Receta).filter_by(nombre=nombre).first()

    if not receta:
        print("Receta no encontrada.")
        return

    try:
        session.delete(receta)
        session.commit()
        print(f"Receta '{nombre}' eliminada con exito.")
    except Exception as e:
        print(f"Error al eliminar receta: {e}")
    finally:
        session.close()


def ver_recetas() -> None:
    session = Session()
    recetas = session.query(Receta).all()

    if recetas:
        print("Recetas disponibles:")
        for receta in recetas:
            print(f"- {receta.nombre}")
    else:
        print("No hay recetas guardadas.")

    session.close()


def buscar_receta() -> None:
    session = Session()
    nombre = input("Nombre de la receta a buscar: ")
    receta = session.query(Receta).filter_by(nombre=nombre).first()

    if receta:
        print(
            f"Nombre: {receta.nombre}\nIngredientes: {receta.ingredientes}\nPasos: {receta.pasos}"
        )
    else:
        print("Receta no encontrada.")

    session.close()
