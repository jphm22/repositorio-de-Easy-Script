from pathlib import Path


def juntar_scripts(carpeta_origen, archivo_salida="scripts_unidos.txt"):
    """Junta todos los archivos .py de una carpeta y sus subcarpetas en un TXT."""
    carpeta = Path(carpeta_origen).expanduser().resolve()
    salida = Path(archivo_salida).expanduser().resolve()
    script_actual = Path(__file__).resolve()

    if not carpeta.exists():
        print(f"Error: la carpeta no existe: {carpeta}")
        return

    if not carpeta.is_dir():
        print(f"Error: la ruta no es una carpeta: {carpeta}")
        return

    archivos_python = sorted(carpeta.rglob("*.py"))
    archivos_procesados = 0

    try:
        with salida.open("w", encoding="utf-8") as archivo_txt:
            for ruta_script in archivos_python:
                # Evita agregar este mismo programa al archivo de salida.
                if ruta_script.resolve() == script_actual:
                    continue

                ruta_relativa = ruta_script.relative_to(carpeta)

                archivo_txt.write("\n" + "=" * 80 + "\n")
                archivo_txt.write(f"ARCHIVO: {ruta_relativa}\n")
                archivo_txt.write("=" * 80 + "\n\n")

                try:
                    contenido = ruta_script.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    contenido = ruta_script.read_text(
                        encoding="utf-8", errors="replace"
                    )
                    archivo_txt.write(
                        "# Aviso: se reemplazaron caracteres que no pudieron leerse.\n\n"
                    )
                except OSError as error:
                    archivo_txt.write(f"# No se pudo leer el archivo: {error}\n")
                    continue

                archivo_txt.write(contenido)
                archivo_txt.write("\n")
                archivos_procesados += 1

    except OSError as error:
        print(f"Error al crear el archivo de salida: {error}")
        return

    print("Proceso completado correctamente.")
    print(f"Scripts procesados: {archivos_procesados}")
    print(f"Archivo generado: {salida}")


if __name__ == "__main__":
    # Si dejas un punto, analiza la misma carpeta donde ejecutes el programa.
    CARPETA_ORIGEN = "."
    ARCHIVO_SALIDA = "scripts_unidos.txt"

    juntar_scripts(CARPETA_ORIGEN, ARCHIVO_SALIDA)
