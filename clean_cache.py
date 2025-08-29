import os
import shutil

def clean_pycache(root_dir):
    """
    Encuentra y elimina todos los directorios __pycache__
    dentro de un directorio raíz.
    """
    count = 0
    for root, dirs, files in os.walk(root_dir):
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            print(f"Eliminando: {pycache_path}")
            shutil.rmtree(pycache_path)
            count += 1
    return count

def clean_mypy_cache(root_dir):
    """
    Encuentra y elimina los directorios .mypy_cache.
    """
    count = 0
    for root, dirs, files in os.walk(root_dir):
        if ".mypy_cache" in dirs:
            mypy_cache_path = os.path.join(root, ".mypy_cache")
            print(f"Eliminando: {mypy_cache_path}")
            shutil.rmtree(mypy_cache_path)
            count += 1
    return count

def clean_logs(root_dir):
    """
    Elimina todos los archivos dentro del directorio 'logs'.
    """
    logs_dir = os.path.join(root_dir, "logs")
    count = 0
    if os.path.isdir(logs_dir):
        print(f"Limpiando directorio: {logs_dir}")
        for filename in os.listdir(logs_dir):
            file_path = os.path.join(logs_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    print(f"  - Eliminado: {file_path}")
                    count += 1
            except Exception as e:
                print(f"Error al eliminar {file_path}. Razón: {e}")
    return count

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))

    print("--- Iniciando limpieza del proyecto ---")

    # 1. Limpiar __pycache__
    pycache_deleted = clean_pycache(project_root)
    print(f"Se eliminaron {pycache_deleted} directorios __pycache__.")

    # 2. Limpiar .mypy_cache
    mypy_deleted = clean_mypy_cache(project_root)
    print(f"Se eliminaron {mypy_deleted} directorios .mypy_cache.")

    # 3. Limpiar carpeta de logs
    logs_deleted = clean_logs(project_root)
    print(f"Se eliminaron {logs_deleted} archivos del directorio de logs.")

    print("\n--- Limpieza completada ---")
