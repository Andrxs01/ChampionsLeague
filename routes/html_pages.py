# routes/html_pages.py
from fastapi import APIRouter, Request, Depends, Form, HTTPException, Query, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError, IntegrityError # Importa las excepciones de SQLAlchemy
from utils.db import get_db
from operations import jugadores_operations, equipos_operations, partidos_operations
from data import models
from data.models import JugadorCreate, JugadorUpdate, EquipoCreate, EquipoUpdate, PartidoCreate, PartidoUpdate
from datetime import date
from collections import defaultdict
from typing import Optional

router = APIRouter(
    tags=["Páginas HTML"],
)

templates = Jinja2Templates(directory="templates")

# --- Rutas de información del proyecto ---

@router.get("/home", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    """
    Muestra la página de inicio con los registros más recientes de jugadores, equipos y partidos.
    """
    try:
        jugadores_recientes = jugadores_operations.get_all_jugadores(db, limit=5)
        equipos_recientes = equipos_operations.get_all_equipos(db, limit=5)
        partidos_recientes = partidos_operations.get_all_partidos(db, limit=5)
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "jugadores": jugadores_recientes, "equipos": equipos_recientes, "partidos": partidos_recientes}
        )
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="¡Goles en contra! Problemas de conexión con la base de datos. Intenta más tarde."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"¡Fuera de juego inesperado en el inicio! {e}"
        )

@router.get("/desarrollador", response_class=HTMLResponse)
async def about_developer(request: Request):
    """Muestra información sobre el desarrollador."""
    return templates.TemplateResponse("about_developer.html", {"request": request})

@router.get("/planeacion", response_class=HTMLResponse)
async def planning_phase(request: Request):
    """Muestra la fase de planeación del proyecto."""
    return templates.TemplateResponse("planning_phase.html", {"request": request})

@router.get("/diseno", response_class=HTMLResponse)
async def design_phase(request: Request):
    """Muestra la fase de diseño del proyecto."""
    return templates.TemplateResponse("design_phase.html", {"request": request})

@router.get("/objetivo", response_class=HTMLResponse)
async def project_objective(request: Request):
    """Muestra el objetivo del proyecto."""
    return templates.TemplateResponse("project_objective.html", {"request": request})


### Rutas para Jugadores

