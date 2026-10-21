# EasyScript V6

Estado: **en validación**. Las reglas de V6 cubren las incidencias aplicables del `REPORTE DE INCIDENCIAS.xlsx`, pero una regla escrita no equivale a una prueba exitosa: V6 se declara final cuando pase el plan de prueba (al final de este documento).

## 1. Flujo final: 3 prompts autosuficientes

```text
01_GenerarMDD.md
  Adjuntos: Cuestionario.docx + Ejemplos_MDD_CORREGIDO.md (de la familia compatible)
  Salida:   MDD_PARCIAL.txt + Reporte_MDD.md
        │
        ▼  Revisión del scripter (compilar, corregir)  →  MDD_FINAL.txt
        │
02_GenerarLogica.md
  Adjuntos: Cuestionario.docx + MDD_FINAL.txt + Base_Conocimiento.md (de la familia compatible)
            (+ opcional: Reporte_MDD.md del paso 01)
  Salida:   Logica_PARCIAL.js + Reporte_Logica.md
        │
        ▼  Revisión del scripter (pegar en iField, guardar, probar)  →  Logica_FINAL.js
        │
03_Control_QA.md
  Adjuntos: Cuestionario.docx + MDD_FINAL.txt + Logica_FINAL.js
  Salida:   Reporte_QA.md (incluye el checklist QA-01…QA-42 de incidencias)
```

Cada paso se ejecuta en un chat nuevo. Si la respuesta se corta, el prompt entrega por partes: responde `CONTINUAR`.

**Uso con E@sy Agent:** el chat no permite adjuntar archivos y rechaza mensajes largos, así que se crean **3 agentes** (uno por paso). El prompt completo del paso va en el campo Prompt del agente; el cuestionario y la base, en Sources. Para verificar que el prompt entró completo, pregúntale al agente cuál es la clave de lectura del final de sus instrucciones. Si se actualiza un prompt V6, hay que volver a pegarlo en su agente.

`00_Agente_EasyScript.md` es un agente único que detecta el paso por los archivos adjuntos; sirve solo en plataformas que permiten adjuntar el prompt del paso en el chat.

**Uso con Copilot Agent Builder (habilidades):** un solo agente con una habilidad por paso. En Instrucciones va `Agente_Copilot/Instrucciones_agente.txt`. En Habilidades se suben los tres .zip de `Agente_Copilot/` (`easyscript-v6-paso1-mdd`, `easyscript-v6-paso2-logica`, `easyscript-v6-paso3-qa`). Cada uno lleva su SKILL.md y el prompt V6 completo del paso en `referencia/`. Cada vez que cambie un prompt V6 hay que regenerar los .zip con `python Herramientas/V6_Empaquetar_Skills.py` y volver a subir el que cambió.

### Uso con Copilot (leer antes de probar)

Los prompts V6 son largos (01 ≈ 170 000 caracteres, 02 ≈ 105 000, 03 ≈ 30 000), y los archivos de ejemplos pesan 5–12 MB. Microsoft no publica un límite oficial claro, pero hay reportes de que Copilot lee solo una parte de los archivos grandes y de que el cuadro de chat admite unos miles de caracteres. Si Copilot no lee el prompt completo, aplicará solo las reglas que alcanzó a leer.

**Cómo dárselo a Copilot.** El prompt se **adjunta como archivo** junto con el cuestionario y la base: pegado como texto en el chat es demasiado largo y Copilot se queda trabado.

Sobre las bases de OneDrive: pesan 5–12 MB, así que Copilot siempre las leerá **en parte**; en la confirmación es normal que diga `parcial`. Están pensadas como material de búsqueda: las reglas y los ejemplos imprescindibles ya están dentro de cada prompt.

Los prompts se ejecutan **sin pedir confirmación**: con solo adjuntar los archivos, la IA debe entregar directamente la confirmación de lectura y los archivos de salida (por partes si no caben). Si aun así pregunta algo, responde "Sí, con los parámetros por defecto".

Cada prompt exige empezar con la **CONFIRMACIÓN DE LECTURA**:

1. Haz primero una prueba con un cuestionario corto: adjunta el prompt (o pégalo) y los archivos, y mira el bloque de confirmación.
2. Si la clave es correcta y la primera y última pregunta coinciden con el cuestionario, Copilot está leyendo todo: continúa normalmente.
3. Si dice `NO ENCONTRADA` o la clave no coincide, Copilot no está leyendo el prompt completo. En ese caso, avisa para preparar una versión dividida (reglas críticas pegadas en el chat y el resto como anexo), en lugar de seguir probando con resultados que no reflejan las reglas.

### Qué adjuntar de `OneDrive_2026-10-15/BASES DE CONOCIMIENTO`

Se elige **una sola carpeta**, la de la línea de servicio del estudio:

| Línea de servicio del estudio | Carpeta |
|---|---|
| BHT, MSU, CRE | `BHT - MSU - CRE` |
| CEX | `CEX` |
| INN (incluye pruebas de producto, SL) | `INN` |
| OBV, PA, TRENDS, CPR | `OBV - PA - TRENDS - CPR` |
| Otra (p. ej. OPS) | la carpeta con estudios más parecidos (mismo tipo de cuestionario) |

