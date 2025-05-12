import csv
from sqlalchemy.orm import Session
from utils.db import SessionLocal
from data.models import Equipo  # Ajusta la ruta si es necesario

def cargar_equipos_desde_csv(ruta_csv: str):
    db: Session = SessionLocal()
    try:
        with open(ruta_csv, newline='', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                equipo = Equipo(
                    nombre=fila['nombre'],
                    pais=fila['pais'],
                    grupo=fila['grupo'],
                    eliminado=fila['eliminado'].lower() == 'true',
                    eliminado_logico=fila.get('eliminado_logico', 'false').lower() == 'true'
                )
                db.add(equipo)
            db.commit()
            print("✅ Equipos cargados correctamente.")
    except Exception as e:
        print("❌ Error al cargar CSV:", e)
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    cargar_equipos_desde_csv("data/equipos.csv")  # Ajusta la ruta si es diferente
