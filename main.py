# main.py
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models import Base # Importar Base para la creación de tablas
from data.models import (
    JugadorCreate, JugadorUpdate,
    EquipoCreate, EquipoUpdate,
    Jugador, Equipo # Importa los modelos Jugador y Equipo directamente
)
from operations import jugadores_operations, equipos_operations
from routes import html_pages # Asegúrate de que html_pages esté importado
import uvicorn

# Cargar variables de entorno del archivo .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está configurada en el archivo .env o en el entorno.")

# Configuración de la base de datos
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear todas las tablas si no existen.
# Esto es útil para el desarrollo local.
# En Render, esto se manejará con el comando de build 'python populate_db.py'.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Champions League 2017/18 Data API",
    description="Una API para gestionar datos de equipos, jugadores y partidos de la UEFA Champions League 2017/18.",
    version="1.0.0",
)

# Montar el directorio estático para servir CSS, JS, imágenes, etc.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir los routers de las páginas HTML
app.include_router(html_pages.router)

# Redirección de la raíz a la página de inicio
@app.get("/", response_class=HTMLResponse, tags=["Inicio"])
async def root(request: Request):
    # Redirigimos a la ruta de la página de inicio en html_pages.py
    return RedirectResponse(url="/home", status_code=302)


# ---------------- JUGADORES (Endpoints API JSON) ----------------
# Estos endpoints son para la API RESTful (JSON).

@app.post("/api/jugadores", response_model=Jugador, tags=["API Jugadores"])
async def crear_jugador_api(
    jugador: JugadorCreate,
    db: Session = Depends(get_db)
):
    try:
        return jugadores_operations.create_jugador(db, jugador)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear jugador: {e}")


@app.get("/api/jugadores", response_model=list[Jugador], tags=["API Jugadores"])
def obtener_jugadores_api(db: Session = Depends(get_db)):
    jugadores = jugadores_operations.get_all_jugadores(db)
    if not jugadores:
        raise HTTPException(status_code=404, detail="No hay jugadores registrados")
    return jugadores

@app.get("/api/jugadores/buscar", response_model=list[Jugador], tags=["API Jugadores"])
def buscar_jugadores_api(
    nombre: str = Query(None),
    equipo_id: int = Query(None),
    nacionalidad: str = Query(None),
    posicion: str = Query(None),
    eliminado: bool = Query(False), # Por defecto, busca no eliminados
    db: Session = Depends(get_db)
):
    resultados = jugadores_operations.search_jugadores(
        db=db,
        nombre=nombre,
        equipo_id=equipo_id,
        nacionalidad=nacionalidad,
        posicion=posicion,
        eliminado=eliminado
    )
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron jugadores que coincidan con los filtros")
    return resultados


@app.get("/api/jugadores/{jugador_id}", response_model=Jugador, tags=["API Jugadores"])
def obtener_jugador_api(jugador_id: int, db: Session = Depends(get_db)):
    jugador = jugadores_operations.get_jugador_by_id(db, jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador

@app.put("/api/jugadores/{jugador_id}", response_model=Jugador, tags=["API Jugadores"])
async def actualizar_jugador_api(
    jugador_id: int,
    jugador: JugadorUpdate,
    db: Session = Depends(get_db)
):
    actualizado = jugadores_operations.update_jugador(db, jugador_id, jugador)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return actualizado

@app.delete("/api/jugadores/{jugador_id}", tags=["API Jugadores"])
def eliminar_jugador_api(jugador_id: int, db: Session = Depends(get_db)):
    eliminado = jugadores_operations.soft_delete_jugador(db, jugador_id) # Usamos soft_delete
    if not eliminado:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return {"mensaje": "Jugador eliminado lógicamente"}

# ---------------- EQUIPOS (Endpoints API JSON) ----------------

@app.post("/api/equipos", response_model=Equipo, tags=["API Equipos"])
def crear_equipo_api(equipo: EquipoCreate, db: Session = Depends(get_db)):
    try:
        return equipos_operations.create_equipo(db, equipo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear equipo: {e}")

@app.get("/api/equipos", response_model=list[Equipo], tags=["API Equipos"])
def obtener_equipos_api(db: Session = Depends(get_db)):
    equipos = equipos_operations.get_all_equipos(db)
    if not equipos:
        raise HTTPException(status_code=404, detail="No hay equipos registrados")
    return equipos

@app.get("/api/equipos/buscar", response_model=list[Equipo], tags=["API Equipos"])
def buscar_equipos_api(
    nombre: str = Query(None),
    grupo: str = Query(None),
    pais: str = Query(None),
    eliminado: bool = Query(False), # Por defecto, busca no eliminados
    db: Session = Depends(get_db)
):
    resultados = equipos_operations.search_equipos(
        db=db,
        nombre=nombre,
        grupo=grupo,
        pais=pais,
        eliminado=eliminado
    )
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron equipos que coincidan con los filtros")
    return resultados

@app.get("/api/equipos/{equipo_id}", response_model=Equipo, tags=["API Equipos"])
def obtener_equipo_api(equipo_id: int, db: Session = Depends(get_db)):
    equipo = equipos_operations.get_equipo_by_id(db, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return equipo

@app.put("/api/equipos/{equipo_id}", response_model=Equipo, tags=["API Equipos"])
def actualizar_equipo_api(equipo_id: int, equipo: EquipoUpdate, db: Session = Depends(get_db)):
    actualizado = equipos_operations.update_equipo(db, equipo_id, equipo)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return actualizado

@app.delete("/api/equipos/{equipo_id}", tags=["API Equipos"])
def eliminar_equipo_api(equipo_id: int, db: Session = Depends(get_db)):
    eliminado = equipos_operations.soft_delete_equipo(db, equipo_id) # Usamos soft_delete
    if not eliminado:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return {"mensaje": "Equipo eliminado lógicamente"}

# Si ejecutas directamente este archivo
if __name__ == "__main__":
    # Para ejecutar con uvicorn directamente desde el script
    # Esto es útil para el desarrollo local
    uvicorn.run(app, host="0.0.0.0", port=8001)
