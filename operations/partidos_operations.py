# operations/partidos_operations.py
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_ # ¡Correcto! Ya estaba importado, lo mantenemos.
from sqlalchemy.exc import IntegrityError, OperationalError
from data import models
from data.models import PartidoCreate, PartidoUpdate
from datetime import date
from typing import Optional

# --- Operaciones CRUD para Partidos ---

def create_partido(db: Session, partido: PartidoCreate):
    """
    Programa un nuevo encuentro en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.
        partido (PartidoCreate): Los datos del partido a programar.

    Returns:
        models.Partido: El partido recién creado.

    Raises:
        ValueError: Si los equipos local y visitante son el mismo, o si un ID de equipo no existe.
        IntegrityError: Si hay un problema de integridad de datos (ej. IDs de equipos no válidos).
        Exception: Para otros errores inesperados durante la creación.
    """
    try:
        if partido.equipo_local_id == partido.equipo_visitante_id:
            raise ValueError("¡Atención! Un equipo no puede jugar contra sí mismo. Revisa los IDs.")

        # Verificar si los equipos existen
        local_team = db.query(models.Equipo).filter(models.Equipo.id == partido.equipo_local_id).first()
        visitor_team = db.query(models.Equipo).filter(models.Equipo.id == partido.equipo_visitante_id).first()

        if not local_team:
            raise ValueError(f"¡Error! El equipo local con ID {partido.equipo_local_id} no se encontró en el registro.")
        if not visitor_team:
            raise ValueError(f"¡Error! El equipo visitante con ID {partido.equipo_visitante_id} no se encontró en el registro.")

        db_partido = models.Partido(
            equipo_local_id=partido.equipo_local_id,
            equipo_visitante_id=partido.equipo_visitante_id,
            goles_local=partido.goles_local,
            goles_visitante=partido.goles_visitante,
            fecha=partido.fecha,
            fase=partido.fase
        )
        db.add(db_partido)
        db.commit()
        db.refresh(db_partido)
        return db_partido
    except ValueError as e:
        db.rollback()
        print(f"Error al programar el partido: {e}")
        raise
    except IntegrityError as e:
        db.rollback()
        print(f"¡Error de integridad al programar el partido! Detalles: {e}")
        raise ValueError("No se pudo programar el partido. Asegúrate de que los IDs de los equipos sean válidos.")
    except Exception as e:
        db.rollback()
        print(f"¡Oops! Un error inesperado ocurrió al crear el partido: {e}")
        raise

