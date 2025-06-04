# routes/html_pages.py
from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from utils.db import get_db
from operations import jugadores_operations, equipos_operations
from data.models import JugadorCreate, JugadorUpdate, EquipoCreate, EquipoUpdate, Jugador, Equipo

router = APIRouter(
    tags=["Páginas HTML"],
)

templates = Jinja2Templates(directory="templates")

# --- Rutas de información del proyecto ---

@router.get("/home", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    jugadores_recientes = jugadores_operations.get_all_jugadores(db, limit=5)
    equipos_recientes = equipos_operations.get_all_equipos(db, limit=5)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "jugadores": jugadores_recientes, "equipos": equipos_recientes}
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
async def listar_jugadores(request: Request, db: Session = Depends(get_db)):
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
    asistencias: int = Form(0),
    imagen_url: str = Form(None)
):
    jugador_data = JugadorCreate(
        nombre=nombre,
        equipo_id=equipo_id,
        posicion=posicion,
        edad=edad,
        nacionalidad=nacionalidad,
        goles=goles,
        asistencias=asistencias,
        imagen_url=imagen_url if imagen_url else None
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
    imagen_url: str = Form(None),
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
        imagen_url=imagen_url if imagen_url else None,
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


# --- Ruta para Búsqueda ---

@router.get("/busqueda", response_class=HTMLResponse)
async def show_search_page(request: Request, db: Session = Depends(get_db), query: str = None):
    jugadores_encontrados = []
    equipos_encontrados = []

    if query:
        jugadores_encontrados = db.query(Jugador).filter(
            Jugador.nombre.ilike(f"%{query}%"),
            Jugador.eliminado_logico == False
        ).all()
        equipos_encontrados = db.query(Equipo).filter(
            Equipo.nombre.ilike(f"%{query}%"),
            Equipo.eliminado_logico == False
        ).all()

    return templates.TemplateResponse(
        "search.html",
        {"request": request, "query": query, "jugadores": jugadores_encontrados, "equipos": equipos_encontrados}
    )

# --- NUEVA RUTA PARA ESTADÍSTICAS ---
@router.get("/estadisticas", response_class=HTMLResponse)
async def show_statistics_page(request: Request, db: Session = Depends(get_db)):
    top_scorers = jugadores_operations.get_top_scorers(db, limit=5) # Obtener los 5 mejores goleadores
    top_assisters = jugadores_operations.get_top_assisters(db, limit=5) # Obtener los 5 mejores asistentes
    teams_by_goals = equipos_operations.get_teams_by_total_goals(db, limit=5) # Obtener los 5 equipos con más goles

    return templates.TemplateResponse(
        "statistics.html",
        {
            "request": request,
            "top_scorers": top_scorers,
            "top_assisters": top_assisters,
            "teams_by_goals": teams_by_goals
        }
    )
