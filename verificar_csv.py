import os
import pandas as pd


def verificar_archivos_csv():
    # Obtener el directorio del script actual
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Rutas de los archivos CSV
    jugadores_path = os.path.join(script_dir, 'data', 'jugadores.csv')
    equipos_path = os.path.join(script_dir, 'data', 'equipos.csv')

    print("Verificación de archivos CSV")
    print("===========================")

    # Verificar archivo de jugadores
    print("\nArchivo de Jugadores:")
    print(f"Ruta: {jugadores_path}")

    if not os.path.exists(jugadores_path):
        print("ERROR: El archivo no existe")
        return

    try:
        jugadores_df = pd.read_csv(jugadores_path, encoding='utf-8')
        print("Archivo leído correctamente")
        print(f"Número de registros: {len(jugadores_df)}")
        print("\nColumnas:")
        print(jugadores_df.columns.tolist())
        print("\nPrimeras 5 filas:")
        print(jugadores_df.head())
    except Exception as e:
        print(f"Error leyendo el archivo: {e}")

    # Verificar archivo de equipos
    print("\n\nArchivo de Equipos:")
    print(f"Ruta: {equipos_path}")

    if not os.path.exists(equipos_path):
        print("ERROR: El archivo no existe")
        return

    try:
        equipos_df = pd.read_csv(equipos_path, encoding='utf-8')
        print("Archivo leído correctamente")
        print(f"Número de registros: {len(equipos_df)}")
        print("\nColumnas:")
        print(equipos_df.columns.tolist())
        print("\nPrimeras 5 filas:")
        print(equipos_df.head())
    except Exception as e:
        print(f"Error leyendo el archivo: {e}")


if __name__ == "__main__":
    verificar_archivos_csv()