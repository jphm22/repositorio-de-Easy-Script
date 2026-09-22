export const REPOSITORY_CONFIG = Object.freeze({
  "project": {
    "name": "EasyScript",
    "version": "3.0.0",
    "description": "Repositorio modular cargado desde rutas reales."
  },
  "sections": [
    {
      "id": "auxiliares",
      "name": "Auxiliares",
      "icon": "🧰",
      "description": "Prompts complementarios para conversión MDD/iField y corrección ortográfica o de estilos.",
      "categories": [
        {
          "id": "auxiliares-recursos",
          "name": "Recursos disponibles",
          "description": "Archivos cargados desde su ruta real.",
          "resources": [
            {
              "id": "auxiliares-metatool-ifield-v3-txt",
              "title": "Metatool Ifield V3",
              "type": "prompt",
              "summary": "Conversión de cuestionarios a MDD, iField y OSM.",
              "virtualPath": "Auxiliares/Metatool Ifield V3.txt",
              "tags": [
                "mdd",
                "ifield",
                "osm"
              ]
            },
            {
              "id": "auxiliares-prompt-ortografia-estilos-txt",
              "title": "Prompt Ortografía y Estilos",
              "type": "prompt",
              "summary": "Corrección ortográfica y aplicación de estilos sobre estructuras MDD.",
              "virtualPath": "Auxiliares/Prompt Ortografia Estilos.txt",
              "tags": [
                "ortografía",
                "estilos",
                "mdd"
              ]
            }
          ]
        }
      ]
    },
    {
      "id": "base-de-conocimiento",
      "name": "Base de conocimiento",
      "icon": "📚",
      "description": "Prompts para construir y estandarizar conocimiento reutilizable de EasyScript.",
      "categories": [
        {
          "id": "base-de-conocimiento-recursos",
          "name": "Recursos disponibles",
          "description": "Archivos cargados desde su ruta real.",
          "resources": [
            {
              "id": "base-de-conocimiento-prompt-base-conocimiento-tipo-easy-script-md",
              "title": "Base de conocimiento tipo Easy Script",
              "type": "prompt",
              "summary": "Genera una base de conocimiento especializada en EasyScript.",
              "virtualPath": "Base de conocimiento/PROMPT_BASE_CONOCIMIENTO_TIPO_EASY_SCRIPT.md",
              "tags": [
                "base de conocimiento",
                "easy script"
              ]
            },
            {
              "id": "base-de-conocimiento-prompt-base-ejemplo-estandar-easy-script-md",
              "title": "Ejemplo estándar Easy Script",
              "type": "prompt",
              "summary": "Ejemplo estándar para estructurar la base de conocimiento.",
              "virtualPath": "Base de conocimiento/PROMPT_BASE_EJEMPLO_ESTANDAR_EASY_SCRIPT.md",
              "tags": [
                "estándar",
                "ejemplo"
              ]
            },
            {
              "id": "base-de-conocimiento-prompt-base-ejemplo-mdd-easy-script-md",
              "title": "Ejemplo MDD Easy Script",
              "type": "prompt",
              "summary": "Ejemplo orientado a estructuras MDD de EasyScript.",
              "virtualPath": "Base de conocimiento/PROMPT_BASE_EJEMPLO_MDD_EASY_SCRIPT.md",
              "tags": [
                "mdd",
                "ejemplo"
              ]
            }
          ]
        }
      ]
    },
    {
      "id": "herramientas",
      "name": "Herramientas",
      "icon": "🛠️",
      "description": "Scripts Python para convertir, consolidar, organizar, inventariar y renombrar archivos.",
      "categories": [
        {
          "id": "herramientas-recursos",
          "name": "Recursos disponibles",
          "description": "Archivos cargados desde su ruta real.",
          "resources": [
            {
              "id": "herramientas-conversormd-py",
              "title": "Conversor a Markdown",
              "type": "script Python",
              "summary": "Convierte distintos formatos a Markdown.",
              "virtualPath": "Herramientas/ConversorMd.py",
              "tags": [
                "python",
                "markdown"
              ]
            },
            {
              "id": "herramientas-juntar-js-py",
              "title": "Unificador JavaScript",
              "type": "script Python",
              "summary": "Consolida archivos JavaScript.",
              "virtualPath": "Herramientas/juntar_js.py",
              "tags": [
                "python",
                "javascript"
              ]
            },
            {
              "id": "herramientas-juntar-markdown-py",
              "title": "Unificador Markdown",
              "type": "script Python",
              "summary": "Consolida archivos Markdown.",
              "virtualPath": "Herramientas/juntar_markdown.py",
              "tags": [
                "python",
                "markdown"
              ]
            },
            {
              "id": "herramientas-juntar-scripts-python-py",
              "title": "Unificador de scripts Python",
              "type": "script Python",
              "summary": "Consolida archivos Python.",
              "virtualPath": "Herramientas/juntar_scripts_python.py",
              "tags": [
                "python",
                "consolidación"
              ]
            },
            {
              "id": "herramientas-juntar-txt-py",
              "title": "Unificador TXT",
              "type": "script Python",
              "summary": "Consolida archivos de texto.",
              "virtualPath": "Herramientas/juntar_txt.py",
              "tags": [
                "python",
                "txt"
              ]
            },
            {
              "id": "herramientas-kb-consolidar-clm-py",
              "title": "Consolidar CLM",
              "type": "script Python",
              "summary": "Consolida materiales de cuestionario, lógica y MDD.",
              "virtualPath": "Herramientas/KB_Consolidar_CLM.py",
              "tags": [
                "python",
                "clm"
              ]
            },
            {
              "id": "herramientas-kb-crear-carpetas-py",
              "title": "Crear carpetas",
              "type": "script Python",
              "summary": "Crea la estructura de carpetas de trabajo.",
              "virtualPath": "Herramientas/KB_Crear_Carpetas.py",
              "tags": [
                "python",
                "carpetas"
              ]
            },
            {
              "id": "herramientas-kb-organizar-archivos-py",
              "title": "Organizar archivos",
              "type": "script Python",
              "summary": "Clasifica archivos en la estructura del repositorio.",
              "virtualPath": "Herramientas/KB_Organizar_Archivos.py",
              "tags": [
                "python",
                "organización"
              ]
            },
            {
              "id": "herramientas-kb-renombrar-archivos-py",
              "title": "Renombrar archivos",
              "type": "script Python",
              "summary": "Renombra archivos según reglas del repositorio.",
              "virtualPath": "Herramientas/KB_Renombrar_Archivos.py",
              "tags": [
                "python",
                "renombrado"
              ]
            },
            {
              "id": "herramientas-kd-procesar-mdd-unicom-py",
              "title": "Procesar MDD Unicom",
              "type": "script Python",
              "summary": "Procesa archivos MDD mediante Unicom.",
              "virtualPath": "Herramientas/KD_procesar_mdd_unicom.py",
              "tags": [
                "python",
                "mdd",
                "unicom"
              ]
            },
            {
              "id": "herramientas-mostrar-estructura-carpetas-y-archivos-py",
              "title": "Mostrar estructura",
              "type": "script Python",
              "summary": "Muestra el árbol de carpetas y archivos.",
              "virtualPath": "Herramientas/mostrar_estructura_carpetas_y_archivos.py",
              "tags": [
                "python",
                "inventario"
              ]
            }
          ]
        }
      ]
    },
    {
      "id": "prompt",
      "name": "Prompt",
      "icon": "⚡",
      "description": "Prompts secuenciales del flujo principal de EasyScript.",
      "categories": [
        {
          "id": "prompt-recursos",
          "name": "Recursos disponibles",
          "description": "Archivos cargados desde su ruta real.",
          "resources": [
            {
              "id": "prompt-00-base-conceptual-txt",
              "title": "00. Base conceptual",
              "type": "prompt",
              "summary": "Criterios conceptuales del flujo EasyScript.",
              "virtualPath": "Prompt/00_Base_Conceptual.txt",
              "tags": [
                "conceptual",
                "estándares"
              ]
            },
            {
              "id": "prompt-01-generacion-mdd-txt",
              "title": "01. Generación MDD",
              "type": "prompt",
              "summary": "Generación de estructura MDD.",
              "virtualPath": "Prompt/01_Generacion_MDD.txt",
              "tags": [
                "mdd",
                "generación"
              ]
            },
            {
              "id": "prompt-02-generacion-logica-txt",
              "title": "02. Generación de lógica",
              "type": "prompt",
              "summary": "Generación de lógica JavaScript para OSM.",
              "virtualPath": "Prompt/02_Generacion_Logica.txt",
              "tags": [
                "javascript",
                "lógica"
              ]
            },
            {
              "id": "prompt-03-control-qa-txt",
              "title": "03. Control QA",
              "type": "prompt",
              "summary": "Validación y control de calidad.",
              "virtualPath": "Prompt/03_Control_QA.txt",
              "tags": [
                "qa",
                "auditoría"
              ]
            }
          ]
        }
      ]
    },
    {
      "id": "qa",
      "name": "QA y auditoría",
      "icon": "🔎",
      "description": "Recursos de control de calidad y auditoría técnica.",
      "categories": [
        {
          "id": "qa-recursos",
          "name": "Recursos disponibles",
          "description": "Archivos cargados desde su ruta real.",
          "resources": [
            {
              "id": "qa-promt-auditor-ifield-v17-1-txt",
              "title": "Auditor iField v17.1",
              "type": "prompt",
              "summary": "Auditoría técnica de cuestionario, MDD y JavaScript.",
              "virtualPath": "QA/Promt Auditor Ifield v17 1.txt",
              "tags": [
                "qa",
                "ifield",
                "auditoría"
              ]
            }
          ]
        }
      ]
    },
    {
      "id": "plantillas",
      "name": "Plantillas",
      "icon": "📄",
      "description": "Archivos base usados por el flujo EasyScript.",
      "categories": [
        {
          "id": "plantillas-recursos",
          "name": "Recursos disponibles",
          "description": "Archivos cargados desde su ruta real.",
          "resources": [
            {
              "id": "plantilla-mdd",
              "title": "Plantilla MDD",
              "type": "plantilla MDD",
              "summary": "Plantilla base para generar estructuras MDD.",
              "virtualPath": "plantilla.mdd",
              "tags": [
                "mdd",
                "plantilla"
              ]
            }
          ]
        }
      ]
    }
  ]
});
