import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models import Base, Jugador, Equipo  # Asegúrate de que estos imports sean correctos

# Cargar variables de entorno del archivo .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está configurada en el archivo .env o en el entorno.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def populate_database():
    db = next(get_db())

    try:
        print("Borrando todas las tablas existentes...")
        Base.metadata.drop_all(bind=engine)
        print("Tablas borradas.")

        print("Creando todas las tablas nuevas...")
        Base.metadata.create_all(bind=engine)
        print("Tablas creadas.")

        # Datos de Equipos (Champions League 2017/18 - Fase de Grupos y Octavos)
        equipos_data = [
            {"nombre": "Real Madrid", "pais": "España", "grupo": "H", "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Real_Madrid_Castilla_CF_logo.svg/1200px-Real_Madrid_Castilla_CF_logo.svg.png"},
            {"nombre": "FC Barcelona", "pais": "España", "grupo": "D", "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/FC_Barcelona_Logo.svg/1200px-FC_Barcelona_Logo.svg.png"},
            {"nombre": "Manchester United", "pais": "Inglaterra", "grupo": "A", "imagen_url": "https://upload.wikimedia.org/wikipedia/en/thumb/7/7a/Manchester_United_FC_crest.svg/1200px-Manchester_United_FC_crest.svg.png"},
            {"nombre": "Juventus", "pais": "Italia", "grupo": "D", "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Juventus_FC_2017_logo.svg/1200px-Juventus_FC_2017_logo.svg.png"},
            {"nombre": "Bayern Munich", "pais": "Alemania", "grupo": "B", "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/FCBayern_Logo.svg/1200px-FCBayern_Logo.svg.png"},
            {"nombre": "Paris Saint-Germain", "pais": "Francia", "grupo": "B", "imagen_url": "https://upload.wikimedia.org/wikipedia/en/thumb/4/47/Paris_Saint-Germain_F.C._logo.svg/1200px-Paris_Saint-Germain_F.C._logo.svg.png"},
            {"nombre": "Liverpool FC", "pais": "Inglaterra", "grupo": "E", "imagen_url": "https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg"},
            {"nombre": "Chelsea FC", "pais": "Inglaterra", "grupo": "C", "imagen_url": "https://upload.wikimedia.org/wikipedia/en/thumb/f/ff/Chelsea_FC.svg/1200px-Chelsea_FC.svg.png"},
            {"nombre": "Tottenham Hotspur", "pais": "Inglaterra", "grupo": "H", "imagen_url": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b4/Tottenham_Hotspur.svg/1200px-Tottenham_Hotspur.svg.png"},
            {"nombre": "Manchester City", "pais": "Inglaterra", "grupo": "F", "imagen_url": "https://upload.wikimedia.org/wikipedia/en/thumb/e/eb/Manchester_City_FC_logo.svg/1200px-Manchester_City_FC_logo.svg.png"},
            {"nombre": "AS Roma", "pais": "Italia", "grupo": "C", "imagen_url": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f7/AS_Roma_logo_%282017%29.svg/1200px-AS_Roma_logo_%282017%29.svg.png"},
            {"nombre": "Sevilla FC", "pais": "España", "grupo": "E", "imagen_url": "https://upload.wikimedia.org/wikipedia/en/thumb/3/3b/Sevilla_FC_logo.svg/1200px-Sevilla_FC_logo.svg.png"},
            {"nombre": "Borussia Dortmund", "pais": "Alemania", "grupo": "H", "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Borussia_Dortmund_logo.svg/1200px-Borussia_Dortmund_logo.svg.png"},
            {"nombre": "FC Porto", "pais": "Portugal", "grupo": "G", "imagen_url": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f1/FC_Porto_logo.svg/1200px-FC_Porto_logo.svg.png"},
            {"nombre": "Shakhtar Donetsk", "pais": "Ucrania", "grupo": "F", "imagen_url": "https://upload.wikimedia.org/wikipedia/en/thumb/7/77/FC_Shakhtar_Donetsk_logo.svg/1200px-FC_Shakhtar_Donetsk_logo.svg.png"},
            {"nombre": "Besiktas JK", "pais": "Turquía", "grupo": "G", "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Be%C5%9Fikta%C5%9F_JK_logo.svg/1200px-Be%C5%9Fikta%C5%9F_JK_logo.svg.png"},
            {"nombre": "RB Leipzig", "pais": "Alemania", "grupo": "G", "imagen_url": "https://upload.wikimedia.org/wikipedia/en/thumb/0/04/RB_Leipzig_logo.svg/1200px-RB_Leipzig_logo.svg.png"},
            {"nombre": "SSC Napoli", "pais": "Italia", "grupo": "F", "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/SSC_Napoli_logo.svg/1200px-SSC_Napoli_logo.svg.png"},
            {"nombre": "AS Monaco", "pais": "Francia", "grupo": "G", "imagen_url": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f0/AS_Monaco_FC_logo.svg/1200px-AS_Monaco_FC_logo.svg.png"},
            {"nombre": "Sporting CP", "pais": "Portugal", "grupo": "D", "imagen_url": "https://upload.wikimedia.org/wikipedia/en/thumb/3/3e/Sporting_CP_logo.svg/1200px-Sporting_CP_logo.svg.png"},
            {"nombre": "CSKA Moscow", "pais": "Rusia", "grupo": "A", "imagen_url": "https://upload.wikimedia.org/wikipedia/en/thumb/2/23/PFC_CSKA_Moscow_logo.svg/1200px-PFC_CSKA_Moscow_logo.svg.png"},
            {"nombre": "Olympiacos FC", "pais": "Grecia", "grupo": "D", "imagen_url": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f1/Olympiacos_FC_logo.svg/1200px-Olympiacos_FC_logo.svg.png"},
            {"nombre": "Benfica", "pais": "Portugal", "grupo": "A", "imagen_url": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a2/SL_Benfica_logo.svg/1200px-SL_Benfica_logo.svg.png"},
            {"nombre": "Atlético Madrid", "pais": "España", "grupo": "C", "imagen_url": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f4/Atletico_Madrid_2017_logo.svg/1200px-Atletico_Madrid_2017_logo.svg.png"},
            {"nombre": "FC Basel", "pais": "Suiza", "grupo": "A", "imagen_url": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b3/FC_Basel_logo.svg/1200px-FC_Basel_logo.svg.png"},
            {"nombre": "Celtic FC", "pais": "Escocia", "grupo": "B", "imagen_url": "https://upload.wikimedia.org/wikipedia/en/thumb/c/cc/Celtic_FC_logo.svg/1200px-Celtic_FC_logo.svg.png"},
            {"nombre": "Feyenoord", "pais": "Países Bajos", "grupo": "F", "imagen_url": "https://upload.wikimedia.org/wikipedia/en/thumb/1/12/Feyenoord_logo.svg/1200px-Feyenoord_logo.svg.png"},
            {"nombre": "Spartak Moscow", "pais": "Rusia", "grupo": "E", "imagen_url": "https://upload.wikimedia.org/wikipedia/en/thumb/0/07/FC_Spartak_Moscow_logo.svg/1200px-FC_Spartak_Moscow_logo.svg.png"},
            {"nombre": "APOEL FC", "pais": "Chipre", "grupo": "H", "imagen_url": "https://upload.wikimedia.org/wikipedia/en/thumb/5/5a/APOEL_FC_logo.svg/1200px-APOEL_FC_logo.svg.png"},
            {"nombre": "Qarabag FK", "pais": "Azerbaiyán", "grupo": "C", "imagen_url": "https://upload.wikimedia.org/wikipedia/en/thumb/2/23/Qaraba%C4%9F_FK_logo.svg/1200px-Qaraba%C4%9F_FK_logo.svg.png"},
            {"nombre": "Maribor", "pais": "Eslovenia", "grupo": "E", "imagen_url": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a2/NK_Maribor_logo.svg/1200px-NK_Maribor_logo.svg.png"},
            {"nombre": "RSC Anderlecht", "pais": "Bélgica", "grupo": "B", "imagen_url": "https://upload.wikimedia.org/wikipedia/en/thumb/c/c2/R.S.C._Anderlecht_logo.svg/1200px-R.S.C._Anderlecht_logo.svg.png"}
        ]

        equipos_obj = {}
        for data in equipos_data:
            equipo = Equipo(**data)
            db.add(equipo)
            db.flush()
            equipos_obj[equipo.nombre] = equipo
        db.commit()
        print("Equipos insertados.")

        # Datos de Jugadores (Champions League 2017/18 - una selección más amplia)
        jugadores_data = [
            # Real Madrid
            {"nombre": "Cristiano Ronaldo", "edad": 38, "posicion": "Delantero", "nacionalidad": "Portugal", "equipo_id": equipos_obj["Real Madrid"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Cristiano_Ronaldo_2018.jpg/800px-Cristiano_Ronaldo_2018.jpg", "goles": 15, "asistencias": 3},
            {"nombre": "Sergio Ramos", "edad": 38, "posicion": "Defensa", "nacionalidad": "España", "equipo_id": equipos_obj["Real Madrid"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Sergio_Ramos_2018.jpg/800px-Sergio_Ramos_2018.jpg", "goles": 1, "asistencias": 0},
            {"nombre": "Luka Modric", "edad": 38, "posicion": "Centrocampista", "nacionalidad": "Croacia", "equipo_id": equipos_obj["Real Madrid"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Luka_Modri%C4%87_2018.jpg/800px-Luka_Modri%C4%87_2018.jpg", "goles": 1, "asistencias": 2},
            {"nombre": "Toni Kroos", "edad": 34, "posicion": "Centrocampista", "nacionalidad": "Alemania", "equipo_id": equipos_obj["Real Madrid"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Toni_Kroos_2018.jpg/800px-Toni_Kroos_2018.jpg", "goles": 0, "asistencias": 3},
            {"nombre": "Gareth Bale", "edad": 34, "posicion": "Delantero", "nacionalidad": "Gales", "equipo_id": equipos_obj["Real Madrid"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Gareth_Bale_2018.jpg/800px-Gareth_Bale_2018.jpg", "goles": 3, "asistencias": 1},
            {"nombre": "Keylor Navas", "edad": 37, "posicion": "Portero", "nacionalidad": "Costa Rica", "equipo_id": equipos_obj["Real Madrid"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Keylor_Navas_2018.jpg/800px-Keylor_Navas_2018.jpg", "goles": 0, "asistencias": 0},
            {"nombre": "Casemiro", "edad": 32, "posicion": "Centrocampista", "nacionalidad": "Brasil", "equipo_id": equipos_obj["Real Madrid"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Casemiro_2018.jpg/800px-Casemiro_2018.jpg", "goles": 1, "asistencias": 0},
            {"nombre": "Isco", "edad": 32, "posicion": "Centrocampista", "nacionalidad": "España", "equipo_id": equipos_obj["Real Madrid"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Isco_2018.jpg/800px-Isco_2018.jpg", "goles": 1, "asistencias": 1},

            # FC Barcelona
            {"nombre": "Lionel Messi", "edad": 37, "posicion": "Delantero", "nacionalidad": "Argentina", "equipo_id": equipos_obj["FC Barcelona"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Lionel_Messi_2018.jpg/800px-Lionel_Messi_2018.jpg", "goles": 6, "asistencias": 2},
            {"nombre": "Luis Suarez", "edad": 37, "posicion": "Delantero", "nacionalidad": "Uruguay", "equipo_id": equipos_obj["FC Barcelona"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Luis_Su%C3%A1rez_2018.jpg/800px-Luis_Su%C3%A1rez_2018.jpg", "goles": 1, "asistencias": 3},
            {"nombre": "Marc-Andre ter Stegen", "edad": 32, "posicion": "Portero", "nacionalidad": "Alemania", "equipo_id": equipos_obj["FC Barcelona"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Marc-Andr%C3%A9_ter_Stegen_2018.jpg/800px-Marc-Andr%C3%A9_ter_Stegen_2018.jpg", "goles": 0, "asistencias": 0},
            {"nombre": "Ivan Rakitic", "edad": 36, "posicion": "Centrocampista", "nacionalidad": "Croacia", "equipo_id": equipos_obj["FC Barcelona"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Ivan_Rakiti%C4%87_2018.jpg/800px-Ivan_Rakiti%C4%87_2018.jpg", "goles": 1, "asistencias": 1},
            {"nombre": "Sergio Busquets", "edad": 35, "posicion": "Centrocampista", "nacionalidad": "España", "equipo_id": equipos_obj["FC Barcelona"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Sergio_Busquets_2018.jpg/800px-Sergio_Busquets_2018.jpg", "goles": 0, "asistencias": 0},
            {"nombre": "Philippe Coutinho", "edad": 32, "posicion": "Centrocampista", "nacionalidad": "Brasil", "equipo_id": equipos_obj["FC Barcelona"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Philippe_Coutinho_2018.jpg/800px-Philippe_Coutinho_2018.jpg", "goles": 0, "asistencias": 1},

            # Manchester United
            {"nombre": "Paul Pogba", "edad": 31, "posicion": "Centrocampista", "nacionalidad": "Francia", "equipo_id": equipos_obj["Manchester United"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Paul_Pogba_2018.jpg/800px-Paul_Pogba_2018.jpg", "goles": 2, "asistencias": 0},
            {"nombre": "Romelu Lukaku", "edad": 31, "posicion": "Delantero", "nacionalidad": "Bélgica", "equipo_id": equipos_obj["Manchester United"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Romelu_Lukaku_2018.jpg/800px-Romelu_Lukaku_2018.jpg", "goles": 5, "asistencias": 1},
            {"nombre": "Alexis Sanchez", "edad": 35, "posicion": "Delantero", "nacionalidad": "Chile", "equipo_id": equipos_obj["Manchester United"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Alexis_S%C3%A1nchez_2018.jpg/800px-Alexis_S%C3%A1nchez_2018.jpg", "goles": 1, "asistencias": 0},
            {"nombre": "David de Gea", "edad": 33, "posicion": "Portero", "nacionalidad": "España", "equipo_id": equipos_obj["Manchester United"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/David_de_Gea_2018.jpg/800px-David_de_Gea_2018.jpg", "goles": 0, "asistencias": 0},
            {"nombre": "Jesse Lingard", "edad": 31, "posicion": "Centrocampista", "nacionalidad": "Inglaterra", "equipo_id": equipos_obj["Manchester United"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Jesse_Lingard_2018.jpg/800px-Jesse_Lingard_2018.jpg", "goles": 0, "asistencias": 0},

            # Juventus
            {"nombre": "Paulo Dybala", "edad": 30, "posicion": "Delantero", "nacionalidad": "Argentina", "equipo_id": equipos_obj["Juventus"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Paulo_Dybala_2018.jpg/800px-Paulo_Dybala_2018.jpg", "goles": 1, "asistencias": 0},
            {"nombre": "Gonzalo Higuain", "edad": 36, "posicion": "Delantero", "nacionalidad": "Argentina", "equipo_id": equipos_obj["Juventus"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Gonzalo_Higua%C3%ADn_2018.jpg/800px-Gonzalo_Higua%C3%ADn_2018.jpg", "goles": 5, "asistencias": 0},
            {"nombre": "Miralem Pjanic", "edad": 34, "posicion": "Centrocampista", "nacionalidad": "Bosnia y Herzegovina", "equipo_id": equipos_obj["Juventus"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Miralem_Pjani%C4%87_2018.jpg/800px-Miralem_Pjani%C4%87_2018.jpg", "goles": 1, "asistencias": 0},
            {"nombre": "Giorgio Chiellini", "edad": 39, "posicion": "Defensa", "nacionalidad": "Italia", "equipo_id": equipos_obj["Juventus"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Giorgio_Chiellini_2018.jpg/800px-Giorgio_Chiellini_2018.jpg", "goles": 0, "asistencias": 0},

            # Bayern Munich
            {"nombre": "Robert Lewandowski", "edad": 35, "posicion": "Delantero", "nacionalidad": "Polonia", "equipo_id": equipos_obj["Bayern Munich"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Robert_Lewandowski_2020.jpg/800px-Robert_Lewandowski_2020.jpg", "goles": 5, "asistencias": 2},
            {"nombre": "Thomas Müller", "edad": 34, "posicion": "Delantero", "nacionalidad": "Alemania", "equipo_id": equipos_obj["Bayern Munich"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Thomas_M%C3%BCller_2020.jpg/800px-Thomas_M%C3%BCller_2020.jpg", "goles": 3, "asistencias": 1},
            {"nombre": "Arjen Robben", "edad": 41, "posicion": "Centrocampista", "nacionalidad": "Países Bajos", "equipo_id": equipos_obj["Bayern Munich"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Arjen_Robben_2018.jpg/800px-Arjen_Robben_2018.jpg", "goles": 2, "asistencias": 0},
            {"nombre": "Manuel Neuer", "edad": 38, "posicion": "Portero", "nacionalidad": "Alemania", "equipo_id": equipos_obj["Bayern Munich"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Manuel_Neuer_2018.jpg/800px-Manuel_Neuer_2018.jpg", "goles": 0, "asistencias": 0},
            {"nombre": "Joshua Kimmich", "edad": 29, "posicion": "Defensa", "nacionalidad": "Alemania", "equipo_id": equipos_obj["Bayern Munich"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Joshua_Kimmich_2018.jpg/800px-Joshua_Kimmich_2018.jpg", "goles": 1, "asistencias": 1},

            # Paris Saint-Germain
            {"nombre": "Neymar Jr.", "edad": 32, "posicion": "Delantero", "nacionalidad": "Brasil", "equipo_id": equipos_obj["Paris Saint-Germain"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Neymar_Jr._2018.jpg/800px-Neymar_Jr._2018.jpg", "goles": 6, "asistencias": 3},
            {"nombre": "Kylian Mbappé", "edad": 25, "posicion": "Delantero", "nacionalidad": "Francia", "equipo_id": equipos_obj["Paris Saint-Germain"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Kylian_Mbapp%C3%A9_2018.jpg/800px-Kylian_Mbapp%C3%A9_2018.jpg", "goles": 4, "asistencias": 3},
            {"nombre": "Edinson Cavani", "edad": 37, "posicion": "Delantero", "nacionalidad": "Uruguay", "equipo_id": equipos_obj["Paris Saint-Germain"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Edinson_Cavani_2018.jpg/800px-Edinson_Cavani_2018.jpg", "goles": 7, "asistencias": 0},
            {"nombre": "Dani Alves", "edad": 41, "posicion": "Defensa", "nacionalidad": "Brasil", "equipo_id": equipos_obj["Paris Saint-Germain"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Dani_Alves_2018.jpg/800px-Dani_Alves_2018.jpg", "goles": 1, "asistencias": 2},

            # Liverpool FC
            {"nombre": "Mohamed Salah", "edad": 32, "posicion": "Delantero", "nacionalidad": "Egipto", "equipo_id": equipos_obj["Liverpool FC"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Mohamed_Salah_2018.jpg/800px-Mohamed_Salah_2018.jpg", "goles": 10, "asistencias": 5},
            {"nombre": "Roberto Firmino", "edad": 32, "posicion": "Delantero", "nacionalidad": "Brasil", "equipo_id": equipos_obj["Liverpool FC"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Roberto_Firmino_2018.jpg/800px-Roberto_Firmino_2018.jpg", "goles": 10, "asistencias": 7},
            {"nombre": "Sadio Mane", "edad": 32, "posicion": "Delantero", "nacionalidad": "Senegal", "equipo_id": equipos_obj["Liverpool FC"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Sadio_Man%C3%A9_2018.jpg/800px-Sadio_Man%C3%A9_2018.jpg", "goles": 10, "asistencias": 1},
            {"nombre": "Virgil van Dijk", "edad": 32, "posicion": "Defensa", "nacionalidad": "Países Bajos", "equipo_id": equipos_obj["Liverpool FC"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Virgil_van_Dijk_2018.jpg/800px-Virgil_van_Dijk_2018.jpg", "goles": 1, "asistencias": 0},

            # Chelsea FC
            {"nombre": "Eden Hazard", "edad": 33, "posicion": "Delantero", "nacionalidad": "Bélgica", "equipo_id": equipos_obj["Chelsea FC"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Eden_Hazard_2018.jpg/800px-Eden_Hazard_2018.jpg", "goles": 3, "asistencias": 3},
            {"nombre": "N'Golo Kante", "edad": 33, "posicion": "Centrocampista", "nacionalidad": "Francia", "equipo_id": equipos_obj["Chelsea FC"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/N%27Golo_Kant%C3%A9_2018.jpg/800px-N%27Golo_Kant%C3%A9_2018.jpg", "goles": 0, "asistencias": 1},
            {"nombre": "Alvaro Morata", "edad": 31, "posicion": "Delantero", "nacionalidad": "España", "equipo_id": equipos_obj["Chelsea FC"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Alvaro_Morata_2018.jpg/800px-Alvaro_Morata_2018.jpg", "goles": 1, "asistencias": 0},

            # Tottenham Hotspur
            {"nombre": "Harry Kane", "edad": 30, "posicion": "Delantero", "nacionalidad": "Inglaterra", "equipo_id": equipos_obj["Tottenham Hotspur"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Harry_Kane_2018.jpg/800px-Harry_Kane_2018.jpg", "goles": 7, "asistencias": 1},
            {"nombre": "Dele Alli", "edad": 28, "posicion": "Centrocampista", "nacionalidad": "Inglaterra", "equipo_id": equipos_obj["Tottenham Hotspur"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Dele_Alli_2018.jpg/800px-Dele_Alli_2018.jpg", "goles": 2, "asistencias": 4},
            {"nombre": "Christian Eriksen", "edad": 32, "posicion": "Centrocampista", "nacionalidad": "Dinamarca", "equipo_id": equipos_obj["Tottenham Hotspur"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Christian_Eriksen_2018.jpg/800px-Christian_Eriksen_2018.jpg", "goles": 2, "asistencias": 2},

            # Manchester City
            {"nombre": "Kevin De Bruyne", "edad": 33, "posicion": "Centrocampista", "nacionalidad": "Bélgica", "equipo_id": equipos_obj["Manchester City"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Kevin_De_Bruyne_2018.jpg/800px-Kevin_De_Bruyne_2018.jpg", "goles": 1, "asistencias": 4},
            {"nombre": "Sergio Agüero", "edad": 36, "posicion": "Delantero", "nacionalidad": "Argentina", "equipo_id": equipos_obj["Manchester City"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Sergio_Ag%C3%BCero_2018.jpg/800px-Sergio_Ag%C3%BCero_2018.jpg", "goles": 4, "asistencias": 1},
            {"nombre": "Raheem Sterling", "edad": 29, "posicion": "Delantero", "nacionalidad": "Inglaterra", "equipo_id": equipos_obj["Manchester City"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Raheem_Sterling_2018.jpg/800px-Raheem_Sterling_2018.jpg", "goles": 4, "asistencias": 0},
            {"nombre": "Gabriel Jesus", "edad": 27, "posicion": "Delantero", "nacionalidad": "Brasil", "equipo_id": equipos_obj["Manchester City"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Gabriel_Jesus_2018.jpg/800px-Gabriel_Jesus_2018.jpg", "goles": 4, "asistencias": 0},

            # AS Roma
            {"nombre": "Edin Džeko", "edad": 38, "posicion": "Delantero", "nacionalidad": "Bosnia y Herzegovina", "equipo_id": equipos_obj["AS Roma"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Edin_D%C5%BEeko_2018.jpg/800px-Edin_D%C5%BEeko_2018.jpg", "goles": 8, "asistencias": 0},
            {"nombre": "Alisson Becker", "edad": 31, "posicion": "Portero", "nacionalidad": "Brasil", "equipo_id": equipos_obj["AS Roma"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Alisson_Becker_2018.jpg/800px-Alisson_Becker_2018.jpg", "goles": 0, "asistencias": 0},
            {"nombre": "Radja Nainggolan", "edad": 36, "posicion": "Centrocampista", "nacionalidad": "Bélgica", "equipo_id": equipos_obj["AS Roma"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Radja_Nainggolan_2018.jpg/800px-Radja_Nainggolan_2018.jpg", "goles": 2, "asistencias": 0},

            # Sevilla FC
            {"nombre": "Éver Banega", "edad": 35, "posicion": "Centrocampista", "nacionalidad": "Argentina", "equipo_id": equipos_obj["Sevilla FC"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/%C3%89ver_Banega_2018.jpg/800px-%C3%89ver_Banega_2018.jpg", "goles": 0, "asistencias": 2},
            {"nombre": "Wissam Ben Yedder", "edad": 33, "posicion": "Delantero", "nacionalidad": "Francia", "equipo_id": equipos_obj["Sevilla FC"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Wissam_Ben_Yedder_2018.jpg/800px-Wissam_Ben_Yedder_2018.jpg", "goles": 6, "asistencias": 0},

            # Borussia Dortmund
            {"nombre": "Marco Reus", "edad": 35, "posicion": "Delantero", "nacionalidad": "Alemania", "equipo_id": equipos_obj["Borussia Dortmund"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Marco_Reus_2018.jpg/800px-Marco_Reus_2018.jpg", "goles": 1, "asistencias": 0},
            {"nombre": "Pierre-Emerick Aubameyang", "edad": 35, "posicion": "Delantero", "nacionalidad": "Gabón", "equipo_id": equipos_obj["Borussia Dortmund"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Pierre-Emerick_Aubameyang_2018.jpg/800px-Pierre-Emerick_Aubameyang_2018.jpg", "goles": 4, "asistencias": 0},

            # FC Porto
            {"nombre": "Vincent Aboubakar", "edad": 32, "posicion": "Delantero", "nacionalidad": "Camerún", "equipo_id": equipos_obj["FC Porto"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Vincent_Aboubakar_2018.jpg/800px-Vincent_Aboubakar_2018.jpg", "goles": 5, "asistencias": 0},
            {"nombre": "Yacine Brahimi", "edad": 34, "posicion": "Centrocampista", "nacionalidad": "Argelia", "equipo_id": equipos_obj["FC Porto"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Yacine_Brahimi_2018.jpg/800px-Yacine_Brahimi_2018.jpg", "goles": 1, "asistencias": 1},

            # Shakhtar Donetsk
            {"nombre": "Taison", "edad": 36, "posicion": "Centrocampista", "nacionalidad": "Brasil", "equipo_id": equipos_obj["Shakhtar Donetsk"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Taison_2018.jpg/800px-Taison_2018.jpg", "goles": 1, "asistencias": 1},
            {"nombre": "Fred", "edad": 31, "posicion": "Centrocampista", "nacionalidad": "Brasil", "equipo_id": equipos_obj["Shakhtar Donetsk"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Fred_2018.jpg/800px-Fred_2018.jpg", "goles": 3, "asistencias": 0},

            # Besiktas JK
            {"nombre": "Ricardo Quaresma", "edad": 40, "posicion": "Delantero", "nacionalidad": "Portugal", "equipo_id": equipos_obj["Besiktas JK"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Ricardo_Quaresma_2018.jpg/800px-Ricardo_Quaresma_2018.jpg", "goles": 4, "asistencias": 0},
            {"nombre": "Cenk Tosun", "edad": 33, "posicion": "Delantero", "nacionalidad": "Turquía", "equipo_id": equipos_obj["Besiktas JK"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Cenk_Tosun_2018.jpg/800px-Cenk_Tosun_2018.jpg", "goles": 4, "asistencias": 0},

            # RB Leipzig
            {"nombre": "Timo Werner", "edad": 28, "posicion": "Delantero", "nacionalidad": "Alemania", "equipo_id": equipos_obj["RB Leipzig"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Timo_Werner_2018.jpg/800px-Timo_Werner_2018.jpg", "goles": 3, "asistencias": 0},
            {"nombre": "Emil Forsberg", "edad": 32, "posicion": "Centrocampista", "nacionalidad": "Suecia", "equipo_id": equipos_obj["RB Leipzig"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Emil_Forsberg_2018.jpg/800px-Emil_Forsberg_2018.jpg", "goles": 0, "asistencias": 1},

            # SSC Napoli
            {"nombre": "Dries Mertens", "edad": 37, "posicion": "Delantero", "nacionalidad": "Bélgica", "equipo_id": equipos_obj["SSC Napoli"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Dries_Mertens_2018.jpg/800px-Dries_Mertens_2018.jpg", "goles": 3, "asistencias": 0},
            {"nombre": "Lorenzo Insigne", "edad": 33, "posicion": "Delantero", "nacionalidad": "Italia", "equipo_id": equipos_obj["SSC Napoli"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Lorenzo_Insigne_2018.jpg/800px-Lorenzo_Insigne_2018.jpg", "goles": 0, "asistencias": 1},

            # AS Monaco
            {"nombre": "Radamel Falcao", "edad": 38, "posicion": "Delantero", "nacionalidad": "Colombia", "equipo_id": equipos_obj["AS Monaco"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Radamel_Falcao_2018.jpg/800px-Radamel_Falcao_2018.jpg", "goles": 3, "asistencias": 0},

            # Sporting CP
            {"nombre": "Bas Dost", "edad": 35, "posicion": "Delantero", "nacionalidad": "Países Bajos", "equipo_id": equipos_obj["Sporting CP"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Bas_Dost_2018.jpg/800px-Bas_Dost_2018.jpg", "goles": 0, "asistencias": 0},

            # CSKA Moscow
            {"nombre": "Alan Dzagoev", "edad": 33, "posicion": "Centrocampista", "nacionalidad": "Rusia", "equipo_id": equipos_obj["CSKA Moscow"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Alan_Dzagoev_2018.jpg/800px-Alan_Dzagoev_2018.jpg", "goles": 1, "asistencias": 0},

            # Atlético Madrid
            {"nombre": "Antoine Griezmann", "edad": 33, "posicion": "Delantero", "nacionalidad": "Francia", "equipo_id": equipos_obj["Atlético Madrid"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Antoine_Griezmann_2018.jpg/800px-Antoine_Griezmann_2018.jpg", "goles": 2, "asistencias": 0},
            {"nombre": "Jan Oblak", "edad": 31, "posicion": "Portero", "nacionalidad": "Eslovenia", "equipo_id": equipos_obj["Atlético Madrid"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Jan_Oblak_2018.jpg/800px-Jan_Oblak_2018.jpg", "goles": 0, "asistencias": 0},

            # FC Basel
            {"nombre": "Dimitri Oberlin", "edad": 26, "posicion": "Delantero", "nacionalidad": "Suiza", "equipo_id": equipos_obj["FC Basel"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Dimitri_Oberlin_2018.jpg/800px-Dimitri_Oberlin_2018.jpg", "goles": 4, "asistencias": 0},

            # Celtic FC
            {"nombre": "Moussa Dembélé", "edad": 27, "posicion": "Delantero", "nacionalidad": "Francia", "equipo_id": equipos_obj["Celtic FC"].id, "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Moussa_Demb%C3%A9l%C3%A9_2018.jpg/800px-Moussa_Demb%C3%A9l%C3%A9_2018.jpg", "goles": 0, "asistencias": 0},
        ]

        for data in jugadores_data:
            jugador = Jugador(**data)
            db.add(jugador)
        db.commit()
        print("Jugadores insertados.")

        print("Base de datos poblada exitosamente.")

    except Exception as e:
        db.rollback()
        print(f"Error al poblar la base de datos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    populate_database()  