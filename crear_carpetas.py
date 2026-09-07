from pathlib import Path

# Ruta donde se crearán las carpetas
ruta_destino = Path(r"C:\Users\Jhan.Huayre\OneDrive - Ipsos\Escritorio\Materiales para EASYSCRIPT\Script_ifield_Sergio\ORGANIZAR")

# Lista de nombres
nombres_carpetas = [
    "INN",
    "BHT-MSU-CRE",
    "HEC",
    "CHP",
    "AMD",
    "CEX",
    "HEC",
    "OBV-CPR-PA-Trends"
]

# Crear la carpeta principal si no existe
ruta_destino.mkdir(parents=True, exist_ok=True)

# Crear las carpetas
for nombre in nombres_carpetas:
    nombre = nombre.strip()

    # Ignorar elementos vacíos
    if not nombre:
        continue

    nueva_carpeta = ruta_destino / nombre
    nueva_carpeta.mkdir(exist_ok=True)
    print(f"Carpeta creada: {nueva_carpeta}")

print("Proceso terminado.")
