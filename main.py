from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from utils.db import SessionLocal, engine, Base
from data.models import (
    JugadorCreate, JugadorUpdate, JugadorWithId,
    EquipoCreate, EquipoUpdate, EquipoWithId,
    Jugador, Equipo
)
from operations import jugadores_operations, equipos_operations

Base.metadata.create_all(bind=engine)

app = FastAPI(

    title="Champions League 17/18 API",
    description="Bienvenido a la API de consulta y gestión de jugadores y equipos de la Champions League 2017/18.",
    version="1.0"
)
@app.get("/", tags=["Inicio"])
def root():
    return {
        "Bienvenido a la API de la Champions League 2017/18 "
    }


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- JUGADORES ----------------

@app.post("/jugadores", response_model=JugadorWithId, tags=["Jugadores"])
def crear_jugador(jugador: JugadorCreate, db: Session = Depends(get_db)):
    existente = db.query(Jugador).filter(
        Jugador.nombre == jugador.nombre,
        Jugador.equipo == jugador.equipo,
        Jugador.eliminado_logico == False
    ).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe un jugador con ese nombre en el mismo equipo")
    return jugadores_operations.crear_jugador(db, jugador)

@app.get("/jugadores", response_model=list[JugadorWithId], tags=["Jugadores"])
def obtener_jugadores(db: Session = Depends(get_db)):
    jugadores = jugadores_operations.obtener_jugadores(db)
    if not jugadores:
        raise HTTPException(status_code=404, detail="No hay jugadores registrados")
    return jugadores

@app.get("/jugadores/buscar", response_model=list[JugadorWithId], tags=["Jugadores"])
def buscar_jugadores(
    nombre: str = Query(None),
    equipo: str = Query(None),
    nacionalidad: str = Query(None),
    posicion: str = Query(None),
    eliminado: bool = Query(None),
    db: Session = Depends(get_db)
):
    resultados = jugadores_operations.buscar_jugadores(
        db=db,
        nombre=nombre,
        equipo=equipo,
        nacionalidad=nacionalidad,
        posicion=posicion,
        eliminado=eliminado
    )
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron jugadores que coincidan con los filtros")
    return resultados

@app.get("/jugadores/{jugador_id}", response_model=JugadorWithId, tags=["Jugadores"])
def obtener_jugador(jugador_id: int, db: Session = Depends(get_db)):
    jugador = jugadores_operations.obtener_jugador_por_id(db, jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador

@app.put("/jugadores/{jugador_id}", response_model=JugadorWithId, tags=["Jugadores"])
def actualizar_jugador(jugador_id: int, jugador: JugadorUpdate, db: Session = Depends(get_db)):
    actualizado = jugadores_operations.actualizar_jugador(db, jugador_id, jugador)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return actualizado

@app.delete("/jugadores/{jugador_id}", tags=["Jugadores"])
def eliminar_jugador(jugador_id: int, db: Session = Depends(get_db)):
    eliminado = jugadores_operations.eliminar_jugador(db, jugador_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return {"mensaje": "Jugador eliminado lógicamente"}

# ---------------- EQUIPOS ----------------

@app.post("/equipos", response_model=EquipoWithId, tags=["Equipos"])
def crear_equipo(equipo: EquipoCreate, db: Session = Depends(get_db)):
    existente = db.query(Equipo).filter(
        Equipo.nombre == equipo.nombre,
        Equipo.pais == equipo.pais,
        Equipo.eliminado_logico == False
    ).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe un equipo con ese nombre y país")
    return equipos_operations.crear_equipo(db, equipo)

@app.get("/equipos", response_model=list[EquipoWithId], tags=["Equipos"])
def obtener_equipos(db: Session = Depends(get_db)):
    equipos = equipos_operations.obtener_equipos(db)
    if not equipos:
        raise HTTPException(status_code=404, detail="No hay equipos registrados")
    return equipos

@app.get("/equipos/buscar", response_model=list[EquipoWithId], tags=["Equipos"])
def buscar_equipos(
    nombre: str = Query(None),
    grupo: str = Query(None),
    pais: str = Query(None),
    eliminado: bool = Query(None),
    db: Session = Depends(get_db)
):
    resultados = equipos_operations.buscar_equipos(
        db=db,
        nombre=nombre,
        grupo=grupo,
        pais=pais,
        eliminado=eliminado
    )
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron equipos que coincidan con los filtros")
    return resultados

@app.get("/equipos/{equipo_id}", response_model=EquipoWithId, tags=["Equipos"])
def obtener_equipo(equipo_id: int, db: Session = Depends(get_db)):
    equipo = equipos_operations.obtener_equipo_por_id(db, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return equipo

@app.put("/equipos/{equipo_id}", response_model=EquipoWithId, tags=["Equipos"])
def actualizar_equipo(equipo_id: int, equipo: EquipoUpdate, db: Session = Depends(get_db)):
    actualizado = equipos_operations.actualizar_equipo(db, equipo_id, equipo)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return actualizado

@app.delete("/equipos/{equipo_id}", tags=["Equipos"])
def eliminar_equipo(equipo_id: int, db: Session = Depends(get_db)):
    eliminado = equipos_operations.eliminar_equipo(db, equipo_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return {"mensaje": "Equipo eliminado "}
