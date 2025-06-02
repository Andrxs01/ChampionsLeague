from fastapi import APIRouter, HTTPException
import os

router = APIRouter()

@router.get("/planeacion", tags=["Documentación"])
def get_planeacion():
    ruta = os.path.join("docs", "planeacion.md")
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()
        return {"contenido": contenido}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo de planeación no encontrado.")
@router.get("/diseno", tags=["Documentación"])
def get_diseno():
    ruta = os.path.join("docs", "diseno.md")
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()
        return {"contenido": contenido}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo de diseño no encontrado.")