| Archivo de la carpeta | Uso en V6 |
|---|---|
| `2_BASE EJEMPLO MDD/*_MDD_CORREGIDO.md` | Se adjunta en el **Paso 1** |
| `3_BASE CONOCIMIENTO/*_BASE_CONOCIMIENTO_CORREGIDO.MD` | Se adjunta en el **Paso 2** |
| `1_BASE EJEMPLO ESTANDARIZACION/` | No se usa (era del flujo V2–V4 con Markdown intermedio) |
| `*_01_CUESTIONARIO_UNIDO`, `*_02_LOGICA_UNIDA`, `*_03_MDD_UNIDO` | No se adjuntan: son la materia prima con la que se construyeron las bases 2 y 3 |

### Variables SHELL en el Paso 2

El Paso 1 **no** genera variables `SHELL_*`: las agrega la plantilla de iField al importar el MDD. Para el Paso 2 hay dos opciones:

- **Recomendada:** usar como `MDD_FINAL.txt` el MDD exportado desde iField después de importarlo; así trae las SHELL reales y el prompt puede verificar que existen.
- Si se usa el MDD antes de importarlo, el prompt 02 asume las SHELL estándar (`SHELL_CHAINID`, `SHELL_RECORDING_CONFIRMATION`, `SHELL_AGE`, `SHELL_GENDER`) solo para lectura y lo deja anotado en su `Reporte_Logica.md`.

### Si el cuestionario tiene imágenes o numeración automática

Revisa en el `Reporte_MDD.md` del Paso 1 la línea "Modalidad de lectura". Si dice `SOLO_TEXTO`, o aparecen muchos `SIN_CODIGO`, la herramienta de IA no vio las imágenes ni la numeración automática de Word. Vuelve a ejecutar adjuntando también el cuestionario exportado a PDF.

### ¿Por qué 3 archivos y no 4?

El borrador de V6 tenía 4 archivos (una `00_Base_Conceptual.txt` compartida + 3 prompts cortos). Se descartó por tres razones:

1. **Se perdía el contenido técnico.** Los prompts del borrador pasaron de ~134 KB / 70 KB (V5.1) a ~6 KB cada uno. Decían "usa APIs corroboradas" o "reutiliza listas", pero ya no traían la sintaxis MDD, los casos de grillas, MaxDiff, bloques, ni el catálogo de funciones OSM. Sin eso el modelo vuelve a improvisar, que es justamente lo que generó las incidencias.
2. **Un adjunto más se lee peor.** Cuando la base conceptual va como archivo adjunto, el modelo la consulta por fragmentos (igual que los archivos de ejemplos de 5–12 MB); sus reglas compiten con los ejemplos y pierden prioridad. Dentro del prompt, las reglas son instrucciones.
3. **Cada etapa necesita una base distinta.** El MDD necesita casos MDD y el de lógica necesita casos JS. V5.1 ya había integrado la base conceptual en la sección 7 de cada prompt; V6 parte de ahí.

Por eso V6 = **V5.1 (contenido validado) + correcciones de incidencias + sección 0 de reglas críticas**. El borrador anterior se conserva en `_borrador_previo/` (puedes borrarlo cuando ya no lo necesites); sus ideas útiles (estados de evidencia, modo `NO_FINAL`, matriz de reglas, no propagación) se integraron.

### Estructura de cada prompt

| Sección | Contenido |
|---|---|
| Paso 0 | **Confirmación de lectura**: la respuesta empieza con la clave de la última línea del prompt, el último caso y la primera/última pregunta del cuestionario. Detecta si Copilot no leyó todo |
| 0 | **Reglas críticas V6**: tabla corta con las reglas que resuelven las incidencias (C01–C22 en MDD, L01–L17 en lógica). Va al inicio para que tenga prioridad y se vuelve a verificar en el autocontrol final |
| 1–3 | Rol, entradas (con advertencias sobre los archivos de ejemplos), parámetros |
| 4 | Reglas de construcción |
| 5 | Revisión antes/después, con **autocontrol de patrones prohibidos** (búsqueda de `__`, `\"`, categorías vacías, `goTo` fuera de `onNext`, listeners Shell, etc.) |
| 6 | Salida, con **protocolo de entrega por partes** para cuestionarios largos |
| 7 | Casos de referencia corregidos (sintaxis válida y coherente con la sección 0) |

## 2. Causas raíz encontradas (además de lo que faltaba en las reglas)

Al revisar V5.1 y las bases de OneDrive se encontraron contradicciones que explican varias incidencias. El modelo copia ejemplos con más fuerza que reglas, así que estas contradicciones eran la causa directa:

