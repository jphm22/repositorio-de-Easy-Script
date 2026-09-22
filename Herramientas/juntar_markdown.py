from pathlib import Path
import argparse


def unir_markdowns(carpeta_raiz: Path, archivo_salida: Path) -> None:
    carpeta_raiz = carpeta_raiz.resolve()
    archivo_salida = archivo_salida.resolve()

    archivos_md = sorted(
        archivo
        for archivo in carpeta_raiz.rglob("*.md")
        if archivo.resolve() != archivo_salida
    )

    if not archivos_md:
        print(f"No se encontraron archivos .md en: {carpeta_raiz}")
        return

    with archivo_salida.open("w", encoding="utf-8") as salida:
        salida.write("# Documentación consolidada\n\n")

        for archivo in archivos_md:
            ruta_relativa = archivo.relative_to(carpeta_raiz)

            salida.write(f"<!-- Archivo: {ruta_relativa.as_posix()} -->\n\n")
            salida.write(f"# {ruta_relativa.as_posix()}\n\n")

            contenido = archivo.read_text(
                encoding="utf-8",
                errors="replace"
            ).strip()

            salida.write(contenido)
            salida.write("\n\n---\n\n")

    print(f"Se unieron {len(archivos_md)} archivos.")
    print(f"Archivo generado: {archivo_salida}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Une todos los archivos Markdown de una carpeta y sus subcarpetas."
    )

    parser.add_argument(
        "carpeta",
        type=Path,
        help="Carpeta raíz que contiene los archivos Markdown"
    )

    parser.add_argument(
        "-o",
        "--salida",
        type=Path,
        default=Path("markdown_unido.md"),
        help="Nombre del archivo final"
    )

    argumentos = parser.parse_args()

    unir_markdowns(argumentos.carpeta, argumentos.salida)