def get_all_partidos(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtiene todos los partidos activos (no eliminados lógicamente), ordenados por fecha.

    Args:
        db (Session): La sesión de la base de datos.
        skip (int): Número de registros a omitir.
        limit (int): Número máximo de registros a devolver.

    Returns:
        List[models.Partido]: Una lista de partidos.

    Raises:
        OperationalError: Si hay un problema de conexión con la base de datos.
        Exception: Para otros errores inesperados.
    """
    try:
        return db.query(models.Partido).options(
            joinedload(models.Partido.equipo_local_obj),
            joinedload(models.Partido.equipo_visitante_obj)
        ).filter(
            models.Partido.eliminado_logico == False
        ).order_by(models.Partido.fecha.asc()).offset(skip).limit(limit).all()
    except OperationalError as e:
        print(f"¡Problema de conexión con la base de datos al obtener partidos! Detalles: {e}")
        raise ConnectionError("No se pudo conectar a la base de datos.")
    except Exception as e:
        print(f"¡Error desconocido al obtener todos los partidos! Detalles: {e}")
        raise

def get_partido_by_id(db: Session, partido_id: int):
    """
    Obtiene un partido específico por su ID.

    Args:
        db (Session): La sesión de la base de datos.
        partido_id (int): El ID del partido.

    Returns:
        Optional[models.Partido]: El partido encontrado o None si no existe.

    Raises:
        OperationalError: Si hay un problema de conexión con la base de datos.
        Exception: Para otros errores inesperados.
    """
    try:
        return db.query(models.Partido).options(
            joinedload(models.Partido.equipo_local_obj),
            joinedload(models.Partido.equipo_visitante_obj)
        ).filter(
            models.Partido.id == partido_id
        ).first()
    except OperationalError as e:
        print(f"¡Problema de conexión con la base de datos al buscar partido por ID! Detalles: {e}")
        raise ConnectionError("No se pudo conectar a la base de datos.")
    except Exception as e:
        print(f"¡Error desconocido al buscar partido por ID {partido_id}! Detalles: {e}")
        raise

def update_partido(db: Session, partido_id: int, partido: PartidoUpdate):
    """
    Actualiza los datos de un partido existente.

    Args:
        db (Session): La sesión de la base de datos.
        partido_id (int): El ID del partido a actualizar.
        partido (PartidoUpdate): Los nuevos datos para el partido.

    Returns:
        Optional[models.Partido]: El partido actualizado o None si no se encontró.

    Raises:
        ValueError: Si los equipos local y visitante son el mismo en la actualización,
                    o si un ID de equipo no existe.
        IntegrityError: Si la actualización causa un problema de integridad de datos.
        Exception: Para otros errores inesperados.
    """
    try:
        db_partido = db.query(models.Partido).filter(models.Partido.id == partido_id).first()
        if db_partido:
            update_data = partido.model_dump(exclude_unset=True)

            # Validar que los IDs de los equipos existan y no sean el mismo
            local_id_new = update_data.get('equipo_local_id', db_partido.equipo_local_id)
            visitor_id_new = update_data.get('equipo_visitante_id', db_partido.equipo_visitante_id)

            if local_id_new == visitor_id_new:
                raise ValueError("¡Error de partido! Los equipos local y visitante no pueden ser el mismo.")

            if 'equipo_local_id' in update_data and update_data['equipo_local_id'] is not None:
                if not db.query(models.Equipo).filter(models.Equipo.id == update_data['equipo_local_id']).first():
                    raise ValueError(f"¡Error! El nuevo equipo local con ID {update_data['equipo_local_id']} no existe.")
            if 'equipo_visitante_id' in update_data and update_data['equipo_visitante_id'] is not None:
                if not db.query(models.Equipo).filter(models.Equipo.id == update_data['equipo_visitante_id']).first():
                    raise ValueError(f"¡Error! El nuevo equipo visitante con ID {update_data['equipo_visitante_id']} no existe.")

            for key, value in update_data.items():
                setattr(db_partido, key, value)
            db.commit()
            db.refresh(db_partido)
        return db_partido
    except ValueError as e:
        db.rollback()
        print(f"Error al actualizar el partido: {e}")
        raise
    except IntegrityError as e:
        db.rollback()
        print(f"¡Error de integridad al actualizar el partido! Detalles: {e}")
        raise ValueError("No se pudo actualizar el partido debido a datos inválidos o duplicados.")
    except Exception as e:
        db.rollback()
        print(f"¡Oops! Un error inesperado ocurrió al actualizar el partido con ID {partido_id}: {e}")
        raise

def soft_delete_partido(db: Session, partido_id: int):
    """
    Realiza una eliminación lógica de un partido (lo marca como eliminado).

    Args:
        db (Session): La sesión de la base de datos.
        partido_id (int): El ID del partido a eliminar lógicamente.

    Returns:
        Optional[models.Partido]: El partido marcado como eliminado o None si no se encontró.

    Raises:
        OperationalError: Si hay un problema de conexión con la base de datos.
        Exception: Para otros errores inesperados.
    """
    try:
        db_partido = db.query(models.Partido).filter(models.Partido.id == partido_id).first()
        if db_partido:
            db_partido.eliminado_logico = True
            db.commit()
            db.refresh(db_partido)
        return db_partido
    except OperationalError as e:
        db.rollback()
        print(f"¡Problema de conexión con la base de datos al eliminar partido {partido_id}! Detalles: {e}")
        raise ConnectionError("No se pudo conectar a la base de datos para anular el partido.")
    except Exception as e:
        db.rollback()
        print(f"¡Error desconocido al intentar eliminar lógicamente el partido con ID {partido_id}! Detalles: {e}")
        raise

def search_partidos(
    db: Session,
    equipo_nombre: Optional[str] = None,
    fase: Optional[str] = None,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    id_partido: Optional[int] = None, # Renombrado para mayor claridad
    eliminado: bool = False
):
    """
    Busca partidos por varios criterios, incluyendo el nombre de los equipos involucrados.

    Args:
        db (Session): La sesión de la base de datos.
        equipo_nombre (Optional[str]): Nombre parcial de un equipo (local o visitante).
        fase (Optional[str]): Fase del torneo (ej. "Grupos", "Semifinales").
        fecha_inicio (Optional[date]): Fecha de inicio del rango de búsqueda.
        fecha_fin (Optional[date]): Fecha de fin del rango de búsqueda.
        id_partido (Optional[int]): ID exacto del partido.
        eliminado (bool): Si se deben incluir partidos eliminados lógicamente.

    Returns:
        List[models.Partido]: Una lista de partidos que coinciden con los criterios.

    Raises:
        OperationalError: Si hay un problema de conexión con la base de datos.
        Exception: Para otros errores inesperados.
    """
    try:
        query = db.query(models.Partido).options(
            joinedload(models.Partido.equipo_local_obj),
            joinedload(models.Partido.equipo_visitante_obj)
        ).filter(models.Partido.eliminado_logico == eliminado)

        if equipo_nombre:
            # Usamos or_ para buscar en el nombre del equipo local O el nombre del equipo visitante
            query = query.filter(
                or_(
                    models.Partido.equipo_local_obj.has(models.Equipo.nombre.ilike(f"%{equipo_nombre}%")),
                    models.Partido.equipo_visitante_obj.has(models.Equipo.nombre.ilike(f"%{equipo_nombre}%"))
                )
            )
        if fase:
            query = query.filter(models.Partido.fase.ilike(f"%{fase}%"))
        if fecha_inicio:
            query = query.filter(models.Partido.fecha >= fecha_inicio)
        if fecha_fin:
            query = query.filter(models.Partido.fecha <= fecha_fin)
        if id_partido:
            query = query.filter(models.Partido.id == id_partido)

        return query.all()
    except OperationalError as e:
        print(f"¡Problema de conexión con la base de datos al buscar partidos! Detalles: {e}")
        raise ConnectionError("No se pudo conectar a la base de datos para la búsqueda de partidos.")
    except Exception as e:
        print(f"¡Error desconocido al buscar partidos! Detalles: {e}")
        raise

# --- Función para obtener partidos eliminados lógicamente ---

def get_soft_deleted_partidos(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtiene los partidos que han sido eliminados lógicamente.

    Args:
        db (Session): La sesión de la base de datos.
        skip (int): Número de registros a omitir.
        limit (int): Número máximo de registros a devolver.

    Returns:
        List[models.Partido]: Una lista de partidos eliminados lógicamente.

    Raises:
        OperationalError: Si hay un problema de conexión con la base de datos.
        Exception: Para otros errores inesperados.
    """
    try:
        return db.query(models.Partido).options(
            joinedload(models.Partido.equipo_local_obj),
            joinedload(models.Partido.equipo_visitante_obj)
        ).filter(
            models.Partido.eliminado_logico == True
        ).offset(skip).limit(limit).all()
    except OperationalError as e:
        print(f"¡Problema de conexión con la base de datos al obtener partidos anulados! Detalles: {e}")
        raise ConnectionError("No se pudo conectar a la base de datos para obtener partidos anulados.")
    except Exception as e:
        print(f"¡Error desconocido al obtener partidos eliminados lógicamente! Detalles: {e}")
        raise