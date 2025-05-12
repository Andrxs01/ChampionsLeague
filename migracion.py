import csv
from sqlalchemy.orm import Session
from data.models import Jugador, Equipo
from utils.db import SessionLocal


# Función para importar jugadores desde un CSV
def importar_jugadores_csv(db: Session, ruta_csv: str):
    with open(ruta_csv, mode="r") as archivo_csv:
        lector_csv = csv.DictReader(archivo_csv)
        jugadores = []

        for fila in lector_csv:
            jugador = Jugador(
                nombre=fila["nombre"],
                equipo=fila["equipo"],
                posicion=fila["posicion"],
                edad=int(fila["edad"]),
                nacionalidad=fila["nacionalidad"],
                goles=int(fila["goles"]),
                asistencias=int(fila["asistencias"]),
                eliminado=fila["eliminado"] == "True",
                eliminado_logico=fila["eliminado_logico"] == "True"
            )
            jugadores.append(jugador)

        # Agregar los jugadores a la base de datos
        db.add_all(jugadores)
        db.commit()


# Función para importar equipos desde un CSV
def importar_equipos_csv(db: Session, ruta_csv: str):
    with open(ruta_csv, mode="r") as archivo_csv:
        lector_csv = csv.DictReader(archivo_csv)
        equipos = []

        for fila in lector_csv:
            equipo = Equipo(
                nombre=fila["nombre"],
                pais=fila["pais"],
                grupo=fila["grupo"],
                eliminado=fila["eliminado"] == "True"
            )
            equipos.append(equipo)

        # Agregar los equipos a la base de datos
        db.add_all(equipos)
        db.commit()


# Función principal para migrar datos
def migrar_datos():
    db = SessionLocal()
    try:
        # Importar jugadores desde CSV
        importar_jugadores_csv(db, "ruta_a_tu_archivo/jugadores.csv")

        # Importar equipos desde CSV
        importar_equipos_csv(db, "ruta_a_tu_archivo/equipos.csv")

        print("Migración completada con éxito!")
    except Exception as e:
        print(f"Ocurrió un error durante la migración: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    migrar_datos()
