from pathlib import Path


def mostrar_estructura(ruta: Path, prefijo: str = "") -> None:
    """Muestra recursivamente carpetas, subcarpetas y archivos en forma de árbol."""
    try:
        elementos = sorted(
            ruta.iterdir(),
            key=lambda elemento: (elemento.is_file(), elemento.name.lower())
        )
    except PermissionError:
        print(f"{prefijo}[Sin permiso para acceder]")
        return
    except OSError as error:
        print(f"{prefijo}[No se pudo leer: {error}]")
        return

    for indice, elemento in enumerate(elementos):
        es_ultimo = indice == len(elementos) - 1
        conector = "└── " if es_ultimo else "├── "

        if elemento.is_dir():
            print(f"{prefijo}{conector}{elemento.name}/")
            nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")
            mostrar_estructura(elemento, nuevo_prefijo)
        else:
            print(f"{prefijo}{conector}{elemento.name}")


def main() -> None:
    # Carpeta en la que está guardado este script.
    ruta_raiz = Path(__file__).resolve().parent

    print("Estructura de carpetas, subcarpetas y archivos")
    print(f"Ruta: {ruta_raiz}")
    print()
    print(f"{ruta_raiz.name}/")
    mostrar_estructura(ruta_raiz)


if __name__ == "__main__":
    main()
