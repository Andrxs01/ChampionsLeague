from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.db import SessionLocal, engine, Base
from data.models import (
    JugadorCreate, JugadorUpdate, JugadorWithId,
    EquipoCreate, EquipoUpdate, EquipoWithId,
    Jugador, Equipo
)
from operations import jugadores_operations, equipos_operations

# Crear las tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Champions League 17/18 API")

# Dependencia para obtener DB session por solicitud
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- JUGADOR ----------------

@app.post("/jugadores", response_model=JugadorWithId)
def crear_jugador(jugador: JugadorCreate, db: Session = Depends(get_db)):
    return jugadores_operations.crear_jugador(db, jugador)

@app.get("/jugadores", response_model=list[JugadorWithId])
def obtener_jugadores(db: Session = Depends(get_db)):
    jugadores = jugadores_operations.obtener_jugadores(db)
    if not jugadores:
        raise HTTPException(status_code=404, detail="No hay jugadores registrados")
    return jugadores

@app.get("/jugadores/{jugador_id}", response_model=JugadorWithId)
def obtener_jugador(jugador_id: int, db: Session = Depends(get_db)):
    jugador = jugadores_operations.obtener_jugador_por_id(db, jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador

@app.put("/jugadores/{jugador_id}", response_model=JugadorWithId)
def actualizar_jugador(jugador_id: int, jugador: JugadorUpdate, db: Session = Depends(get_db)):
    actualizado = jugadores_operations.actualizar_jugador(db, jugador_id, jugador)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return actualizado

@app.delete("/jugadores/{jugador_id}")
def eliminar_jugador(jugador_id: int, db: Session = Depends(get_db)):
    eliminado = jugadores_operations.eliminar_jugador(db, jugador_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return {"mensaje": "Jugador eliminado lógicamente"}

# ---------------- EQUIPO ----------------

@app.post("/equipos", response_model=EquipoWithId)
def crear_equipo(equipo: EquipoCreate, db: Session = Depends(get_db)):
    return equipos_operations.crear_equipo(db, equipo)

@app.get("/equipos", response_model=list[EquipoWithId])
def obtener_equipos(db: Session = Depends(get_db)):
    equipos = equipos_operations.obtener_equipos(db)
    if not equipos:
        raise HTTPException(status_code=404, detail="No hay equipos registrados")
    return equipos

@app.get("/equipos/{equipo_id}", response_model=EquipoWithId)
def obtener_equipo(equipo_id: int, db: Session = Depends(get_db)):
    equipo = equipos_operations.obtener_equipo_por_id(db, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return equipo

@app.put("/equipos/{equipo_id}", response_model=EquipoWithId)
def actualizar_equipo(equipo_id: int, equipo: EquipoUpdate, db: Session = Depends(get_db)):
    actualizado = equipos_operations.actualizar_equipo(db, equipo_id, equipo)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return actualizado

@app.delete("/equipos/{equipo_id}")
def eliminar_equipo(equipo_id: int, db: Session = Depends(get_db)):
    eliminado = equipos_operations.eliminar_equipo(db, equipo_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return {"mensaje": "Equipo eliminado lógicamente"}
