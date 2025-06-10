# operations/jugadores_operations.py
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_ # ¡Importante! Añadido para el operador OR en filtros
from sqlalchemy.exc import IntegrityError, OperationalError
from data import models
from data.models import JugadorCreate, JugadorUpdate
from typing import Optional

# --- Operaciones CRUD para Jugadores ---

def create_jugador(db: Session, jugador: JugadorCreate):
    """
    Crea un nuevo jugador en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.
        jugador (JugadorCreate): Los datos del jugador a crear.

    Returns:
        models.Jugador: El jugador recién creado.

    Raises:
        IntegrityError: Si hay un problema de integridad de datos (ej. equipo_id no existe).
        ValueError: Si el equipo_id no corresponde a un equipo existente.
        Exception: Para otros errores inesperados durante la creación.
    """
    try:
        # Verificar si el equipo_id existe antes de crear el jugador
        equipo_existente = db.query(models.Equipo).filter(models.Equipo.id == jugador.equipo_id).first()
        if not equipo_existente:
            raise ValueError(f"¡Atención! El equipo con ID {jugador.equipo_id} no existe. No se puede crear el jugador.")

        db_jugador = models.Jugador(
            nombre=jugador.nombre,
            equipo_id=jugador.equipo_id,
            posicion=jugador.posicion,
            edad=jugador.edad,
            nacionalidad=jugador.nacionalidad,
            goles=jugador.goles,
            asistencias=jugador.asistencias,
        )
        db.add(db_jugador)
        db.commit()
        db.refresh(db_jugador)
        return db_jugador
    except ValueError as e:
        db.rollback()
        print(f"Error al crear jugador: {e}")
        raise
    except IntegrityError as e:
        db.rollback()
        print(f"¡Error de integridad al fichar al jugador! Detalles: {e}")
        raise ValueError("No se pudo fichar al jugador. Asegúrate de que el equipo_id sea válido.")
    except Exception as e:
        db.rollback()
        print(f"¡Oops! Un error inesperado ocurrió al crear el jugador: {e}")
        raise

def get_all_jugadores(db: Session, skip: int = 0, limit: Optional[int] = None):
    """
    Obtiene todos los jugadores activos (no eliminados lógicamente).

    Args:
        db (Session): La sesión de la base de datos.
        skip (int): Número de registros a omitir.
        limit (Optional[int]): Número máximo de registros a devolver.

    Returns:
        List[models.Jugador]: Una lista de jugadores.

    Raises:
        OperationalError: Si hay un problema de conexión con la base de datos.
        Exception: Para otros errores inesperados.
    """
    try:
        query = db.query(models.Jugador).options(joinedload(models.Jugador.equipo_obj)).filter(
            models.Jugador.eliminado_logico == False
        ).offset(skip)

        if limit is not None:
            query = query.limit(limit)

        return query.all()
    except OperationalError as e:
        print(f"¡Problema de conexión con la base de datos al obtener jugadores! Detalles: {e}")
        raise ConnectionError("No se pudo conectar a la base de datos.")
    except Exception as e:
        print(f"¡Error desconocido al obtener todos los jugadores! Detalles: {e}")
        raise

def get_jugador_by_id(db: Session, jugador_id: int):
    """
    Obtiene un jugador por su ID.

    Args:
        db (Session): La sesión de la base de datos.
        jugador_id (int): El ID del jugador.

    Returns:
        Optional[models.Jugador]: El jugador encontrado o None si no existe.

    Raises:
        OperationalError: Si hay un problema de conexión con la base de datos.
        Exception: Para otros errores inesperados.
    """
    try:
        return db.query(models.Jugador).options(joinedload(models.Jugador.equipo_obj)).filter(
            models.Jugador.id == jugador_id
        ).first()
    except OperationalError as e:
        print(f"¡Problema de conexión con la base de datos al buscar jugador por ID! Detalles: {e}")
        raise ConnectionError("No se pudo conectar a la base de datos.")
    except Exception as e:
        print(f"¡Error desconocido al buscar jugador por ID {jugador_id}! Detalles: {e}")
        raise

