import pandas as pd
from sqlalchemy.orm import sessionmaker
from utils.db import engine
from data.models import Jugador, Equipo

# Crear la sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Cargar datos de los archivos CSV usando pandas
jugadores_df = pd.read_csv('data/jugadores.csv', encoding='utf-8')
equipos_df = pd.read_csv('data/equipos.csv', encoding='utf-8')

# Insertar datos de jugadores en la base de datos
for index, row in jugadores_df.iterrows():
    jugador = Jugador(
        nombre=row['nombre'],
        equipo=row['equipo'],
        posicion=row['posicion'],
        edad=row['edad'],
        nacionalidad=row['nacionalidad'],
        goles=row['goles'],
        asistencias=row['asistencias'],
        eliminado=row['eliminado'],
        eliminado_logico=row['eliminado_logico']
    )
    db.add(jugador)

# Insertar datos de equipos en la base de datos
for index, row in equipos_df.iterrows():
    equipo = Equipo(
        nombre=row['nombre'],
        pais=row['pais'],
        grupo=row['grupo'],
        eliminado=row['eliminado']
    )
    db.add(equipo)

# Commit y cierre
db.commit()
db.close()

print("Migración completa.")
