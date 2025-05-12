# operations/jugador_operations.py
from sqlalchemy.orm import Session
from models import Jugador, JugadorCreate, JugadorUpdate, Equipo, EquipoCreate, EquipoUpdate
# Crear equipo
def crear_equipo(db: Session, equipo: EquipoCreate):
    db_equipo = Equipo(**equipo.dict())
    db.add(db_equipo)
    db.commit()
    db.refresh(db_equipo)
    return db_equipo

# Obtener todos los equipos
def obtener_equipos(db: Session):
    return db.query(Equipo).all()

# Obtener equipo por ID
def obtener_equipo_por_id(db: Session, equipo_id: int):
    return db.query(Equipo).filter(Equipo.id == equipo_id).first()

# Actualizar equipo
def actualizar_equipo(db: Session, equipo_id: int, equipo: EquipoUpdate):
    db_equipo = db.query(Equipo).filter(Equipo.id == equipo_id).first()
    if not db_equipo:
        return None
    for key, value in equipo.dict().items():
        setattr(db_equipo, key, value)
    db.commit()
    db.refresh(db_equipo)
    return db_equipo

# Eliminar equipo (opcionalmente eliminación lógica)
def eliminar_equipo(db: Session, equipo_id: int):
    db_equipo = db.query(Equipo).filter(Equipo.id == equipo_id).first()
    if not db_equipo:
        return None
    db.delete(db_equipo)
    db.commit()
    return db_equipo

# Crear jugador
def crear_jugador(db: Session, jugador: JugadorCreate):
    db_jugador = Jugador(**jugador.dict())
    db.add(db_jugador)
    db.commit()
    db.refresh(db_jugador)
    return db_jugador

# Obtener todos los jugadores no eliminados lógicamente
def obtener_jugadores(db: Session):
    return db.query(Jugador).filter(Jugador.eliminado_logico == False).all()

# Obtener jugador por ID
def obtener_jugador_por_id(db: Session, jugador_id: int):
    return db.query(Jugador).filter(Jugador.id == jugador_id, Jugador.eliminado_logico == False).first()

# Actualizar jugador
def actualizar_jugador(db: Session, jugador_id: int, jugador: JugadorUpdate):
    db_jugador = db.query(Jugador).filter(Jugador.id == jugador_id, Jugador.eliminado_logico == False).first()
    if not db_jugador:
        return None
    for key, value in jugador.dict().items():
        setattr(db_jugador, key, value)
    db.commit()
    db.refresh(db_jugador)
    return db_jugador

# Eliminación lógica
def eliminar_jugador(db: Session, jugador_id: int):
    db_jugador = db.query(Jugador).filter(Jugador.id == jugador_id).first()
    if not db_jugador:
        return None
    db_jugador.eliminado_logico = True
    db.commit()
    return db_jugador