def update_jugador(db: Session, jugador_id: int, jugador: JugadorUpdate):
    """
    Actualiza los datos de un jugador existente.

    Args:
        db (Session): La sesión de la base de datos.
        jugador_id (int): El ID del jugador a actualizar.
        jugador (JugadorUpdate): Los nuevos datos para el jugador.

    Returns:
        Optional[models.Jugador]: El jugador actualizado o None si no se encontró.

    Raises:
        ValueError: Si el equipo_id proporcionado no existe.
        IntegrityError: Si la actualización causa un problema de integridad de datos.
        Exception: Para otros errores inesperados.
    """
    try:
        db_jugador = db.query(models.Jugador).filter(models.Jugador.id == jugador_id).first()
        if db_jugador:
            update_data = jugador.model_dump(exclude_unset=True)
            if 'equipo_id' in update_data and update_data['equipo_id'] is not None:
                equipo_existente = db.query(models.Equipo).filter(models.Equipo.id == update_data['equipo_id']).first()
                if not equipo_existente:
                    raise ValueError(f"¡Atención! El equipo con ID {update_data['equipo_id']} no existe. No se puede actualizar el jugador.")

            for key, value in update_data.items():
                setattr(db_jugador, key, value)
            db.commit()
            db.refresh(db_jugador)
        return db_jugador
    except ValueError as e:
        db.rollback()
        print(f"Error al actualizar jugador: {e}")
        raise
    except IntegrityError as e:
        db.rollback()
        print(f"¡Error de integridad al actualizar al jugador! Detalles: {e}")
        raise ValueError("No se pudo actualizar el jugador debido a datos inválidos o duplicados.")
    except Exception as e:
        db.rollback()
        print(f"¡Oops! Un error inesperado ocurrió al actualizar el jugador con ID {jugador_id}: {e}")
        raise

def soft_delete_jugador(db: Session, jugador_id: int):
    """
    Realiza una eliminación lógica de un jugador (lo marca como eliminado).

    Args:
        db (Session): La sesión de la base de datos.
        jugador_id (int): El ID del jugador a eliminar lógicamente.

    Returns:
        Optional[models.Jugador]: El jugador marcado como eliminado o None si no se encontró.

    Raises:
        OperationalError: Si hay un problema de conexión con la base de datos.
        Exception: Para otros errores inesperados.
    """
    try:
        db_jugador = db.query(models.Jugador).filter(models.Jugador.id == jugador_id).first()
        if db_jugador:
            db_jugador.eliminado_logico = True
            db.commit()
            db.refresh(db_jugador)
        return db_jugador
    except OperationalError as e:
        db.rollback()
        print(f"¡Problema de conexión con la base de datos al eliminar jugador {jugador_id}! Detalles: {e}")
        raise ConnectionError("No se pudo conectar a la base de datos para eliminar al jugador.")
    except Exception as e:
        db.rollback()
        print(f"¡Error desconocido al intentar eliminar lógicamente al jugador con ID {jugador_id}! Detalles: {e}")
        raise

def search_jugadores(
    db: Session,
    query_str: Optional[str] = None, # Renombrado para evitar conflicto con 'query' de SQLAlchemy
    equipo_id: Optional[int] = None,
    posicion: Optional[str] = None,
    nacionalidad: Optional[str] = None,
    id_jugador: Optional[int] = None, # Renombrado para mayor claridad
    eliminado: bool = False
):
    """
    Busca jugadores por varios criterios, incluyendo el nombre del jugador o el nombre de su equipo.
    Ideal para búsquedas generales como "Real Madrid" que deberían mostrar jugadores del Real Madrid.

    Args:
        db (Session): La sesión de la base de datos.
        query_str (Optional[str]): Cadena de búsqueda general (nombre de jugador o nombre de equipo).
        equipo_id (Optional[int]): ID exacto del equipo.
        posicion (Optional[str]): Posición del jugador.
        nacionalidad (Optional[str]): Nacionalidad del jugador.
        id_jugador (Optional[int]): ID exacto del jugador.
        eliminado (bool): Si se deben incluir jugadores eliminados lógicamente.

    Returns:
        List[models.Jugador]: Una lista de jugadores que coinciden con los criterios.

    Raises:
        OperationalError: Si hay un problema de conexión con la base de datos.
        Exception: Para otros errores inesperados.
    """
    try:
        base_query = db.query(models.Jugador).options(joinedload(models.Jugador.equipo_obj)).filter(
            models.Jugador.eliminado_logico == eliminado
        )

        filters = []

        if query_str:
            # Si se proporciona una cadena de búsqueda,
            # busca en el nombre del jugador O en el nombre del equipo asociado
            filters.append(
                or_(
                    models.Jugador.nombre.ilike(f"%{query_str}%"),
                    models.Jugador.equipo_obj.has(models.Equipo.nombre.ilike(f"%{query_str}%"))
                )
            )
        if equipo_id:
            filters.append(models.Jugador.equipo_id == equipo_id)
        if posicion:
            filters.append(models.Jugador.posicion.ilike(f"%{posicion}%"))
        if nacionalidad:
            filters.append(models.Jugador.nacionalidad.ilike(f"%{nacionalidad}%"))
        if id_jugador:
            filters.append(models.Jugador.id == id_jugador)

        # Aplica todos los filtros
        if filters:
            base_query = base_query.filter(*filters)

        return base_query.all()
    except OperationalError as e:
        print(f"¡Problema de conexión con la base de datos al buscar jugadores! Detalles: {e}")
        raise ConnectionError("No se pudo conectar a la base de datos para la búsqueda de jugadores.")
    except Exception as e:
        print(f"¡Error desconocido al buscar jugadores! Detalles: {e}")
        raise

