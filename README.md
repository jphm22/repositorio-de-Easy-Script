# EasyScript modular

## Cambios principales

- El estilo visual original se conserva en `css/styles.css`.
- El catálogo ya no incrusta el contenido de los recursos dentro de `index.html`.
- `js/repository-config.js` contiene solo metadatos y rutas.
- Cada archivo se carga bajo demanda mediante `fetch()`.
- La aplicación se dividió en configuración, utilidades, renderizado Markdown, store, componentes y orquestación.

## Ejecución

Desde la carpeta del proyecto:

```powershell
python -m http.server 8000
```

Luego abre `http://localhost:8000`. No abras `index.html` directamente con `file://`, porque los navegadores bloquean la carga local mediante `fetch()`.

## Agregar recursos

1. Guarda el archivo en su carpeta real.
2. Agrega únicamente sus metadatos y `virtualPath` en `js/repository-config.js`.
3. No es necesario modificar el HTML, CSS ni la lógica de la aplicación.