| Hallazgo | Dónde | Incidencias que causaba |
|---|---|---|
| El caso 5 de lógica ponía listeners en `SHELL_AGE`/`SHELL_GENDER`, y la tabla de familias decía "`onNext` de la variable Shell" | V5.1 02 §4.3 y §7 | Código en listeners Shell |
| El parámetro decía `BACKCHECK_IMPLICA_GRABACION = SI`, pero §4.16 y §7.2 decían "no asumas que BACKCHECK implica grabación" y "no asumas `_A1`" | V5.1 02 y 03 | No puso backchecks; sin validación de consentimiento `_A1` |
| La base de conocimiento trae funciones `OSM.Survey.Term = function(){… goTo …}` y nada lo prohibía | Bases OneDrive | El script no se puede guardar (`goTo` solo en eventos de salida) |
| Los casos usaban el alias `s.` sin declararlo, aunque el parámetro pedía `OSM.Survey` completo | V5.1 02 §7 | Errores de referencia |
| No había una sintaxis única de listas ni advertencia sobre los errores reales. Verificado con el compilador MDM de Data Collection 7: fallan el `define` sin `;`, la coma colgante tras `use`, la falta de coma antes de categorías locales y la coma tras la última categoría; y **un `use` con un nombre de lista inexistente compila sin error pero deja la pregunta sin categorías** | V5.1 01 §4.10 y casos 6 y 7 | Sintaxis de lista compartida incorrecta; preguntas "sin escalas" |
| El caso 2 usaba `\"` dentro de cadenas MDD (no es válido) y el parámetro de comentario usaba `"Cyan"` sin duplicar | V5.1 01 §3 y caso 2 | Errores de compilación del MDD |
| "Genera tablas de cuota únicamente si existe sintaxis corroborada" | V5.1 01 §4.13 | No crea las cuotas |
| "`SystemVariables = false` cuando el compilador lo soporte" (condición que el modelo no puede verificar) | V5.1 01 §4.18 | Variables de sistema en el conversor |
| La normalización decía "conserva letras" (Ç, Ñ y tildes son letras) | V5.1 01 §4.2 | `QPREÇO/CUSTO` como nombre de variable |
| Las bases de ejemplo usan `SIN_CODIGO_001…` como identificadores documentales | Bases OneDrive | Preguntas con número convertidas en `SIN_CODIGO_001` |
| Los MDD de ejemplo traen variables de la plantilla iField (`SOURCEPROJECTID`, `NWB_*`, `System_*`) y `INFO_INTRO_1` | Bases OneDrive | Variables no pedidas (`INICIO`, `INFO_INTRO_1`, `LINK`…) |
| "Si `94/96/98/99` siempre llevan `fix`", pero varios casos tenían `_94` sin `fix` | V5.1 01 casos 9, 17, 21 | `fix`/`exclusive` inconsistentes |
| Los casos muestran el número de pregunta en la etiqueta (`F21.`, `P18.`) y la regla decía no hacerlo en iField | V5.1 01 §4.3 vs §7 | Número de pregunta en el fraseo |
| La organización del JS por familias (visibilidad, piping, BC, routing en secciones separadas) obligaba a varios listeners por pregunta | V5.1 02 §6.1 | Varios eventos iguales para una misma pregunta |
| §4.8 pedía "limpiar respuestas de elementos que dejan de ser válidos" | V5.1 02 §4.8 | Blanquea textos cuando hay un salto |
| El caso 10 tenía llaves sin cerrar; el caso 19 asignaba la cuota después del `goTo` y sobrescribía la cuota con cada `setAnswers` | V5.1 02 §7 | Lógica incorrecta copiada del ejemplo |
| No había protocolo para salidas largas ni matriz de cobertura visible (el inventario era "interno") | V5.1 01 y 02 | Escalas y preguntas omitidas; lógica incompleta; hubo que reejecutar |

## 3. Matriz de incidencias → corrección V6

Referencias: **01** = `01_GenerarMDD.md`, **02** = `02_GenerarLogica.md`, **03** = `03_Control_QA.md`. Se excluyen las filas "No aplica" (copy-over, adicionales y proyectos anteriores a EasyScript). El proyecto piloto Gloria Reclutamiento no tiene incidencias detalladas en el Excel.

