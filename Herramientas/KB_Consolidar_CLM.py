#!/usr/bin/env python3
"""
Consolida los archivos de una carpeta en exactamente tres salidas:

1. CUESTIONARIO_UNIDO.md  <- convierte y une todos los DOCX
2. LOGICA_UNIDA.txt       <- une directamente todos los JS como texto
3. MDD_UNIDO.txt          <- une todos los TXT de MDD

No crea archivos intermedios ni modifica los originales.

Requisito:
    pip install python-docx

Uso:
    python consolidar_inn.py "C:\ruta\INN"

Si no se indica una ruta, procesa la carpeta donde está el script.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable

try:
    from docx import Document
    from docx.document import Document as DocumentType
    from docx.table import Table
    from docx.text.paragraph import Paragraph
except ImportError:
    print(
        "ERROR: Falta la librería python-docx. "
        "Instálala con: pip install python-docx",
        file=sys.stderr,
    )
    raise SystemExit(1)


SALIDA_CUESTIONARIO = "1_CUESTIONARIO_UNIDO.md"
SALIDA_LOGICA = "2_LOGICA_UNIDA.txt"
SALIDA_MDD = "3_MDD_UNIDO.txt"
SALIDAS = {SALIDA_CUESTIONARIO, SALIDA_LOGICA, SALIDA_MDD}


def ordenar_archivos(archivos: Iterable[Path]) -> list[Path]:
    """Ordena de manera natural, considerando correctamente los números."""
    def clave(path: Path):
        return [
            int(fragmento) if fragmento.isdigit() else fragmento.lower()
            for fragmento in re.split(r"(\d+)", path.name)
        ]

    return sorted(archivos, key=clave)


def leer_texto(path: Path) -> str:
    """Lee un archivo probando codificaciones habituales en Windows."""
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue

    return path.read_text(encoding="utf-8", errors="replace")


def limpiar_markdown(texto: str) -> str:
    """Escapa caracteres que podrían romper una tabla Markdown."""
    return texto.replace("|", r"\|").replace("\r", "").replace("\n", "<br>").strip()


def texto_parrafo(parrafo: Paragraph) -> str:
    """Convierte el contenido básico de un párrafo a Markdown."""
    partes: list[str] = []

    for run in parrafo.runs:
        texto = run.text
        if not texto:
            continue

        # Conserva énfasis básicos sin generar archivos auxiliares.
        if run.bold and run.italic:
            texto = f"***{texto}***"
        elif run.bold:
            texto = f"**{texto}**"
        elif run.italic:
            texto = f"*{texto}*"
        if run.underline:
            texto = f"<u>{texto}</u>"

        partes.append(texto)

    return "".join(partes).strip()


def iterar_bloques(documento: DocumentType):
    """Recorre párrafos y tablas en el mismo orden en que aparecen."""
    for elemento in documento.element.body.iterchildren():
        if elemento.tag.endswith("}p"):
            yield Paragraph(elemento, documento)
        elif elemento.tag.endswith("}tbl"):
            yield Table(elemento, documento)


def tabla_a_markdown(tabla: Table) -> str:
    """Convierte una tabla DOCX a una tabla Markdown."""
    filas: list[list[str]] = []

    for fila in tabla.rows:
        celdas = [limpiar_markdown(celda.text) for celda in fila.cells]
        filas.append(celdas)

    if not filas:
        return ""

    columnas = max(len(fila) for fila in filas)
    filas = [fila + [""] * (columnas - len(fila)) for fila in filas]

    lineas = ["| " + " | ".join(filas[0]) + " |"]
    lineas.append("| " + " | ".join(["---"] * columnas) + " |")

    for fila in filas[1:]:
        lineas.append("| " + " | ".join(fila) + " |")

    return "\n".join(lineas)


def parrafo_a_markdown(parrafo: Paragraph) -> str:
    texto = texto_parrafo(parrafo)
    if not texto:
        return ""

    estilo = (parrafo.style.name if parrafo.style else "").lower()

    encabezado = re.search(r"(?:heading|título|titulo)\s*(\d+)", estilo)
    if encabezado:
        nivel = min(max(int(encabezado.group(1)), 1), 6)
        return f"{'#' * nivel} {texto}"

    if "list bullet" in estilo or "viñeta" in estilo or "vineta" in estilo:
        return f"- {texto}"

    if "list number" in estilo or "numerad" in estilo:
        return f"1. {texto}"

    return texto


def docx_a_markdown(path: Path) -> str:
    """Convierte un DOCX a Markdown en memoria."""
    documento = Document(path)
    bloques: list[str] = []

    for bloque in iterar_bloques(documento):
        if isinstance(bloque, Paragraph):
            convertido = parrafo_a_markdown(bloque)
        else:
            convertido = tabla_a_markdown(bloque)

        if convertido:
            bloques.append(convertido)

    return "\n\n".join(bloques).strip()


def encabezado_seccion(nombre_archivo: str, extension_salida: str) -> str:
    if extension_salida == ".md":
        return f"# Archivo: {nombre_archivo}"
    return f"{'=' * 80}\nARCHIVO: {nombre_archivo}\n{'=' * 80}"


def unir_docx(carpeta: Path, salida: Path) -> int:
    archivos = ordenar_archivos(carpeta.glob("*.docx"))
    secciones: list[str] = ["# Cuestionarios consolidados"]

    for archivo in archivos:
        if archivo.name.startswith("~$"):
            continue
        contenido = docx_a_markdown(archivo)
        secciones.append(
            f"{encabezado_seccion(archivo.name, '.md')}\n\n{contenido}"
        )

    salida.write_text("\n\n---\n\n".join(secciones) + "\n", encoding="utf-8")
    return len([a for a in archivos if not a.name.startswith("~$")])


def es_mdd(path: Path) -> bool:
    """Selecciona TXT cuyo nombre termina en _MDD.txt, sin importar mayúsculas."""
    return path.name.lower().endswith("_mdd.txt")


def unir_textos(archivos: Iterable[Path], salida: Path) -> int:
    seleccionados = ordenar_archivos(archivos)
    secciones: list[str] = []

    for archivo in seleccionados:
        contenido = leer_texto(archivo).rstrip()
        secciones.append(
            f"{encabezado_seccion(archivo.name, '.txt')}\n\n{contenido}"
        )

    texto_final = "\n\n".join(secciones)
    if texto_final:
        texto_final += "\n"
    salida.write_text(texto_final, encoding="utf-8")
    return len(seleccionados)


def consolidar(carpeta: Path) -> None:
    salida_cuestionario = carpeta / SALIDA_CUESTIONARIO
    salida_logica = carpeta / SALIDA_LOGICA
    salida_mdd = carpeta / SALIDA_MDD

    cantidad_docx = unir_docx(carpeta, salida_cuestionario)

    # Los JS se leen como texto y se agregan directamente a una única salida TXT.
    # No se crea una copia TXT individual por cada archivo JS.
    archivos_js = [
        path for path in carpeta.iterdir()
        if path.is_file() and path.suffix.lower() == ".js"
    ]
    cantidad_js = unir_textos(archivos_js, salida_logica)

    archivos_mdd = [
        path for path in carpeta.iterdir()
        if path.is_file() and path.name not in SALIDAS and es_mdd(path)
    ]
    cantidad_mdd = unir_textos(archivos_mdd, salida_mdd)

    print("\nProceso completado")
    print("=" * 60)
    print(f"Cuestionarios DOCX unidos: {cantidad_docx}")
    print(f"Salida: {salida_cuestionario}")
    print()
    print(f"Archivos JS unidos:        {cantidad_js}")
    print(f"Salida: {salida_logica}")
    print()
    print(f"Archivos MDD unidos:       {cantidad_mdd}")
    print(f"Salida: {salida_mdd}")


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Genera un consolidado de cuestionario, lógica y MDD."
    )
    parser.add_argument(
        "carpeta",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parent,
        help=(
            "Carpeta que contiene los DOCX, JS y TXT. "
            "Por defecto se usa la carpeta del script."
        ),
    )
    return parser


def main() -> int:
    args = crear_parser().parse_args()
    carpeta = args.carpeta.expanduser().resolve()

    if not carpeta.is_dir():
        print(f"ERROR: La carpeta no existe: {carpeta}", file=sys.stderr)
        return 1

    try:
        consolidar(carpeta)
        return 0
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
