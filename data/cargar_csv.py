import csv
from sqlalchemy.orm import Session
from utils.db import SessionLocal
from data.models import Jugador  # Ajusta la ruta según tu estructura

def cargar_jugadores_desde_csv(ruta_csv: str):
    db: Session = SessionLocal()
    try:
        with open(ruta_csv, newline='', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                jugador = Jugador(
                    nombre=fila['nombre'],
                    equipo=fila['equipo'],
                    posicion=fila['posicion'],
                    edad=int(fila['edad']),
                    nacionalidad=fila['nacionalidad'],
                    goles=int(fila['goles']),
                    asistencias=int(fila['asistencias']),
                    eliminado=fila['eliminado'].lower() == 'true',
                    eliminado_logico=fila.get('eliminado_logico', 'false').lower() == 'true',  # por si no está en todos los registros
                )
                db.add(jugador)
            db.commit()
            print("✅ Jugadores cargados correctamente.")
    except Exception as e:
        print("❌ Error al cargar CSV:", e)
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    cargar_jugadores_desde_csv("data/jugadores.csv")  # Ajusta ruta si es necesario