| # | Proyecto (scripter) | Incidencia | Corrección V6 | Control QA | Riesgo residual |
|---|---|---|---|---|---|
| 1 | Miraflores (Magda) | P2: elementos desordenados en el MDD | 01 C02, §4.7 (orden visual de categorías, no ordenar por código), §4.20 (orden de nodos) | QA-02, QA-03 | R |
| 2 | Miraflores | `CUOTA_RANGOEDAD_2` estaba como imagen y no salió | 01 C14, C18, §4.13, §5.A inventario de imágenes, caso 31 | QA-11, QA-21 | L |
| 3 | Miraflores | Indicaciones entre paréntesis `(MOSTRAR TARJETA)` fuera de la etiqueta | 01 C03, C04, §4.3, §4.3.1 | QA-06 | R |
| 4 | MSU Pañales (Samantha) | No generó la variable de INTRO | 01 C12, §4.1 "Textos INTRO", §4.16 | QA-23 | R |
| 5 | MSU Pañales | No muestra indicaciones al encuestador | 01 C04, léxico ENC de §4.3 | QA-06 | R · L |
| 6 | MSU Pañales | Considerar ejemplos de MaxDiff | 01 §4.12 y caso 19; 02 casos 11B y 21 | QA-22 | R |
| 7 | MSU Pañales | Identificar listas de preguntas | 01 C08, §4.10 (inventario y sintaxis canónica) | QA-19 | R |
| 8 | MSU Pañales | No crea las cuotas (tabla) | 01 C14, §4.13 (cada dimensión → `CUOTA_*`), caso 31; 02 `QUOTA_ASSIGNMENT` | QA-21 | R · L |
| 9 | INN PT Alpha (Mario) | Opciones con imágenes: generar cada opción con su código para editar | 01 C15, §4.16.2 (`{#resource:'VAR_COD.jpg'#}` + lista de recursos en QA) | QA-12 | L |
| 10 | INN PT Alpha | Incluir instrucciones de la pregunta ("Selecione apenas uma resposta") | 01 §4.3 (instrucciones al entrevistado en la etiqueta), caso 35 | QA-06 | R |
| 11 | INN PT Alpha | Respetar el orden de las opciones | 01 C02, §4.7 | QA-03 | R |
| 12 | INN PT Alpha | Mantener negrita y subrayado | 01 C03, tabla Word→HTML de §4.3 | QA-09 | L |
| 13 | OBS Lima 1200 (Magda) | No lee números entre paréntesis en opciones ni algunas indicaciones | 01 §4.7 (ya existía), C04 | QA-08, QA-06 | R |
| 14 | PA Poder Judicial (Max) | No usa listas | 01 C08, §4.10 | QA-19 | R |
| 15 | PA Poder Judicial | IDs faltantes; etiqueta completa como nombre de variable | 01 C05, §4.2 (protocolo de recuperación de IDs) | QA-13 | R |
| 16 | PA Poder Judicial | Grilla con atributos numerados → preguntas individuales | 01 C07, §4.11 "Señales de grilla", caso 32 | QA-18 | R |
| 17 | PA Poder Judicial | Categoría vacía al final `_7 "" [value = 7]` | 01 C09, §4.7, autocontrol §5.B.8 | QA-15 | R |
| 18 | PA Poder Judicial | `ConversorMd.py` toma variables de sistema | 01 C13 (`SystemVariables = false` obligatorio). **Herramienta:** ver §4 de este README | QA-24 | H |
| 19 | PA Poder Judicial | El compilador no mostró todas las preguntas; no se pudo generar lógica | 01 §5.B.8 (sintaxis: `\"`, `use` en `fields`, comas, `End Metadata`), §6.0 entrega completa | QA-01 | R · H |
| 20 | INN Trident (Julio) | Error por librería de Python no mencionada | **Herramienta:** ver §4. 01 registra dependencias del pipeline | QA-39 | H |
| 21 | Imagen Hyundai (Edgar) | Sin escalas/opciones; hubo que reejecutar | 01 C19, §6.0 (entrega por partes), autocontrol "categórica sin categorías" | QA-04 | S |
| 22 | Imagen Hyundai | Eliminó indicaciones al encuestador | 01 C04, §4.3 | QA-06 | R |
| 23 | Imagen Hyundai | Caja de texto en "Otros" sin "especificar" | 01 C10, §4.8 (señales de captura) | QA-16 | R |
| 24 | Imagen Hyundai | No crea listas para escalas repetidas | 01 C08, §4.10 | QA-19 | R |
| 25 | Imagen Hyundai | Prefiere que el número de pregunta no vaya en el fraseo (iField) | 01 parámetro `NUMERO_EN_ETIQUETA` (NO por defecto en iField), §4.3, nota en §7.5 | QA-10 | D |
| 26 | Imagen Hyundai | Algunas grillas mal creadas | 01 C07, §4.11 | QA-18 | R |
| 27 | Imagen Hyundai | Gran parte de la lógica omitida | 02 L01, matriz de reglas completa, §6.0 entrega por partes | QA-28 | S |
| 28 | Creative Lab Selecta (Edgar) | El MDD omitió varias preguntas | 01 C01, matriz de cobertura y control de secuencia de IDs en `Reporte_MDD.md`, §6.0 | QA-01 | L · S |
| 29 | Creative Lab Selecta | No respeta saltos de línea ni negritas | 01 C03, tabla Word→HTML | QA-09 | L |
| 30 | Creative Lab Selecta | Lógica solo básica (backcheck y filtro) | 02 L01, léxico de §4.1, casos 26–29 | QA-28 | S |
| 31 | MSU U&A Untables (Edgar) | No generó escalas; hubo que reejecutar | 01 C19, §6.0 | QA-04 | S |
| 32 | MSU U&A Untables | F6 y A1X con estructura incorrecta | 01 §4.11 (señales de grilla), §5.B contraste estructura por estructura | QA-18 | R |
| 33 | MSU U&A Untables | A4 dividido en `A4_1`, `A4_2`, `A4_3` | 01 C07, caso 32 | QA-18 | R |
| 34 | MSU U&A Untables | Omitió A4x, A10, D2, D3, D4a, D4b | 01 C01, matriz de cobertura, alarma de extracción (§2.4) | QA-01 | L · S |
| 35 | INN TetraTop (Max) | Auxiliar sin ID: etiqueta como ID y etiqueta vacía; usar `F3_1` | 01 C05, §4.2, caso 33 | QA-13 | R |
| 36 | INN TetraTop | `fix`/`exclusive` en todo tipo de pregunta | 01 C11, tabla de decisión de §4.8, casos corregidos | QA-17 | R |
| 37 | INN TetraTop | `__Cod` en lugar de `_Cod`; `_C__Cod` en lugar de `_C_Cod` | 01 C06, §4.2, autocontrol | QA-14 | R |
| 38 | INN TetraTop | `info` de inicio puesto al final | 01 C02, §4.16, §4.20 | QA-02, QA-23 | R |
| 39 | INN TetraTop | Variables innecesarias de link/ID (ELIMI está bien) | 01 C12, lista negra/blanca de §4.1 | QA-23, QA-24 | R · D |
| 40 | INN TetraTop | Todavía no crea listas | 01 C08 | QA-19 | R |
| 41 | INN TetraTop | No usa tipo `date` | 01 C15, §4.14 | QA-25 | R |
| 42 | INN TetraTop | Foto: categórica con "Foto adjuntada"/"Tomar foto"; adjunto en iField | 01 C15, §4.15 | QA-26 | R |
| 43 | INN TetraTop | `If` con `return` dentro de `addEventListener` | 02 L05, §4.7 (ejemplo incorrecto/correcto) | QA-31 | R |
| 44 | INN TetraTop | Validar consentimiento: `SHELL_RECORDING_CONFIRMATION` = `_A1` | 02 L08, parámetro `CODIGO_ACEPTACION_SHELL`, §4.16; 03 §27 | QA-34 | R |
| 45 | INN TetraTop | Creó validación de foto (se configura en el GUI) | 01 §4.15; 02 L11, §4.17 | QA-26 | R |
| 46 | INN TetraTop | `If`/`show`/`goto` redundantes | 02 L11, §4.7, caso 29 | QA-36 | R |
| 47 | INN TetraTop | Código en listeners de variables SHELL | 02 L06, §4.16, caso 5 reescrito | QA-32 | R |
| 48 | INN TetraTop | Asignar respuestas y mostrar/ocultar en `onBeforeNavigateTo` | 02 L07, §4.3, §4.5, casos 5, 6, 16 | QA-35 | R |
| 49 | PA Hecatombe (Héctor) | Grilla con atributos numerados → preguntas individuales | 01 C07, caso 32 | QA-18 | R |
| 50 | CEX LMCX Não Compradores (Héctor) | Sintaxis incorrecta de lista compartida | 01 C08, sintaxis canónica y tabla de errores verificados de §4.10, autocontrol §5.B.8 | QA-19 | R |
| 51 | CEX LMCX | Variables que no están en el cuestionario (`INICIO`, `INFO_INTRO_1`, `INFO_LINK`, `ID_BASE`, `LINK`) | 01 C12, lista negra de §4.1, advertencia sobre los ejemplos (§2.1) | QA-23 | R |
| 52 | CEX LMCX | Carácter especial en nombre de variable (`QPREÇO/CUSTO`) | 01 C06, transliteración ASCII de §4.2 | QA-14 | R |
| 53 | CRE PostTest Mobil (Julio) | Publicidad a randomizar quedó en un `info` y no en bloques | 01 C17, §4.11 "Rotación de módulos", caso 21 | QA-20 | R |
| 54 | CRE PostTest Mobil | Omitió una pregunta, cambió preguntas de lugar, omitió instrucciones | 01 C01, C02, C04 | QA-01, QA-02, QA-06 | L · S |
| 55 | INN OVN (Edgar) | Funciones para terminar por filtro: el script no se puede guardar (`goto` solo en Exit Events) | 02 L02, §4.7, §4.9, advertencia sobre la base (§2.1) | QA-29 | R |
| 56 | INN OVN | No puso los backchecks | 02 L08, `BACKCHECK_IMPLICA_GRABACION = SI` sin contradicciones | QA-34 | R |
| 57 | MSU Siggi (Héctor) | Instrucciones de BC tomadas como instrucciones al encuestador | 01 C04, léxico BC de §4.3; 02 §4.16 | QA-07 | R |
| 58 | MSU Siggi | Dos listas Sí/No por una tilde | 01 C08, equivalencia por tildes de §4.10, caso 34 | QA-19 | R |
| 59 | MSU Siggi | No incorpora piping del texto de otra respuesta | 01 C16, §4.16.1; 02 L09, §4.15, caso 27 | QA-27 | R |
| 60 | MSU Siggi | Instrucciones de programador tomadas como de encuestador | 01 C04, léxico PROG y precedencia de §4.3 | QA-07 | R |
| 61 | MSU Siggi | Grabación incorrecta para BC Indirect | 02 L08, "Variantes de BC" en §4.16 (se marca `PARCIAL`, no se aplica el patrón estándar en silencio). **Requiere el patrón real: ver §5** | QA-34 | D |
| 62 | MSU Siggi | Varios eventos iguales para una misma pregunta (fin de BC + cancelación) | 02 L04, §4.7, organización por pregunta en §6.1, caso 28 | QA-33 | R |
| 63 | MSU Siggi | `TERMINATE VALID` tomado como encuesta efectiva | 02 L03, léxico de §4.1, §4.9, caso 26 | QA-30 | R |
| 64 | MSU Siggi | Blanquea respuestas de texto cuando hay un salto | 02 L10, §4.8 | QA-37 | R |
| 65 | InnoTrack Bonle (Magda) | No reconoció las variables y las puso como `SIN_CODIGO_001` | 01 C05, protocolo de §4.2, alarma de §2.4, advertencia sobre los ejemplos | QA-13 | L |
| 66 | InnoTrack Bonle | No detectó todas las etiquetas HTML | 01 §4.3 (HTML literal + tabla Word→HTML) | QA-09 | L |
| 67 | InnoTrack Bonle | Cambió el texto de las preguntas | 01 C03, §4.3.1 (ya existía) | QA-05 | R |
| 68 | InnoTrack Bonle | Instrucciones intercaladas al final o no detectadas; RU/RM con color no tratados como instrucción | 01 C04 (posición exacta, color, `RU`/`RM` son instrucción y cardinalidad), ejemplo P7 de §4.3 | QA-06 | R · L |
| 69 | InnoTrack Bonle | Crea `<strong></strong>` vacías | 01 C09, §4.3, autocontrol | QA-09 | R |
| 70 | InnoTrack Bonle | Desordenó el orden del cuestionario | 01 C02, §4.20 | QA-02 | R |

