from pathlib import Path

# Carpeta donde se encuentra este script
carpeta = Path(__file__).resolve().parent

# Archivo TXT que se generara
archivo_salida = carpeta / "archivos_js_unidos.txt"

# Buscar recursivamente todos los archivos .js
archivos_js = sorted(
    (
        archivo
        for archivo in carpeta.rglob("*.js")
        if archivo.is_file()
    ),
    key=lambda archivo: str(archivo.relative_to(carpeta)).lower(),
)

if not archivos_js:
    print(
        "No se encontraron archivos .js "
        "en la carpeta ni en sus subcarpetas."
    )
    raise SystemExit(1)

with archivo_salida.open(
    "w",
    encoding="utf-8",
    newline="\n",
) as salida:
    for numero, archivo in enumerate(archivos_js, start=1):
        ruta_relativa = archivo.relative_to(carpeta)

        try:
            contenido = archivo.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            contenido = archivo.read_text(
                encoding="latin-1",
                errors="replace",
            )

        # Separador para identificar cada archivo
        salida.write(f"/* {'=' * 70} */\n")
        salida.write(f"/* Archivo: {ruta_relativa} */\n")
        salida.write(f"/* {'=' * 70} */\n\n")
        salida.write(contenido)

        # Separacion entre archivos
        if contenido and not contenido.endswith("\n"):
            salida.write("\n")

        salida.write("\n")

        print(
            f"[{numero}/{len(archivos_js)}] "
            f"Agregado: {ruta_relativa}"
        )

print()
print(f"Se unieron {len(archivos_js)} archivos JS.")
print(f"Resultado: {archivo_salida}")
