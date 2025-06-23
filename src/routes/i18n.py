from fastapi import APIRouter, HTTPException, Depends, Body
from typing import Dict, Any, List

# Importamos nuestro nuevo servicio y las dependencias de autenticación
from services import i18n_service
from dependencies import get_current_admin_user

router = APIRouter(prefix="/i18n", tags=["Internationalization (i18n)"])

@router.get("/", response_model=List[str])
def list_available_languages():
    """
    Endpoint público para obtener la lista de códigos de idioma disponibles.
    Ej: ["en", "es"]
    """
    return i18n_service.get_available_languages()

@router.get("/{lang_code}")
def get_language_file(lang_code: str):
    """
    Endpoint público para obtener el JSON completo de un idioma.
    Astro usaría este endpoint para buscar las traducciones.
    """
    translations = i18n_service.get_translations(lang_code)
    if translations is None:
        raise HTTPException(status_code=404, detail=f"Language '{lang_code}' not found.")
    return translations

@router.put("/{lang_code}", dependencies=[Depends(get_current_admin_user)])
def update_language_file(lang_code: str, data: Dict[str, Any] = Body(...)):
    """
    Endpoint protegido para actualizar o añadir una o más claves a un archivo
    de idioma. Requiere autenticación de administrador.
    """
    updated_translations = i18n_service.update_translations(lang_code, data)
    return {
        "message": f"Language '{lang_code}' updated successfully.",
        "data": updated_translations
    }