@router.get("/jugadores_lista", response_class=HTMLResponse)
async def listar_jugadores(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Muestra la lista de todos los jugadores activos.
    """
    try:
        jugadores = jugadores_operations.get_all_jugadores(db)
        return templates.TemplateResponse(
            "jugadores/list.html",
            {"request": request, "jugadores": jugadores}
        )
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="¡Tarjeta roja! No pudimos conectar con la base de datos para listar jugadores."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"¡Error inesperado al recuperar la lista de jugadores! {e}"
        )

@router.get("/jugadores/{jugador_id}", response_class=HTMLResponse)
async def ver_jugador(request: Request, jugador_id: int, db: Session = Depends(get_db)):
    """
    Muestra los detalles de un jugador específico.
    """
    try:
        jugador = jugadores_operations.get_jugador_by_id(db, jugador_id)
        if not jugador or jugador.eliminado_logico:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="¡Jugador no encontrado o ya colgó las botas!")
        return templates.TemplateResponse(
            "jugadores/detail.html",
            {"request": request, "jugador": jugador}
        )
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="¡Problemas técnicos en el VAR! No se pudo consultar la base de datos."
        )
    except HTTPException: # Re-raise HTTPExceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"¡Error inesperado al buscar los datos del jugador! {e}"
        )

@router.get("/jugadores_crear", response_class=HTMLResponse)
async def show_create_jugador_form(request: Request, db: Session = Depends(get_db)):
    """
    Muestra el formulario para crear un nuevo jugador.
    """
    try:
        equipos = equipos_operations.get_all_equipos(db)
        return templates.TemplateResponse("jugadores/create.html", {"request": request, "equipos": equipos})
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="¡Problemas de red! No se pudieron cargar los equipos para el formulario."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"¡Error inesperado al preparar el formulario de fichajes! {e}"
        )

@router.post("/jugadores_crear", response_class=HTMLResponse)
async def create_jugador(
    request: Request,
    db: Session = Depends(get_db),
    nombre: str = Form(...),
    equipo_id: int = Form(...),
    posicion: str = Form(...),
    edad: int = Form(...),
    nacionalidad: str = Form(...),
    goles: int = Form(0),
    asistencias: int = Form(0)
):
    """
    Procesa el envío del formulario para crear un nuevo jugador.
    """
    jugador_data = JugadorCreate(
        nombre=nombre,
        equipo_id=equipo_id,
        posicion=posicion,
        edad=edad,
        nacionalidad=nacionalidad,
        goles=goles,
        asistencias=asistencias
    )
    try:
        jugador_creado = jugadores_operations.create_jugador(db, jugador_data)
        return RedirectResponse(url=f"/jugadores/{jugador_creado.id}", status_code=status.HTTP_303_SEE_OTHER)
    except ValueError as e:
        equipos = equipos_operations.get_all_equipos(db)
        return templates.TemplateResponse(
            "jugadores/create.html",
            {"request": request, "equipos": equipos, "error_message": f"¡Fichaje fallido! {e}"}
        )
    except OperationalError:
        equipos = equipos_operations.get_all_equipos(db)
        return templates.TemplateResponse(
            "jugadores/create.html",
            {"request": request, "equipos": equipos, "error_message": "¡Fallo en la conexión! No se pudo registrar al jugador."}
        )
    except Exception as e:
        equipos = equipos_operations.get_all_equipos(db)
        return templates.TemplateResponse(
            "jugadores/create.html",
            {"request": request, "equipos": equipos, "error_message": f"¡Error inesperado al fichar al jugador! {e}"}
        )

@router.get("/jugadores_editar/{jugador_id}", response_class=HTMLResponse)
async def show_edit_jugador_form(request: Request, jugador_id: int, db: Session = Depends(get_db)):
    """
    Muestra el formulario para editar un jugador existente.
    """
    try:
        jugador = jugadores_operations.get_jugador_by_id(db, jugador_id)
        if not jugador:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="¡Jugador no encontrado para editar!")
        equipos = equipos_operations.get_all_equipos(db)
        return templates.TemplateResponse(
            "jugadores/edit.html",
            {"request": request, "jugador": jugador, "equipos": equipos}
        )
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="¡Error de conexión! No se pudo cargar la información del jugador para editar."
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"¡Error inesperado al preparar la edición del jugador! {e}"
        )

@router.post("/jugadores_editar/{jugador_id}", response_class=HTMLResponse)
async def edit_jugador(
    request: Request,
    jugador_id: int,
    db: Session = Depends(get_db),
    nombre: str = Form(...),
    equipo_id: int = Form(...),
    posicion: str = Form(...),
    edad: int = Form(...),
    nacionalidad: str = Form(...),
    goles: int = Form(0),
    asistencias: int = Form(0),
    eliminado_logico: bool = Form(False)
):
    """
    Procesa el envío del formulario para actualizar un jugador.
    """
    jugador_update_data = JugadorUpdate(
        nombre=nombre,
        equipo_id=equipo_id,
        posicion=posicion,
        edad=edad,
        nacionalidad=nacionalidad,
        goles=goles,
        asistencias=asistencias,
        eliminado_logico=eliminado_logico
    )
    try:
        jugador_actualizado = jugadores_operations.update_jugador(db, jugador_id, jugador_update_data)
        if not jugador_actualizado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="¡Jugador no encontrado para actualizar!")
        return RedirectResponse(url=f"/jugadores/{jugador_actualizado.id}", status_code=status.HTTP_303_SEE_OTHER)
    except ValueError as e:
        jugador = jugadores_operations.get_jugador_by_id(db, jugador_id)
        equipos = equipos_operations.get_all_equipos(db)
        return templates.TemplateResponse(
            "jugadores/edit.html",
            {"request": request, "jugador": jugador, "equipos": equipos, "error_message": f"¡Error en la actualización! {e}"}
        )
    except OperationalError:
        jugador = jugadores_operations.get_jugador_by_id(db, jugador_id)
        equipos = equipos_operations.get_all_equipos(db)
        return templates.TemplateResponse(
            "jugadores/edit.html",
            {"request": request, "jugador": jugador, "equipos": equipos, "error_message": "¡Fallo en la conexión! No se pudo actualizar al jugador."}
        )
    except HTTPException:
        raise
    except Exception as e:
        jugador = jugadores_operations.get_jugador_by_id(db, jugador_id)
        equipos = equipos_operations.get_all_equipos(db)
        return templates.TemplateResponse(
            "jugadores/edit.html",
            {"request": request, "jugador": jugador, "equipos": equipos, "error_message": f"¡Error inesperado al actualizar al jugador! {e}"}
        )

@router.post("/jugadores_eliminar/{jugador_id}", response_class=HTMLResponse)
async def eliminar_jugador_logico(request: Request, jugador_id: int, db: Session = Depends(get_db)):
    """
    Realiza una eliminación lógica de un jugador.
    """
    try:
        jugador_eliminado = jugadores_operations.soft_delete_jugador(db, jugador_id)
        if not jugador_eliminado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="¡Jugador no encontrado para eliminación lógica!")
        return RedirectResponse(url="/jugadores_lista", status_code=status.HTTP_303_SEE_OTHER)
    except OperationalError:
        jugadores = jugadores_operations.get_all_jugadores(db)
        return templates.TemplateResponse(
            "jugadores/list.html",
            {"request": request, "jugadores": jugadores, "error_message": "¡Problemas de red! No se pudo eliminar al jugador."}
        )
    except HTTPException:
        raise
    except Exception as e:
        jugadores = jugadores_operations.get_all_jugadores(db)
        return templates.TemplateResponse("jugadores/list.html", {"request": request, "jugadores": jugadores, "error_message": f"¡Error al enviar al jugador al banquillo! {e}"})

### Rutas para Equipos

@router.get("/equipos_lista", response_class=HTMLResponse)
async def listar_equipos(request: Request, db: Session = Depends(get_db)):
    """
    Muestra la lista de todos los equipos activos.
    """
    try:
        equipos = equipos_operations.get_all_equipos(db)
        return templates.TemplateResponse(
            "equipos/list.html",
            {"request": request, "equipos": equipos}
        )
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="¡El árbitro ha parado el partido! No se pudo conectar con la base de datos para listar equipos."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"¡Error inesperado al recuperar la lista de equipos! {e}"
        )

@router.get("/equipos/{equipo_id}", response_class=HTMLResponse)
async def ver_equipo(request: Request, equipo_id: int, db: Session = Depends(get_db)):
    """
    Muestra los detalles de un equipo específico.
    """
    try:
        equipo = equipos_operations.get_equipo_by_id(db, equipo_id)
        if not equipo or equipo.eliminado_logico:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="¡Equipo no encontrado o descendido!")
        return templates.TemplateResponse(
            "equipos/detail.html",
            {"request": request, "equipo": equipo}
        )
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="¡Fallo en la conexión! No se pudo consultar los datos del equipo."
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"¡Error inesperado al buscar los datos del equipo! {e}"
        )

@router.get("/equipos_crear", response_class=HTMLResponse)
async def show_create_equipo_form(request: Request):
    """
    Muestra el formulario para crear un nuevo equipo.
    """
    return templates.TemplateResponse("equipos/create.html", {"request": request})

@router.post("/equipos_crear", response_class=HTMLResponse)
async def create_equipo(
    request: Request,
    db: Session = Depends(get_db),
    nombre: str = Form(...),
    pais: str = Form(...),
    grupo: str = Form(...),
    imagen_url: str = Form(None)
):
    """
    Procesa el envío del formulario para crear un nuevo equipo.
    """
    equipo_data = EquipoCreate(
        nombre=nombre,
        pais=pais,
        grupo=grupo,
        imagen_url=imagen_url if imagen_url else None
    )
    try:
        equipo_creado = equipos_operations.create_equipo(db, equipo_data)
        return RedirectResponse(url=f"/equipos/{equipo_creado.id}", status_code=status.HTTP_303_SEE_OTHER)
    except ValueError as e:
        return templates.TemplateResponse(
            "equipos/create.html",
            {"request": request, "error_message": f"¡Error al inscribir el equipo! {e}"}
        )
    except OperationalError:
        return templates.TemplateResponse(
            "equipos/create.html",
            {"request": request, "error_message": "¡Problemas de conexión! No se pudo registrar el equipo."}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "equipos/create.html",
            {"request": request, "error_message": f"¡Error inesperado al crear el equipo! {e}"}
        )

@router.get("/equipos_editar/{equipo_id}", response_class=HTMLResponse)
async def show_edit_equipo_form(request: Request, equipo_id: int, db: Session = Depends(get_db)):
    """
    Muestra el formulario para editar un equipo existente.
    """
    try:
        equipo = equipos_operations.get_equipo_by_id(db, equipo_id)
        if not equipo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="¡Equipo no encontrado para editar!")
        return templates.TemplateResponse(
            "equipos/edit.html",
            {"request": request, "equipo": equipo}
        )
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="¡Error de conexión! No se pudo cargar la información del equipo para editar."
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"¡Error inesperado al preparar la edición del equipo! {e}"
        )

@router.post("/equipos_editar/{equipo_id}", response_class=HTMLResponse)
async def edit_equipo(
    request: Request,
    equipo_id: int,
    db: Session = Depends(get_db),
    nombre: str = Form(...),
    pais: str = Form(...),
    grupo: str = Form(...),
    imagen_url: str = Form(None),
    eliminado_logico: bool = Form(False)
):
    """
    Procesa el envío del formulario para actualizar un equipo.
    """
    equipo_update_data = EquipoUpdate(
        nombre=nombre,
        pais=pais,
        grupo=grupo,
        imagen_url=imagen_url if imagen_url else None,
        eliminado_logico=eliminado_logico
    )
    try:
        equipo_actualizado = equipos_operations.update_equipo(db, equipo_id, equipo_update_data)
        if not equipo_actualizado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="¡Equipo no encontrado para actualizar!")
        return RedirectResponse(url=f"/equipos/{equipo_actualizado.id}", status_code=status.HTTP_303_SEE_OTHER)
    except ValueError as e:
        equipo = equipos_operations.get_equipo_by_id(db, equipo_id)
        return templates.TemplateResponse(
            "equipos/edit.html",
            {"request": request, "equipo": equipo, "error_message": f"¡Error en la actualización! {e}"}
        )
    except OperationalError:
        equipo = equipos_operations.get_equipo_by_id(db, equipo_id)
        return templates.TemplateResponse(
            "equipos/edit.html",
            {"request": request, "equipo": equipo, "error_message": "¡Fallo en la conexión! No se pudo actualizar el equipo."}
        )
    except HTTPException:
        raise
    except Exception as e:
        equipo = equipos_operations.get_equipo_by_id(db, equipo_id)
        return templates.TemplateResponse(
            "equipos/edit.html",
            {"request": request, "equipo": equipo, "error_message": f"¡Error inesperado al actualizar el equipo! {e}"}
        )

@router.post("/equipos_eliminar/{equipo_id}", response_class=HTMLResponse)
async def eliminar_equipo_logico(request: Request, equipo_id: int, db: Session = Depends(get_db)):
    """
    Realiza una eliminación lógica de un equipo.
    """
    try:
        equipo_eliminado = equipos_operations.soft_delete_equipo(db, equipo_id)
        if not equipo_eliminado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="¡Equipo no encontrado para eliminación lógica!")
        return RedirectResponse(url="/equipos_lista", status_code=status.HTTP_303_SEE_OTHER)
    except OperationalError:
        equipos = equipos_operations.get_all_equipos(db)
        return templates.TemplateResponse(
            "equipos/list.html",
            {"request": request, "equipos": equipos, "error_message": "¡Problemas de red! No se pudo eliminar el equipo."}
        )
    except HTTPException:
        raise
    except Exception as e:
        equipos = equipos_operations.get_all_equipos(db)
        return templates.TemplateResponse("equipos/list.html", {"request": request, "equipos": equipos, "error_message": f"¡Error al retirar el equipo de la competición! {e}"})


### Ruta para Búsqueda Global

@router.get("/busqueda", response_class=HTMLResponse)
async def show_search_page(
    request: Request,
    db: Session = Depends(get_db),
    # Parámetro de búsqueda general
    query: Optional[str] = Query(None, description="Término general de búsqueda (nombre de jugador, equipo)"),

    # Parámetros para búsqueda de Jugadores (ahora como Optional[str] para manejo manual de errores)
    jugador_id: Optional[str] = Query(None, description="ID del jugador"),
    jugador_posicion: Optional[str] = Query(None, description="Posición del jugador"),
    jugador_nacionalidad: Optional[str] = Query(None, description="Nacionalidad del jugador"),
    jugador_equipo_id: Optional[str] = Query(None, description="ID del equipo del jugador"),

    # Parámetros para búsqueda de Equipos (ahora como Optional[str] para manejo manual de errores)
    equipo_id: Optional[str] = Query(None, description="ID del equipo"),
    equipo_pais: Optional[str] = Query(None, description="País del equipo"),
    equipo_grupo: Optional[str] = Query(None, description="Grupo del equipo"),

    # Parámetros para búsqueda de Partidos (ahora como Optional[str] para manejo manual de errores)
    partido_id: Optional[str] = Query(None, description="ID del partido"),
    partido_fase: Optional[str] = Query(None, description="Fase del partido"),
    partido_fecha_inicio: Optional[str] = Query(None, description="Fecha de inicio (AAAA-MM-DD)"),
    partido_fecha_fin: Optional[str] = Query(None, description="Fecha de fin (AAAA-MM-DD)"),
    partido_equipo_nombre: Optional[str] = Query(None, description="Nombre de un equipo en el partido")
):
    """
    Permite buscar jugadores, equipos y partidos utilizando diversos criterios.
    Los campos numéricos y de fecha ahora manejan errores de conversión de forma más robusta.
    """
    error_messages = []

    # Conversión de tipos y manejo de errores para parámetros numéricos/fechas
    converted_params = {}

    def safe_int_conversion(param_name, value):
        if value:
            try:
                return int(value)
            except ValueError:
                error_messages.append(f"¡Atención! El campo '{param_name}' debe ser un número entero válido.")
        return None

    def safe_date_conversion(param_name, value):
        if value:
            try:
                return date.fromisoformat(value)
            except ValueError:
                error_messages.append(f"¡Atención! El campo '{param_name}' debe tener el formato YYYY-MM-DD.")
        return None

    converted_params['jugador_id'] = safe_int_conversion("ID de Jugador", jugador_id)
    converted_params['jugador_equipo_id'] = safe_int_conversion("ID de Equipo (Jugador)", jugador_equipo_id)
    converted_params['equipo_id'] = safe_int_conversion("ID de Equipo", equipo_id)
    converted_params['partido_id'] = safe_int_conversion("ID de Partido", partido_id)
    converted_params['partido_fecha_inicio'] = safe_date_conversion("Fecha de Inicio (Partido)", partido_fecha_inicio)
    converted_params['partido_fecha_fin'] = safe_date_conversion("Fecha de Fin (Partido)", partido_fecha_fin)

    jugadores_encontrados = []
    equipos_encontrados = []
    partidos_encontrados = []

    # Realizar búsqueda solo si no hay errores de conversión y si se proporciona algún criterio
    if not error_messages and (
        query or jugador_posicion or jugador_nacionalidad or partido_fase or partido_equipo_nombre or
        any(converted_params.values()) # Verifica si algún ID o fecha convertida tiene valor
    ):
        try:
            # Llamar a las funciones de búsqueda actualizadas en operations
            jugadores_encontrados = jugadores_operations.search_jugadores(
                db,
                query_str=query, # Usamos 'query_str' como se definió en jugadores_operations
                id_jugador=converted_params['jugador_id'],
                posicion=jugador_posicion,
                nacionalidad=jugador_nacionalidad,
                equipo_id=converted_params['jugador_equipo_id']
            )
            equipos_encontrados = equipos_operations.search_equipos(
                db,
                nombre=query,
                id_equipo=converted_params['equipo_id'],
                pais=equipo_pais,
                grupo=equipo_grupo
            )
            partidos_encontrados = partidos_operations.search_partidos(
                db,
                id_partido=converted_params['partido_id'],
                fase=partido_fase,
                fecha_inicio=converted_params['partido_fecha_inicio'],
                fecha_fin=converted_params['partido_fecha_fin'],
                equipo_nombre=partido_equipo_nombre if partido_equipo_nombre else query
            )
        except OperationalError:
            error_messages.append("¡Fallo en la conexión! No se pudo realizar la búsqueda en la base de datos.")
        except Exception as e:
            error_messages.append(f"¡Error inesperado al buscar! {e}")

    return templates.TemplateResponse(
        "search.html",
        {
            "request": request,
            "query": query,
            "error_messages": error_messages, # Pasar los mensajes de error a la plantilla

            # Pasar los parámetros de búsqueda ORIGINALES (str) de vuelta a la plantilla
            # para que los inputs del formulario mantengan su valor.
            "jugador_id": jugador_id,
            "jugador_posicion": jugador_posicion,
            "jugador_nacionalidad": jugador_nacionalidad,
            "jugador_equipo_id": jugador_equipo_id,

            "equipo_id": equipo_id,
            "equipo_pais": equipo_pais,
            "equipo_grupo": equipo_grupo,

            "partido_id": partido_id,
            "partido_fase": partido_fase,
            "partido_fecha_inicio": partido_fecha_inicio,
            "partido_fecha_fin": partido_fecha_fin,
            "partido_equipo_nombre": partido_equipo_nombre,

            "jugadores": jugadores_encontrados,
            "equipos": equipos_encontrados,
            "partidos": partidos_encontrados
        }
    )

### Rutas para Estadísticas

@router.get("/estadisticas", response_class=HTMLResponse)
async def show_statistics_page(request: Request, db: Session = Depends(get_db)):
    """
    Muestra las estadísticas destacadas (máximos goleadores, asistentes, equipos por goles).
    """
    try:
        top_scorers = jugadores_operations.get_top_scorers(db, limit=10)
        top_assisters = jugadores_operations.get_top_assisters(db, limit=10)
        teams_by_goals = equipos_operations.get_teams_by_total_goals(db, limit=10)

        return templates.TemplateResponse(
            "statistics.html",
            {
                "request": request,
                "top_scorers": top_scorers,
                "top_assisters": top_assisters,
                "teams_by_goals": teams_by_goals
            }
        )
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="¡Apagón en el estadio! No se pudieron cargar las estadísticas. Revisa la conexión."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"¡Error inesperado al obtener las estadísticas! {e}"
        )

### Rutas para Partidos

@router.get("/partidos_lista", response_class=HTMLResponse)
async def listar_partidos(request: Request, db: Session = Depends(get_db)):
    """
    Muestra la lista de todos los partidos activos, agrupados por fase.
    """
    try:
        all_partidos = partidos_operations.get_all_partidos(db)
        # Agrupar partidos por fase
        partidos_por_fase = defaultdict(list)
        # Definir un orden para las fases (puedes ajustar el orden si es necesario)
        orden_fases = ["Fase de Grupos", "Octavos de Final", "Cuartos de Final", "Semifinal", "Final"]

        for partido in all_partidos:
            partidos_por_fase[partido.fase].append(partido)

        # Convertir a una lista de tuplas (fase, partidos_en_fase) ordenada por el orden_fases
        partidos_agrupados = []
        for fase in orden_fases:
            if fase in partidos_por_fase:
                # Opcional: ordenar partidos dentro de cada fase por fecha
                sorted_partidos_en_fase = sorted(partidos_por_fase[fase], key=lambda p: p.fecha)
                partidos_agrupados.append((fase, sorted_partidos_en_fase))

        # Añadir cualquier fase que no estuviera en `orden_fases` al final (útil para fases personalizadas)
        for fase in sorted(partidos_por_fase.keys()):
            if fase not in orden_fases:
                sorted_partidos_en_fase = sorted(partidos_por_fase[fase], key=lambda p: p.fecha)
                partidos_agrupados.append((fase, sorted_partidos_en_fase))


        return templates.TemplateResponse(
            "partidos/list.html",
            {"request": request, "partidos_agrupados": partidos_agrupados}
        )
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="¡Se cortó la transmisión! No se pudieron cargar los partidos. Problemas de conexión."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"¡Error inesperado al obtener el calendario de partidos! {e}"
        )

@router.get("/partidos_crear", response_class=HTMLResponse)
async def show_create_partido_form(request: Request, db: Session = Depends(get_db)):
    """
    Muestra el formulario para crear un nuevo partido.
    """
    try:
        equipos = equipos_operations.get_all_equipos(db)
        return templates.TemplateResponse("partidos/create.html", {"request": request, "equipos": equipos})
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="¡Error de conexión! No se pudieron cargar los equipos para programar el partido."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"¡Error inesperado al preparar el formulario de partido! {e}"
        )

@router.post("/partidos_crear", response_class=HTMLResponse)
async def create_partido(
    request: Request,
    db: Session = Depends(get_db),
    equipo_local_id: int = Form(...),
    equipo_visitante_id: int = Form(...),
    goles_local: int = Form(...),
    goles_visitante: int = Form(...),
    fecha: date = Form(...),
    fase: str = Form(...)
):
    """
    Procesa el envío del formulario para crear un nuevo partido.
    """
    partido_data = PartidoCreate(
        equipo_local_id=equipo_local_id,
        equipo_visitante_id=equipo_visitante_id,
        goles_local=goles_local,
        goles_visitante=goles_visitante,
        fecha=fecha,
        fase=fase
    )
    try:
        partido_creado = partidos_operations.create_partido(db, partido_data)
        return RedirectResponse(url=f"/partidos_lista", status_code=status.HTTP_303_SEE_OTHER)
    except ValueError as e:
        equipos = equipos_operations.get_all_equipos(db)
        return templates.TemplateResponse(
            "partidos/create.html",
            {"request": request, "equipos": equipos, "error_message": f"¡Problema al programar el partido! {e}"}
        )
    except OperationalError:
        equipos = equipos_operations.get_all_equipos(db)
        return templates.TemplateResponse(
            "partidos/create.html",
            {"request": request, "equipos": equipos, "error_message": "¡Fallo de conexión! No se pudo registrar el partido."}
        )
    except Exception as e:
        equipos = equipos_operations.get_all_equipos(db)
        return templates.TemplateResponse(
            "partidos/create.html",
            {"request": request, "equipos": equipos, "error_message": f"¡Error inesperado al crear el partido! {e}"}
        )

@router.get("/partidos_editar/{partido_id}", response_class=HTMLResponse)
async def show_edit_partido_form(request: Request, partido_id: int, db: Session = Depends(get_db)):
    """
    Muestra el formulario para editar un partido existente.
    """
    try:
        partido = partidos_operations.get_partido_by_id(db, partido_id)
        if not partido:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="¡Partido no encontrado para editar!")
        equipos = equipos_operations.get_all_equipos(db)
        return templates.TemplateResponse(
            "partidos/edit.html",
            {"request": request, "partido": partido, "equipos": equipos}
        )
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="¡Error de conexión! No se pudo cargar la información del partido para editar."
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"¡Error inesperado al preparar la edición del partido! {e}"
        )

@router.post("/partidos_editar/{partido_id}", response_class=HTMLResponse)
async def edit_partido(
    request: Request,
    partido_id: int,
    db: Session = Depends(get_db),
    equipo_local_id: int = Form(...),
    equipo_visitante_id: int = Form(...),
    goles_local: int = Form(...),
    goles_visitante: int = Form(...),
    fecha: date = Form(...),
    fase: str = Form(...),
    eliminado_logico: bool = Form(False)
):
    """
    Procesa el envío del formulario para actualizar un partido.
    """
    partido_update_data = PartidoUpdate(
        equipo_local_id=equipo_local_id,
        equipo_visitante_id=equipo_visitante_id,
        goles_local=goles_local,
        goles_visitante=goles_visitante,
        fecha=fecha,
        fase=fase,
        eliminado_logico=eliminado_logico
    )
    try:
        partido_actualizado = partidos_operations.update_partido(db, partido_id, partido_update_data)
        if not partido_actualizado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="¡Partido no encontrado para actualizar!")
        return RedirectResponse(url=f"/partidos_lista", status_code=status.HTTP_303_SEE_OTHER)
    except ValueError as e:
        partido = partidos_operations.get_partido_by_id(db, partido_id)
        equipos = equipos_operations.get_all_equipos(db)
        return templates.TemplateResponse(
            "partidos/edit.html",
            {"request": request, "partido": partido, "equipos": equipos, "error_message": f"¡Problema al actualizar el partido! {e}"}
        )
    except OperationalError:
        partido = partidos_operations.get_partido_by_id(db, partido_id)
        equipos = equipos_operations.get_all_equipos(db)
        return templates.TemplateResponse(
            "partidos/edit.html",
            {"request": request, "partido": partido, "equipos": equipos, "error_message": "¡Fallo de conexión! No se pudo actualizar el partido."}
        )
    except HTTPException:
        raise
    except Exception as e:
        partido = partidos_operations.get_partido_by_id(db, partido_id)
        equipos = equipos_operations.get_all_equipos(db)
        return templates.TemplateResponse(
            "partidos/edit.html",
            {"request": request, "partido": partido, "equipos": equipos, "error_message": f"¡Error inesperado al actualizar el partido! {e}"}
        )

@router.post("/partidos_eliminar/{partido_id}", response_class=HTMLResponse)
async def eliminar_partido_logico(request: Request, partido_id: int, db: Session = Depends(get_db)):
    """
    Realiza una eliminación lógica de un partido.
    """
    try:
        partido_eliminado = partidos_operations.soft_delete_partido(db, partido_id)
        if not partido_eliminado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="¡Partido no encontrado para anular!")
        return RedirectResponse(url="/partidos_lista", status_code=status.HTTP_303_SEE_OTHER)
    except OperationalError:
        partidos = partidos_operations.get_all_partidos(db)
        return templates.TemplateResponse(
            "partidos/list.html",
            {"request": request, "partidos_agrupados": partidos, "error_message": "¡Problemas de red! No se pudo anular el partido."}
        )
    except HTTPException:
        raise
    except Exception as e:
        partidos = partidos_operations.get_all_partidos(db)
        return templates.TemplateResponse("partidos/list.html", {"request": request, "partidos_agrupados": partidos, "error_message": f"¡Error al anular el partido! {e}"})


### Ruta para Historial de Eliminados

@router.get("/historial_eliminados", response_class=HTMLResponse)
async def show_deleted_history(request: Request, db: Session = Depends(get_db)):
    """
    Muestra un historial de los registros eliminados lógicamente (jugadores, equipos, partidos).
    """
    try:
        deleted_jugadores = jugadores_operations.get_soft_deleted_jugadores(db)
        deleted_equipos = equipos_operations.get_soft_deleted_equipos(db)
        deleted_partidos = partidos_operations.get_soft_deleted_partidos(db)

        return templates.TemplateResponse(
            "history_deleted.html",
            {
                "request": request,
                "deleted_jugadores": deleted_jugadores,
                "deleted_equipos": deleted_equipos,
                "deleted_partidos": deleted_partidos
            }
        )
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="¡El marcador no responde! No se pudo cargar el historial de eliminados. Problemas de conexión."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"¡Error inesperado al cargar el historial de eliminados! {e}"
        )