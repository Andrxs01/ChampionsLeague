from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os

router = APIRouter()
templates = Jinja2Templates(directory="templates") # Asegúrate de que esto esté bien configurado si lo usas aquí también

@router.get("/planeacion", tags=["Documentación"], response_class=HTMLResponse)
async def get_planeacion(request: Request):
    ruta = os.path.join("docs", "planeacion.md")
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            contenido_md = f.read()
        # Puedes renderizarlo en una plantilla o devolverlo como texto plano si prefieres
        # Para HTML puro, lo devolveremos como texto preformateado o convertido a HTML si tuvieras una librería markdown-to-html
        # Por ahora, para mantenerlo simple y cumplir con HTML puro, lo pondremos en un <pre>
        return templates.TemplateResponse("documentacion_template.html", {"request": request, "titulo": "Fase de Planeación", "contenido": contenido_md})
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo de planeación no encontrado.")

@router.get("/diseno", tags=["Documentación"], response_class=HTMLResponse)
async def get_diseno(request: Request):
    ruta = os.path.join("docs", "diseno.md")
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            contenido_md = f.read()
        return templates.TemplateResponse("documentacion_template.html", {"request": request, "titulo": "Fase de Diseño", "contenido": contenido_md})
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo de diseño no encontrado.")

@router.get("/desarrollador", tags=["Documentación"], response_class=HTMLResponse)
async def get_desarrollador(request: Request):
    info_desarrollador = {
        "nombre": "Tu Nombre Completo",
        "email": "tu.email@example.com",
        "github": "https://github.com/tu_usuario_github",
        "carrera": "Tu Carrera/Estudios"
    }
    return templates.TemplateResponse("info_desarrollador.html", {"request": request, "info": info_desarrollador})

@router.get("/objetivo", tags=["Documentación"], response_class=HTMLResponse)
async def get_objetivo(request: Request):
    objetivo_proyecto = {
        "titulo": "Objetivo Principal del Proyecto",
        "descripcion": "El objetivo principal de este proyecto es desarrollar una API RESTful y una interfaz web para gestionar jugadores y equipos de la Champions League 2017/18, permitiendo operaciones CRUD (Crear, Leer, Actualizar, Eliminar Lógicamente) con manejo de imágenes y documentación accesible."
    }
    return templates.TemplateResponse("objetivo_proyecto.html", {"request": request, "objetivo": objetivo_proyecto})
