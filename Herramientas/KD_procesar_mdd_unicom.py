#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesamiento unificado de archivos MDD mediante UNICOM.

Para cada archivo .mdd:
1. Lo abre una sola vez en UNICOM Intelligence Professional.
2. Copia una sola vez todo el contenido visible.
3. Extrae _Osm_AdvancedScript y genera un archivo .js.
4. Elimina el bloque completo HData y genera un archivo .txt.
5. Registra los resultados de ambas tareas en un reporte consolidado.

Requisitos:
    Windows
    UNICOM asociado con la extensión .mdd
    pip install pyautogui pyperclip pywin32

Uso:
    python procesar_mdd_unificado_unicom.py
    python procesar_mdd_unificado_unicom.py "C:\\ruta\\a\\carpeta"
"""

from pathlib import Path
import os
import re
import sys
import time

import pyautogui
import pyperclip
import win32api
import win32con
import win32gui
import win32process


# ============================================================
# CONFIGURACIÓN
# ============================================================
EXTENSION = ".mdd"
NOMBRE_CARPETA_SALIDA = "MDD_PROCESADOS"
NOMBRE_SUBCARPETA_JS = "JS_EXTRAIDOS"
NOMBRE_SUBCARPETA_TXT = "TXT_SIN_HDATA"
NOMBRE_SUBCARPETA_DIAGNOSTICO = "DIAGNOSTICOS"
NOMBRE_REPORTE = "REPORTE_PROCESAMIENTO_UNIFICADO.txt"

TIEMPO_MAXIMO_APERTURA = 45
ESPERA_DESPUES_DE_CARGAR = 4
ESPERA_DESPUES_CLIC = 1
TIEMPO_MAXIMO_PORTAPAPELES = 20
ESPERA_ENTRE_ARCHIVOS = 2

POSICION_X = 0.50
POSICION_Y = 0.55

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.25

PATRON_ADVANCED_INICIO = re.compile(
    r'_Osm_AdvancedScript\s*=\s*"',
    re.IGNORECASE,
)
PATRON_ADVANCED_FIN = re.compile(
    r'"\s*,?\s*(?=_Osm_GlobalizationType\s*=)',
    re.IGNORECASE | re.DOTALL,
)
PATRON_HDATA = re.compile(
    r"(?im)^[ \t]*HData[ \t]*(?:-|=)?[ \t]*\n?[ \t]*\["
)


# ============================================================
# AUTOMATIZACIÓN DE VENTANAS
# ============================================================
def liberar_teclas():
    for tecla in ("ctrl", "shift", "alt"):
        try:
            pyautogui.keyUp(tecla)
        except Exception:
            pass


def normalizar_texto(texto):
    return texto.strip().lower()


def obtener_titulo(hwnd):
    try:
        return win32gui.GetWindowText(hwnd).strip()
    except Exception:
        return ""


def ventana_visible(hwnd):
    try:
        if not hwnd or not win32gui.IsWindow(hwnd):
            return False
        if not win32gui.IsWindowVisible(hwnd):
            return False
        izquierda, arriba, derecha, abajo = win32gui.GetWindowRect(hwnd)
        return derecha > izquierda and abajo > arriba
    except Exception:
        return False


def enumerar_ventanas():
    resultados = []

    def callback(hwnd, lista):
        if ventana_visible(hwnd):
            titulo = obtener_titulo(hwnd)
            if titulo:
                lista.append((hwnd, titulo))

    win32gui.EnumWindows(callback, resultados)
    return resultados


def titulo_corresponde_archivo(titulo, archivo):
    titulo_normalizado = normalizar_texto(titulo)
    if not titulo_normalizado or "splashscreen" in titulo_normalizado:
        return False
    if "unicom intelligence professional" not in titulo_normalizado:
        return False
    return (
        normalizar_texto(archivo.name) in titulo_normalizado
        or normalizar_texto(archivo.stem) in titulo_normalizado
    )


def buscar_ventana_del_archivo(archivo, tiempo_maximo):
    inicio = time.time()
    ultimo_titulo = ""

    while time.time() - inicio < tiempo_maximo:
        for hwnd, titulo in enumerar_ventanas():
            if "unicom intelligence professional" in normalizar_texto(titulo):
                ultimo_titulo = titulo
                if titulo_corresponde_archivo(titulo, archivo):
                    print()
                    return hwnd

        transcurrido = int(time.time() - inicio)
        print(
            f"\rEsperando UNICOM: {transcurrido}/{tiempo_maximo} segundos",
            end="",
            flush=True,
        )
        time.sleep(0.5)

    print()
    if ultimo_titulo:
        print(f"Último título de UNICOM detectado: {ultimo_titulo}")
    return None


def activar_ventana(hwnd, maximizar=True):
    if not ventana_visible(hwnd):
        return False

    liberar_teclas()
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        time.sleep(0.4)
        if maximizar:
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            time.sleep(0.5)
        pyautogui.press("alt")
        time.sleep(0.2)
        win32gui.BringWindowToTop(hwnd)
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(1)
        return win32gui.GetForegroundWindow() == hwnd
    except Exception:
        try:
            hwnd_actual = win32gui.GetForegroundWindow()
            hilo_actual, _ = win32process.GetWindowThreadProcessId(hwnd_actual)
            hilo_objetivo, _ = win32process.GetWindowThreadProcessId(hwnd)
            unidos = False
            try:
                if hilo_actual != hilo_objetivo:
                    win32process.AttachThreadInput(
                        hilo_actual, hilo_objetivo, True
                    )
                    unidos = True
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                if maximizar:
                    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                win32gui.BringWindowToTop(hwnd)
                win32gui.SetForegroundWindow(hwnd)
            finally:
                if unidos:
                    win32process.AttachThreadInput(
                        hilo_actual, hilo_objetivo, False
                    )
            time.sleep(1)
            return win32gui.GetForegroundWindow() == hwnd
        except Exception:
            return False


def hacer_clic_dentro_de_ventana(hwnd):
    izquierda, arriba, derecha, abajo = win32gui.GetWindowRect(hwnd)
    x = izquierda + int((derecha - izquierda) * POSICION_X)
    y = arriba + int((abajo - arriba) * POSICION_Y)
    win32api.SetCursorPos((x, y))
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def esperar_portapapeles(marcador, tiempo_maximo):
    inicio = time.time()
    while time.time() - inicio < tiempo_maximo:
        try:
            contenido = pyperclip.paste()
            if contenido and contenido != marcador:
                return contenido
        except Exception:
            pass
        time.sleep(0.25)
    return None


def abrir_y_localizar_archivo(archivo):
    print(f"Abriendo: {archivo.name}")
    try:
        os.startfile(str(archivo.resolve()))
    except Exception as error:
        return None, f"No se pudo abrir el archivo: {error}"

    hwnd = buscar_ventana_del_archivo(archivo, TIEMPO_MAXIMO_APERTURA)
    if hwnd is None:
        return None, "UNICOM no mostró el archivo dentro del tiempo permitido."
    return hwnd, "Archivo abierto correctamente."


def copiar_contenido_unicom(hwnd, archivo, hwnd_consola):
    if not titulo_corresponde_archivo(obtener_titulo(hwnd), archivo):
        return None, "La ventana de UNICOM no corresponde al MDD solicitado."

    if not activar_ventana(hwnd, maximizar=True):
        return None, "No se pudo activar la ventana de UNICOM."

    if win32gui.GetForegroundWindow() == hwnd_consola:
        return None, "La consola continuó activa; se canceló la copia."

    print(f"Esperando {ESPERA_DESPUES_DE_CARGAR} segundos para cargar...")
    time.sleep(ESPERA_DESPUES_DE_CARGAR)
    hacer_clic_dentro_de_ventana(hwnd)
    time.sleep(ESPERA_DESPUES_CLIC)

    if win32gui.GetForegroundWindow() != hwnd:
        return None, "UNICOM perdió el foco después del clic."

    marcador = f"__COPIA_PENDIENTE_{time.time()}__"
    pyperclip.copy(marcador)
    print("Seleccionando y copiando una sola vez el contenido de UNICOM...")
    pyautogui.hotkey("ctrl", "a")
    liberar_teclas()
    time.sleep(1)

    if win32gui.GetForegroundWindow() != hwnd:
        return None, "UNICOM perdió el foco antes de copiar."

    pyautogui.hotkey("ctrl", "c")
    liberar_teclas()
    contenido = esperar_portapapeles(marcador, TIEMPO_MAXIMO_PORTAPAPELES)

    if contenido is None:
        return None, "No se obtuvo contenido nuevo desde el portapapeles."
    if not contenido.strip():
        return None, "El contenido copiado está vacío."
    return contenido, "Contenido copiado correctamente."


# ============================================================
# TRANSFORMACIONES
# ============================================================
def limpiar_texto(texto):
    return (
        texto.replace("\ufeff", "")
        .replace("\x00", "")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
    )


def _es_cierre_advanced_script(texto, posicion_comilla):
    """Valida si una comilla impar cierra el valor MDD de AdvancedScript."""
    resto = texto[posicion_comilla + 1:]

    # Después del valor puede comenzar cualquier propiedad del HData,
    # no necesariamente _Osm_GlobalizationType, o puede cerrarse el bloque.
    patron_siguiente = re.compile(
        r"(?is)^\s*,?\s*(?:\n\s*)?"
        r"(?=(?:_[A-Za-z][A-Za-z0-9_]*\s*=)|(?:\]))"
    )
    return patron_siguiente.match(resto) is not None


def _buscar_cierre_cadena_mdd(texto, inicio_contenido):
    """Busca la comilla externa respetando comillas MDD duplicadas.

    En MDD, una comilla contenida dentro del texto se representa como "".
    Una secuencia impar tiene una comilla externa al final; solo se acepta
    como cierre si después empieza otra propiedad o termina el bloque HData.
    """
    posicion = inicio_contenido
    longitud = len(texto)

    while posicion < longitud:
        if texto[posicion] != '"':
            posicion += 1
            continue

        fin_racha = posicion
        while fin_racha < longitud and texto[fin_racha] == '"':
            fin_racha += 1

        cantidad = fin_racha - posicion
        if cantidad % 2 == 1:
            candidata = fin_racha - 1
            if _es_cierre_advanced_script(texto, candidata):
                return candidata

        posicion = fin_racha

    return None


def extraer_advanced_script(texto):
    """Extrae AdvancedScript sin depender de GlobalizationType.

    Admite:
    - comillas internas duplicadas: "";
    - cierre antes de cualquier propiedad _Osm_* u otra propiedad con _;
    - cierre directo del bloque HData;
    - variantes de espacios, saltos de línea y coma separadora.
    """
    texto = limpiar_texto(texto)
    candidatos = []
    inicios = list(PATRON_ADVANCED_INICIO.finditer(texto))

    if not inicios:
        tiene_hdata = bool(re.search(r'(?im)^\s*HData\s*(?:-|=)?\s*\[', texto))
        detalle = (
            "Se detectó HData, pero no contiene _Osm_AdvancedScript."
            if tiene_hdata else
            "La copia no contiene HData ni _Osm_AdvancedScript; "
            "probablemente UNICOM copió otra vista o aún no había terminado de cargar."
        )
        raise ValueError(detalle)

    errores = []
    for numero, inicio in enumerate(inicios, start=1):
        fin = _buscar_cierre_cadena_mdd(texto, inicio.end())
        if fin is None:
            muestra = texto[inicio.start():inicio.start() + 180].replace('\n', '\\n')
            errores.append(f"aparición {numero}: cierre no reconocido; inicio={muestra!r}")
            continue

        javascript = texto[inicio.end():fin]
        javascript = javascript.replace('""', '"').strip("\n")
        if javascript.strip():
            candidatos.append((numero, javascript + "\n"))

    if not candidatos:
        raise ValueError(
            f"Se encontraron {len(inicios)} apariciones de _Osm_AdvancedScript, "
            "pero no se reconoció un cierre MDD válido. " + " | ".join(errores)
        )

    numero, javascript = max(candidatos, key=lambda item: len(item[1]))
    return javascript, numero, len(inicios)

def eliminar_hdata(texto):
    """Elimina HData - [contenido], incluso si hay corchetes anidados."""
    texto = limpiar_texto(texto)
    posicion = 0
    partes = []
    bloques_eliminados = 0

    while True:
        coincidencia = PATRON_HDATA.search(texto, posicion)
        if not coincidencia:
            partes.append(texto[posicion:])
            break

        inicio_bloque = coincidencia.start()
        inicio_corchete = texto.find("[", coincidencia.start(), coincidencia.end())
        profundidad = 0
        dentro_cadena = False
        escape = False
        fin_bloque = None

        for indice in range(inicio_corchete, len(texto)):
            caracter = texto[indice]
            if dentro_cadena:
                if escape:
                    escape = False
                elif caracter == "\\":
                    escape = True
                elif caracter == '"':
                    dentro_cadena = False
                continue

            if caracter == '"':
                dentro_cadena = True
            elif caracter == "[":
                profundidad += 1
            elif caracter == "]":
                profundidad -= 1
                if profundidad == 0:
                    fin_bloque = indice + 1
                    break

        if fin_bloque is None:
            raise ValueError("Se encontró HData, pero su bloque [ ... ] no está cerrado.")

        partes.append(texto[posicion:inicio_bloque])
        posicion = fin_bloque
        bloques_eliminados += 1

        while posicion < len(texto) and texto[posicion] in " \t":
            posicion += 1
        if posicion < len(texto) and texto[posicion] == ";":
            posicion += 1
        while posicion < len(texto) and texto[posicion] in " \t":
            posicion += 1
        if posicion < len(texto) and texto[posicion] == "\n":
            posicion += 1

    resultado = "".join(partes)
    resultado = re.sub(r"[ \t]+\n", "\n", resultado)
    resultado = re.sub(r"\n{3,}", "\n\n", resultado)
    return resultado.strip() + "\n", bloques_eliminados


# ============================================================
# PROCESAMIENTO
# ============================================================
def buscar_archivos_mdd(carpeta):
    return sorted(
        archivo
        for archivo in carpeta.iterdir()
        if archivo.is_file() and archivo.suffix.lower() == EXTENSION
    )


def guardar_diagnostico(carpeta, archivo, contenido):
    destino = carpeta / f"{archivo.stem}_CONTENIDO_COPIADO.txt"
    destino.write_text(contenido, encoding="utf-8-sig", newline="\n")
    return destino


def procesar_archivo(
    archivo,
    carpeta_js,
    carpeta_txt,
    carpeta_diagnostico,
    hwnd_consola,
    numero,
    total,
):
    print()
    print("=" * 72)
    print(f"[{numero}/{total}] {archivo.name}")
    print("=" * 72)

    resultado = {
        "archivo": archivo,
        "copia": False,
        "js": False,
        "txt": False,
        "destino_js": None,
        "destino_txt": None,
        "error_copia": "",
        "error_js": "",
        "error_txt": "",
        "apariciones": 0,
        "aparicion_usada": 0,
        "bloques_hdata": 0,
    }

    hwnd, razon = abrir_y_localizar_archivo(archivo)
    if hwnd is None:
        resultado["error_copia"] = razon
        return resultado

    contenido, razon = copiar_contenido_unicom(hwnd, archivo, hwnd_consola)
    if contenido is None:
        resultado["error_copia"] = razon
        return resultado

    resultado["copia"] = True
    diagnostico_guardado = None

    try:
        javascript, aparicion, total_apariciones = extraer_advanced_script(contenido)
        destino_js = carpeta_js / f"{archivo.stem}.js"
        destino_js.write_text(javascript, encoding="utf-8", newline="\n")
        resultado["js"] = True
        resultado["destino_js"] = destino_js
        resultado["apariciones"] = total_apariciones
        resultado["aparicion_usada"] = aparicion
        print(f"JS generado: {destino_js}")
        print(
            f"AdvancedScript: {total_apariciones} apariciones; "
            f"se utilizó la {aparicion}."
        )
    except Exception as error:
        resultado["error_js"] = str(error)
        print(f"ERROR JS: {error}")

    try:
        contenido_sin_hdata, bloques_hdata = eliminar_hdata(contenido)
        destino_txt = carpeta_txt / f"{archivo.stem}.txt"
        destino_txt.write_text(
            contenido_sin_hdata,
            encoding="utf-8-sig",
            newline="\n",
        )
        resultado["txt"] = True
        resultado["destino_txt"] = destino_txt
        resultado["bloques_hdata"] = bloques_hdata
        print(f"TXT generado: {destino_txt}")
        print(f"Bloques HData eliminados: {bloques_hdata}")
    except Exception as error:
        resultado["error_txt"] = str(error)
        print(f"ERROR TXT: {error}")

    if not resultado["js"] or not resultado["txt"]:
        diagnostico_guardado = guardar_diagnostico(
            carpeta_diagnostico, archivo, contenido
        )
        print(f"Diagnóstico guardado: {diagnostico_guardado}")

    time.sleep(ESPERA_ENTRE_ARCHIVOS)
    return resultado



def seleccionar_archivos(archivos, nombre_solicitado=None):
    """Selecciona todos los MDD o uno solo por nombre/ruta/stem.

    Prioridad:
    1. Ruta exacta existente.
    2. Nombre exacto, sin distinguir mayúsculas.
    3. Stem exacto, permitiendo omitir .mdd.
    4. Coincidencia parcial única.
    """
    if not nombre_solicitado:
        return archivos

    solicitado = str(nombre_solicitado).strip().strip('"').strip("'")
    ruta = Path(solicitado).expanduser()

    if ruta.is_file():
        if ruta.suffix.lower() != EXTENSION:
            raise ValueError(f"El archivo indicado no tiene extensión {EXTENSION}: {ruta}")
        return [ruta.resolve()]

    objetivo = solicitado.casefold()
    objetivo_stem = Path(solicitado).stem.casefold()

    exactos = [
        archivo for archivo in archivos
        if archivo.name.casefold() == objetivo
        or archivo.stem.casefold() == objetivo
        or archivo.stem.casefold() == objetivo_stem
    ]
    if len(exactos) == 1:
        return exactos
    if len(exactos) > 1:
        nombres = "\n".join(f"  - {a.name}" for a in exactos)
        raise ValueError(f"El nombre coincide con más de un archivo:\n{nombres}")

    parciales = [
        archivo for archivo in archivos
        if objetivo in archivo.name.casefold()
        or objetivo_stem in archivo.stem.casefold()
    ]
    if len(parciales) == 1:
        return parciales
    if len(parciales) > 1:
        nombres = "\n".join(f"  - {a.name}" for a in parciales)
        raise ValueError(
            "El texto indicado coincide con varios archivos. "
            f"Escriba un nombre más preciso:\n{nombres}"
        )

    disponibles = "\n".join(f"  - {a.name}" for a in archivos)
    raise ValueError(
        f"No se encontró el MDD solicitado: {solicitado}\n"
        f"Archivos disponibles:\n{disponibles}"
    )


def resultado_tiene_error(resultado):
    """Un caso es erróneo si falló la copia, el JS o el TXT."""
    return not (
        resultado.get("copia", False)
        and resultado.get("js", False)
        and resultado.get("txt", False)
    )


def describir_error(resultado):
    errores = []
    if resultado.get("error_copia"):
        errores.append(f"copia: {resultado['error_copia']}")
    if resultado.get("error_js"):
        errores.append(f"JS: {resultado['error_js']}")
    if resultado.get("error_txt"):
        errores.append(f"TXT: {resultado['error_txt']}")
    if not errores:
        if not resultado.get("copia"):
            errores.append("copia incompleta")
        if not resultado.get("js"):
            errores.append("JS no generado")
        if not resultado.get("txt"):
            errores.append("TXT no generado")
    return " | ".join(errores)


def mostrar_casos_con_error(resultados, numero_ronda):
    fallidos = [r for r in resultados if resultado_tiene_error(r)]
    if not fallidos:
        return []

    print()
    print("=" * 72)
    print(f"CASOS CON ERROR DESPUÉS DE LA RONDA {numero_ronda}")
    print("=" * 72)
    for indice, resultado in enumerate(fallidos, start=1):
        print(f"{indice}. {resultado['archivo'].name}")
        print(f"   {describir_error(resultado)}")
    return fallidos


def solicitar_reintentos(fallidos):
    """Permite reintentar todos, algunos por número, o terminar."""
    print()
    print("Opciones:")
    print("  T o ENTER  = reintentar todos los casos con error")
    print("  1,3,5      = reintentar solo esos números")
    print("  N          = terminar sin más reintentos")

    while True:
        try:
            respuesta = input("Seleccione una opción: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nNo se realizarán más reintentos.")
            return []

        if not respuesta or respuesta.casefold() in {"t", "todos", "s", "si", "sí"}:
            return fallidos
        if respuesta.casefold() in {"n", "no", "salir", "q"}:
            return []

        partes = [p.strip() for p in respuesta.split(",") if p.strip()]
        try:
            indices = sorted(set(int(p) for p in partes))
        except ValueError:
            print("Opción inválida. Use T, N o números separados por comas.")
            continue

        if not indices or any(i < 1 or i > len(fallidos) for i in indices):
            print(f"Los números deben estar entre 1 y {len(fallidos)}.")
            continue
        return [fallidos[i - 1] for i in indices]


def combinar_resultado_anterior(anterior, nuevo):
    """Conserva salidas correctas previas cuando el reintento es parcial."""
    combinado = dict(nuevo)
    for tipo, destino, error in (
        ("js", "destino_js", "error_js"),
        ("txt", "destino_txt", "error_txt"),
    ):
        if anterior.get(tipo) and not nuevo.get(tipo):
            combinado[tipo] = True
            combinado[destino] = anterior.get(destino)
            combinado[error] = ""

    combinado["copia"] = anterior.get("copia", False) or nuevo.get("copia", False)
    if combinado["copia"]:
        combinado["error_copia"] = ""
    return combinado


def ejecutar_ronda(archivos, carpeta_js, carpeta_txt, carpeta_diagnostico,
                    hwnd_consola, numero_ronda):
    resultados = []
    total = len(archivos)
    print()
    print("#" * 72)
    print(f"RONDA DE PROCESAMIENTO {numero_ronda} | ARCHIVOS: {total}")
    print("#" * 72)

    for numero, archivo in enumerate(archivos, start=1):
        resultado = procesar_archivo(
            archivo,
            carpeta_js,
            carpeta_txt,
            carpeta_diagnostico,
            hwnd_consola,
            numero,
            total,
        )
        resultados.append(resultado)
    return resultados

def crear_reporte(carpeta_salida, carpeta_entrada, archivos, resultados):
    completos = sum(r["js"] and r["txt"] for r in resultados)
    parciales = sum(r["copia"] and (r["js"] != r["txt"]) for r in resultados)
    fallidos = len(resultados) - completos - parciales
    js_generados = sum(r["js"] for r in resultados)
    txt_generados = sum(r["txt"] for r in resultados)

    lineas = [
        "=" * 80,
        "REPORTE DE PROCESAMIENTO UNIFICADO DE ARCHIVOS MDD",
        "=" * 80,
        f"Carpeta de entrada: {carpeta_entrada}",
        f"MDD encontrados: {len(archivos)}",
        f"Procesados completamente: {completos}",
        f"Procesados parcialmente: {parciales}",
        f"Fallidos: {fallidos}",
        f"JS generados: {js_generados}",
        f"TXT generados: {txt_generados}",
        "",
        "DETALLE POR ARCHIVO",
        "-" * 80,
    ]

    for indice, resultado in enumerate(resultados, start=1):
        lineas.extend(
            [
                f"{indice}. {resultado['archivo'].name}",
                f"   Copia desde UNICOM: {'OK' if resultado['copia'] else 'ERROR'}",
                f"   JS AdvancedScript: {'OK' if resultado['js'] else 'ERROR'}",
                f"   TXT sin HData: {'OK' if resultado['txt'] else 'ERROR'}",
            ]
        )
        if resultado["destino_js"]:
            lineas.append(f"   Destino JS: {resultado['destino_js']}")
        if resultado["destino_txt"]:
            lineas.append(f"   Destino TXT: {resultado['destino_txt']}")
        if resultado["js"]:
            lineas.append(
                "   AdvancedScript: "
                f"{resultado['apariciones']} apariciones; "
                f"usada {resultado['aparicion_usada']}"
            )
        if resultado["txt"]:
            lineas.append(
                f"   Bloques HData eliminados: {resultado['bloques_hdata']}"
            )
        if resultado["error_copia"]:
            lineas.append(f"   Error de copia: {resultado['error_copia']}")
        if resultado["error_js"]:
            lineas.append(f"   Error JS: {resultado['error_js']}")
        if resultado["error_txt"]:
            lineas.append(f"   Error TXT: {resultado['error_txt']}")
        lineas.append("")

    reporte = carpeta_salida / NOMBRE_REPORTE
    reporte.write_text(
        "\n".join(lineas).rstrip() + "\n",
        encoding="utf-8-sig",
        newline="\n",
    )
    return reporte, completos, parciales, fallidos, js_generados, txt_generados


def main():
    # Sin argumento: procesa todos los MDD de la carpeta actual.
    # Con argumento: procesa únicamente el archivo solicitado.
    nombre_solicitado = sys.argv[1] if len(sys.argv) >= 2 else None

    if nombre_solicitado and Path(nombre_solicitado).expanduser().is_file():
        ruta_indicada = Path(nombre_solicitado).expanduser().resolve()
        carpeta_entrada = ruta_indicada.parent
    else:
        carpeta_entrada = Path.cwd()

    if not carpeta_entrada.is_dir():
        print(f"ERROR: La carpeta no existe: {carpeta_entrada}")
        return 1

    archivos_disponibles = buscar_archivos_mdd(carpeta_entrada)
    if not archivos_disponibles:
        print(f"No se encontraron archivos .mdd en: {carpeta_entrada}")
        return 0

    try:
        archivos = seleccionar_archivos(archivos_disponibles, nombre_solicitado)
    except ValueError as error:
        print(f"ERROR: {error}")
        return 2

    carpeta_salida = carpeta_entrada / NOMBRE_CARPETA_SALIDA
    carpeta_js = carpeta_salida / NOMBRE_SUBCARPETA_JS
    carpeta_txt = carpeta_salida / NOMBRE_SUBCARPETA_TXT
    carpeta_diagnostico = carpeta_salida / NOMBRE_SUBCARPETA_DIAGNOSTICO

    carpeta_js.mkdir(parents=True, exist_ok=True)
    carpeta_txt.mkdir(parents=True, exist_ok=True)
    carpeta_diagnostico.mkdir(parents=True, exist_ok=True)

    hwnd_consola = win32gui.GetForegroundWindow()

    print("=" * 72)
    print("PROCESAMIENTO UNIFICADO DE MDD MEDIANTE UNICOM")
    print("=" * 72)
    print(f"Carpeta de entrada: {carpeta_entrada}")
    print(f"Carpeta de salida:  {carpeta_salida}")
    if nombre_solicitado:
        print(f"Modo:                UN SOLO ARCHIVO")
        print(f"Archivo:             {archivos[0].name}")
    else:
        print(f"Modo:                TODOS LOS ARCHIVOS")
        print(f"MDD encontrados:     {len(archivos)}")
    print("Cada MDD se abrirá y copiará una sola vez por intento.")
    print("No use el mouse ni el teclado durante la automatización.")
    print("El proceso comenzará en 5 segundos...")
    time.sleep(5)

    resultados_por_archivo = {}
    numero_ronda = 1
    archivos_ronda = archivos
    interrumpido = False

    try:
        while archivos_ronda:
            resultados_ronda = ejecutar_ronda(
                archivos_ronda,
                carpeta_js,
                carpeta_txt,
                carpeta_diagnostico,
                hwnd_consola,
                numero_ronda,
            )

            for nuevo in resultados_ronda:
                clave = str(nuevo["archivo"].resolve()).casefold()
                anterior = resultados_por_archivo.get(clave)
                resultados_por_archivo[clave] = (
                    combinar_resultado_anterior(anterior, nuevo)
                    if anterior else nuevo
                )

            resultados_actuales = [
                resultados_por_archivo[str(a.resolve()).casefold()]
                for a in archivos
            ]
            fallidos = mostrar_casos_con_error(resultados_actuales, numero_ronda)

            if not fallidos:
                print("\nTodos los archivos finalizaron correctamente.")
                break

            seleccionados = solicitar_reintentos(fallidos)
            if not seleccionados:
                break

            archivos_ronda = [r["archivo"] for r in seleccionados]
            numero_ronda += 1
            print("\nEl reintento comenzará en 3 segundos...")
            time.sleep(3)

    except KeyboardInterrupt:
        interrumpido = True
        print("\nProceso interrumpido por el usuario.")
    finally:
        liberar_teclas()

    resultados = [
        resultados_por_archivo[str(a.resolve()).casefold()]
        for a in archivos
        if str(a.resolve()).casefold() in resultados_por_archivo
    ]

    reporte, completos, parciales, fallidos, js_generados, txt_generados = (
        crear_reporte(carpeta_salida, carpeta_entrada, archivos, resultados)
    )

    activar_ventana(hwnd_consola, maximizar=False)

    print()
    print("=" * 72)
    print("PROCESO FINALIZADO" if not interrumpido else "PROCESO INTERRUMPIDO")
    print("=" * 72)
    print(f"Rondas ejecutadas:         {numero_ronda}")
    print(f"Procesados completamente:  {completos}")
    print(f"Procesados parcialmente:   {parciales}")
    print(f"Fallidos:                  {fallidos}")
    print(f"JS generados:              {js_generados}")
    print(f"TXT generados:             {txt_generados}")
    print(f"Reporte:                    {reporte}")

    return 1 if interrumpido or parciales or fallidos else 0

if __name__ == "__main__":
    raise SystemExit(main())