### 3.1 ¿El error es del prompt o de Copilot?

**Verificación de cobertura.** El script `Herramientas/V6_Auditar_Incidencias.py` revisa el texto de los tres prompts y confirma, para cada una de las 70 incidencias, que (1) existe la regla, (2) no queda ninguna regla o ejemplo que la contradiga y (3) el QA del Paso 3 tiene su control. Resultado actual: **70/70**. Con el mismo criterio, V5.1 daba 0/70: tenía muchas reglas, pero también ejemplos y frases que las contradecían, o no tenía el control en el QA. Si se edita un prompt, se vuelve a correr: `python Herramientas/V6_Auditar_Incidencias.py Prompt/V6`.

**Riesgo residual** (última columna de la matriz):

| Código | Significado | Si la incidencia reaparece… |
|---|---|---|
| R | Regla explícita, sin contradicciones, con ejemplo y control QA | …y la confirmación de lectura está bien, es **incumplimiento del modelo** (Copilot no aplicó una regla que sí recibió) |
| L | Depende de que la herramienta **lea** el archivo completo, sus imágenes, colores, formato o la numeración automática de Word | Revisar primero la confirmación de lectura y la "Modalidad de lectura": suele ser un **límite de lectura** de la herramienta o del archivo de entrada |
| S | Depende de una **salida larga** (cuestionarios extensos) | Revisar si la respuesta se cortó o si se perdió una parte al pedir `CONTINUAR`: **límite de salida** |
| H | Depende de una **herramienta externa** (conversor, librerías) | No es del prompt (§4) |
| D | Depende de una **decisión del equipo** todavía pendiente | Es una definición pendiente (§5), no un error del prompt ni de Copilot |

