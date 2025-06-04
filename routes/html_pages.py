# routes/html_pages.py
from fastapi import APIRouter, Request, Depends, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from utils.db import get_db
from operations import jugadores_operations, equipos_operations, partidos_operations
from data import models
from data.models import JugadorCreate, JugadorUpdate, EquipoCreate, EquipoUpdate, PartidoCreate, PartidoUpdate, Jugador, Equipo, Partido
from datetime import date
from collections import defaultdict
from typing import Optional # ¡Asegúrate de que Optional esté importado!

router = APIRouter(
    tags=["Páginas HTML"],
)

templates = Jinja2Templates(directory="templates")

# --- Rutas de información del proyecto ---

@router.get("/home", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    jugadores_recientes = jugadores_operations.get_all_jugadores(db, limit=5)
    equipos_recientes = equipos_operations.get_all_equipos(db, limit=5)
    partidos_recientes = partidos_operations.get_all_partidos(db, limit=5)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "jugadores": jugadores_recientes, "equipos": equipos_recientes, "partidos": partidos_recientes}
    )

@router.get("/desarrollador", response_class=HTMLResponse)
async def about_developer(request: Request):
    return templates.TemplateResponse("about_developer.html", {"request": request})

@router.get("/planeacion", response_class=HTMLResponse)
async def planning_phase(request: Request):
    return templates.TemplateResponse("planning_phase.html", {"request": request})

@router.get("/diseno", response_class=HTMLResponse)
async def design_phase(request: Request):
    return templates.TemplateResponse("design_phase.html", {"request": request})

@router.get("/objetivo", response_class=HTMLResponse)
async def project_objective(request: Request):
    return templates.TemplateResponse("project_objective.html", {"request": request})

# --- Rutas para Jugadores (Listar, Ver, Crear, Editar, Eliminar) ---

@router.get("/jugadores_lista", response_class=HTMLResponse)
async def listar_jugadores(
        request: Request,
        db: Session = Depends(get_db)
):

    jugadores = jugadores_operations.get_all_jugadores(db)

    return templates.TemplateResponse(
        "jugadores/list.html",

        {"request": request, "jugadores": jugadores}
    )

@router.get("/jugadores/{jugador_id}", response_class=HTMLResponse)
async def ver_jugador(request: Request, jugador_id: int, db: Session = Depends(get_db)):
    jugador = jugadores_operations.get_jugador_by_id(db, jugador_id)
    if not jugador or jugador.eliminado_logico:
        raise HTTPException(status_code=404, detail="Jugador no encontrado o eliminado")
    return templates.TemplateResponse(
        "jugadores/detail.html",
        {"request": request, "jugador": jugador}
    )

@router.get("/jugadores_crear", response_class=HTMLResponse)
async def show_create_jugador_form(request: Request, db: Session = Depends(get_db)):
    equipos = equipos_operations.get_all_equipos(db)
    return templates.TemplateResponse("jugadores/create.html", {"request": request, "equipos": equipos})

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
        equipo_existente = equipos_operations.get_equipo_by_id(db, equipo_id)
        if not equipo_existente or equipo_existente.eliminado_logico:
            equipos = equipos_operations.get_all_equipos(db)
            return templates.TemplateResponse(
                "jugadores/create.html",
                {"request": request, "equipos": equipos, "error_message": "El ID del equipo no es válido o el equipo no está activo."}
            )

        jugador_creado = jugadores_operations.create_jugador(db, jugador_data)
        return RedirectResponse(url=f"/jugadores/{jugador_creado.id}", status_code=303)
    except Exception as e:
        equipos = equipos_operations.get_all_equipos(db)
        return templates.TemplateResponse(
            "jugadores/create.html",
            {"request": request, "equipos": equipos, "error_message": f"Error al crear jugador: {e}"}
        )

