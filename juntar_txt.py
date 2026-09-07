from pathlib import Path

# Carpeta donde esta ubicado este script
carpeta = Path(__file__).resolve().parent

# Archivo que se generara
archivo_salida = carpeta / "archivo_unido.txt"

# Busca recursivamente todos los TXT en la carpeta y sus subcarpetas,
# excepto el propio archivo de salida.
archivos_txt = sorted(
    (
        archivo
        for archivo in carpeta.rglob("*.txt")
        if archivo.is_file()
        and archivo.resolve() != archivo_salida.resolve()
    ),
    key=lambda archivo: str(archivo.relative_to(carpeta)).lower(),
)

if not archivos_txt:
    print("No se encontraron archivos TXT en la carpeta ni en sus subcarpetas.")
else:
    with archivo_salida.open("w", encoding="utf-8", newline="") as salida:
        for numero, archivo in enumerate(archivos_txt, start=1):
            ruta_relativa = archivo.relative_to(carpeta)

            try:
                contenido = archivo.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                contenido = archivo.read_text(
                    encoding="latin-1",
                    errors="replace",
                )

            # Agrega un encabezado para identificar el archivo de origen.
            salida.write(f"===== {ruta_relativa} =====\n")
            salida.write(contenido)

            # Garantiza una separacion clara entre archivos.
            if contenido and not contenido.endswith("\n"):
                salida.write("\n")
            salida.write("\n")

            print(f"[{numero}/{len(archivos_txt)}] Agregado: {ruta_relativa}")

    print(f"\nProceso terminado. Se unieron {len(archivos_txt)} archivos.")
    print(f"Archivo generado: {archivo_salida}")