**Procedimiento de diagnóstico** (para responder "¿por qué salió esto?"):

1. **¿La respuesta empieza con la CONFIRMACIÓN DE LECTURA y la clave es correcta?** Las claves están solo en la última línea de cada prompt (`MDD-V6-QUINUA-4718`, `LOG-V6-CAMU-2953`, `QA-V6-MACA-8061`). Si falta o es otra, Copilot no leyó el prompt completo: el resultado no refleja las reglas. Es un **límite de la herramienta**.
2. **¿La primera y la última pregunta que reporta coinciden con el cuestionario, y la modalidad es `DOCX_COMPLETO`?** Si no, Copilot no leyó el cuestionario completo o no vio imágenes/formato: **límite de lectura**. (Nota: varias omisiones reportadas, como D2–D4b, están al final del cuestionario, lo que es compatible con una lectura parcial, aunque no lo prueba.)
3. **¿La salida está completa?** Si se cortó o se perdió contenido entre partes: **límite de salida**.
4. **¿La incidencia está en la matriz con riesgo R?** Si pasó los puntos 1–3 y aun así no cumplió la regla, es **incumplimiento del modelo**. El prompt la contenía; conviene registrarla en el Excel indicando la regla (por ejemplo, "incumple C07") para medir qué reglas el modelo respeta menos.
5. **¿No hay ninguna regla que cubra el caso, o la regla es ambigua?** Entonces es **una mejora pendiente del prompt** (responsabilidad nuestra): se agrega la regla, su control en el QA y su fila en la matriz.