@router.get("/jugadores_editar/{jugador_id}", response_class=HTMLResponse)
async def show_edit_jugador_form(request: Request, jugador_id: int, db: Session = Depends(get_db)):
    jugador = jugadores_operations.get_jugador_by_id(db, jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado para editar")
    equipos = equipos_operations.get_all_equipos(db)
    return templates.TemplateResponse(
        "jugadores/edit.html",
        {"request": request, "jugador": jugador, "equipos": equipos}
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
        equipo_existente = equipos_operations.get_equipo_by_id(db, equipo_id)
        if not equipo_existente or equipo_existente.eliminado_logico:
            jugador = jugadores_operations.get_jugador_by_id(db, jugador_id)
            equipos = equipos_operations.get_all_equipos(db)
            return templates.TemplateResponse(
                "jugadores/edit.html",
                {"request": request, "jugador": jugador, "equipos": equipos, "error_message": "El ID del equipo no es válido o el equipo no está activo."}
            )

        jugador_actualizado = jugadores_operations.update_jugador(db, jugador_id, jugador_update_data)
        if not jugador_actualizado:
            raise HTTPException(status_code=404, detail="Jugador no encontrado para actualizar")
        return RedirectResponse(url=f"/jugadores/{jugador_actualizado.id}", status_code=303)
    except Exception as e:
        jugador = jugadores_operations.get_jugador_by_id(db, jugador_id)
        equipos = equipos_operations.get_all_equipos(db)
        return templates.TemplateResponse(
            "jugadores/edit.html",
            {"request": request, "jugador": jugador, "equipos": equipos, "error_message": f"Error al actualizar jugador: {e}"}
        )

@router.post("/jugadores_eliminar/{jugador_id}", response_class=HTMLResponse)
async def eliminar_jugador_logico(request: Request, jugador_id: int, db: Session = Depends(get_db)):
    try:
        jugador_eliminado = jugadores_operations.soft_delete_jugador(db, jugador_id)
        if not jugador_eliminado:
            raise HTTPException(status_code=404, detail="Jugador no encontrado para eliminación lógica")
        return RedirectResponse(url="/jugadores_lista", status_code=303)
    except Exception as e:
        jugadores = jugadores_operations.get_all_jugadores(db)
        return templates.TemplateResponse("jugadores/list.html", {"request": request, "jugadores": jugadores, "error_message": f"Error al eliminar jugador: {e}"})


# --- Rutas para Equipos (Listar, Ver, Crear, Editar, Eliminar) ---

@router.get("/equipos_lista", response_class=HTMLResponse)
async def listar_equipos(request: Request, db: Session = Depends(get_db)):
    equipos = equipos_operations.get_all_equipos(db)
    return templates.TemplateResponse(
        "equipos/list.html",
        {"request": request, "equipos": equipos}
    )

@router.get("/equipos/{equipo_id}", response_class=HTMLResponse)
async def ver_equipo(request: Request, equipo_id: int, db: Session = Depends(get_db)):
    equipo = equipos_operations.get_equipo_by_id(db, equipo_id)
    if not equipo or equipo.eliminado_logico:
        raise HTTPException(status_code=404, detail="Equipo no encontrado o eliminado")
    return templates.TemplateResponse(
        "equipos/detail.html",
        {"request": request, "equipo": equipo}
    )

@router.get("/equipos_crear", response_class=HTMLResponse)
async def show_create_equipo_form(request: Request):
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
    equipo_data = EquipoCreate(
        nombre=nombre,
        pais=pais,
        grupo=grupo,
        imagen_url=imagen_url if imagen_url else None
    )
    try:
        equipo_creado = equipos_operations.create_equipo(db, equipo_data)
        return RedirectResponse(url=f"/equipos/{equipo_creado.id}", status_code=303)
    except Exception as e:
        return templates.TemplateResponse(
            "equipos/create.html",
            {"request": request, "error_message": f"Error al crear equipo: {e}"}
        )

@router.get("/equipos_editar/{equipo_id}", response_class=HTMLResponse)
async def show_edit_equipo_form(request: Request, equipo_id: int, db: Session = Depends(get_db)):
    equipo = equipos_operations.get_equipo_by_id(db, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado para editar")
    return templates.TemplateResponse(
        "equipos/edit.html",
        {"request": request, "equipo": equipo}
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
            raise HTTPException(status_code=404, detail="Equipo no encontrado para actualizar")
        return RedirectResponse(url=f"/equipos/{equipo_actualizado.id}", status_code=303)
    except Exception as e:
        equipo = equipos_operations.get_equipo_by_id(db, equipo_id)
        return templates.TemplateResponse(
            "equipos/edit.html",
            {"request": request, "equipo": equipo, "error_message": f"Error al actualizar equipo: {e}"}
        )

@router.post("/equipos_eliminar/{equipo_id}", response_class=HTMLResponse)
async def eliminar_equipo_logico(request: Request, equipo_id: int, db: Session = Depends(get_db)):
    try:
        equipo_eliminado = equipos_operations.soft_delete_equipo(db, equipo_id)
        if not equipo_eliminado:
            raise HTTPException(status_code=404, detail="Equipo no encontrado para eliminación lógica")
        return RedirectResponse(url="/equipos_lista", status_code=303)
    except Exception as e:
        equipos = equipos_operations.get_all_equipos(db)
        return templates.TemplateResponse("equipos/list.html", {"request": request, "equipos": equipos, "error_message": f"Error al eliminar equipo: {e}"})


# --- Ruta para Búsqueda (ACTUALIZADA para manejar 422) ---

@router.get("/busqueda", response_class=HTMLResponse)
async def show_search_page(
    request: Request,
    db: Session = Depends(get_db),
    query: Optional[str] = Query(None),

    # Parámetros para búsqueda de Jugadores (ahora como Optional[str] para manejo manual)
    jugador_id: Optional[str] = Query(None), # Cambiado a str
    jugador_posicion: Optional[str] = Query(None),
    jugador_nacionalidad: Optional[str] = Query(None),
    jugador_equipo_id: Optional[str] = Query(None), # Cambiado a str

    # Parámetros para búsqueda de Equipos (ahora como Optional[str] para manejo manual)
    equipo_id: Optional[str] = Query(None), # Cambiado a str
    equipo_pais: Optional[str] = Query(None),
    equipo_grupo: Optional[str] = Query(None),

    # Parámetros para búsqueda de Partidos (ahora como Optional[str] para manejo manual)
    partido_id: Optional[str] = Query(None), # Cambiado a str
    partido_fase: Optional[str] = Query(None),
    partido_fecha_inicio: Optional[str] = Query(None), # Cambiado a str
    partido_fecha_fin: Optional[str] = Query(None),   # Cambiado a str
    partido_equipo_nombre: Optional[str] = Query(None)
):
    # Variables convertidas para pasar a las operaciones
    converted_jugador_id: Optional[int] = None
    converted_jugador_equipo_id: Optional[int] = None
    converted_equipo_id: Optional[int] = None
    converted_partido_id: Optional[int] = None
    converted_partido_fecha_inicio: Optional[date] = None
    converted_partido_fecha_fin: Optional[date] = None

    # Lógica de conversión: de str a int, None si es vacío o no numérico
    if jugador_id and jugador_id.isdigit():
        converted_jugador_id = int(jugador_id)
    if jugador_equipo_id and jugador_equipo_id.isdigit():
        converted_jugador_equipo_id = int(jugador_equipo_id)
    if equipo_id and equipo_id.isdigit():
        converted_equipo_id = int(equipo_id)
    if partido_id and partido_id.isdigit():
        converted_partido_id = int(partido_id)

    # Lógica de conversión: de str a date, None si es vacío o formato incorrecto
    if partido_fecha_inicio:
        try:
            converted_partido_fecha_inicio = date.fromisoformat(partido_fecha_inicio)
        except ValueError:
            # Puedes añadir logging aquí si quieres registrar intentos de fechas inválidas
            pass
    if partido_fecha_fin:
        try:
            converted_partido_fecha_fin = date.fromisoformat(partido_fecha_fin)
        except ValueError:
            # Puedes añadir logging aquí si quieres registrar intentos de fechas inválidas
            pass

    jugadores_encontrados = []
    equipos_encontrados = []
    partidos_encontrados = []

    # Se realiza la búsqueda solo si hay al menos un criterio especificado
    # Ahora usamos las variables convertidas para la lógica de la condición
    if query or converted_jugador_id or jugador_posicion or jugador_nacionalidad or converted_jugador_equipo_id or \
       converted_equipo_id or equipo_pais or equipo_grupo or \
       converted_partido_id or partido_fase or converted_partido_fecha_inicio or converted_partido_fecha_fin or partido_equipo_nombre:

        # Llamar a las funciones de búsqueda actualizadas en operations
        jugadores_encontrados = jugadores_operations.search_jugadores(
            db,
            nombre=query,
            id=converted_jugador_id,
            posicion=jugador_posicion,
            nacionalidad=jugador_nacionalidad,
            equipo_id=converted_jugador_equipo_id
        )
        equipos_encontrados = equipos_operations.search_equipos(
            db,
            nombre=query,
            id=converted_equipo_id,
            pais=equipo_pais,
            grupo=equipo_grupo
        )
        partidos_encontrados = partidos_operations.search_partidos(
            db,
            id=converted_partido_id,
            fase=partido_fase,
            fecha_inicio=converted_partido_fecha_inicio,
            fecha_fin=converted_partido_fecha_fin,
            equipo_nombre=partido_equipo_nombre
        )

    return templates.TemplateResponse(
        "search.html",
        {
            "request": request,
            "query": query,

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

# --- Rutas para Estadísticas ---
@router.get("/estadisticas", response_class=HTMLResponse)
async def show_statistics_page(request: Request, db: Session = Depends(get_db)):
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

# --- Rutas para Partidos ---

@router.get("/partidos_lista", response_class=HTMLResponse)
async def listar_partidos(request: Request, db: Session = Depends(get_db)):
    all_partidos = partidos_operations.get_all_partidos(db)
    # Agrupar partidos por fase
    partidos_por_fase = defaultdict(list)
    # Definir un orden para las fases
    orden_fases = ["Fase de Grupos", "Octavos de Final", "Cuartos de Final", "Semifinal", "Final"]

    for partido in all_partidos:
        partidos_por_fase[partido.fase].append(partido)

    # Convertir a una lista de tuplas (fase, partidos_en_fase) ordenada
    partidos_agrupados = []
    for fase in orden_fases:
        if fase in partidos_por_fase:
            # Opcional: ordenar partidos dentro de cada fase por fecha
            sorted_partidos_en_fase = sorted(partidos_por_fase[fase], key=lambda p: p.fecha)
            partidos_agrupados.append((fase, sorted_partidos_en_fase))

    return templates.TemplateResponse(
        "partidos/list.html",
        {"request": request, "partidos_agrupados": partidos_agrupados}
    )

@router.get("/partidos_crear", response_class=HTMLResponse)
async def show_create_partido_form(request: Request, db: Session = Depends(get_db)):
    equipos = equipos_operations.get_all_equipos(db)
    return templates.TemplateResponse("partidos/create.html", {"request": request, "equipos": equipos})

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
    partido_data = PartidoCreate(
        equipo_local_id=equipo_local_id,
        equipo_visitante_id=equipo_visitante_id,
        goles_local=goles_local,
        goles_visitante=goles_visitante,
        fecha=fecha,
        fase=fase
    )
    try:
        if equipo_local_id == equipo_visitante_id:
             equipos = equipos_operations.get_all_equipos(db)
             return templates.TemplateResponse(
                "partidos/create.html",
                {"request": request, "equipos": equipos, "error_message": "El equipo local y el visitante no pueden ser el mismo."}
            )

        equipo_local_existente = equipos_operations.get_equipo_by_id(db, equipo_local_id)
        equipo_visitante_existente = equipos_operations.get_equipo_by_id(db, equipo_visitante_id)

        if not equipo_local_existente or equipo_local_existente.eliminado_logico:
            equipos = equipos_operations.get_all_equipos(db)
            return templates.TemplateResponse(
                "partidos/create.html",
                {"request": request, "equipos": equipos, "error_message": "El ID del equipo local no es válido o está inactivo."}
            )
        if not equipo_visitante_existente or equipo_visitante_existente.eliminado_logico:
            equipos = equipos_operations.get_all_equipos(db)
            return templates.TemplateResponse(
                "partidos/create.html",
                {"request": request, "equipos": equipos, "error_message": "El ID del equipo visitante no es válido o está inactivo."}
            )

        partido_creado = partidos_operations.create_partido(db, partido_data)
        return RedirectResponse(url=f"/partidos_lista", status_code=303)
    except Exception as e:
        equipos = equipos_operations.get_all_equipos(db)
        return templates.TemplateResponse(
            "partidos/create.html",
            {"request": request, "equipos": equipos, "error_message": f"Error al crear partido: {e}"}
        )

@router.get("/partidos_editar/{partido_id}", response_class=HTMLResponse)
async def show_edit_partido_form(request: Request, partido_id: int, db: Session = Depends(get_db)):
    partido = partidos_operations.get_partido_by_id(db, partido_id)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado para editar")
    equipos = equipos_operations.get_all_equipos(db)
    return templates.TemplateResponse(
        "partidos/edit.html",
        {"request": request, "partido": partido, "equipos": equipos}
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
        if equipo_local_id == equipo_visitante_id:
             partido = partidos_operations.get_partido_by_id(db, partido_id)
             equipos = equipos_operations.get_all_equipos(db)
             return templates.TemplateResponse(
                "partidos/edit.html",
                {"request": request, "partido": partido, "equipos": equipos, "error_message": "El equipo local y el visitante no pueden ser el mismo."}
            )

        equipo_local_existente = equipos_operations.get_equipo_by_id(db, equipo_local_id)
        equipo_visitante_existente = equipos_operations.get_equipo_by_id(db, equipo_visitante_id)

        if not equipo_local_existente or equipo_local_existente.eliminado_logico:
            partido = partidos_operations.get_partido_by_id(db, partido_id)
            equipos = equipos_operations.get_all_equipos(db)
            return templates.TemplateResponse(
                "partidos/edit.html",
                {"request": request, "partido": partido, "equipos": equipos, "error_message": "El ID del equipo local no es válido o está inactivo."}
            )
        if not equipo_visitante_existente or equipo_visitante_existente.eliminado_logico:
            partido = partidos_operations.get_partido_by_id(db, partido_id)
            equipos = equipos_operations.get_all_equipos(db)
            return templates.TemplateResponse(
                "partidos/edit.html",
                {"request": request, "partido": partido, "equipos": equipos, "error_message": "El ID del equipo visitante no es válido o está inactivo."}
            )

        partido_actualizado = partidos_operations.update_partido(db, partido_id, partido_update_data)
        if not partido_actualizado:
            raise HTTPException(status_code=404, detail="Partido no encontrado para actualizar")
        return RedirectResponse(url=f"/partidos_lista", status_code=303)
    except Exception as e:
        partido = partidos_operations.get_partido_by_id(db, partido_id)
        equipos = equipos_operations.get_all_equipos(db)
        return templates.TemplateResponse(
            "partidos/edit.html",
            {"request": request, "partido": partido, "equipos": equipos, "error_message": f"Error al actualizar partido: {e}"}
        )

@router.post("/partidos_eliminar/{partido_id}", response_class=HTMLResponse)
async def eliminar_partido_logico(request: Request, partido_id: int, db: Session = Depends(get_db)):
    try:
        partido_eliminado = partidos_operations.soft_delete_partido(db, partido_id)
        if not partido_eliminado:
            raise HTTPException(status_code=404, detail="Partido no encontrado para eliminación lógica")
        return RedirectResponse(url="/partidos_lista", status_code=303)
    except Exception as e:
        partidos = partidos_operations.get_all_partidos(db)
        return templates.TemplateResponse("partidos/list.html", {"request": request, "partidos": partidos, "error_message": f"Error al eliminar partido: {e}"})

# --- NUEVA RUTA: Historial de Eliminados ---
@router.get("/historial_eliminados", response_class=HTMLResponse)
async def show_deleted_history(request: Request, db: Session = Depends(get_db)):
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