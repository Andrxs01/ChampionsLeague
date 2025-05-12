import os
import pandas as pd
from sqlalchemy.orm import Session
from utils.db import SessionLocal, engine
from data.models import Jugador, Equipo


def migrar_equipos(ruta_csv: str):
    """
    Migra datos de equipos desde un CSV a la base de datos

    :param ruta_csv: Ruta del archivo CSV con datos de equipos
    """
    db = SessionLocal()

    try:
        # Leer el CSV
        df = pd.read_csv(ruta_csv, encoding='utf-8')

        # Filtrar equipos que no están eliminados de la Champions
        df_activos = df[df['eliminado'] == False]

        print(f"Iniciando migración de equipos. Total de registros: {len(df_activos)}")

        for _, row in df_activos.iterrows():
            # Verificar si el equipo ya existe para evitar duplicados
            equipo_existente = db.query(Equipo).filter(
                Equipo.nombre == row['nombre'],
                Equipo.pais == row['pais']
            ).first()

            if not equipo_existente:
                nuevo_equipo = Equipo(
                    id=row['id'],
                    nombre=row['nombre'],
                    pais=row['pais'],
                    grupo=row['grupo'],
                    # 'eliminado' significa eliminado de la Champions
                    eliminado=row['eliminado'],
                    # 'eliminado_logico' significa borrado del sistema
                    eliminado_logico=row['eliminado_logico']
                )
                db.add(nuevo_equipo)

        # Commit de los cambios
        db.commit()
        print(f"Migración de equipos completada. Registros insertados: {len(df_activos)}")

        # Imprimir detalles adicionales
        print("\nDetalles de equipos:")
        print(f"Total de equipos en CSV: {len(df)}")
        print(f"Equipos activos en Champions: {len(df_activos)}")
        print(f"Equipos eliminados de Champions: {len(df[df['eliminado'] == True])}")
        print(f"Equipos eliminados lógicamente: {len(df[df['eliminado_logico'] == True])}")

    except Exception as e:
        # Rollback en caso de error
        db.rollback()
        print(f"Error en la migración de equipos: {e}")

    finally:
        # Cerrar la sesión
        db.close()


def migrar_jugadores(ruta_csv: str):
    """
    Migra datos de jugadores desde un CSV a la base de datos

    :param ruta_csv: Ruta del archivo CSV con datos de jugadores
    """
    db = SessionLocal()

    try:
        # Leer el CSV
        df = pd.read_csv(ruta_csv, encoding='utf-8')

        # Filtrar jugadores que no están eliminados de la Champions
        df_activos = df[df['eliminado'] == False]

        print(f"Iniciando migración de jugadores. Total de registros: {len(df_activos)}")

        for _, row in df_activos.iterrows():
            # Verificar si el jugador ya existe para evitar duplicados
            jugador_existente = db.query(Jugador).filter(
                Jugador.nombre == row['nombre'],
                Jugador.equipo == row['equipo']
            ).first()

            if not jugador_existente:
                nuevo_jugador = Jugador(
                    id=row['id'],
                    nombre=row['nombre'],
                    equipo=row['equipo'],
                    posicion=row['posicion'],
                    edad=row['edad'],
                    nacionalidad=row['nacionalidad'],
                    goles=row['goles'],
                    asistencias=row['asistencias'],
                    # 'eliminado' significa eliminado de la Champions
                    eliminado=row['eliminado'],
                    # 'eliminado_logico' significa borrado del sistema
                    eliminado_logico=row['eliminado_logico']
                )
                db.add(nuevo_jugador)

        # Commit de los cambios
        db.commit()
        print(f"Migración de jugadores completada. Registros insertados: {len(df_activos)}")

        # Imprimir detalles adicionales
        print("\nDetalles de jugadores:")
        print(f"Total de jugadores en CSV: {len(df)}")
        print(f"Jugadores activos en Champions: {len(df_activos)}")
        print(f"Jugadores eliminados de Champions: {len(df[df['eliminado'] == True])}")
        print(f"Jugadores eliminados lógicamente: {len(df[df['eliminado_logico'] == True])}")

    except Exception as e:
        # Rollback en caso de error
        db.rollback()
        print(f"Error en la migración de jugadores: {e}")

    finally:
        # Cerrar la sesión
        db.close()


def migrar_datos():
    """
    Función principal para migrar datos desde CSVs
    """
    # Obtener el directorio del script actual
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Rutas de los archivos CSV
    jugadores_path = os.path.join(script_dir, 'data', 'jugadores.csv')
    equipos_path = os.path.join(script_dir, 'data', 'equipos.csv')

    print("Iniciando proceso de migración de datos")
    print("======================================")

    # Migrar equipos
    migrar_equipos(equipos_path)

    # Migrar jugadores
    migrar_jugadores(jugadores_path)

    print("\nProceso de migración completado.")


def limpiar_datos():
    """
    Función para limpiar todos los registros existentes antes de la migración
    """
    db = SessionLocal()

    try:
        # Eliminar todos los registros existentes
        db.query(Jugador).delete()
        db.query(Equipo).delete()

        # Commit de los cambios
        db.commit()
        print("Todos los registros existentes han sido eliminados.")

    except Exception as e:
        # Rollback en caso de error
        db.rollback()
        print(f"Error al limpiar los datos: {e}")

    finally:
        # Cerrar la sesión
        db.close()


if __name__ == "__main__":
    # Crear todas las tablas
    from utils.db import Base

    Base.metadata.create_all(bind=engine)

    # Limpiar datos existentes (opcional)
    limpiar_datos()

    # Ejecutar migración
    migrar_datos()