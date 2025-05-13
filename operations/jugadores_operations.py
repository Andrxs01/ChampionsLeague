from sqlalchemy.orm import Session
from data.models import Jugador, JugadorCreate, JugadorUpdate

# Crear jugador
def crear_jugador(db: Session, jugador: JugadorCreate):
    db_jugador = Jugador(**jugador.dict())
    db.add(db_jugador)
    db.commit()
    db.refresh(db_jugador)
    return db_jugador

# Obtener todos los jugadores no eliminados lógicamente
def obtener_jugadores(db: Session, nombre=None, equipo=None, nacionalidad=None, posicion=None, eliminado=None):
    query = db.query(Jugador).filter(Jugador.eliminado_logico == False)

    if nombre:
        query = query.filter(Jugador.nombre.ilike(f"%{nombre}%"))
    if equipo:
        query = query.filter(Jugador.equipo.ilike(f"%{equipo}%"))
    if nacionalidad:
        query = query.filter(Jugador.nacionalidad.ilike(f"%{nacionalidad}%"))
    if posicion:
        query = query.filter(Jugador.posicion.ilike(f"%{posicion}%"))
    if eliminado is not None:
        query = query.filter(Jugador.eliminado == eliminado)

    return query.all()

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

# Eliminación lógica de jugador
def eliminar_jugador(db: Session, jugador_id: int):
    db_jugador = db.query(Jugador).filter(Jugador.id == jugador_id).first()
    if not db_jugador:
        return None
    db_jugador.eliminado_logico = True
    db.commit()
    return db_jugador

# Búsqueda avanzada de jugadores
def buscar_jugadores(db: Session, nombre: str = None, equipo: str = None, posicion: str = None, nacionalidad: str = None, eliminado: bool = None):
    query = db.query(Jugador).filter(Jugador.eliminado_logico == False)
    if nombre:
        query = query.filter(Jugador.nombre.ilike(f"%{nombre}%"))
    if equipo:
        query = query.filter(Jugador.equipo.ilike(f"%{equipo}%"))
    if posicion:
        query = query.filter(Jugador.posicion.ilike(f"%{posicion}%"))
    if nacionalidad:
        query = query.filter(Jugador.nacionalidad.ilike(f"%{nacionalidad}%"))
    if eliminado is not None:
        query = query.filter(Jugador.eliminado == eliminado)

    return query.all()