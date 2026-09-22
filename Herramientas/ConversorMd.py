"""
Conversor de documentos a Markdown.

- Para formatos soportados por MarkItDown (PowerPoint, PDF, HTML, CSV, JSON,
  XML, ZIP, EPUB, etc.) usa MarkItDown.
- Para .sav usa pyreadstat y genera un diccionario (codebook) en Markdown
  con etiquetas de variables, tipos, niveles de medición, valores perdidos
  y tablas de etiquetas de valores; los datos se exportan a CSV separado.
- Para .mdd (Unicom Intelligence/Dimensions) usa COM (pywin32) para extraer
  la estructura del cuestionario desde el MDD y, si existe el .ddf hermano,
  los datos de vdata como CSV separado.
- Para .mrs (mrScriptBasic) y .dms (Data Management Script) de Unicom
  Intelligence/Dimensions, que son archivos de texto plano, vuelca el
  contenido del script en un bloque de código Markdown.

Uso básico desde terminal:
    python ConversorMd.py

Uso indicando una carpeta:
    python ConversorMd.py "C:\\ruta\\a\\mi\\carpeta"

Uso con carpeta de salida personalizada:
    python ConversorMd.py "C:\\ruta\\a\\mi\\carpeta" -o "md_salida"

Uso recursivo, incluyendo subcarpetas:
    python ConversorMd.py "C:\\ruta\\a\\mi\\carpeta" -r

Extensiones soportadas por defecto:
    .ppt, .pptx, .pdf, .html, .htm, .csv, .json, .xml, .zip, .epub,
    .sav, .mdd, .mrs, .dms

Requisitos:
    pip install "markitdown[pdf,pptx]" pyreadstat
    # Para .mdd/.ddf:
    # - Windows con Unicom Intelligence instalado:
    pip install pywin32 pandas numpy
    # - Linux: usar WInbase/py-wine.sh con SPSS Data Collection bajo Wine.
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import warnings
from pathlib import Path
from typing import Iterable, Optional

# openpyxl emite UserWarning ruidosos para extensiones de Excel que no
# afectan la conversión a Markdown (Data Validation, Conditional Formatting,
# etc.). Se silencian antes de importar MarkItDown.
warnings.filterwarnings("ignore", category=UserWarning, module=r"openpyxl(\..*)?")

# pydub (dependencia de MarkItDown para audio) avisa al importarse si no
# encuentra ffmpeg/avconv. No afecta la conversión de documentos/scripts.
warnings.filterwarnings("ignore", category=RuntimeWarning, module=r"pydub(\..*)?")

from markitdown import MarkItDown

try:
    import pyreadstat  # type: ignore
    PYREADSTAT_DISPONIBLE = True
except ImportError:
    PYREADSTAT_DISPONIBLE = False

try:
    import win32com.client as _win32  # type: ignore
    import numpy as _np  # type: ignore
    import pandas as _pd  # type: ignore
    MDD_DISPONIBLE = True
except ImportError:
    MDD_DISPONIBLE = False


EXTENSIONES_MARKITDOWN = {
    ".ppt",  ".pptx",
    ".pdf",
    ".html", ".htm",
    ".csv",  ".json", ".xml",
    ".zip",
    ".epub",
}
EXTENSIONES_SPSS = {".sav"}
EXTENSIONES_MDD = {".mdd"}
# Scripts de texto plano de Unicom Intelligence/Dimensions.
# mrScriptBasic -> resaltado tipo VBScript; DMS no tiene resaltado estándar.
EXTENSIONES_SCRIPT = {".mrs": "vbscript", ".dms": "text"}
EXTENSIONES_PERMITIDAS = (
    EXTENSIONES_MARKITDOWN
    | EXTENSIONES_SPSS
    | EXTENSIONES_MDD
    | set(EXTENSIONES_SCRIPT)
)
CARPETA_SALIDA_DEFAULT = "markdown_convertidos"
PY_WINE_ENV = "CONVERSORMD_PY_WINE"
PY_WINE_DEFAULT = Path("/home/rowen/Proyectos/WInbase/py-wine.sh")
MDD_VERSION_WINE = "6.0.1.4.107"


def _obtener_py_wine() -> Optional[Path]:
    """Devuelve el lanzador py-wine.sh si esta disponible."""
    candidatos: list[Path] = []
    if os.environ.get(PY_WINE_ENV):
        candidatos.append(Path(os.environ[PY_WINE_ENV]))
    candidatos.append(PY_WINE_DEFAULT)

    for candidato in candidatos:
        if candidato.is_file():
            return candidato
    return None


def _mdd_backend_disponible() -> bool:
    return MDD_DISPONIBLE or _obtener_py_wine() is not None


def obtener_archivos(
    directorio: Path,
    extensiones: set[str],
    recursivo: bool = False,
) -> list[Path]:
    """
    Obtiene los archivos permitidos dentro del directorio.

    Args:
        directorio: Carpeta donde se buscarán los archivos.
        extensiones: Extensiones permitidas, por ejemplo {".pdf", ".sav", ".mdd"}.
        recursivo: Si es True, busca también dentro de subcarpetas.

    Returns:
        Lista de rutas de archivos encontrados.
    """
    patron = "**/*" if recursivo else "*"

    return sorted(
        archivo
        for archivo in directorio.glob(patron)
        if archivo.is_file()
        and archivo.suffix.lower() in extensiones
        and not archivo.name.startswith("~$")
    )


def construir_ruta_salida(
    archivo: Path,
    directorio_base: Path,
    carpeta_salida: Path,
    recursivo: bool = False,
) -> Path:
    """
    Construye la ruta de salida del archivo Markdown.

    Para .sav y .mdd se conserva la extensión original como parte del nombre
    (``CO26-015551-01.sav.md``, ``CO26-015551-01.mdd.md``) para evitar que
    archivos con el mismo stem pero distinta extensión se sobrescriban entre
    sí (caso típico: un proyecto con .mdd, .ddf y .sav del mismo cuestionario).

    Si el modo recursivo está activo, conserva la estructura relativa
    de subcarpetas dentro de la carpeta de salida.
    """
    extension = archivo.suffix.lower()
    if extension in EXTENSIONES_SPSS | EXTENSIONES_MDD | set(EXTENSIONES_SCRIPT):
        nombre_md = f"{archivo.stem}{extension}.md"
    else:
        nombre_md = f"{archivo.stem}.md"

    if recursivo:
        ruta_relativa = archivo.relative_to(directorio_base)
        return carpeta_salida / ruta_relativa.parent / nombre_md

    return carpeta_salida / nombre_md


def construir_ruta_csv_datos(ruta_md: Path) -> Path:
    """Ruta del CSV de datos asociado a un Markdown de base."""
    return ruta_md.with_suffix(".csv")


def construir_ruta_csv_mdd(ruta_md: Path) -> Path:
    """Ruta del CSV de datos asociado a un Markdown de MDD."""
    return construir_ruta_csv_datos(ruta_md)


def exportar_datos_sav_csv(
    archivo: Path,
    csv_path: Path,
    chunksize: int = 100_000,
) -> tuple[int, int]:
    """Exporta los datos completos de un .sav a CSV por chunks."""
    if not PYREADSTAT_DISPONIBLE:
        raise ImportError(
            "Para convertir archivos .sav se necesita pyreadstat. "
            "Instálalo con: pip install pyreadstat"
        )

    _, meta = pyreadstat.read_sav(
        str(archivo),
        metadataonly=True,
        apply_value_formats=False,
        user_missing=True,
    )

    csv_path.parent.mkdir(parents=True, exist_ok=True)
    total_rows = 0
    total_cols = len(meta.column_names)
    escribio_header = False

    for df, _ in pyreadstat.read_file_in_chunks(
        pyreadstat.read_sav,
        str(archivo),
        chunksize=chunksize,
        apply_value_formats=False,
        user_missing=True,
        dates_as_pandas_datetime=True,
    ):
        modo = "w" if not escribio_header else "a"
        encoding = "utf-8-sig" if not escribio_header else "utf-8"
        df.to_csv(
            csv_path,
            mode=modo,
            header=not escribio_header,
            index=False,
            encoding=encoding,
        )
        escribio_header = True
        total_rows += len(df)
        total_cols = len(df.columns)

    if not escribio_header:
        with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(meta.column_names)

    return total_rows, total_cols


def generar_diccionario_sav(
    archivo: Path,
    csv_path: Optional[Path] = None,
    total_rows_csv: Optional[int] = None,
    total_cols_csv: Optional[int] = None,
) -> str:
    """
    Lee un archivo .sav de SPSS y devuelve su diccionario en formato Markdown.

    El diccionario incluye, por cada variable:
        - Etiqueta de la variable
        - Tipo SPSS original
        - Nivel de medida (nominal, ordinal, escala)
        - Rangos o valores perdidos definidos
        - Tabla de etiquetas de valores (códigos -> etiquetas)

    Args:
        archivo: Ruta al archivo .sav.

    Returns:
        Texto en Markdown con el diccionario.
    """
    if not PYREADSTAT_DISPONIBLE:
        raise ImportError(
            "Para convertir archivos .sav se necesita pyreadstat. "
            "Instálalo con: pip install pyreadstat"
        )

    _, meta = pyreadstat.read_sav(
        str(archivo),
        metadataonly=True,
        apply_value_formats=False,
        user_missing=True,
    )

    lineas: list[str] = []

    # Encabezado general del archivo
    titulo = meta.file_label or archivo.stem
    lineas.append(f"# Diccionario: {titulo}")
    lineas.append("")
    lineas.append(f"- **Archivo:** `{archivo.name}`")
    lineas.append(f"- **Casos:** {meta.number_rows}")
    lineas.append(f"- **Variables:** {meta.number_columns}")
    if meta.file_encoding:
        lineas.append(f"- **Codificación:** {meta.file_encoding}")
    lineas.append("")

    if csv_path:
        lineas.append("## Datos")
        lineas.append("")
        lineas.append(f"- **CSV:** `{csv_path.name}`")
        lineas.append(f"- **Filas:** {total_rows_csv if total_rows_csv is not None else meta.number_rows}")
        lineas.append(f"- **Columnas:** {total_cols_csv if total_cols_csv is not None else meta.number_columns}")
        lineas.append("")

    # Índice de variables
    lineas.append("## Índice de variables")
    lineas.append("")
    lineas.append("| # | Variable | Etiqueta |")
    lineas.append("|---|----------|----------|")
    for i, var in enumerate(meta.column_names, start=1):
        etiqueta = (meta.column_labels[i - 1] or "").replace("|", "\\|")
        lineas.append(f"| {i} | `{var}` | {etiqueta} |")
    lineas.append("")

    # Detalle por variable
    lineas.append("## Detalle por variable")
    lineas.append("")

    for i, var in enumerate(meta.column_names):
        etiqueta = meta.column_labels[i] or "(sin etiqueta)"
        tipo = meta.original_variable_types.get(var, "")
        medida = meta.variable_measure.get(var, "")

        lineas.append(f"### `{var}`")
        lineas.append("")
        lineas.append(f"- **Etiqueta:** {etiqueta}")
        if tipo:
            lineas.append(f"- **Tipo SPSS:** {tipo}")
        if medida:
            lineas.append(f"- **Nivel de medida:** {medida}")

        # Valores perdidos definidos por el usuario
        rangos_perdidos = getattr(meta, "missing_ranges", {}).get(var)
        valores_perdidos = getattr(meta, "missing_user_values", {}).get(var)
        if rangos_perdidos:
            lineas.append(f"- **Rangos perdidos:** {rangos_perdidos}")
        if valores_perdidos:
            lineas.append(f"- **Valores perdidos:** {valores_perdidos}")

        # Etiquetas de valores
        etiquetas_valores = meta.variable_value_labels.get(var)
        if etiquetas_valores:
            lineas.append("- **Valores:**")
            lineas.append("")
            lineas.append("| Código | Etiqueta |")
            lineas.append("|--------|----------|")
            for codigo, etq in etiquetas_valores.items():
                etq_limpia = str(etq).replace("|", "\\|")
                lineas.append(f"| {codigo} | {etq_limpia} |")

        lineas.append("")

    return "\n".join(lineas)


def _parse_row(row: str) -> list[str]:
    row = row.strip()
    if row.startswith('|'):
        row = row[1:]
    if row.endswith('|'):
        row = row[:-1]
    return [cell.strip() for cell in row.split('|')]


def _es_fila_separadora(linea: str) -> bool:
    return bool(re.match(r'^\|[\s\-|:]+\|?\s*$', linea.strip()))


def _procesar_tabla(
    lineas_tabla: list[str],
    rellenar_celdas_vacias: bool = False,
) -> list[str]:
    """Rellena celdas combinadas verticalmente detectadas en Markdown."""
    sep_idx = next(
        (i for i, l in enumerate(lineas_tabla) if _es_fila_separadora(l)), None
    )
    if sep_idx is None:
        return lineas_tabla

    num_cols = len(_parse_row(lineas_tabla[sep_idx]))
    if num_cols == 0:
        return lineas_tabla

    ultimo_valor: list[str] = [''] * num_cols
    resultado: list[str] = []

    for idx, linea in enumerate(lineas_tabla):
        if idx <= sep_idx:
            resultado.append(linea)
            continue

        celdas = _parse_row(linea)

        for col_idx, celda in enumerate(celdas[:num_cols]):
            if celda:
                ultimo_valor[col_idx] = celda

        while len(celdas) < num_cols:
            celdas.append(ultimo_valor[len(celdas)])

        if rellenar_celdas_vacias:
            for col_idx, celda in enumerate(celdas[:num_cols]):
                if not celda and ultimo_valor[col_idx]:
                    celdas[col_idx] = ultimo_valor[col_idx]

        resultado.append('| ' + ' | '.join(celdas[:num_cols]) + ' |')

    return resultado


def rellenar_celdas_combinadas(
    texto: str,
    rellenar_celdas_vacias: bool = False,
) -> str:
    """Repite el contenido de celdas combinadas verticalmente en cada fila afectada."""
    lineas = texto.split('\n')
    resultado: list[str] = []
    i = 0

    while i < len(lineas):
        if lineas[i].strip().startswith('|'):
            j = i
            while j < len(lineas) and lineas[j].strip().startswith('|'):
                j += 1
            bloque = lineas[i:j]
            if any(_es_fila_separadora(l) for l in bloque):
                resultado.extend(
                    _procesar_tabla(
                        bloque,
                        rellenar_celdas_vacias=rellenar_celdas_vacias,
                    )
                )
            else:
                resultado.extend(bloque)
            i = j
        else:
            resultado.append(lineas[i])
            i += 1

    return '\n'.join(resultado)


def _label_mdm(obj) -> str:
    """Extrae texto de etiqueta de un objeto MDM de forma defensiva."""
    try:
        v = getattr(obj, "LabelText", None)
        if isinstance(v, str) and v:
            return v
    except Exception:
        pass
    try:
        lbl = getattr(obj, "Label", None)
        if lbl is not None:
            txt = getattr(lbl, "LabelText", None)
            if isinstance(txt, str) and txt:
                return txt
            return str(lbl)
    except Exception:
        pass
    return ""


def _render_field_mdm(field, lineas: list, depth: int = 0) -> None:
    """
    Renderiza un campo MDM y sus sub-campos de forma recursiva.

    Maneja correctamente loops/grids 2D+: un loop como F6 expone tanto
    ``Categories`` (iteraciones _1.._N) como ``Fields`` (sub-campos por
    iteración, p. ej. ``Rp`` con sus propias categorías Si/No).
    """
    if depth > 8:
        return

    try:
        nombre = field.Name
    except Exception:
        return

    etiqueta = _label_mdm(field)
    nivel = min(depth + 3, 6)  # h3 para top-level, baja un nivel por anidación
    prefijo = "#" * nivel

    lineas.append(f"{prefijo} `{nombre}`")
    lineas.append("")
    if etiqueta:
        lineas.append(f"- **Etiqueta:** {etiqueta}")

    # Categorías (iteraciones de loop o respuestas de categórica)
    try:
        cats = field.Categories
        n_cats = cats.Count
    except Exception:
        n_cats = 0

    if n_cats:
        lineas.append("- **Categorías:**")
        lineas.append("")
        lineas.append("| Código | Etiqueta |")
        lineas.append("|--------|----------|")
        for j in range(n_cats):
            try:
                cat = cats[j]
                cod = cat.Name
                etq = _label_mdm(cat).replace("|", "\\|")
                lineas.append(f"| {cod} | {etq} |")
            except Exception:
                continue
        lineas.append("")

    # Sub-campos (loops/grids/blocks compuestos): recursión
    try:
        subs = field.Fields
        n_subs = subs.Count
    except Exception:
        n_subs = 0

    if n_subs:
        lineas.append(f"- **Sub-campos:** {n_subs}")
        lineas.append("")
        for k in range(n_subs):
            try:
                _render_field_mdm(subs[k], lineas, depth=depth + 1)
            except Exception as exc:
                lineas.append(f"> Error en sub-campo {k}: {exc}")
                lineas.append("")

    if not n_cats and not n_subs:
        lineas.append("")


def _df_a_markdown(df, max_filas: int = 50_000) -> str:
    """Convierte un DataFrame a tabla Markdown sin dependencia de tabulate."""
    if df.empty:
        return "*Sin datos*"
    aviso = ""
    if len(df) > max_filas:
        aviso = (
            f"\n> Tabla truncada a {max_filas:,} de {len(df):,} filas.\n\n"
        )
        df = df.head(max_filas)
    cols = [str(c) for c in df.columns]
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    filas = [
        "| " + " | ".join(_celda_a_str(v) for v in row) + " |"
        for _, row in df.iterrows()
    ]
    return aviso + "\n".join([header, sep] + filas)


def _celda_a_str(v) -> str:
    """Serializa un valor a texto para tabla Markdown, escapando '|'."""
    if v is None:
        return ""
    try:
        # NaN/NaT de pandas
        if _pd.isna(v):
            return ""
    except Exception:
        pass
    return str(v).replace("|", "\\|").replace("\n", " ")


def _sanitizar_columna(valores):
    """
    Convierte una columna cruda de Recordset.GetRows a una lista segura.

    pywintypes.datetime + None mezclados rompen la inferencia de NumPy
    (provoca 'NoneType has no attribute total_seconds'). Se normalizan
    los datetimes a pandas.Timestamp (naive) y se mantienen None.
    """
    out = []
    for v in valores:
        if v is None:
            out.append(None)
            continue
        # pywintypes.datetime expone .year/.month/.day y suele tener tzinfo
        if hasattr(v, "year") and hasattr(v, "month") and hasattr(v, "day"):
            try:
                out.append(
                    _pd.Timestamp(
                        int(v.year), int(v.month), int(v.day),
                        int(getattr(v, "hour", 0) or 0),
                        int(getattr(v, "minute", 0) or 0),
                        int(getattr(v, "second", 0) or 0),
                    )
                )
                continue
            except Exception:
                out.append(str(v))
                continue
        out.append(v)
    return out


def _mapear_codigo_categoria(valor, mapa: dict[int, str]):
    """Convierte IDs de categoria Dimensions a cat.Name si el valor los contiene."""
    if valor is None or not mapa or not isinstance(valor, str):
        return valor

    texto = valor.strip()
    if not (texto.startswith("{") and texto.endswith("}")):
        return valor

    inner = texto[1:-1].strip()
    if not inner:
        return valor

    separador = ";" if ";" in inner and "," not in inner else ","
    nombres = []
    for parte in inner.replace(";", ",").split(","):
        parte = parte.strip()
        if not parte:
            continue
        try:
            nombres.append(mapa.get(int(parte), parte))
        except ValueError:
            nombres.append(parte)
    return "{" + separador.join(nombres) + "}"


def _construir_mapa_global_categoria_mdm(fields) -> dict[int, str]:
    """Construye {cat.Value: cat.Name} desde todos los campos MDM."""
    mapa: dict[int, str] = {}
    try:
        n_fields = fields.Count
    except Exception:
        return mapa

    for i in range(n_fields):
        try:
            field = fields[i]
        except Exception:
            continue

        try:
            cats = field.Categories
            for j in range(cats.Count):
                try:
                    cat = cats[j]
                    mapa[int(cat.Value)] = cat.Name
                except (TypeError, ValueError, Exception):
                    continue
        except Exception:
            pass

        try:
            mapa.update(_construir_mapa_global_categoria_mdm(field.Fields))
        except Exception:
            pass

    return mapa


def _construir_mapa_categorymap_mdd(ruta_mdd: Path) -> dict[int, str]:
    """Construye {value: name} desde el categorymap XML del MDD."""
    mapa: dict[int, str] = {}
    try:
        with ruta_mdd.open("r", encoding="utf-8", errors="ignore") as f:
            contenido = f.read()
    except OSError:
        return mapa

    bloque = re.search(
        r"<categorymap\b[^>]*>(.*?)</categorymap>",
        contenido,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not bloque:
        return mapa

    for tag in re.finditer(r"<categoryid\b([^>]*)/?>", bloque.group(1), re.IGNORECASE):
        attrs = dict(re.findall(r'(\w+)\s*=\s*"([^"]*)"', tag.group(1)))
        try:
            mapa[int(attrs["value"])] = attrs["name"]
        except (KeyError, ValueError):
            continue
    return mapa


def _construir_mapa_categoria_mdd(ruta_mdd: Path, fields=None) -> dict[int, str]:
    mapa = _construir_mapa_categorymap_mdd(ruta_mdd)
    if fields is not None:
        for codigo, nombre in _construir_mapa_global_categoria_mdm(fields).items():
            mapa.setdefault(codigo, nombre)
    return mapa


def _crear_copia_mdd_para_wine(origen: Path, destino: Path) -> None:
    """Copia un MDD y baja solo los atributos de version para abrirlo con DC 6.0.1."""
    with origen.open("r", encoding="utf-8", newline="") as f:
        contenido = f.read()

    for prop in ("mdm_createversion", "mdm_lastversion"):
        patron = re.compile(r'(' + re.escape(prop) + r'\s*=\s*")[^"]*(")')
        contenido = patron.sub(r"\g<1>" + MDD_VERSION_WINE + r"\g<2>", contenido)

    with destino.open("w", encoding="utf-8", newline="") as f:
        f.write(contenido)


def _script_mdd_wine() -> str:
    return textwrap.dedent(
        r'''
        import os
        import sys
        import re
        import win32com.client as _win32
        import pandas as _pd

        AD_OPEN_FORWARD_ONLY = 0
        AD_LOCK_READ_ONLY = 1
        TOMLIB_PATH = r"Z:\home\rowen\Proyectos\WInbase\ejemplos\dimensions-pipeline\TOMLIB"


        def _linux_a_windows(path):
            if not path:
                return ""
            s = str(path)
            if len(s) >= 3 and s[1] == ":" and s[2] in ("\\", "/"):
                return s
            if s.startswith("/"):
                return "Z:" + s.replace("/", "\\")
            return s


        def _label_mdm(obj):
            try:
                v = getattr(obj, "LabelText", None)
                if isinstance(v, str) and v:
                    return v
            except Exception:
                pass
            try:
                lbl = getattr(obj, "Label", None)
                if lbl is not None:
                    txt = getattr(lbl, "LabelText", None)
                    if isinstance(txt, str) and txt:
                        return txt
                    return str(lbl)
            except Exception:
                pass
            return ""


        def _render_field_mdm(field, lineas, depth=0):
            if depth > 8:
                return

            try:
                nombre = field.Name
            except Exception:
                return

            etiqueta = _label_mdm(field)
            nivel = min(depth + 3, 6)
            prefijo = "#" * nivel

            lineas.append(f"{prefijo} `{nombre}`")
            lineas.append("")
            if etiqueta:
                lineas.append(f"- **Etiqueta:** {etiqueta}")

            try:
                cats = field.Categories
                n_cats = cats.Count
            except Exception:
                n_cats = 0

            if n_cats:
                lineas.append("- **Categorias:**")
                lineas.append("")
                lineas.append("| Codigo | Etiqueta |")
                lineas.append("|--------|----------|")
                for j in range(n_cats):
                    try:
                        cat = cats[j]
                        cod = cat.Name
                        etq = _label_mdm(cat).replace("|", "\\|")
                        lineas.append(f"| {cod} | {etq} |")
                    except Exception:
                        continue
                lineas.append("")

            try:
                subs = field.Fields
                n_subs = subs.Count
            except Exception:
                n_subs = 0

            if n_subs:
                lineas.append(f"- **Sub-campos:** {n_subs}")
                lineas.append("")
                for k in range(n_subs):
                    try:
                        _render_field_mdm(subs[k], lineas, depth=depth + 1)
                    except Exception as exc:
                        lineas.append(f"> Error en sub-campo {k}: {exc}")
                        lineas.append("")

            if not n_cats and not n_subs:
                lineas.append("")


        def _normalizar_valor(v):
            if v is None:
                return None
            if hasattr(v, "year") and hasattr(v, "month") and hasattr(v, "day"):
                try:
                    return _pd.Timestamp(
                        int(v.year), int(v.month), int(v.day),
                        int(getattr(v, "hour", 0) or 0),
                        int(getattr(v, "minute", 0) or 0),
                        int(getattr(v, "second", 0) or 0),
                    )
                except Exception:
                    return str(v)
            return v


        def _valor_csv(v):
            v = _normalizar_valor(v)
            if v is None:
                return ""
            try:
                if _pd.isna(v):
                    return ""
            except Exception:
                pass
            return v


        def _construir_mapa_global_categoria_mdm(fields):
            mapa = {}
            try:
                n_fields = fields.Count
            except Exception:
                return mapa

            for i in range(n_fields):
                try:
                    field = fields[i]
                except Exception:
                    continue

                try:
                    cats = field.Categories
                    for j in range(cats.Count):
                        try:
                            cat = cats[j]
                            mapa[int(cat.Value)] = cat.Name
                        except Exception:
                            continue
                except Exception:
                    pass

                try:
                    mapa.update(_construir_mapa_global_categoria_mdm(field.Fields))
                except Exception:
                    pass

            return mapa


        def _construir_mapa_categorymap_mdd(mdd_path):
            mapa = {}
            try:
                with open(_linux_a_windows(mdd_path), "r", encoding="utf-8", errors="ignore") as f:
                    contenido = f.read()
            except OSError:
                return mapa

            bloque = re.search(
                r"<categorymap\b[^>]*>(.*?)</categorymap>",
                contenido,
                flags=re.IGNORECASE | re.DOTALL,
            )
            if not bloque:
                return mapa

            for tag in re.finditer(r"<categoryid\b([^>]*)/?>", bloque.group(1), re.IGNORECASE):
                attrs = dict(re.findall(r'(\w+)\s*=\s*"([^"]*)"', tag.group(1)))
                try:
                    mapa[int(attrs["value"])] = attrs["name"]
                except (KeyError, ValueError):
                    continue
            return mapa


        def _construir_mapa_categoria_mdd(mdd_path, fields):
            mapa = _construir_mapa_categorymap_mdd(mdd_path)
            for codigo, nombre in _construir_mapa_global_categoria_mdm(fields).items():
                if codigo not in mapa:
                    mapa[codigo] = nombre
            return mapa


        def _mapear_codigo_categoria(valor, mapa):
            if valor is None or not mapa or not isinstance(valor, str):
                return valor

            texto = valor.strip()
            if not (texto.startswith("{") and texto.endswith("}")):
                return valor

            inner = texto[1:-1].strip()
            if not inner:
                return valor

            separador = ";" if ";" in inner and "," not in inner else ","
            nombres = []
            for parte in inner.replace(";", ",").split(","):
                parte = parte.strip()
                if not parte:
                    continue
                try:
                    nombres.append(mapa.get(int(parte), parte))
                except ValueError:
                    nombres.append(parte)
            return "{" + separador.join(nombres) + "}"


        def _aplicar_category_names(df, mapa):
            if not mapa or df.empty:
                return df
            for col in df.columns:
                df[col] = df[col].map(lambda v: _mapear_codigo_categoria(v, mapa))
            return df


        def _abrir_mrconnection_para_lectura(mdd_win, ddf_win):
            from conexion import MRConnection, MRReader

            class _MRConnectionCategoryNames(MRConnection):
                def open(self, mdd_mode=""):
                    if not self.mdd_path or not os.path.isfile(self.mdd_path):
                        raise FileNotFoundError(f"MDD no existe: {self.mdd_path}")
                    if self.ddf_path and not os.path.isfile(self.ddf_path):
                        raise FileNotFoundError(f"DDF no existe: {self.ddf_path}")

                    self.mdm = _win32.Dispatch("MDM.Document")
                    if self.read_only:
                        self.mdm.Open(self.mdd_path, "", 1)
                    else:
                        self.mdm.Open(self.mdd_path, mdd_mode)

                    if self.ddf_path:
                        base_conn_str = (
                            "Provider=mrOleDB.Provider.2;"
                            "Data Source=mrDataFileDsc;"
                            f"Location={self.ddf_path};"
                            f"Initial Catalog={self.mdd_path};"
                            "MR Init Category Names=1;"
                        )
                        self._conn_str = base_conn_str + "MR Init Category Values=0"
                        self.conn = _win32.Dispatch("ADODB.Connection")
                        try:
                            self.conn.Open(self._conn_str)
                        except Exception:
                            try:
                                self.conn.Close()
                            except Exception:
                                pass
                            self._conn_str = base_conn_str.rstrip(";")
                            self.conn = _win32.Dispatch("ADODB.Connection")
                            self.conn.Open(self._conn_str)
                        self.reader = MRReader(self.conn)

                    self._open = True
                    return self

            return _MRConnectionCategoryNames(mdd_win, ddf_win, read_only=True)


        def _exportar_vdata_csv(mdd_win, ddf_win, csv_path, mapa_categoria):
            if TOMLIB_PATH not in sys.path:
                sys.path.insert(0, TOMLIB_PATH)

            with _abrir_mrconnection_para_lectura(mdd_win, ddf_win) as mc:
                df = mc.query_to_dataframe(
                    "SELECT * FROM vdata",
                    show_progress=False,
                )

            df = _aplicar_category_names(df, mapa_categoria)
            df.to_csv(
                _linux_a_windows(csv_path),
                index=False,
                encoding="utf-8-sig",
            )
            return len(df), len(df.columns)


        def generar_md_mdd(
            mdd_path,
            ddf_path,
            csv_path,
            original_mdd_name,
            original_ddf_name,
            original_csv_name,
        ):
            mdd_win = _linux_a_windows(mdd_path)
            ddf_win = _linux_a_windows(ddf_path)
            mdm = _win32.Dispatch("MDM.Document")
            lineas = []

            try:
                mdm.Open(mdd_win, "")

                stem = original_mdd_name.rsplit(".", 1)[0]
                lineas.append(f"# Base MDD: {stem}")
                lineas.append("")
                lineas.append(f"- **Archivo MDD:** `{original_mdd_name}`")
                if original_ddf_name:
                    lineas.append(f"- **Archivo DDF:** `{original_ddf_name}`")
                lineas.append("- **Ejecutor MDD:** `WInbase / Wine`")
                lineas.append("")

                lineas.append("## Estructura del cuestionario")
                lineas.append("")

                try:
                    n_campos = mdm.Fields.Count
                except Exception:
                    n_campos = 0

                for i in range(n_campos):
                    try:
                        _render_field_mdm(mdm.Fields[i], lineas, depth=0)
                    except Exception as exc:
                        lineas.append(f"> Error en campo {i}: {exc}")
                        lineas.append("")

                if ddf_path:
                    mapa_categoria = _construir_mapa_categoria_mdd(mdd_path, mdm.Fields)
                    try:
                        mdm.Close()
                    except Exception:
                        pass
                    mdm = None

                    lineas.append("## Datos (vdata)")
                    lineas.append("")
                    total_rows, total_cols = _exportar_vdata_csv(
                        mdd_win,
                        ddf_win,
                        csv_path,
                        mapa_categoria,
                    )
                    lineas.append(f"- **CSV:** `{original_csv_name}`")
                    lineas.append(f"- **Filas:** {total_rows}")
                    lineas.append(f"- **Columnas:** {total_cols}")
                    lineas.append("")

            finally:
                try:
                    mdm.Close()
                except Exception:
                    pass

            return "\n".join(lineas)


        def main():
            if len(sys.argv) != 8:
                raise SystemExit(
                    "uso: helper.py mdd_path ddf_path output_path csv_path "
                    "original_mdd_name original_ddf_name original_csv_name"
                )

            (
                mdd_path,
                ddf_path,
                output_path,
                csv_path,
                original_mdd_name,
                original_ddf_name,
                original_csv_name,
            ) = sys.argv[1:]
            contenido = generar_md_mdd(
                mdd_path,
                ddf_path,
                csv_path,
                original_mdd_name,
                original_ddf_name,
                original_csv_name,
            )
            with open(_linux_a_windows(output_path), "w", encoding="utf-8", newline="\n") as f:
                f.write(contenido)


        if __name__ == "__main__":
            main()
        '''
    ).lstrip()


def generar_md_mdd_wine(
    mdd_path: Path,
    ddf_path: Optional[Path] = None,
    csv_path: Optional[Path] = None,
) -> str:
    """Convierte MDD usando WInbase/py-wine.sh cuando pywin32 no existe en Linux."""
    py_wine = _obtener_py_wine()
    if py_wine is None:
        raise ImportError(
            "Para convertir .mdd se necesita pywin32 nativo o WInbase/py-wine.sh. "
            f"Define {PY_WINE_ENV} si el lanzador esta en otra ruta."
        )

    with tempfile.TemporaryDirectory(prefix="conversormd-mdd-") as tmp_dir:
        tmp = Path(tmp_dir)
        tmp_mdd = tmp / mdd_path.name
        tmp_ddf = tmp / ddf_path.name if ddf_path else None
        output_md = tmp / f"{mdd_path.name}.md"
        output_csv = tmp / csv_path.name if csv_path else None
        helper = tmp / "mdd_wine_helper.py"

        _crear_copia_mdd_para_wine(mdd_path, tmp_mdd)
        if ddf_path:
            shutil.copy2(ddf_path, tmp_ddf)
        helper.write_text(_script_mdd_wine(), encoding="utf-8")

        cmd = [
            str(py_wine),
            str(helper),
            str(tmp_mdd),
            str(tmp_ddf) if tmp_ddf else "",
            str(output_md),
            str(output_csv) if output_csv else "",
            mdd_path.name,
            ddf_path.name if ddf_path else "",
            csv_path.name if csv_path else "",
        ]
        resultado = subprocess.run(
            cmd,
            cwd=str(mdd_path.parent),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        if resultado.returncode != 0:
            detalle = "\n".join(
                parte.strip()
                for parte in (resultado.stdout, resultado.stderr)
                if parte.strip()
            )
            raise RuntimeError(f"Fallo la conversion .mdd via Wine: {detalle}")

        if csv_path and output_csv:
            csv_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(output_csv, csv_path)

        return output_md.read_text(encoding="utf-8")


def generar_md_mdd(
    mdd_path: Path,
    ddf_path: Optional[Path] = None,
    csv_path: Optional[Path] = None,
) -> str:
    """
    Convierte un MDD a Markdown y opcionalmente exporta su DDF a CSV.

    Lógica replicada de TOMLIB/conexion.py (MRConnection / MRReader):
        - Apertura de MDM.Document con la ruta del MDD.
        - Iteración top-level de mdm.Fields (nombre, etiqueta, categorías).
        - Si hay DDF: ADODB.Connection con provider mrOleDB, SELECT * FROM vdata
          y exportación de vdata a CSV separado.
    """
    if not MDD_DISPONIBLE:
        return generar_md_mdd_wine(mdd_path, ddf_path, csv_path)

    AD_OPEN_FORWARD_ONLY = 0
    AD_LOCK_READ_ONLY = 1
    CHUNK = 30_000

    mdm = _win32.Dispatch("MDM.Document")
    conn = None
    lineas: list[str] = []

    try:
        mdm.Open(str(mdd_path))

        lineas.append(f"# Base MDD: {mdd_path.stem}")
        lineas.append("")
        lineas.append(f"- **Archivo MDD:** `{mdd_path.name}`")
        if ddf_path:
            lineas.append(f"- **Archivo DDF:** `{ddf_path.name}`")
        lineas.append("")

        # ── Estructura del cuestionario (MDM) ──────────────────────────────
        lineas.append("## Estructura del cuestionario")
        lineas.append("")

        try:
            n_campos = mdm.Fields.Count
        except Exception:
            n_campos = 0

        for i in range(n_campos):
            try:
                _render_field_mdm(mdm.Fields[i], lineas, depth=0)
            except Exception as exc:
                lineas.append(f"> Error en campo {i}: {exc}")
                lineas.append("")

        # ── Datos (DDF) ────────────────────────────────────────────────────
        if ddf_path:
            mapa_categoria = _construir_mapa_categoria_mdd(mdd_path, mdm.Fields)
            conn_str = (
                "Provider=mrOleDB.Provider.2;"
                "Data Source=mrDataFileDsc;"
                f"Location={ddf_path};"
                f"Initial Catalog={mdd_path};"
                "MR Init Category Names=1;"
                "MR Init Category Values=0"
            )
            conn = _win32.Dispatch("ADODB.Connection")
            try:
                conn.Open(conn_str)
            except Exception:
                conn_str = conn_str.rsplit(";", 1)[0]
                conn = _win32.Dispatch("ADODB.Connection")
                conn.Open(conn_str)

            lineas.append("## Datos (vdata)")
            lineas.append("")

            rs = _win32.Dispatch("ADODB.Recordset")
            rs.Open(
                "SELECT * FROM vdata",
                conn,
                AD_OPEN_FORWARD_ONLY,
                AD_LOCK_READ_ONLY,
            )

            num_fields = rs.Fields.Count
            columns = [rs.Fields.Item(k).Name for k in range(num_fields)]
            chunks: list = []

            try:
                while not rs.EOF:
                    raw = rs.GetRows(CHUNK)
                    if not raw:
                        break
                    arrays = {}
                    for idx, col in enumerate(columns):
                        # dtype=object evita la inferencia de datetime64 de
                        # NumPy (que falla con pywintypes.datetime + None),
                        # y _sanitizar_columna normaliza los datetimes COM.
                        arrays[col] = _np.array(
                            _sanitizar_columna(raw[idx]),
                            dtype=object,
                        )
                    chunks.append(_pd.DataFrame(arrays))
            finally:
                try:
                    rs.Close()
                except Exception:
                    pass

            df = (
                _pd.concat(chunks, ignore_index=True)
                if chunks
                else _pd.DataFrame()
            )
            for col in df.columns:
                df[col] = df[col].map(
                    lambda v, m=mapa_categoria: _mapear_codigo_categoria(v, m)
                )

            if csv_path:
                csv_path.parent.mkdir(parents=True, exist_ok=True)
                df.to_csv(csv_path, index=False, encoding="utf-8-sig")

            lineas.append(f"- **CSV:** `{csv_path.name if csv_path else '(no exportado)'}`")
            lineas.append(f"- **Filas:** {len(df)}")
            lineas.append(f"- **Columnas:** {len(df.columns)}")
            lineas.append("")

    finally:
        try:
            if conn is not None:
                conn.Close()
        except Exception:
            pass
        try:
            mdm.Close()
        except Exception:
            pass

    return "\n".join(lineas)


def _leer_texto(archivo: Path) -> str:
    """Lee un archivo de texto probando varias codificaciones habituales."""
    for encoding in ("utf-8-sig", "utf-16", "latin-1"):
        try:
            return archivo.read_text(encoding=encoding)
        except (UnicodeError, UnicodeDecodeError):
            continue
    # Último recurso: no falla, reemplaza bytes inválidos.
    return archivo.read_text(encoding="utf-8", errors="replace")


def generar_md_script(archivo: Path) -> str:
    """
    Convierte un script de texto plano (.mrs, .dms) a Markdown.

    Vuelca el contenido íntegro del script dentro de un bloque de código,
    usando una sugerencia de lenguaje según la extensión. La valla del bloque
    se alarga si el propio script contiene secuencias de backticks, para no
    romper el formato Markdown.

    Args:
        archivo: Ruta al archivo .mrs o .dms.

    Returns:
        Texto en Markdown con el script en un bloque de código.
    """
    extension = archivo.suffix.lower()
    lenguaje = EXTENSIONES_SCRIPT.get(extension, "text")
    contenido = _leer_texto(archivo)

    # Valla de al menos 3 backticks, mayor que cualquier racha del contenido.
    max_backticks = max(
        (len(m) for m in re.findall(r"`+", contenido)),
        default=0,
    )
    valla = "`" * max(3, max_backticks + 1)

    lineas = [
        f"# Script: {archivo.name}",
        "",
        f"- **Archivo:** `{archivo.name}`",
        f"- **Tipo:** {extension}",
        "",
        f"{valla}{lenguaje}",
        contenido,
        valla,
        "",
    ]
    return "\n".join(lineas)


def convertir_archivo(
    md: MarkItDown,
    archivo: Path,
    ruta_salida: Path,
    sobrescribir: bool,
) -> bool:
    """
    Convierte un archivo individual a Markdown.

    Despacha según la extensión:
        - .sav -> genera diccionario con pyreadstat y datos en CSV.
        - .mdd -> genera estructura + datos (si hay .ddf) vía pywin32.
        - .mrs/.dms -> vuelca el script de texto en un bloque de código.
        - resto -> usa MarkItDown.

    Args:
        md: Instancia de MarkItDown.
        archivo: Archivo origen.
        ruta_salida: Ruta donde se guardará el .md.
        sobrescribir: Si es False, no reemplaza archivos ya existentes.

    Returns:
        True si se convirtió correctamente, False si se omitió.
    """
    if ruta_salida.exists() and not sobrescribir:
        print(f"OMITIDO, ya existe: {ruta_salida}")
        return False

    ruta_salida.parent.mkdir(parents=True, exist_ok=True)

    extension = archivo.suffix.lower()

    if extension in EXTENSIONES_SPSS:
        if not PYREADSTAT_DISPONIBLE:
            print(f"OMITIDO (.sav sin pyreadstat): {archivo.name}")
            return False
        csv_salida = construir_ruta_csv_datos(ruta_salida)
        if csv_salida.exists() and not sobrescribir:
            print(f"OMITIDO, ya existe: {csv_salida}")
            return False
        total_rows, total_cols = exportar_datos_sav_csv(archivo, csv_salida)
        contenido = generar_diccionario_sav(
            archivo,
            csv_salida,
            total_rows,
            total_cols,
        )
        ruta_salida.write_text(contenido, encoding="utf-8")
        print(f"OK (diccionario SPSS): {archivo.name} -> {ruta_salida}")
        print(f"OK (CSV SPSS): {archivo.name} -> {csv_salida}")
    elif extension in EXTENSIONES_MDD:
        if not _mdd_backend_disponible():
            print(f"OMITIDO (.mdd sin pywin32 ni WInbase/py-wine.sh): {archivo.name}")
            return False
        ddf_path = archivo.with_suffix(".ddf")
        tiene_ddf = ddf_path.exists()
        csv_salida = construir_ruta_csv_datos(ruta_salida) if tiene_ddf else None
        if csv_salida and csv_salida.exists() and not sobrescribir:
            print(f"OMITIDO, ya existe: {csv_salida}")
            return False
        contenido = generar_md_mdd(
            archivo,
            ddf_path if tiene_ddf else None,
            csv_salida,
        )
        ruta_salida.write_text(contenido, encoding="utf-8")
        sufijo = " + DDF" if tiene_ddf else ""
        backend = "MDD" if MDD_DISPONIBLE else "MDD via Wine"
        print(f"OK ({backend}{sufijo}): {archivo.name} -> {ruta_salida}")
        if csv_salida:
            print(f"OK (CSV vdata): {archivo.name} -> {csv_salida}")
    elif extension in EXTENSIONES_SCRIPT:
        contenido = generar_md_script(archivo)
        ruta_salida.write_text(contenido, encoding="utf-8")
        print(f"OK (script {extension}): {archivo.name} -> {ruta_salida}")
    else:
        resultado = md.convert(str(archivo))
        contenido = rellenar_celdas_combinadas(
            resultado.text_content,
            rellenar_celdas_vacias=False,
        )
        ruta_salida.write_text(contenido, encoding="utf-8")
        print(f"OK: {archivo.name} -> {ruta_salida}")

    return True


def convertir_directorio(
    directorio: Path,
    carpeta_salida: str = CARPETA_SALIDA_DEFAULT,
    extensiones: Iterable[str] = EXTENSIONES_PERMITIDAS,
    recursivo: bool = False,
    sobrescribir: bool = True,
) -> int:
    """
    Convierte archivos soportados de un directorio a Markdown.

    Args:
        directorio: Carpeta donde están los archivos origen.
        carpeta_salida: Nombre o ruta de la carpeta de salida.
        extensiones: Extensiones permitidas.
        recursivo: Busca archivos también en subcarpetas.
        sobrescribir: Reemplaza archivos Markdown existentes.
    """
    directorio = directorio.resolve()

    if not directorio.exists():
        raise FileNotFoundError(f"El directorio no existe: {directorio}")

    if not directorio.is_dir():
        raise NotADirectoryError(f"La ruta indicada no es un directorio: {directorio}")

    extensiones_normalizadas = {
        ext.lower() if ext.startswith(".") else f".{ext.lower()}"
        for ext in extensiones
    }
    extensiones_no_soportadas = extensiones_normalizadas - EXTENSIONES_PERMITIDAS
    if extensiones_no_soportadas:
        print(
            "AVISO: extensiones no soportadas omitidas: "
            f"{', '.join(sorted(extensiones_no_soportadas))}"
        )
        extensiones_normalizadas &= EXTENSIONES_PERMITIDAS

    # Aviso si pidió .sav pero no tiene pyreadstat instalado
    if EXTENSIONES_SPSS & extensiones_normalizadas and not PYREADSTAT_DISPONIBLE:
        print(
            "AVISO: pyreadstat no está instalado. "
            "Los archivos .sav se omitirán. Instala con: pip install pyreadstat"
        )

    # Aviso si pidio .mdd pero no hay backend COM disponible.
    if EXTENSIONES_MDD & extensiones_normalizadas and not _mdd_backend_disponible():
        print(
            "AVISO: no hay pywin32 nativo ni WInbase/py-wine.sh disponible. "
            "Los archivos .mdd se omitirán. En Linux define "
            f"{PY_WINE_ENV}=/ruta/a/py-wine.sh o instala WInbase."
        )

    salida = Path(carpeta_salida)
    if not salida.is_absolute():
        salida = directorio / salida

    archivos = obtener_archivos(directorio, extensiones_normalizadas, recursivo)

    if not archivos:
        print("No se encontraron archivos para convertir.")
        print(f"Directorio revisado: {directorio}")
        habilitadas = ", ".join(sorted(extensiones_normalizadas)) or "(ninguna)"
        print(f"Extensiones habilitadas: {habilitadas}")
        return 0

    print(f"Directorio origen: {directorio}")
    print(f"Carpeta salida: {salida}")
    print(f"Archivos encontrados: {len(archivos)}")
    print("-" * 60)

    md = MarkItDown()
    convertidos = 0
    errores = 0
    omitidos = 0

    for archivo in archivos:
        try:
            ruta_salida = construir_ruta_salida(archivo, directorio, salida, recursivo)
            se_convirtio = convertir_archivo(md, archivo, ruta_salida, sobrescribir)

            if se_convirtio:
                convertidos += 1
            else:
                omitidos += 1

        except Exception as exc:
            errores += 1
            print(f"ERROR: {archivo} -> {exc}")

    print("-" * 60)
    print("Proceso finalizado.")
    print(f"Convertidos: {convertidos}")
    print(f"Omitidos: {omitidos}")
    print(f"Errores: {errores}")
    return errores


def crear_parser() -> argparse.ArgumentParser:
    """
    Crea el parser de argumentos para ejecutar el script desde terminal.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Convierte documentos a Markdown. Soporta los formatos de MarkItDown "
            "(PowerPoint, PDF, HTML, CSV, JSON, XML, ZIP, EPUB, etc.), .sav de "
            "SPSS (codebook + datos CSV vía pyreadstat), .mdd/.ddf de Unicom Intelligence "
            "(estructura + datos vía pywin32) y scripts .mrs/.dms de Unicom "
            "Intelligence (volcado del texto en bloque de código)."
        )
    )

    parser.add_argument(
        "directorio",
        nargs="?",
        default=".",
        help="Directorio a convertir. Si no se indica, usa el directorio actual.",
    )

    parser.add_argument(
        "-o",
        "--output",
        default=CARPETA_SALIDA_DEFAULT,
        help=f"Carpeta de salida. Por defecto: {CARPETA_SALIDA_DEFAULT}",
    )

    parser.add_argument(
        "-r",
        "--recursivo",
        action="store_true",
        help="Busca archivos también dentro de subcarpetas.",
    )

    parser.add_argument(
        "--no-sobrescribir",
        action="store_true",
        help="No reemplaza archivos .md que ya existan.",
    )

    parser.add_argument(
        "--extensiones",
        nargs="+",
        default=sorted(EXTENSIONES_PERMITIDAS),
        help="Extensiones a convertir. Ejemplo: --extensiones .pdf .sav .mdd",
    )

    return parser


def main() -> int:
    """
    Punto de entrada del script.
    """
    parser = crear_parser()
    args = parser.parse_args()

    try:
        errores = convertir_directorio(
            directorio=Path(args.directorio),
            carpeta_salida=args.output,
            extensiones=args.extensiones,
            recursivo=args.recursivo,
            sobrescribir=not args.no_sobrescribir,
        )
        return 1 if errores else 0

    except Exception as exc:
        print(f"ERROR GENERAL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
