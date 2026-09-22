from pathlib import Path
import re
import shutil

# ============================================================
# CONFIGURACION
# ============================================================

# La carpeta raiz es la carpeta donde esta guardado este script.
RUTA_RAIZ = Path(__file__).resolve().parent

# True: muestra los movimientos, pero no modifica archivos.
# False: mueve los archivos realmente.
MODO_PRUEBA = False

# Extensiones que nunca se moveran.
EXTENSIONES_IGNORADAS = {".py"}

# Categoria detectada -> carpeta principal.
CATEGORIAS = {
    "PROMPT": "1_PROMPT",
    "MDD": "2_MDD",
    "LOGICA": "3_LOGICA",
    "CUESTIONARIO": "4_CUESTIONARIO",
}

# Codigo encontrado en el archivo -> subcarpeta de destino.
# Aqui se resuelve la agrupacion de codigos.
MAPA_CODIGOS = {
    "AMD": "AMD",
    "BHT": "BHT-MSU-CRE",
    "MSU": "BHT-MSU-CRE",
    "CRE": "BHT-MSU-CRE",
    "CEX": "CEX",
    "CHP": "CHP",
    "HEC": "HEC",
    "INN": "INN",
    "OBV": "OBV-CPR-PA-Trends",
    "CPR": "OBV-CPR-PA-Trends",
    "PA": "OBV-CPR-PA-Trends",
    "TRENDS": "OBV-CPR-PA-Trends",
}

CARPETAS_ORGANIZADAS = set(CATEGORIAS.values())


def normalizar(texto: str) -> str:
    """Convierte el texto a mayusculas y uniformiza separadores."""
    texto = texto.upper().strip()
    texto = texto.replace("_", "-")
    texto = re.sub(r"\s*-\s*", "-", texto)
    texto = re.sub(r"-+", "-", texto)
    return texto


def detectar_categoria(nombre_archivo: str):
    """Detecta la categoria usando el nombre del archivo sin extension."""
    nombre = normalizar(Path(nombre_archivo).stem)

    # Se revisa primero CUESTIONARIO porque es el termino mas largo.
    for categoria in ("CUESTIONARIO", "LOGICA", "PROMPT", "MDD"):
        patron = rf"(?:^|[^A-Z0-9]){categoria}(?:$|[^A-Z0-9])"
        if re.search(patron, nombre):
            return categoria

    return None


def detectar_subcarpeta(nombre_archivo: str):
    """Detecta el codigo del proyecto y devuelve su carpeta agrupada."""
    nombre = normalizar(Path(nombre_archivo).stem)

    # Normalmente el codigo aparece al inicio: CPR_..., CRE_..., MSU_...
    coincidencia = re.match(r"^([A-Z]+)(?:[^A-Z]|$)", nombre)
    if coincidencia:
        codigo_inicial = coincidencia.group(1)
        if codigo_inicial in MAPA_CODIGOS:
            return MAPA_CODIGOS[codigo_inicial]

    # Respaldo: busca un codigo valido en cualquier parte del nombre.
    for codigo in sorted(MAPA_CODIGOS, key=len, reverse=True):
        patron = rf"(?:^|[^A-Z0-9]){re.escape(codigo)}(?:$|[^A-Z0-9])"
        if re.search(patron, nombre):
            return MAPA_CODIGOS[codigo]

    return None


def crear_estructura() -> None:
    """Crea la estructura requerida si alguna carpeta no existe."""
    (RUTA_RAIZ / CATEGORIAS["PROMPT"]).mkdir(parents=True, exist_ok=True)

    subcarpetas = sorted(set(MAPA_CODIGOS.values()))
    for categoria in ("MDD", "LOGICA", "CUESTIONARIO"):
        for subcarpeta in subcarpetas:
            (RUTA_RAIZ / CATEGORIAS[categoria] / subcarpeta).mkdir(
                parents=True,
                exist_ok=True,
            )


def nombre_disponible(destino: Path) -> Path:
    """Evita reemplazar archivos existentes agregando _1, _2, etc."""
    if not destino.exists():
        return destino

    contador = 1
    while True:
        candidato = destino.with_name(
            f"{destino.stem}_{contador}{destino.suffix}"
        )
        if not candidato.exists():
            return candidato
        contador += 1


def esta_dentro_de_carpeta_organizada(archivo: Path) -> bool:
    """Indica si el archivo ya se encuentra en una carpeta final."""
    try:
        partes = archivo.relative_to(RUTA_RAIZ).parts[:-1]
    except ValueError:
        return False

    return any(parte.upper() in CARPETAS_ORGANIZADAS for parte in partes)


def obtener_archivos():
    """Obtiene archivos pendientes, incluyendo formatos distintos de .py."""
    script_actual = Path(__file__).resolve()

    for archivo in RUTA_RAIZ.rglob("*"):
        if not archivo.is_file():
            continue
        if archivo.resolve() == script_actual:
            continue
        if archivo.suffix.lower() in EXTENSIONES_IGNORADAS:
            continue
        if esta_dentro_de_carpeta_organizada(archivo):
            continue
        yield archivo


def organizar_archivos() -> None:
    movidos = 0
    omitidos = 0
    errores = 0

    print(f"Carpeta raiz: {RUTA_RAIZ}")
    print(f"Modo prueba: {'SI' if MODO_PRUEBA else 'NO'}")
    print("-" * 78)

    # En modo real crea toda la estructura antes de organizar.
    if not MODO_PRUEBA:
        crear_estructura()

    archivos = list(obtener_archivos())

    if not archivos:
        print("No se encontraron archivos pendientes de organizar.")
        return

    for archivo in archivos:
        categoria = detectar_categoria(archivo.name)

        if not categoria:
            print(f"[OMITIDO] No se detecto categoria: {archivo.name}")
            omitidos += 1
            continue

        # Los archivos PROMPT van directamente a 1_PROMPT.
        if categoria == "PROMPT":
            carpeta_destino = RUTA_RAIZ / CATEGORIAS[categoria]
        else:
            subcarpeta = detectar_subcarpeta(archivo.name)
            if not subcarpeta:
                print(f"[OMITIDO] No se detecto codigo: {archivo.name}")
                omitidos += 1
                continue

            carpeta_destino = (
                RUTA_RAIZ / CATEGORIAS[categoria] / subcarpeta
            )

        destino = nombre_disponible(carpeta_destino / archivo.name)

        try:
            origen_relativo = archivo.relative_to(RUTA_RAIZ)
            destino_relativo = destino.relative_to(RUTA_RAIZ)

            if MODO_PRUEBA:
                print(f"[PRUEBA] {origen_relativo} -> {destino_relativo}")
            else:
                carpeta_destino.mkdir(parents=True, exist_ok=True)
                shutil.move(str(archivo), str(destino))
                print(f"[MOVIDO] {origen_relativo} -> {destino_relativo}")

            movidos += 1

        except (OSError, shutil.Error) as error:
            print(f"[ERROR] {archivo.name}: {error}")
            errores += 1

    print("-" * 78)
    etiqueta = "Detectados para mover" if MODO_PRUEBA else "Movidos"
    print(f"{etiqueta}: {movidos}")
    print(f"Omitidos: {omitidos}")
    print(f"Errores: {errores}")


if __name__ == "__main__":
    organizar_archivos()
