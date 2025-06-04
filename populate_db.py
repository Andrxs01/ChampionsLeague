# populate_db.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models import Base, Jugador, Equipo, Partido # Importar Partido
from datetime import date

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
        # Usando URLs de placehold.co para simplificar la gestión de imágenes
        equipos_data = [
            {"nombre": "Real Madrid", "pais": "España", "grupo": "H",
             "imagen_url": "https://www.palladiumhotelgroup.com/content/dam/palladium/images/sponsorships/real-madrid/phg_sponsorship_real_madrid_baloncesto_header_logo.png.transform/rendition-md/image.png"},
            {"nombre": "FC Barcelona", "pais": "España", "grupo": "D",
             "imagen_url": "https://tse1.mm.bing.net/th/id/OIP.kc8-MEtNhw_GvS1BfBXW8AHaHa?rs=1&pid=ImgDetMain"},
            {"nombre": "Manchester United", "pais": "Inglaterra", "grupo": "A",
             "imagen_url": "https://tse1.mm.bing.net/th/id/OIP.fja0qpGK2jB8BqIkwPPttQHaHf?rs=1&pid=ImgDetMain"},
            {"nombre": "Juventus", "pais": "Italia", "grupo": "D",
             "imagen_url": "https://th.bing.com/th/id/R.3c4e3112a463ae8efe8a7a0c8e40cd13?rik=Ji35bOsYUptvGg&riu=http%3a%2f%2f1000marcas.net%2fwp-content%2fuploads%2f2020%2f01%2fJuventus-logo.png&ehk=6AHrWJ53F1JKUolXY%2boYs%2fQOABq%2b2XD6U8%2fmMNXAR5c%3d&risl=&pid=ImgRaw&r=0"},
            {"nombre": "Bayern Munich", "pais": "Alemania", "grupo": "B",
             "imagen_url": "https://tse4.mm.bing.net/th/id/OIP.hGa0pQAgF4g8c5FPbrOXuAHaHa?rs=1&pid=ImgDetMain"},
            {"nombre": "Paris Saint-Germain", "pais": "Francia", "grupo": "B",
             "imagen_url": "https://www.ecured.cu/images/thumb/4/44/Escudopsg.jpg/1200px-Escudopsg.jpg"},
            {"nombre": "Liverpool FC", "pais": "Inglaterra", "grupo": "E",
             "imagen_url": "https://tse4.mm.bing.net/th/id/OIP.iHQxSyxUIPLyASWY2wUomgHaE7?rs=1&pid=ImgDetMain"},
            {"nombre": "Chelsea FC", "pais": "Inglaterra", "grupo": "C",
             "imagen_url": "https://logodownload.org/wp-content/uploads/2017/02/chelsea-fc-logo-0.png"},
            {"nombre": "Tottenham Hotspur", "pais": "Inglaterra", "grupo": "H",
             "imagen_url": "https://logos-world.net/wp-content/uploads/2020/06/Tottenham-Hotspur-Logo.png"},
            {"nombre": "Manchester City", "pais": "Inglaterra", "grupo": "F",
             "imagen_url": "https://tse1.mm.bing.net/th/id/OIP.VCPWH5E83tV47m4Pvdr1QQHaHa?rs=1&pid=ImgDetMain"},
            {"nombre": "AS Roma", "pais": "Italia", "grupo": "C",
             "imagen_url": "https://th.bing.com/th/id/OIP.wk5DnP-OEbzHSAkUZvbvZQHaJl?rs=1&pid=ImgDetMain"},
            {"nombre": "Sevilla FC", "pais": "España", "grupo": "E",
             "imagen_url": "https://th.bing.com/th/id/R.67be7accb14002c14dacb41bacd87b9f?rik=D1GVDq%2brLbdOLg&riu=http%3a%2f%2flogos-download.com%2fwp-content%2fuploads%2f2016%2f05%2fSevilla_FC_logo_logotipo_logotype.jpg&ehk=i9imDpSJ876PBEKXIau%2flfxBhJpbw4YCO1CxAnnUOG4%3d&risl=&pid=ImgRaw&r=0"},
            {"nombre": "Borussia Dortmund", "pais": "Alemania", "grupo": "H",
             "imagen_url": "https://tse2.mm.bing.net/th/id/OIP.zG-TOvm2M8appExrOKJ2sQHaHa?rs=1&pid=ImgDetMain"},
            {"nombre": "FC Porto", "pais": "Portugal", "grupo": "G",
             "imagen_url": "https://bootflare.com/wp-content/uploads/2023/03/Porto-Logo.png"},
            {"nombre": "Shakhtar Donetsk", "pais": "Ucrania", "grupo": "F",
             "imagen_url": "https://th.bing.com/th/id/R.aa2eebe0ac231177ca649c792b9ac323?rik=SDFWpnx5XAs7Rg&pid=ImgRaw&r=0"},
            {"nombre": "Besiktas JK", "pais": "Turquía", "grupo": "G",
             "imagen_url": "https://tse1.mm.bing.net/th/id/OIP.0elaLSPd2tjZdKcQ3aLRxAHaEK?rs=1&pid=ImgDetMain"},
            {"nombre": "RB Leipzig", "pais": "Alemania", "grupo": "G",
             "imagen_url": "https://th.bing.com/th/id/OIP.yyklLd19krrVzC0eyMNksQHaEK?w=299&h=180&c=7&r=0&o=5&pid=1.7"},
            {"nombre": "SSC Napoli", "pais": "Italia", "grupo": "F",
             "imagen_url": "https://th.bing.com/th/id/OIP.h3z-nVstWndGLuO7fnUavAAAAA?w=183&h=183&c=7&r=0&o=5&pid=1.7"},
            {"nombre": "AS Monaco", "pais": "Francia", "grupo": "G",
             "imagen_url": "https://logodetimes.com/times/monaco/logo-monaco-4096.png"},
            {"nombre": "Sporting CP", "pais": "Portugal", "grupo": "D",
             "imagen_url": "https://tse3.mm.bing.net/th/id/OIP.DZbmpSBBF3ayLER_A_I0egHaHa?rs=1&pid=ImgDetMain"},
            {"nombre": "CSKA Moscow", "pais": "Rusia", "grupo": "A",
             "imagen_url": "https://tse4.mm.bing.net/th/id/OIP.XM-85Ra9MiSQpeBskp0_HAHaKG?rs=1&pid=ImgDetMain"},
            {"nombre": "Olympiacos FC", "pais": "Grecia", "grupo": "D",
             "imagen_url": "https://th.bing.com/th/id/R.ca1f024263c4efd2b9419344c257f164?rik=4nxniS5Rd5BKgg&pid=ImgRaw&r=0"},
            {"nombre": "Benfica", "pais": "Portugal", "grupo": "A",
             "imagen_url": "https://logos-world.net/wp-content/uploads/2020/11/Benfica-Logo-1999-present.jpg"},
            {"nombre": "Atlético Madrid", "pais": "España", "grupo": "C",
             "imagen_url": "https://paco-casal.com/wp-content/uploads/2017/07/escudo.jpg"},
            {"nombre": "FC Basel", "pais": "Suiza", "grupo": "A",
             "imagen_url": "https://th.bing.com/th/id/R.512d76d9380234f54d37174b4e9fe86b?rik=uTHnhXNyn3u%2bsw&pid=ImgRaw&r=0"},
            {"nombre": "Celtic FC", "pais": "Escocia", "grupo": "B",
             "imagen_url": "https://tse2.mm.bing.net/th/id/OIP.nu4dbrP5gYBdQaPNazMs3wHaHa?rs=1&pid=ImgDetMain"},
            {"nombre": "Feyenoord", "pais": "Países Bajos", "grupo": "F",
             "imagen_url": "https://tse2.mm.bing.net/th/id/OIP.3o9pUn0zTq4sSra7huHLawHaEK?rs=1&pid=ImgDetMain"},
            {"nombre": "Spartak Moscow", "pais": "Rusia", "grupo": "E",
             "imagen_url": "https://th.bing.com/th/id/R.c938cb08e5e0673a7e203f05e0fc9e43?rik=b8PaY9LSIlwseQ&riu=http%3a%2f%2flofrev.net%2fwp-content%2fphotos%2f2014%2f08%2fFC-Shakhtar-Donetsk-Logo-e1406959872383.jpg&ehk=R3WPON06r72qbEfKqwQ%2fTu8kBWnW5XzOl%2fHlMAXzEDQ%3d&risl=&pid=ImgRaw&r=0"},
            {"nombre": "APOEL FC", "pais": "Chipre", "grupo": "H",
             "imagen_url": "https://tse1.mm.bing.net/th/id/OIP.Vlg56Ik3_PIPtVLT0uZNWAHaE8?rs=1&pid=ImgDetMain"},
            {"nombre": "Qarabag FK", "pais": "Azerbaiyán", "grupo": "C",
             "imagen_url": "https://th.bing.com/th/id/R.fc30fa2403ee6f30186413f249368a38?rik=CI0ZxC5WNiy9gA&riu=http%3a%2f%2fww1.prweb.com%2fprfiles%2f2014%2f09%2f18%2f12181053%2fFK_Qarabag_Agdam.png&ehk=%2bxslzqddtJF3OE4D3OCIrUMJcf1NCRoTN9AZB9GzRvE%3d&risl=&pid=ImgRaw&r=0"},
            {"nombre": "Maribor", "pais": "Eslovenia", "grupo": "E",
             "imagen_url": "https://tse1.mm.bing.net/th/id/OIP.hSULt8i7KfzQ5OpXZDI-5wHaF_?rs=1&pid=ImgDetMain"},
            {"nombre": "RSC Anderlecht", "pais": "Bélgica", "grupo": "B",
             "imagen_url": "https://logos-world.net/wp-content/uploads/2020/11/Anderlecht-Logo-2009-2010.png"}
        ]

        equipos_obj = {}
        for data in equipos_data:
            equipo = Equipo(**data)
            db.add(equipo)
            db.flush() # Para que el ID esté disponible antes de commit
            equipos_obj[equipo.nombre] = equipo
        db.commit()
        print("Equipos insertados.")

        # Datos de Jugadores (Champions League 2017/18 - una selección más amplia)
        # NOTA: imagen_url ha sido eliminada del modelo Jugador
        jugadores_data = [
            # Real Madrid
            {"nombre": "Cristiano Ronaldo", "edad": 38, "posicion": "Delantero", "nacionalidad": "Portugal", "equipo_id": equipos_obj["Real Madrid"].id, "goles": 15, "asistencias": 3},
            {"nombre": "Sergio Ramos", "edad": 38, "posicion": "Defensa", "nacionalidad": "España", "equipo_id": equipos_obj["Real Madrid"].id, "goles": 1, "asistencias": 0},
            {"nombre": "Luka Modric", "edad": 38, "posicion": "Centrocampista", "nacionalidad": "Croacia", "equipo_id": equipos_obj["Real Madrid"].id, "goles": 1, "asistencias": 2},
            {"nombre": "Toni Kroos", "edad": 34, "posicion": "Centrocampista", "nacionalidad": "Alemania", "equipo_id": equipos_obj["Real Madrid"].id, "goles": 0, "asistencias": 3},
            {"nombre": "Gareth Bale", "edad": 34, "posicion": "Delantero", "nacionalidad": "Gales", "equipo_id": equipos_obj["Real Madrid"].id, "goles": 3, "asistencias": 1},
            {"nombre": "Keylor Navas", "edad": 37, "posicion": "Portero", "nacionalidad": "Costa Rica", "equipo_id": equipos_obj["Real Madrid"].id, "goles": 0, "asistencias": 0},
            {"nombre": "Casemiro", "edad": 32, "posicion": "Centrocampista", "nacionalidad": "Brasil", "equipo_id": equipos_obj["Real Madrid"].id, "goles": 1, "asistencias": 0},
            {"nombre": "Isco", "edad": 32, "posicion": "Centrocampista", "nacionalidad": "España", "equipo_id": equipos_obj["Real Madrid"].id, "goles": 1, "asistencias": 1},
            {"nombre": "Dani Carvajal", "edad": 32, "posicion": "Defensa", "nacionalidad": "España", "equipo_id": equipos_obj["Real Madrid"].id, "goles": 0, "asistencias": 1},
            {"nombre": "Marcelo", "edad": 36, "posicion": "Defensa", "nacionalidad": "Brasil", "equipo_id": equipos_obj["Real Madrid"].id, "goles": 0, "asistencias": 2},
            {"nombre": "Karim Benzema", "edad": 36, "posicion": "Delantero", "nacionalidad": "Francia", "equipo_id": equipos_obj["Real Madrid"].id, "goles": 5, "asistencias": 1},

            # FC Barcelona
            {"nombre": "Lionel Messi", "edad": 37, "posicion": "Delantero", "nacionalidad": "Argentina", "equipo_id": equipos_obj["FC Barcelona"].id, "goles": 6, "asistencias": 2},
            {"nombre": "Luis Suarez", "edad": 37, "posicion": "Delantero", "nacionalidad": "Uruguay", "equipo_id": equipos_obj["FC Barcelona"].id, "goles": 1, "asistencias": 3},
            {"nombre": "Marc-Andre ter Stegen", "edad": 32, "posicion": "Portero", "nacionalidad": "Alemania", "equipo_id": equipos_obj["FC Barcelona"].id, "goles": 0, "asistencias": 0},
            {"nombre": "Ivan Rakitic", "edad": 36, "posicion": "Centrocampista", "nacionalidad": "Croacia", "equipo_id": equipos_obj["FC Barcelona"].id, "goles": 1, "asistencias": 1},
            {"nombre": "Sergio Busquets", "edad": 35, "posicion": "Centrocampista", "nacionalidad": "España", "equipo_id": equipos_obj["FC Barcelona"].id, "goles": 0, "asistencias": 0},
            {"nombre": "Philippe Coutinho", "edad": 32, "posicion": "Centrocampista", "nacionalidad": "Brasil", "equipo_id": equipos_obj["FC Barcelona"].id, "goles": 0, "asistencias": 1},
            {"nombre": "Gerard Piqué", "edad": 37, "posicion": "Defensa", "nacionalidad": "España", "equipo_id": equipos_obj["FC Barcelona"].id, "goles": 1, "asistencias": 0},
            {"nombre": "Jordi Alba", "edad": 35, "posicion": "Defensa", "nacionalidad": "España", "equipo_id": equipos_obj["FC Barcelona"].id, "goles": 0, "asistencias": 2},

            # Manchester United
            {"nombre": "Paul Pogba", "edad": 31, "posicion": "Centrocampista", "nacionalidad": "Francia", "equipo_id": equipos_obj["Manchester United"].id, "goles": 2, "asistencias": 0},
            {"nombre": "Romelu Lukaku", "edad": 31, "posicion": "Delantero", "nacionalidad": "Bélgica", "equipo_id": equipos_obj["Manchester United"].id, "goles": 5, "asistencias": 1},
            {"nombre": "Alexis Sanchez", "edad": 35, "posicion": "Delantero", "nacionalidad": "Chile", "equipo_id": equipos_obj["Manchester United"].id, "goles": 1, "asistencias": 0},
            {"nombre": "David de Gea", "edad": 33, "posicion": "Portero", "nacionalidad": "España", "equipo_id": equipos_obj["Manchester United"].id, "goles": 0, "asistencias": 0},
            {"nombre": "Jesse Lingard", "edad": 31, "posicion": "Centrocampista", "nacionalidad": "Inglaterra", "equipo_id": equipos_obj["Manchester United"].id, "goles": 0, "asistencias": 0},
            {"nombre": "Marcus Rashford", "edad": 26, "posicion": "Delantero", "nacionalidad": "Inglaterra", "equipo_id": equipos_obj["Manchester United"].id, "goles": 0, "asistencias": 0},

            # Juventus
            {"nombre": "Paulo Dybala", "edad": 30, "posicion": "Delantero", "nacionalidad": "Argentina", "equipo_id": equipos_obj["Juventus"].id, "goles": 1, "asistencias": 0},
            {"nombre": "Gonzalo Higuain", "edad": 36, "posicion": "Delantero", "nacionalidad": "Argentina", "equipo_id": equipos_obj["Juventus"].id, "goles": 5, "asistencias": 0},
            {"nombre": "Miralem Pjanic", "edad": 34, "posicion": "Centrocampista", "nacionalidad": "Bosnia y Herzegovina", "equipo_id": equipos_obj["Juventus"].id, "goles": 1, "asistencias": 0},
            {"nombre": "Giorgio Chiellini", "edad": 39, "posicion": "Defensa", "nacionalidad": "Italia", "equipo_id": equipos_obj["Juventus"].id, "goles": 0, "asistencias": 0},
            {"nombre": "Gianluigi Buffon", "edad": 46, "posicion": "Portero", "nacionalidad": "Italia", "equipo_id": equipos_obj["Juventus"].id, "goles": 0, "asistencias": 0},
            {"nombre": "Douglas Costa", "edad": 33, "posicion": "Delantero", "nacionalidad": "Brasil", "equipo_id": equipos_obj["Juventus"].id, "goles": 0, "asistencias": 3},

            # Bayern Munich
            {"nombre": "Robert Lewandowski", "edad": 35, "posicion": "Delantero", "nacionalidad": "Polonia", "equipo_id": equipos_obj["Bayern Munich"].id, "goles": 5, "asistencias": 2},
            {"nombre": "Thomas Müller", "edad": 34, "posicion": "Delantero", "nacionalidad": "Alemania", "equipo_id": equipos_obj["Bayern Munich"].id, "goles": 3, "asistencias": 1},
            {"nombre": "Arjen Robben", "edad": 41, "posicion": "Centrocampista", "nacionalidad": "Países Bajos", "equipo_id": equipos_obj["Bayern Munich"].id, "goles": 2, "asistencias": 0},
            {"nombre": "Manuel Neuer", "edad": 38, "posicion": "Portero", "nacionalidad": "Alemania", "equipo_id": equipos_obj["Bayern Munich"].id, "goles": 0, "asistencias": 0},
            {"nombre": "Joshua Kimmich", "edad": 29, "posicion": "Defensa", "nacionalidad": "Alemania", "equipo_id": equipos_obj["Bayern Munich"].id, "goles": 1, "asistencias": 1},
            {"nombre": "Mats Hummels", "edad": 35, "posicion": "Defensa", "nacionalidad": "Alemania", "equipo_id": equipos_obj["Bayern Munich"].id, "goles": 0, "asistencias": 0},

            # Paris Saint-Germain
            {"nombre": "Neymar Jr.", "edad": 32, "posicion": "Delantero", "nacionalidad": "Brasil", "equipo_id": equipos_obj["Paris Saint-Germain"].id, "goles": 6, "asistencias": 3},
            {"nombre": "Kylian Mbappé", "edad": 25, "posicion": "Delantero", "nacionalidad": "Francia", "equipo_id": equipos_obj["Paris Saint-Germain"].id, "goles": 4, "asistencias": 3},
            {"nombre": "Edinson Cavani", "edad": 37, "posicion": "Delantero", "nacionalidad": "Uruguay", "equipo_id": equipos_obj["Paris Saint-Germain"].id, "goles": 7, "asistencias": 0},
            {"nombre": "Dani Alves", "edad": 41, "posicion": "Defensa", "nacionalidad": "Brasil", "equipo_id": equipos_obj["Paris Saint-Germain"].id, "goles": 1, "asistencias": 2},
            {"nombre": "Marco Verratti", "edad": 31, "posicion": "Centrocampista", "nacionalidad": "Italia", "equipo_id": equipos_obj["Paris Saint-Germain"].id, "goles": 0, "asistencias": 1},

            # Liverpool FC
            {"nombre": "Mohamed Salah", "edad": 32, "posicion": "Delantero", "nacionalidad": "Egipto", "equipo_id": equipos_obj["Liverpool FC"].id, "goles": 10, "asistencias": 5},
            {"nombre": "Roberto Firmino", "edad": 32, "posicion": "Delantero", "nacionalidad": "Brasil", "equipo_id": equipos_obj["Liverpool FC"].id, "goles": 10, "asistencias": 7},
            {"nombre": "Sadio Mane", "edad": 32, "posicion": "Delantero", "nacionalidad": "Senegal", "equipo_id": equipos_obj["Liverpool FC"].id, "goles": 10, "asistencias": 1},
            {"nombre": "Virgil van Dijk", "edad": 32, "posicion": "Defensa", "nacionalidad": "Países Bajos", "equipo_id": equipos_obj["Liverpool FC"].id, "goles": 1, "asistencias": 0},
            {"nombre": "Jordan Henderson", "edad": 34, "posicion": "Centrocampista", "nacionalidad": "Inglaterra", "equipo_id": equipos_obj["Liverpool FC"].id, "goles": 0, "asistencias": 0},
            {"nombre": "Trent Alexander-Arnold", "edad": 25, "posicion": "Defensa", "nacionalidad": "Inglaterra", "equipo_id": equipos_obj["Liverpool FC"].id, "goles": 0, "asistencias": 1},

            # Chelsea FC
            {"nombre": "Eden Hazard", "edad": 33, "posicion": "Delantero", "nacionalidad": "Bélgica", "equipo_id": equipos_obj["Chelsea FC"].id, "goles": 3, "asistencias": 3},
            {"nombre": "N'Golo Kante", "edad": 33, "posicion": "Centrocampista", "nacionalidad": "Francia", "equipo_id": equipos_obj["Chelsea FC"].id, "goles": 0, "asistencias": 1},
            {"nombre": "Alvaro Morata", "edad": 31, "posicion": "Delantero", "nacionalidad": "España", "equipo_id": equipos_obj["Chelsea FC"].id, "goles": 1, "asistencias": 0},
            {"nombre": "Thibaut Courtois", "edad": 32, "posicion": "Portero", "nacionalidad": "Bélgica", "equipo_id": equipos_obj["Chelsea FC"].id, "goles": 0, "asistencias": 0},

            # Tottenham Hotspur
            {"nombre": "Harry Kane", "edad": 30, "posicion": "Delantero", "nacionalidad": "Inglaterra", "equipo_id": equipos_obj["Tottenham Hotspur"].id, "goles": 7, "asistencias": 1},
            {"nombre": "Dele Alli", "edad": 28, "posicion": "Centrocampista", "nacionalidad": "Inglaterra", "equipo_id": equipos_obj["Tottenham Hotspur"].id, "goles": 2, "asistencias": 4},
            {"nombre": "Christian Eriksen", "edad": 32, "posicion": "Centrocampista", "nacionalidad": "Dinamarca", "equipo_id": equipos_obj["Tottenham Hotspur"].id, "goles": 2, "asistencias": 2},
            {"nombre": "Son Heung-min", "edad": 31, "posicion": "Delantero", "nacionalidad": "Corea del Sur", "equipo_id": equipos_obj["Tottenham Hotspur"].id, "goles": 4, "asistencias": 1},

            # Manchester City
            {"nombre": "Kevin De Bruyne", "edad": 33, "posicion": "Centrocampista", "nacionalidad": "Bélgica", "equipo_id": equipos_obj["Manchester City"].id, "goles": 1, "asistencias": 4},
            {"nombre": "Sergio Agüero", "edad": 36, "posicion": "Delantero", "nacionalidad": "Argentina", "equipo_id": equipos_obj["Manchester City"].id, "goles": 4, "asistencias": 1},
            {"nombre": "Raheem Sterling", "edad": 29, "posicion": "Delantero", "nacionalidad": "Inglaterra", "equipo_id": equipos_obj["Manchester City"].id, "goles": 4, "asistencias": 0},
            {"nombre": "Gabriel Jesus", "edad": 27, "posicion": "Delantero", "nacionalidad": "Brasil", "equipo_id": equipos_obj["Manchester City"].id, "goles": 4, "asistencias": 0},
            {"nombre": "Leroy Sané", "edad": 28, "posicion": "Delantero", "nacionalidad": "Alemania", "equipo_id": equipos_obj["Manchester City"].id, "goles": 0, "asistencias": 4},

            # AS Roma
            {"nombre": "Edin Džeko", "edad": 38, "posicion": "Delantero", "nacionalidad": "Bosnia y Herzegovina", "equipo_id": equipos_obj["AS Roma"].id, "goles": 8, "asistencias": 0},
            {"nombre": "Alisson Becker", "edad": 31, "posicion": "Portero", "nacionalidad": "Brasil", "equipo_id": equipos_obj["AS Roma"].id, "goles": 0, "asistencias": 0},
            {"nombre": "Radja Nainggolan", "edad": 36, "posicion": "Centrocampista", "nacionalidad": "Bélgica", "equipo_id": equipos_obj["AS Roma"].id, "goles": 2, "asistencias": 0},
            {"nombre": "Kostas Manolas", "edad": 33, "posicion": "Defensa", "nacionalidad": "Grecia", "equipo_id": equipos_obj["AS Roma"].id, "goles": 1, "asistencias": 0},

            # Sevilla FC
            {"nombre": "Éver Banega", "edad": 35, "posicion": "Centrocampista", "nacionalidad": "Argentina", "equipo_id": equipos_obj["Sevilla FC"].id, "goles": 0, "asistencias": 2},
            {"nombre": "Wissam Ben Yedder", "edad": 33, "posicion": "Delantero", "nacionalidad": "Francia", "equipo_id": equipos_obj["Sevilla FC"].id, "goles": 6, "asistencias": 0},
            {"nombre": "Steven N'Zonzi", "edad": 35, "posicion": "Centrocampista", "nacionalidad": "Francia", "equipo_id": equipos_obj["Sevilla FC"].id, "goles": 1, "asistencias": 0},

            # Borussia Dortmund
            {"nombre": "Marco Reus", "edad": 35, "posicion": "Delantero", "nacionalidad": "Alemania", "equipo_id": equipos_obj["Borussia Dortmund"].id, "goles": 1, "asistencias": 0},
            {"nombre": "Pierre-Emerick Aubameyang", "edad": 35, "posicion": "Delantero", "nacionalidad": "Gabón", "equipo_id": equipos_obj["Borussia Dortmund"].id, "goles": 4, "asistencias": 0},
            {"nombre": "Julian Weigl", "edad": 28, "posicion": "Centrocampista", "nacionalidad": "Alemania", "equipo_id": equipos_obj["Borussia Dortmund"].id, "goles": 0, "asistencias": 0},

            # FC Porto
            {"nombre": "Vincent Aboubakar", "edad": 32, "posicion": "Delantero", "nacionalidad": "Camerún", "equipo_id": equipos_obj["FC Porto"].id, "goles": 5, "asistencias": 0},
            {"nombre": "Yacine Brahimi", "edad": 34, "posicion": "Centrocampista", "nacionalidad": "Argelia", "equipo_id": equipos_obj["FC Porto"].id, "goles": 1, "asistencias": 1},
            {"nombre": "Hector Herrera", "edad": 34, "posicion": "Centrocampista", "nacionalidad": "México", "equipo_id": equipos_obj["FC Porto"].id, "goles": 0, "asistencias": 0},

            # Shakhtar Donetsk
            {"nombre": "Taison", "edad": 36, "posicion": "Centrocampista", "nacionalidad": "Brasil", "equipo_id": equipos_obj["Shakhtar Donetsk"].id, "goles": 1, "asistencias": 1},
            {"nombre": "Fred", "edad": 31, "posicion": "Centrocampista", "nacionalidad": "Brasil", "equipo_id": equipos_obj["Shakhtar Donetsk"].id, "goles": 3, "asistencias": 0},
            {"nombre": "Bernard", "edad": 31, "posicion": "Delantero", "nacionalidad": "Brasil", "equipo_id": equipos_obj["Shakhtar Donetsk"].id, "goles": 0, "asistencias": 0},

            # Besiktas JK
            {"nombre": "Ricardo Quaresma", "edad": 40, "posicion": "Delantero", "nacionalidad": "Portugal", "equipo_id": equipos_obj["Besiktas JK"].id, "goles": 4, "asistencias": 0},
            {"nombre": "Cenk Tosun", "edad": 33, "posicion": "Delantero", "nacionalidad": "Turquía", "equipo_id": equipos_obj["Besiktas JK"].id, "goles": 4, "asistencias": 0},
            {"nombre": "Anderson Talisca", "edad": 30, "posicion": "Centrocampista", "nacionalidad": "Brasil", "equipo_id": equipos_obj["Besiktas JK"].id, "goles": 4, "asistencias": 0},

            # RB Leipzig
            {"nombre": "Timo Werner", "edad": 28, "posicion": "Delantero", "nacionalidad": "Alemania", "equipo_id": equipos_obj["RB Leipzig"].id, "goles": 3, "asistencias": 0},
            {"nombre": "Emil Forsberg", "edad": 32, "posicion": "Centrocampista", "nacionalidad": "Suecia", "equipo_id": equipos_obj["RB Leipzig"].id, "goles": 0, "asistencias": 1},
            {"nombre": "Naby Keïta", "edad": 29, "posicion": "Centrocampista", "nacionalidad": "Guinea", "equipo_id": equipos_obj["RB Leipzig"].id, "goles": 0, "asistencias": 0},

            # SSC Napoli
            {"nombre": "Dries Mertens", "edad": 37, "posicion": "Delantero", "nacionalidad": "Bélgica", "equipo_id": equipos_obj["SSC Napoli"].id, "goles": 3, "asistencias": 0},
            {"nombre": "Lorenzo Insigne", "edad": 33, "posicion": "Delantero", "nacionalidad": "Italia", "equipo_id": equipos_obj["SSC Napoli"].id, "goles": 0, "asistencias": 1},
            {"nombre": "Marek Hamšík", "edad": 36, "posicion": "Centrocampista", "nacionalidad": "Eslovaquia", "equipo_id": equipos_obj["SSC Napoli"].id, "goles": 0, "asistencias": 0},

            # AS Monaco
            {"nombre": "Radamel Falcao", "edad": 38, "posicion": "Delantero", "nacionalidad": "Colombia", "equipo_id": equipos_obj["AS Monaco"].id, "goles": 3, "asistencias": 0},
            {"nombre": "Fabinho", "edad": 30, "posicion": "Centrocampista", "nacionalidad": "Brasil", "equipo_id": equipos_obj["AS Monaco"].id, "goles": 0, "asistencias": 0},

            # Sporting CP
            {"nombre": "Bas Dost", "edad": 35, "posicion": "Delantero", "nacionalidad": "Países Bajos", "equipo_id": equipos_obj["Sporting CP"].id, "goles": 0, "asistencias": 0},
            {"nombre": "Bruno Fernandes", "edad": 29, "posicion": "Centrocampista", "nacionalidad": "Portugal", "equipo_id": equipos_obj["Sporting CP"].id, "goles": 0, "asistencias": 0},

            # CSKA Moscow
            {"nombre": "Alan Dzagoev", "edad": 33, "posicion": "Centrocampista", "nacionalidad": "Rusia", "equipo_id": equipos_obj["CSKA Moscow"].id, "goles": 1, "asistencias": 0},
            {"nombre": "Igor Akinfeev", "edad": 38, "posicion": "Portero", "nacionalidad": "Rusia", "equipo_id": equipos_obj["CSKA Moscow"].id, "goles": 0, "asistencias": 0},

            # Atlético Madrid
            {"nombre": "Antoine Griezmann", "edad": 33, "posicion": "Delantero", "nacionalidad": "Francia", "equipo_id": equipos_obj["Atlético Madrid"].id, "goles": 2, "asistencias": 0},
            {"nombre": "Jan Oblak", "edad": 31, "posicion": "Portero", "nacionalidad": "Eslovenia", "equipo_id": equipos_obj["Atlético Madrid"].id, "goles": 0, "asistencias": 0},
            {"nombre": "Koke", "edad": 32, "posicion": "Centrocampista", "nacionalidad": "España", "equipo_id": equipos_obj["Atlético Madrid"].id, "goles": 0, "asistencias": 0},

            # FC Basel
            {"nombre": "Dimitri Oberlin", "edad": 26, "posicion": "Delantero", "nacionalidad": "Suiza", "equipo_id": equipos_obj["FC Basel"].id, "goles": 4, "asistencias": 0},
            {"nombre": "Michael Lang", "edad": 33, "posicion": "Defensa", "nacionalidad": "Suiza", "equipo_id": equipos_obj["FC Basel"].id, "goles": 0, "asistencias": 0},

            # Celtic FC
            {"nombre": "Moussa Dembélé", "edad": 27, "posicion": "Delantero", "nacionalidad": "Francia", "equipo_id": equipos_obj["Celtic FC"].id, "goles": 0, "asistencias": 0},
            {"nombre": "Scott Sinclair", "edad": 35, "posicion": "Delantero", "nacionalidad": "Inglaterra", "equipo_id": equipos_obj["Celtic FC"].id, "goles": 0, "asistencias": 0},

            # Feyenoord
            {"nombre": "Nicolai Jørgensen", "edad": 33, "posicion": "Delantero", "nacionalidad": "Dinamarca", "equipo_id": equipos_obj["Feyenoord"].id, "goles": 0, "asistencias": 0},

            # Spartak Moscow
            {"nombre": "Quincy Promes", "edad": 32, "posicion": "Delantero", "nacionalidad": "Países Bajos", "equipo_id": equipos_obj["Spartak Moscow"].id, "goles": 0, "asistencias": 0},

            # APOEL FC
            {"nombre": "Igor de Camargo", "edad": 41, "posicion": "Delantero", "nacionalidad": "Bélgica", "equipo_id": equipos_obj["APOEL FC"].id, "goles": 0, "asistencias": 0},

            # Qarabag FK
            {"nombre": "Dino Ndlovu", "edad": 34, "posicion": "Delantero", "nacionalidad": "Sudáfrica", "equipo_id": equipos_obj["Qarabag FK"].id, "goles": 0, "asistencias": 0},

            # Maribor
            {"nombre": "Marcos Tavares", "edad": 40, "posicion": "Delantero", "nacionalidad": "Brasil", "equipo_id": equipos_obj["Maribor"].id, "goles": 0, "asistencias": 0},

            # RSC Anderlecht
            {"nombre": "Lukasz Teodorczyk", "edad": 33, "posicion": "Delantero", "nacionalidad": "Polonia", "equipo_id": equipos_obj["RSC Anderlecht"].id, "goles": 0, "asistencias": 0},
        ]

        for data in jugadores_data:
            jugador = Jugador(**data)
            db.add(jugador)
        db.commit()
        print("Jugadores insertados.")

        # --- Datos de Partidos (Champions League 2017/18) ---
        # Algunos partidos representativos de la Fase de Grupos, Octavos, Cuartos, Semifinal y Final
        partidos_data = [
            # Fase de Grupos (Ejemplos)
            {"equipo_local_id": equipos_obj["Real Madrid"].id, "equipo_visitante_id": equipos_obj["APOEL FC"].id, "goles_local": 3, "goles_visitante": 0, "fecha": date(2017, 9, 13), "fase": "Fase de Grupos"},
            {"equipo_local_id": equipos_obj["FC Barcelona"].id, "equipo_visitante_id": equipos_obj["Juventus"].id, "goles_local": 3, "goles_visitante": 0, "fecha": date(2017, 9, 12), "fase": "Fase de Grupos"},
            {"equipo_local_id": equipos_obj["Manchester United"].id, "equipo_visitante_id": equipos_obj["FC Basel"].id, "goles_local": 3, "goles_visitante": 0, "fecha": date(2017, 9, 12), "fase": "Fase de Grupos"},
            {"equipo_local_id": equipos_obj["Bayern Munich"].id, "equipo_visitante_id": equipos_obj["RSC Anderlecht"].id, "goles_local": 3, "goles_visitante": 0, "fecha": date(2017, 9, 12), "fase": "Fase de Grupos"},
            {"equipo_local_id": equipos_obj["Paris Saint-Germain"].id, "equipo_visitante_id": equipos_obj["Celtic FC"].id, "goles_local": 5, "goles_visitante": 0, "fecha": date(2017, 9, 12), "fase": "Fase de Grupos"},
            {"equipo_local_id": equipos_obj["Liverpool FC"].id, "equipo_visitante_id": equipos_obj["Sevilla FC"].id, "goles_local": 2, "goles_visitante": 2, "fecha": date(2017, 9, 13), "fase": "Fase de Grupos"},
            {"equipo_local_id": equipos_obj["Chelsea FC"].id, "equipo_visitante_id": equipos_obj["Qarabag FK"].id, "goles_local": 6, "goles_visitante": 0, "fecha": date(2017, 9, 12), "fase": "Fase de Grupos"},
            {"equipo_local_id": equipos_obj["Tottenham Hotspur"].id, "equipo_visitante_id": equipos_obj["Borussia Dortmund"].id, "goles_local": 3, "goles_visitante": 1, "fecha": date(2017, 9, 13), "fase": "Fase de Grupos"},
            {"equipo_local_id": equipos_obj["Manchester City"].id, "equipo_visitante_id": equipos_obj["Feyenoord"].id, "goles_local": 4, "goles_visitante": 0, "fecha": date(2017, 9, 13), "fase": "Fase de Grupos"},
            {"equipo_local_id": equipos_obj["AS Roma"].id, "equipo_visitante_id": equipos_obj["Atlético Madrid"].id, "goles_local": 0, "goles_visitante": 0, "fecha": date(2017, 9, 12), "fase": "Fase de Grupos"},
            {"equipo_local_id": equipos_obj["FC Porto"].id, "equipo_visitante_id": equipos_obj["Besiktas JK"].id, "goles_local": 1, "goles_visitante": 3, "fecha": date(2017, 9, 13), "fase": "Fase de Grupos"},
            {"equipo_local_id": equipos_obj["Shakhtar Donetsk"].id, "equipo_visitante_id": equipos_obj["SSC Napoli"].id, "goles_local": 2, "goles_visitante": 1, "fecha": date(2017, 9, 13), "fase": "Fase de Grupos"},
            {"equipo_local_id": equipos_obj["RB Leipzig"].id, "equipo_visitante_id": equipos_obj["AS Monaco"].id, "goles_local": 1, "goles_visitante": 1, "fecha": date(2017, 9, 13), "fase": "Fase de Grupos"},
            {"equipo_local_id": equipos_obj["Sporting CP"].id, "equipo_visitante_id": equipos_obj["Olympiacos FC"].id, "goles_local": 3, "goles_visitante": 2, "fecha": date(2017, 9, 12), "fase": "Fase de Grupos"},
            {"equipo_local_id": equipos_obj["CSKA Moscow"].id, "equipo_visitante_id": equipos_obj["Benfica"].id, "goles_local": 2, "goles_visitante": 1, "fecha": date(2017, 9, 12), "fase": "Fase de Grupos"},
            {"equipo_local_id": equipos_obj["Maribor"].id, "equipo_visitante_id": equipos_obj["Spartak Moscow"].id, "goles_local": 1, "goles_visitante": 1, "fecha": date(2017, 9, 13), "fase": "Fase de Grupos"},

            # Octavos de Final (Ida)
            {"equipo_local_id": equipos_obj["Juventus"].id, "equipo_visitante_id": equipos_obj["Tottenham Hotspur"].id, "goles_local": 2, "goles_visitante": 2, "fecha": date(2018, 2, 13), "fase": "Octavos de Final"},
            {"equipo_local_id": equipos_obj["FC Basel"].id, "equipo_visitante_id": equipos_obj["Manchester City"].id, "goles_local": 0, "goles_visitante": 4, "fecha": date(2018, 2, 13), "fase": "Octavos de Final"},
            {"equipo_local_id": equipos_obj["FC Porto"].id, "equipo_visitante_id": equipos_obj["Liverpool FC"].id, "goles_local": 0, "goles_visitante": 5, "fecha": date(2018, 2, 14), "fase": "Octavos de Final"},
            {"equipo_local_id": equipos_obj["Real Madrid"].id, "equipo_visitante_id": equipos_obj["Paris Saint-Germain"].id, "goles_local": 3, "goles_visitante": 1, "fecha": date(2018, 2, 14), "fase": "Octavos de Final"},
            {"equipo_local_id": equipos_obj["Chelsea FC"].id, "equipo_visitante_id": equipos_obj["FC Barcelona"].id, "goles_local": 1, "goles_visitante": 1, "fecha": date(2018, 2, 20), "fase": "Octavos de Final"},
            {"equipo_local_id": equipos_obj["Bayern Munich"].id, "equipo_visitante_id": equipos_obj["Besiktas JK"].id, "goles_local": 5, "goles_visitante": 0, "fecha": date(2018, 2, 20), "fase": "Octavos de Final"},
            {"equipo_local_id": equipos_obj["Sevilla FC"].id, "equipo_visitante_id": equipos_obj["Manchester United"].id, "goles_local": 0, "goles_visitante": 0, "fecha": date(2018, 2, 21), "fase": "Octavos de Final"},
            {"equipo_local_id": equipos_obj["Shakhtar Donetsk"].id, "equipo_visitante_id": equipos_obj["AS Roma"].id, "goles_local": 2, "goles_visitante": 1, "fecha": date(2018, 2, 21), "fase": "Octavos de Final"},

            # Octavos de Final (Vuelta)
            {"equipo_local_id": equipos_obj["Tottenham Hotspur"].id, "equipo_visitante_id": equipos_obj["Juventus"].id, "goles_local": 1, "goles_visitante": 2, "fecha": date(2018, 3, 7), "fase": "Octavos de Final"},
            {"equipo_local_id": equipos_obj["Manchester City"].id, "equipo_visitante_id": equipos_obj["FC Basel"].id, "goles_local": 1, "goles_visitante": 2, "fecha": date(2018, 3, 7), "fase": "Octavos de Final"},
            {"equipo_local_id": equipos_obj["Paris Saint-Germain"].id, "equipo_visitante_id": equipos_obj["Real Madrid"].id, "goles_local": 1, "goles_visitante": 2, "fecha": date(2018, 3, 6), "fase": "Octavos de Final"},
            {"equipo_local_id": equipos_obj["Liverpool FC"].id, "equipo_visitante_id": equipos_obj["FC Porto"].id, "goles_local": 0, "goles_visitante": 0, "fecha": date(2018, 3, 6), "fase": "Octavos de Final"},
            {"equipo_local_id": equipos_obj["FC Barcelona"].id, "equipo_visitante_id": equipos_obj["Chelsea FC"].id, "goles_local": 3, "goles_visitante": 0, "fecha": date(2018, 3, 14), "fase": "Octavos de Final"},
            {"equipo_local_id": equipos_obj["Besiktas JK"].id, "equipo_visitante_id": equipos_obj["Bayern Munich"].id, "goles_local": 1, "goles_visitante": 3, "fecha": date(2018, 3, 14), "fase": "Octavos de Final"},
            {"equipo_local_id": equipos_obj["Manchester United"].id, "equipo_visitante_id": equipos_obj["Sevilla FC"].id, "goles_local": 1, "goles_visitante": 2, "fecha": date(2018, 3, 13), "fase": "Octavos de Final"},
            {"equipo_local_id": equipos_obj["AS Roma"].id, "equipo_visitante_id": equipos_obj["Shakhtar Donetsk"].id, "goles_local": 1, "goles_visitante": 0, "fecha": date(2018, 3, 13), "fase": "Octavos de Final"},

            # Cuartos de Final (Ida)
            {"equipo_local_id": equipos_obj["Juventus"].id, "equipo_visitante_id": equipos_obj["Real Madrid"].id, "goles_local": 0, "goles_visitante": 3, "fecha": date(2018, 4, 3), "fase": "Cuartos de Final"},
            {"equipo_local_id": equipos_obj["Sevilla FC"].id, "equipo_visitante_id": equipos_obj["Bayern Munich"].id, "goles_local": 1, "goles_visitante": 2, "fecha": date(2018, 4, 3), "fase": "Cuartos de Final"},
            {"equipo_local_id": equipos_obj["Liverpool FC"].id, "equipo_visitante_id": equipos_obj["Manchester City"].id, "goles_local": 3, "goles_visitante": 0, "fecha": date(2018, 4, 4), "fase": "Cuartos de Final"},
            {"equipo_local_id": equipos_obj["FC Barcelona"].id, "equipo_visitante_id": equipos_obj["AS Roma"].id, "goles_local": 4, "goles_visitante": 1, "fecha": date(2018, 4, 4), "fase": "Cuartos de Final"},

            # Cuartos de Final (Vuelta)
            {"equipo_local_id": equipos_obj["Real Madrid"].id, "equipo_visitante_id": equipos_obj["Juventus"].id, "goles_local": 1, "goles_visitante": 3, "fecha": date(2018, 4, 11), "fase": "Cuartos de Final"}, # Real Madrid avanza 4-3 global
            {"equipo_local_id": equipos_obj["Bayern Munich"].id, "equipo_visitante_id": equipos_obj["Sevilla FC"].id, "goles_local": 0, "goles_visitante": 0, "fecha": date(2018, 4, 11), "fase": "Cuartos de Final"}, # Bayern avanza 2-1 global
            {"equipo_local_id": equipos_obj["Manchester City"].id, "equipo_visitante_id": equipos_obj["Liverpool FC"].id, "goles_local": 1, "goles_visitante": 2, "fecha": date(2018, 4, 10), "fase": "Cuartos de Final"}, # Liverpool avanza 5-1 global
            {"equipo_local_id": equipos_obj["AS Roma"].id, "equipo_visitante_id": equipos_obj["FC Barcelona"].id, "goles_local": 3, "goles_visitante": 0, "fecha": date(2018, 4, 10), "fase": "Cuartos de Final"}, # Roma avanza 4-4 por goles de visitante

            # Semifinal (Ida)
            {"equipo_local_id": equipos_obj["Bayern Munich"].id, "equipo_visitante_id": equipos_obj["Real Madrid"].id, "goles_local": 1, "goles_visitante": 2, "fecha": date(2018, 4, 25), "fase": "Semifinal"},
            {"equipo_local_id": equipos_obj["Liverpool FC"].id, "equipo_visitante_id": equipos_obj["AS Roma"].id, "goles_local": 5, "goles_visitante": 2, "fecha": date(2018, 4, 24), "fase": "Semifinal"},

            # Semifinal (Vuelta)
            {"equipo_local_id": equipos_obj["Real Madrid"].id, "equipo_visitante_id": equipos_obj["Bayern Munich"].id, "goles_local": 2, "goles_visitante": 2, "fecha": date(2018, 5, 1), "fase": "Semifinal"}, # Real Madrid avanza 4-3 global
            {"equipo_local_id": equipos_obj["AS Roma"].id, "equipo_visitante_id": equipos_obj["Liverpool FC"].id, "goles_local": 4, "goles_visitante": 2, "fecha": date(2018, 5, 2), "fase": "Semifinal"}, # Liverpool avanza 7-6 global

            # Final
            {"equipo_local_id": equipos_obj["Real Madrid"].id, "equipo_visitante_id": equipos_obj["Liverpool FC"].id, "goles_local": 3, "goles_visitante": 1, "fecha": date(2018, 5, 26), "fase": "Final"}
        ]

        for data in partidos_data:
            partido = Partido(**data)
            db.add(partido)
        db.commit()
        print("Partidos insertados.")

        print("Base de datos poblada exitosamente.")

    except Exception as e:
        db.rollback()
        print(f"Error al poblar la base de datos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    populate_database()
