import json
import os
from typing import Dict, Any, List

# Ruta al directorio donde guardamos los archivos de idioma
I18N_DIR = "src/i18n"

def get_available_languages() -> List[str]:
    """
    Escanea el directorio i18n y devuelve una lista de los idiomas disponibles
    (basado en los nombres de archivo .json).
    """
    langs = []
    if not os.path.exists(I18N_DIR):
        return []
        
    for filename in os.listdir(I18N_DIR):
        if filename.endswith(".json"):
            langs.append(filename[:-5])  # Elimina la extensión '.json'
    return sorted(langs)

def get_translations(lang_code: str) -> Dict[str, Any] | None:
    """
    Lee y devuelve el contenido de un archivo de idioma específico.
    Devuelve None si el archivo no existe.
    """
    filepath = os.path.join(I18N_DIR, f"{lang_code}.json")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def update_translations(lang_code: str, new_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Actualiza un archivo de idioma. Carga los datos existentes, los fusiona
    con los nuevos datos y guarda el archivo completo.
    Crea el archivo si no existe.
    """
    filepath = os.path.join(I18N_DIR, f"{lang_code}.json")
    
    # Asegurarse de que el directorio i18n exista
    if not os.path.exists(I18N_DIR):
        os.makedirs(I18N_DIR)

    current_data = get_translations(lang_code) or {}
    
    # Fusiona los datos viejos con los nuevos
    current_data.update(new_data)
    
    # Escribe el archivo actualizado de vuelta al disco
    with open(filepath, 'w', encoding='utf-8') as f:
        # indent=2 para que el JSON sea legible. ensure_ascii=False para acentos.
        json.dump(current_data, f, ensure_ascii=False, indent=2)
        
    return current_data