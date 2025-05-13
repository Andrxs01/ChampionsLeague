from sqlalchemy.orm import Session
from data.models import Equipo, EquipoCreate, EquipoUpdate

# Crear equipo
def crear_equipo(db: Session, equipo: EquipoCreate):
    db_equipo = Equipo(**equipo.dict())
    db.add(db_equipo)
    db.commit()
    db.refresh(db_equipo)
    return db_equipo

# Obtener todos los equipos no eliminados lógicamente
def obtener_equipos(db: Session, nombre=None, pais=None, grupo=None, eliminado=None):
    query = db.query(Equipo).filter(Equipo.eliminado_logico == False)

    if nombre:
        query = query.filter(Equipo.nombre.ilike(f"%{nombre}%"))
    if pais:
        query = query.filter(Equipo.pais.ilike(f"%{pais}%"))
    if grupo:
        query = query.filter(Equipo.grupo.ilike(f"%{grupo}%"))
    if eliminado is not None:
        query = query.filter(Equipo.eliminado == eliminado)

    return query.all()

# Obtener equipo por ID
def obtener_equipo_por_id(db: Session, equipo_id: int):
    return db.query(Equipo).filter(Equipo.id == equipo_id, Equipo.eliminado_logico == False).first()

# Actualizar equipo
def actualizar_equipo(db: Session, equipo_id: int, equipo: EquipoUpdate):
    db_equipo = db.query(Equipo).filter(Equipo.id == equipo_id, Equipo.eliminado_logico == False).first()
    if not db_equipo:
        return None
    for key, value in equipo.dict().items():
        setattr(db_equipo, key, value)
    db.commit()
    db.refresh(db_equipo)
    return db_equipo

# Eliminación lógica de equipo
def eliminar_equipo(db: Session, equipo_id: int):
    db_equipo = db.query(Equipo).filter(Equipo.id == equipo_id).first()
    if not db_equipo:
        return None
    db_equipo.eliminado_logico = True
    db.commit()
    return db_equipo

# Búsqueda avanzada de equipos
def buscar_equipos(db: Session, nombre: str = None, grupo: str = None, pais: str = None, eliminado: bool = None):
    query = db.query(Equipo).filter(Equipo.eliminado_logico == False)
    if nombre:
        query = query.filter(Equipo.nombre.ilike(f"%{nombre}%"))
    if grupo:
        query = query.filter(Equipo.grupo.ilike(f"%{grupo}%"))
    if pais:
        query = query.filter(Equipo.pais.ilike(f"%{pais}%"))
    if eliminado is not None:
        query = query.filter(Equipo.eliminado == eliminado)

    return query.all()