Con V6, los puntos 1–4 permiten demostrar con evidencia cuándo el problema no está en las reglas. El punto 5 sigue siendo posible: un caso que el cuestionario plantee de una forma que ninguna incidencia anterior mostró.

## 4. Incidencias que no se resuelven solo con el prompt

| # | Incidencia | Qué hace V6 | Qué falta fuera del prompt |
|---|---|---|---|
| 18 | `ConversorMd.py` incluye variables de sistema de Dimensions | El MDD sale con `SystemVariables = false`, así que el compilador no las crea | Filtrar en el conversor los campos con `IsSystem = True` al recorrer `mdm.Fields` (sugerencia del scripter) |
| 20 | Faltaba una librería de Python | Se registra como dependencia del pipeline | `ConversorMd.py` importa `markitdown`; documentar en un `requirements.txt` o en el README del repo: `pip install "markitdown[pdf,pptx]" pyreadstat pywin32 pandas numpy` (y `pyautogui pyperclip pywin32` para `KD_procesar_mdd_unicom.py`) |
| 19 | El compilador no mostró todas las preguntas | V6 previene los errores de sintaxis más comunes | Si persiste, revisar el log del compilador para ubicar la primera línea con error |

## 5. Decisiones que conviene confirmar con el equipo

1. **BC Indirect (#61).** En las cuatro bases de OneDrive no hay ningún ejemplo de "BC indirecto". V6 lo marca como `PARCIAL` para que el scripter lo complete, en vez de inventar un patrón. Si me pasas cómo debe programarse (dónde inicia y termina la grabación, qué identificador usa), lo agrego como caso corroborado y la regla pasa a `IMPLEMENTADA`.
2. **Número de pregunta en la etiqueta (#25).** V6 usa por defecto `NUMERO_EN_ETIQUETA = NO` para iField (preferencia de Edgar). En los MDD corregidos de OneDrive la práctica está dividida (~43 % de las etiquetas con número). Si otro scripter prefiere el número, basta con indicar `NUMERO_EN_ETIQUETA = SI` al ejecutar el prompt.
3. **Variables de link/ID (#39).** Max sugirió consultar un estándar. V6 aplica la regla más estricta: solo `ELIMI` y `GRACIAS_ELIMI` son obligatorias; todo lo demás debe estar en el cuestionario.
4. **`discard()` en `GRACIAS_ELIMI`.** Es el patrón mayoritario de la base (las terminaciones por filtro se descartan). Si algún proyecto necesita conservar las terminadas, se indica al ejecutar el prompt 02.
5. **Convenciones del JS real que difieren de V6 (pruebas de oct 2026).** Los JS reales de OVN y Untables usan listeners en `SHELL_AGE`/`SHELL_GENDER` y el alias `s`, graban el BACKCHECK sin condicionar a `SHELL_RECORDING_CONFIRMATION` y hacen el `discard()` en el `onNext` de `ELIMI` (sin `GRACIAS_ELIMI`). V6 mantiene lo que pidieron las incidencias #44, #47 y #56 (L06, L08, L13). Hyundai ya sigue el patrón de V6 (lee la Shell desde `INICIO`). Conviene acordar un solo estándar.

## 6. Plan de prueba sugerido (para declarar V6 final)

Reejecutar V6 con los cuestionarios que generaron incidencias y revisar el checklist QA-01…QA-42 del prompt 03:

| Proyecto | Qué valida principalmente |
|---|---|
| MSU U&A Untables / Creative Lab Selecta | Cobertura (preguntas y escalas omitidas), grillas, entrega por partes |
| PA Poder Judicial / Hecatombe | IDs, grillas numeradas, listas, categorías vacías |
| InnoTrack Bonle | `SIN_CODIGO`, HTML, instrucciones intercaladas, orden |
| MSU Siggi CUA | BC (normal e indirecto), PROG vs ENC, piping, `TERMINATE VALID`, listeners duplicados, Sí/No |
| INN Pack Test TetraTop | Auxiliares, `__Cod`, foto, fecha, `return`, Shell, `onBeforeNavigateTo` |
| CEX LMCX Não Compradores | Lista compartida, caracteres especiales, variables inventadas |
| INN OVN Product Test | `goTo` en funciones (el script debe poder guardarse) y backchecks |
| Proyecto Miraflores / MSU Pañales | Cuotas en imagen, INTRO, MaxDiff |

Criterio sugerido: V6 es final cuando, en esos proyectos, el checklist no tenga `FALLA` en controles `CRÍTICA`/`ALTA` y el script se pueda importar y guardar en iField sin corregir sintaxis.

## 7. Qué reporte sale en cada paso

| Archivo | Paso | Quién lo hace | Para qué sirve |
|---|---|---|---|
| `Reporte_MDD.md` | 1 | El mismo prompt que generó el MDD | Autocontrol. Empieza por "Qué revisar primero" (lo único que hay que leer si todo está bien); luego estado, control de secuencia de IDs, matriz de cobertura, imágenes y dependencias para la lógica. Guía la revisión del scripter antes de pasar a `MDD_FINAL` |
| `Reporte_Logica.md` | 2 | El mismo prompt que generó la lógica | Autocontrol: matriz de reglas, listeners generados, reglas bloqueadas o parciales. Guía la revisión del scripter antes de pasar a `Logica_FINAL` |
| `Reporte_QA.md` | 3 | Prompt 03, independiente | Auditoría final de Cuestionario ↔ MDD_FINAL ↔ Lógica_FINAL con el checklist QA-01…QA-42 |

### ¿Qué tan confiable es el `Reporte_MDD.md`?

Lo escribe el mismo modelo que generó el MDD. Si el modelo **no vio** una pregunta (por ejemplo, porque estaba en un cuadro de texto o una imagen que la herramienta no leyó), tampoco la pondrá en la matriz de cobertura. Para que eso no pase desapercibido, V6 agrega tres controles que no dependen de que el modelo "se acuerde":

1. **Control de secuencia de IDs:** el reporte recorre la numeración del cuestionario y lista cada salto (P5 → P7) con su explicación. Un salto sin explicar es la señal más rápida de una pregunta omitida. Al scripter le basta mirar esa tabla.
2. **Modalidad de lectura:** si dice `SOLO_TEXTO` o `PARCIAL`, la herramienta no vio imágenes ni formato; hay que volver a ejecutar adjuntando el PDF.
3. **Totales:** preguntas del cuestionario frente a preguntas del MDD.

Aun así, el reporte reduce el tiempo de revisión pero no reemplaza una pasada del scripter por el índice del cuestionario. El QA del Paso 3 vuelve a verificar la cobertura de forma independiente.

Los reportes de los pasos 1 y 2 no reemplazan al QA: son el "parte de trabajo" del generador. El QA del Paso 3 no da por buena ninguna afirmación de esos reportes sin verificarla.

## 8. Cómo se mantiene V6

- **Si una prueba falla, se corrigen solo los prompts de esta carpeta** (`01`, `02`, `03`), agregando o ajustando la regla en la sección 4, su resumen en la sección 0 y su control en el checklist del prompt 03. Luego se agrega la fila correspondiente en la matriz de incidencias (§3).
- **Versiones:** mientras V6 esté "en validación", se edita aquí. Cuando se declare final, los cambios siguientes van en una copia `Prompt/V6.1/` y se actualiza `js/repository-config.js` para que la web cargue la versión nueva.
- **Las bases de OneDrive no se tocan para corregir errores.** Los prompts V6 ya indican que, si un ejemplo contradice una regla, prevalece el prompt. Solo se actualizan en dos casos:
  1. Para **agregar estudios nuevos**: se consolidan con `Herramientas/KB_Consolidar_CLM.py` (genera los `*_UNIDO`) y se regeneran las bases 2 y 3 con los prompts de la carpeta `Base de conocimiento/`.
  2. Si un **ejemplo incorrecto** de la base se sigue copiando aunque el prompt lo prohíba (por ejemplo, las funciones `OSM.Survey.Term` con `goTo` o los listeners en `SHELL_AGE`), conviene corregir o quitar ese ejemplo de la base.

## 9. Historial

- V2–V4: flujo de 4 prompts con Markdown intermedio (histórico).
- V5: base conceptual separada + 3 prompts.
- V5.1: 3 prompts autosuficientes (base integrada en la sección 7 de cada uno). Última versión usada en producción.
- V6: V5.1 + correcciones de las 70 incidencias del reporte, eliminación de contradicciones internas, sección 0 de reglas críticas, autocontroles, entrega por partes y checklist de incidencias en QA.
- V6 (actualización oct 2026, tras probar Claude Sonnet, Gemini Argon y GPT free en OVN, Untables y Hyundai contra la metadata y el JS reales; ver `Comparacion_Modelos_V6.xlsx`):
  - 01: C20 lo tachado no existe (y nueva tabla §7.1 "Instrucciones tachadas — NO programar" en el reporte); C21 la leyenda de colores del cuestionario manda; C22 + §4.22 bloque estándar `B_NSE` (idéntico en los 3 estudios reales); disparador "MOSTRAR IMÁGENES" en C15/4.16.2; 6 patrones nuevos en el autocontrol 5.B.8 (`other(...)` mal ubicado, listas sin `define`, `ELIMI`, tachados, color de programador, NSE inventado).
  - 02: L16 no programar lo tachado; L17 + §4.23 lógica estándar del NSE (cálculo, filtro y cuota).
  - 03: QA-40 contenido tachado, QA-41 módulo NSE, QA-42 opciones con imagen.
  - Base de conocimiento: sin cambios (el bloque NSE ya está en la base BHT-MSU-CRE y ahora va también dentro de los prompts, así que sirve con cualquier base).