# --- Funciones para Estadísticas de Jugadores ---

def get_top_scorers(db: Session, limit: int = 10):
    """
    Obtiene a los máximos goleadores activos.

    Args:
        db (Session): La sesión de la base de datos.
        limit (int): El número máximo de jugadores a devolver.

    Returns:
        List[models.Jugador]: Una lista de los jugadores con más goles.

    Raises:
        OperationalError: Si hay un problema de conexión con la base de datos.
        Exception: Para otros errores inesperados.
    """
    try:
        return db.query(models.Jugador).options(joinedload(models.Jugador.equipo_obj)).filter(
            models.Jugador.eliminado_logico == False
        ).order_by(models.Jugador.goles.desc()).limit(limit).all()
    except OperationalError as e:
        print(f"¡Problema de conexión con la base de datos al obtener máximos goleadores! Detalles: {e}")
        raise ConnectionError("No se pudo conectar a la base de datos para obtener estadísticas de goleadores.")
    except Exception as e:
        print(f"¡Error desconocido al obtener los máximos goleadores! Detalles: {e}")
        raise

def get_top_assisters(db: Session, limit: int = 10):
    """
    Obtiene a los máximos asistentes activos.

    Args:
        db (Session): La sesión de la base de datos.
        limit (int): El número máximo de jugadores a devolver.

    Returns:
        List[models.Jugador]: Una lista de los jugadores con más asistencias.

    Raises:
        OperationalError: Si hay un problema de conexión con la base de datos.
        Exception: Para otros errores inesperados.
    """
    try:
        return db.query(models.Jugador).options(joinedload(models.Jugador.equipo_obj)).filter(
            models.Jugador.eliminado_logico == False
        ).order_by(models.Jugador.asistencias.desc()).limit(limit).all()
    except OperationalError as e:
        print(f"¡Problema de conexión con la base de datos al obtener máximos asistentes! Detalles: {e}")
        raise ConnectionError("No se pudo conectar a la base de datos para obtener estadísticas de asistentes.")
    except Exception as e:
        print(f"¡Error desconocido al obtener los máximos asistentes! Detalles: {e}")
        raise

def get_soft_deleted_jugadores(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtiene todos los jugadores que han sido eliminados lógicamente.

    Args:
        db (Session): La sesión de la base de datos.
        skip (int): Número de registros a omitir.
        limit (int): Número máximo de registros a devolver.

    Returns:
        List[models.Jugador]: Una lista de jugadores eliminados lógicamente.

    Raises:
        OperationalError: Si hay un problema de conexión con la base de datos.
        Exception: Para otros errores inesperados.
    """
    try:
        return db.query(models.Jugador).options(joinedload(models.Jugador.equipo_obj)).filter(
            models.Jugador.eliminado_logico == True
        ).offset(skip).limit(limit).all()
    except OperationalError as e:
        print(f"¡Problema de conexión con la base de datos al obtener jugadores eliminados! Detalles: {e}")
        raise ConnectionError("No se pudo conectar a la base de datos para obtener jugadores eliminados.")
    except Exception as e:
        print(f"¡Error desconocido al obtener jugadores eliminados lógicamente! Detalles: {e}")
        raise