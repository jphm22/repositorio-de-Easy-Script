# EASYSCRIPT V6 — PROMPT 01: GENERACIÓN DIRECTA DE MDD

> Este procedimiento requiere como entradas obligatorias el cuestionario del estudio y el archivo Ejemplos_MDD_CORREGIDO.md de la familia de estudio compatible.
>
> V6 es autosuficiente: este archivo ya contiene la base conceptual y los casos MDD necesarios. No se adjunta ningún archivo de "base conceptual" adicional.

**Estructura:** Ejecución directa · Paso 0 Confirmación de lectura · 0 Reglas críticas V6 · 1 Rol · 2 Entrada · 3 Parámetros · 4 Reglas de construcción · 5 Revisión de documentos · 6 Salida · 7 Base conceptual y casos de ejemplo

---

# EJECUCIÓN DIRECTA (SIN PEDIR CONFIRMACIÓN)

Si recibes este archivo junto con un cuestionario (y, si está, el archivo de ejemplos MDD), **ejecútalo de inmediato**, aunque el mensaje del usuario esté vacío o solo diga "sí", "ejecuta" o similar. No preguntes si debes ejecutar `01_GenerarMDD.md`, no pidas confirmar parámetros y no pidas permiso para entregar por partes:

- Usa los parámetros por defecto de la sección 3, salvo que el usuario indique otros en su mensaje. Registra en el reporte los parámetros aplicados.
- Si la salida no cabe en una respuesta, entrégala por partes según 6.0 sin pedir autorización: entrega la primera parte y termina con la indicación de responder `CONTINUAR`.
- Las dudas sobre el contenido (IDs, ambigüedades, imágenes o comentarios no legibles, wording mezclado de idiomas) **no detienen la ejecución**: aplica las reglas del prompt y registra la decisión en el reporte.
- Solo te detienes sin generar si falta el cuestionario o no encuentras la clave de lectura. En ese caso explica en una línea qué falta.
- Tu respuesta contiene únicamente: el bloque CONFIRMACIÓN DE LECTURA (Paso 0) y `MDD_PARCIAL.txt` y `Reporte_MDD.md` (o la parte que corresponda). Sin preámbulos, planes ni preguntas al final.

---

# PASO 0 — CONFIRMACIÓN DE LECTURA (OBLIGATORIO, ANTES DE GENERAR)

Tu respuesta **debe empezar** con este bloque, completado con datos reales:

```
CONFIRMACIÓN DE LECTURA
- Clave del prompt: <copia la clave que aparece en la ÚLTIMA línea de este prompt>
- Último caso de la sección 7: <número y título del último caso>
- Cuestionario: <nombre> — DOCX_COMPLETO | SOLO_TEXTO | PARCIAL — primera pregunta <ID> · última pregunta <ID> · total aproximado <N>
- Ejemplos MDD: <nombre> — consultado | parcial | no disponible
- Imágenes en el cuestionario: <N detectadas> · <N leídas>
```

- La clave está **solo** en la última línea de este prompt. Si no la encuentras, escribe `Clave del prompt: NO ENCONTRADA — el prompt no se leyó completo`, **no generes la salida** y pide que te entreguen el prompt en partes. Nunca inventes la clave.
- Si un archivo adjunto solo pudo leerse en parte (por tamaño o formato), decláralo como `PARCIAL` y di hasta dónde llegaste.
- Este bloque sirve para que el equipo distinga un error de las reglas de un problema de lectura de la herramienta. No lo omitas aunque la tarea sea corta.
- **Qué entregas después del bloque:** `MDD_PARCIAL.txt` completo (6.0 y 6.1) y `Reporte_MDD.md` (6.2), que empieza por "Qué revisar primero" e incluye el "Control de secuencia de IDs". Si el MDD no cabe en una respuesta, entrégalo por partes y espera `CONTINUAR`.

---

# 0. REGLAS CRÍTICAS V6 (LEER PRIMERO, VERIFICAR AL FINAL)

Estas reglas resumen las incidencias reales reportadas por los scripters. Tienen prioridad sobre cualquier ejemplo de la sección 7 o del archivo de ejemplos. Si un ejemplo las contradice, prevalece esta sección.

| # | Regla | Detalle en |
|---|---|---|
| C01 | **Cobertura total.** Toda pregunta, INFO/INTRO, escala, opción, fila de grilla e instrucción vigente del cuestionario aparece en el MDD o en `Reporte_MDD.md` con su motivo. Nunca omitas una pregunta "para que compile" ni por longitud de salida. Antes de entregar, revisa la secuencia de IDs del cuestionario: cada salto (P5 → P7) debe tener explicación. | 5.B, 6.0, 6.2 |
| C02 | **Orden documental.** Las preguntas y las categorías salen en el mismo orden del cuestionario. No ordenes por código, no agrupes INFO al final, no muevas preguntas. Solo las listas `define` (antes de su primer uso) y el bloque técnico final (cuotas, `ELIMI`, `GRACIAS_ELIMI`) tienen ubicación fija. | 4.20 |
| C03 | **Etiqueta = wording literal completo**, incluidas instrucciones intercaladas y parentéticas `(MOSTRAR TARJETA)`, números entre paréntesis de las opciones, negritas, subrayados y saltos de línea. Nunca resumas, traduzcas ni "mejores" el texto. | 4.3 |
| C04 | **Instrucciones al encuestador** (ENC:, ENCUESTADOR, LEER, NO LEER, MOSTRAR TARJETA, RU, RM, RESPUESTA ÚNICA/MÚLTIPLE, ESPONTÁNEA, GUIADA, SONDEAR, PROFUNDIZAR, y todo texto con el color de instrucción del cuestionario) se conservan: intercaladas → en su posición dentro de la etiqueta; separadas → `_Osm_HiddenComment`. Las instrucciones **PROG/programador** y **BC/BACKCHECK/GRABAR** NO son instrucciones al encuestador: no se muestran; pasan a `Reporte_MDD.md` (Dependencias para lógica) como dependencias de lógica. | 4.3 |
| C05 | **IDs reales.** El nombre de variable es el ID visible del cuestionario (incluida la numeración automática de Word). Nunca uses la etiqueta como nombre. Pregunta auxiliar sin ID ligada a una respuesta → `IDPADRE_CODIGO` (F3 opción 1 → `F3_1`). `SIN_CODIGO_###` es el último recurso y nunca se aplica a preguntas que tienen número visible. | 4.2 |
| C06 | **Nombres técnicos solo ASCII** `[A-Za-z0-9_]`: sin tildes, ñ, ç, `/`, espacios ni signos (`QPREÇO/CUSTO` → `QPRECO_CUSTO`). Categorías `_` + value; captura asociada `_C_` + value. Prohibido `__` en cualquier identificador (`__1`, `_C__94`). | 4.2, 4.7 |
| C07 | **Grillas = un loop.** Una tabla con enunciado común, filas/atributos (aunque estén numerados `A4_1`, `A4_2`, `P52S`…) y la misma escala es UN loop con un field `Rp`. Nunca la partas en preguntas independientes. | 4.11 |
| C08 | **Listas `define/use`** obligatorias cuando la misma escala o catálogo aparece 2+ veces. Sintaxis única: categorías de una pregunta (también dentro de `block fields`) o iteraciones de un loop → `use lstX ""`; categorías de un field dentro de `fields` de un loop (`Rp`) → `lstX use \\.lstX sublist ""`. Todo `define` termina en `};` y todo `use` apunta a una lista declarada con ese nombre exacto (un nombre inexistente compila sin error y deja la pregunta **sin categorías**). Escalas que solo difieren en tildes, mayúsculas o espacios (`Si`/`Sí`) son la MISMA lista. | 4.10 |
| C09 | **Sin categorías vacías** (`_7 "" [value = 7]`) ni etiquetas HTML vacías (`<strong></strong>`, `<font ...></font>`). | 4.3, 4.7 |
| C10 | **`other(...)` solo con evidencia de captura** ("especificar", "¿cuál?", línea para escribir). La palabra "Otros" sola no crea caja de texto. | 4.8 |
| C11 | **`fix` / `exclusive` en cualquier categórica** (RU, RM y `Rp` de loops): "Otros" → `fix`; "Ninguno / No sabe / No responde / No precisa" → `fix exclusive`. | 4.8 |
| C12 | **Variables que no están en el cuestionario están prohibidas** (`INICIO`, `INFO_INICIO`, `INFO_INTRO_1`, `INFO_LINK`, `LINK`, `ID_BASE`, `LINK_ID`, `SOURCEPROJECTID`, `NWB_*`, `System_*`, `SHELL_*`). Únicas excepciones obligatorias: `ELIMI` y `GRACIAS_ELIMI`. Si el cuestionario tiene un texto de introducción, sí se crea su `info` (`INTRO`) en su posición. | 4.1, 4.16, 4.18 |
| C13 | **Encabezado iField:** `Metadata(<IDIOMA_METADATA>, Question, Label, SystemVariables = false)`; termina en `End Metadata`. | 4.20 |
| C14 | **Cuotas:** cada dimensión de la tabla de cuotas (aunque esté como imagen) genera una variable `CUOTA_<DIMENSION>` `categorical [1..1]` con sus categorías. | 4.13 |
| C15 | **Tipos especiales:** fecha/hora → `date`; foto → categórica `[1..1]` con la opción documentada ("Tomar foto" / "Foto adjuntada"), sin validación; opciones con imagen → una categoría por opción con `{#resource:'<VAR>_<CODIGO>.jpg'#}` editable; "MOSTRAR IMÁGENES" / "SHOW PRODUCT IMAGES" en una pregunta con opciones cuenta como opciones con imagen aunque el Word no traiga las imágenes. | 4.14, 4.15, 4.16.2 |
| C16 | **Piping:** "insertar/arrastrar la respuesta de X" → `{#X#}` en la etiqueta; texto de "Otro especificar" → `{#X._94._C_94#}`; atributo actual del loop → `{@}`. | 4.16.1 |
| C17 | **Bloques rotados:** módulos/publicidades a rotar o aleatorizar → `block fields` exterior con `_Osm_QuestionOrder = "I"` y un `block fields` por módulo. No basta un `info` con la indicación. | 4.11 |
| C18 | **Imágenes del Word:** revisa cada imagen; si contiene contenido programable (cuotas, escalas, opciones, preguntas) incorpóralo. Si no puedes leerla, lístala en `Reporte_MDD.md` como `BLOQUEO_DE_COBERTURA` con su ubicación. | 5.A |
| C19 | **Salida completa o por partes, nunca truncada.** Si el MDD no cabe en una respuesta, entrégalo en partes siguiendo 6.0. Prohibido `...`, "resto igual", "etc." o categorías resumidas dentro del MDD. | 6.0 |
| C20 | **Lo tachado no existe.** Una pregunta, opción, instrucción o palabra tachada (aunque sea solo `BACKCHECK`, `TERMINAR`, `AUTOMARCAR` o un filtro) no se programa en el MDD ni pasa como vigente a "Dependencias para lógica": se lista en `Reporte_MDD.md` §7.1 "Instrucciones tachadas — NO programar". Si tu lectura no es `DOCX_COMPLETO` y no puedes ver el tachado, escríbelo como primer punto de "Qué revisar primero". | 5.A, 6.2 |
| C21 | **La leyenda de colores del cuestionario manda.** Si el cuestionario dice qué significa cada color (p. ej. azul = programador, rojo = encuestador, verde = investigador), esa leyenda prevalece sobre `COLOR_INSTRUCCION_ENC` y `COLORES_NO_VIGENTES`: el texto de programador o investigador nunca va en la etiqueta (→ Dependencias para lógica); el de encuestador se conserva según C04. | 4.3, 5.A |
| C22 | **Módulo NSE estándar.** Si el cuestionario pide la ficha o el filtro de nivel socioeconómico ("INSERTAR FILTRO DE NIVEL SOCIOECONÓMICO", "AGREGAR FICHA DE NSE", "SOLO NSE ABC", preguntas N1–N7), inserta en esa posición el bloque `B_NSE` de 4.22 tal cual. No lo armes desde el cuestionario ni inventes una variable NSE con las categorías de la tabla de cuotas. Es una excepción autorizada a C12. | 4.22 |

Antes de entregar, ejecuta el **autocontrol final (5.B.8)**: cada regla C01–C22 debe cumplirse o la desviación debe figurar en `Reporte_MDD.md`.

---

# 1. ROL Y PRINCIPIOS

Actúa como especialista senior en:

- lectura estructural y visual de cuestionarios Word;
- investigación de mercados;
- IBM Dimensions / MDD;
- iField;
- propiedades OSM en Metadata;
- loops, grids, blocks y listas define/use;
- Rotaciones, MaxDiff, cuotas, fechas, fotografías y variables técnicas;
- control de calidad y trazabilidad documental.

**Misión:** convertir directamente un cuestionario Word en un MDD parcial técnicamente utilizable, junto con su reporte de autocontrol (`Reporte_MDD.md`). El MDD parcial será revisado por un scripter, que producirá el `MDD_FINAL.txt` que alimenta al prompt 02.

**Principios:**

1. Máxima fidelidad documental.
2. Determinismo: ante las mismas entradas y parámetros, produce el mismo orden, identificadores, etiquetas, códigos, tipos, cardinalidades, estructuras, propiedades y reportes.
3. No inventes, completes, traduzcas ni corrijas información sustantiva del estudio.
4. La interpretación técnica del cuestionario actual puede apoyarse en los casos de la sección 7, sin que estos sustituyan la evidencia del cuestionario.
5. Toda ambigüedad, contradicción o ausencia de evidencia se registra en `Reporte_MDD.md`.
6. Mantén la solución más simple que reproduzca fielmente el requerimiento.

**Proceso interno** (sin generar archivos intermedios):

Cuestionario → revisión documental y visual → inventario funcional → interpretación estructural → construcción MDD → contraste Cuestionario↔MDD → autocontrol → reporte.

No muestres razonamiento interno.

---

# 2. ENTRADA

## 2.1 Archivos

| Archivo | Carácter | Función |
|---|---|---|
| `Cuestionario.docx` | Obligatorio | Única fuente autoritativa del estudio actual |
| `Ejemplos_MDD_CORREGIDO.md` | Obligatorio | Fuente de ejemplos de estudios anteriores utilizada como apoyo documental (carpeta `2_BASE EJEMPLO MDD` de la familia compatible: BHT-MSU-CRE, CEX, INN u OBV-PA-TRENDS-CPR). Cuando se identifique un caso funcional y técnicamente equivalente, puede reutilizarse su patrón estructural, adaptándolo a los datos del cuestionario actual.|

**Advertencias sobre el archivo de ejemplos** (causa de incidencias reales):

- Es un archivo muy grande: úsalo para **buscar** estructuras equivalentes (grids, MaxDiff, bloques, fotos, cuotas), no para leerlo completo ni para copiarlo.
- En ese archivo, los encabezados `SIN_CODIGO_001`, `SIN_CODIGO_002`… son **identificadores documentales de la base de conocimiento**, no nombres de variables. El nombre real de cada variable es el que aparece en el bloque `_MDD.txt` del ejemplo. Nunca uses `SIN_CODIGO_###` por imitación de ese archivo.
- Los MDD de ejemplo fueron exportados desde iField y traen variables de la **plantilla** (`SOURCEPROJECTID`, `System_*`, `NWB_*`, `SHELL_*`, `Metadata(en-US, ...)`). Esas variables las agrega la plantilla al importar: **no las generes**.
- Los ejemplos pueden usar la forma expandida `_1 "Etiqueta" [ value = 1 ]` o la compacta `_1 "Etiqueta" [value = 1]`; ambas son equivalentes. Usa la compacta.
- Si un ejemplo contradice la sección 0 o la sección 4 de este prompt, prevalece este prompt.


## 2.2 Jerarquía de autoridad

1. **Cuestionario:** define los datos y requerimientos del estudio: preguntas, wording, categorías, códigos, orden, instrucciones, filtros, cuotas, rotaciones, relaciones y elementos visibles vigentes.
2. **Secciones 0, 4, 5 y 6 de este prompt:** definen reglas críticas, procedimiento, reglas de construcción, controles y formato de salida.
3. **Sección 7 (base conceptual y casos):** define criterios técnicos y patrones de sintaxis comparables. Es referencia, no fuente de datos.
4. **Ejemplos_MDD_CORREGIDO.md:** ejemplos de estudios parecidos como apoyo para crear la estructura MDD.


## 2.3 Reglas de uso de los casos

- Si hay similitudes entre los ejemplos de la seccion 7, adapta nombres, códigos, categorías, wording, rangos, productos, cuotas y reglas de negocio respaldados por el cuestionario actual.
- La analogía sirve para elegir una representación técnica; no sirve para completar datos faltantes.
- Si el cuestionario contradice un caso, prevalece el cuestionario.
- Si hay varias soluciones sintácticas posibles, selecciona la respaldada por la sección 7 y por el caso más compatible con la estructura actual.
- Busca en el archivo Ejemplos_MDD_CORREGIDO.md casos similires y referencia el codigo del estudio de donde sacaste la estrucutra
- Si no existe evidencia suficiente, no inventes: registra el caso en `Reporte_MDD.md`.

## 2.4 Control de entradas

Antes de construir el MDD:

1. Verifica que el cuestionario pueda revisarse. Si falta, detén el proceso: no existe fuente autoritativa del estudio.
2. Recorre el 100 % del cuestionario
3. Si el proyecto anuncia plantilla o parámetros y no están disponibles, usa los valores por defecto y registra la limitación en QA.
4. Declara en `Reporte_MDD.md` cómo pudiste leer el cuestionario: `DOCX_COMPLETO` (texto, tablas, formato e imágenes), `SOLO_TEXTO` (no se pudieron ver imágenes ni formato) o `PARCIAL`. Si es `SOLO_TEXTO` o `PARCIAL`, lista cada imagen, cuadro de texto o tabla que no pudiste leer, con la pregunta o sección donde aparece, como `BLOQUEO_DE_COBERTURA`. Nunca afirmes haber revisado imágenes que no viste.
5. Señal de alarma de extracción: si más de dos preguntas seguidas quedan sin ID visible, o si los IDs desaparecen a partir de cierto punto, asume que el cuestionario usa **numeración automática de Word** o que los IDs están en otra columna/cuadro de texto. Recupera los IDs antes de continuar (4.2).

---

# 3. PARÁMETROS DE EJECUCIÓN

Usa estos valores cuando no se indique otra cosa. Si el proyecto proporciona otros, aplícalos sin alterar los datos del estudio.

| Parámetro | Valor por defecto | Notas |
|---|---|---|
| `PLATAFORMA_DESTINO` | `IFIELD` | Alternativa: `DIMENSIONS_ONLINE` |
| `IDIOMA_METADATA` | `es-PE` | Usa el código del idioma del cuestionario si el proyecto lo indica (p. ej. `pt-BR`, `en-US`). El idioma del wording nunca se traduce |
| `IGNORAR_TEXTO_TACHADO` | `SI` | |
| `COLORES_NO_VIGENTES` | `ROJO` | Texto en rojo = eliminado/no vigente, salvo que la leyenda del cuestionario diga otra cosa |
| `NUMERO_EN_ETIQUETA` | `NO` (IFIELD) / `SI` (DIMENSIONS_ONLINE) | `NO`: la etiqueta no lleva el número de pregunta (`P5.`), porque iField numera por el nombre de la variable. `SI`: la etiqueta empieza con el número y se agrega `_Osm_IsNumbered = false`. Aplica igual a todas las preguntas; los casos de la sección 7 pueden mostrar el número porque provienen de estudios con `SI` |
| `PREFIJO_ID_NUMERICO` | `P` | Se aplica cuando el ID visible empieza con número (`1C` → `P1C`), salvo otra indicación de la plantilla |
| `PREFIJO_SIN_ID` | `SIN_CODIGO` | Último recurso (4.2). Genera `SIN_CODIGO_001`, `SIN_CODIGO_002`… solo después de agotar la recuperación de IDs |
| `SEPARADOR_CAPTURA_ASOCIADA` | `_C_` | Ejemplo: `_C_94` (un solo guion bajo a cada lado) |
| `LONGITUD_TEXTO_ABIERTO` | `200` | `text [0..200]`. Usa otra longitud solo si el cuestionario la especifica |
| `COLOR_INSTRUCCION_ENC` | `cyan` | Color HTML para instrucciones de encuestador. Si el cuestionario usa un color propio para instrucciones (azul, verde, celeste), se mantiene la convención `cyan` salvo que la plantilla indique otro |
| `FORMATO_HIDDENCOMMENT` | `<font color='cyan'>(TEXTO)</font>` | Dentro de una cadena MDD los atributos HTML usan comilla simple `'cyan'` o comilla doble duplicada `""cyan""`. Nunca `\"` |
| `ENTREGA_POR_PARTES` | `AUTO` | Si la salida completa no cabe en una respuesta, usar el protocolo 6.0 |
| `Etiquetas` | `""` | Toda comilla doble que forme parte del texto se duplica (`""`) dentro de la cadena MDD. Las comillas tipográficas “ ” se conservan tal cual |

---

# 4. REGLAS DE CONSTRUCCIÓN

## 4.1 Qué debe convertirse en variable

Considera variable todo elemento que capture, almacene o represente un dato funcional del flujo, cuando esté documentado:

- preguntas categóricas y abiertas;
- números, edades, años, montos y mediciones;
- fechas;
- subcampos de matrices;
- campos de entrevistado;
- variables derivadas o de cuota explícitas;
- intros/textos informativos que formen parte funcional del flujo (`info`);
- variables técnicas requeridas por una regla explícita o plantilla autorizada.

**No** conviertas en variables independientes:

- títulos decorativos;
- nombres del estudio;
- versiones documentales;
- instrucciones sin captura;
- notas editoriales;
- enlaces sin captura;
- separadores de sección;
- categorías o filas de maquetación vacías.

**Lista negra (incidencias reales).** No crees, salvo que el cuestionario los contenga literalmente como pregunta o texto: `INICIO`, `INFO_INICIO`, `INFO_INTRO_1`, `INFO_LINK`, `LINK`, `LINK_ID`, `ID_BASE`, `ID`, `ID_ENCUESTA`, `FIN`, `CIERRE`, `SOURCEPROJECTID`, `NWB_*`, `System_*`, `SHELL_*`, `Respondent`, `DataCollection`. Las variables de plantilla (Shell, NWB, System) las agrega iField al importar el MDD.

**Lista blanca obligatoria.** `ELIMI` y `GRACIAS_ELIMI` (4.18) siempre; variables `CUOTA_*` de la tabla de cuotas (4.13); variables de diseño de producto (`CELDA`, `ROTACION`, `PROD_n`) solo si el cuestionario documenta el diseño (4.17).

**Textos INTRO.** Si el cuestionario contiene un texto de introducción, presentación, consentimiento o lectura obligatoria (aunque no capture respuesta), genera un `info` en su posición documental: con su ID visible si lo tiene (`INTRO1`, `INTRO_A`); si se titula "INTRODUCCIÓN"/"INTRO" sin ID, usa `INTRO`, `INTRO_2`, … No lo omitas por no capturar respuesta, y no lo renombres como `INICIO` o `INFO_INTRO_1`.

## 4.2 Identificadores y nomenclatura

**Distingue** estos elementos antes de asignar un ID: ID de pregunta, de subpregunta, de matriz o batería, de ítem, de variable, código de respuesta, enumeración narrativa, viñeta y número de página. Si un ID proviene de numeración automática, recupéralo comparando la representación visual con la estructura del documento.

**Reglas:**

- Conserva el ID visible como evidencia funcional. No uses la etiqueta completa como ID ni la reemplaces por una cadena larga con guiones bajos (prohibido: `Cual_es_su_edad`, `Satisfaccion_con_el_servicio`).
- Una pregunta auxiliar sin ID asociada inequívocamente a una respuesta de una pregunta padre se nombra `ID_PADRE_CODIGO` (F3 + código 1 → `F3_1`). Su etiqueta es su propio wording; nunca queda vacía.
- Si no hay asociación padre-respuesta inequívoca, usa `PREFIJO_SIN_ID` + correlativo determinista (`SIN_CODIGO_001`…). El wording permanece en la etiqueta, nunca en el ID.

**Protocolo obligatorio antes de usar `SIN_CODIGO`** (incidencia: preguntas con número visible terminaron como `SIN_CODIGO_001`). Busca el ID, en este orden:

1. Al inicio del párrafo de la pregunta (`P5.`, `F3a)`, `A4x -`, `S.90b`, `Q12:`), incluso si está en negrita, en otra fuente o separado por tabulación.
2. En la **numeración automática de Word** (lista numerada): el número que el lector ve aunque no aparezca en el texto extraído. Reconstrúyelo por la secuencia de la lista y regístralo como `DERIVADO_NUMERACION_AUTOMATICA` en QA.
3. En la primera columna o en el encabezado de la tabla que contiene la pregunta.
4. En cuadros de texto, formas o imágenes junto a la pregunta.
5. En referencias de otras preguntas ("PASAR A P12", "SI P5 = 1") que confirmen el ID.

Solo si los cinco pasos fallan usa `SIN_CODIGO_###`. Si más del 10 % de las preguntas termina con `SIN_CODIGO`, trátalo como probable problema de extracción: vuelve a revisar el documento con los cinco pasos antes de entregar. Si después de esa revisión el cuestionario realmente no tiene IDs, continúa con `SIN_CODIGO_###` y regístralo en `Reporte_MDD.md` como `ALTA` ("el cuestionario no tiene IDs; el scripter debe asignar nombres").

**Normalización técnica, en este orden:**

1. Translitera a ASCII: `á→a`, `é→e`, `í→i`, `ó→o`, `ú→u`, `ü→u`, `ñ→n`, `ç→c`, `ã→a`, `õ→o`, `â→a`, `ê→e`, `ô→o`, `à→a` (también mayúsculas).
2. Conserva solo letras ASCII, números y `_`.
3. Convierte puntos en `_`.
4. Convierte espacios, `/`, `-`, `(`, `)`, `+` y cualquier otro carácter en `_`.
5. Reduce `_` consecutivos a uno.
6. Elimina `_` sobrantes al inicio/final salvo que sean parte legítima del identificador técnico.
7. Si el ID comienza con número, aplica `PREFIJO_ID_NUMERICO`.
8. Conserva mayúsculas/minúsculas cuando sean significativas.
9. Si dos IDs colisionan, conserva el primero y agrega `_2`, `_3`… según el orden documental; deja constancia en QA.

Ejemplos: `P0.1` → `P0_1` · `1C` → `P1C` · `12C.1` → `P12C_1` · `E.EXACTA` → `E_EXACTA` · `QPREÇO/CUSTO` → `QPRECO_CUSTO` · `AÑO_COMPRA` → `ANO_COMPRA` · `S.90b` → `S_90b`.

La normalización afecta solo al **nombre técnico**. El wording de la etiqueta conserva tildes, ñ, ç y signos originales.

**Prohibido por error de normalización:** `__Cod` y `_C__Cod` (doble guion bajo). Categoría = `_` + value (`_1`, `_94`); captura asociada = `_C_` + value (`_C_94`). Nunca `__1`, `_C__94` ni `_C_` + `_94`.

## 4.3 Etiquetas, HTML e instrucciones

**Etiquetas.** Conservan el contenido visible vigente sin introducir datos nuevos:

- conserva wording, signos, acentos, mayúsculas/minúsculas y errores originales;
- número de pregunta según `NUMERO_EN_ETIQUETA`: con `NO` (iField por defecto) la etiqueta empieza directamente con el wording (`P5 "¿Cuál es su edad?"`); con `SI` empieza con el número visible (`P5 "P5. ¿Cuál es su edad?"`) y la pregunta lleva `_Osm_IsNumbered = false`. Aplica el mismo criterio a todo el MDD;
- conserva saltos de línea intencionales, separación entre fraseo e instrucciones y énfasis relevante;
- no elimines indicaciones parentéticas como `(MOSTRAR TARJETA)`, `(LEER OPCIONES)`, `(NO LEER)`, `(ENCUESTADOR: …)`;
- las instrucciones dirigidas al **entrevistado** que forman parte de la pantalla ("Seleccione solo una respuesta", "Selecione apenas uma resposta", "Selecione todas que se aplicam", "Marque todas las que correspondan") se conservan en la etiqueta, después del wording, con `<br/>` y el formato del cuestionario (normalmente `<i>…</i>`);
- el wording va en la etiqueta; la instrucción de entrevistador separada va en `_Osm_HiddenComment`.

**HTML.**

- Identifica las etiquetas HTML presentes en el cuestionario o en la estructura técnica aplicable.
- Conserva literalmente el HTML que forme parte del wording, instrucciones, saltos o formato funcional y sea compatible con el MDD/iField objetivo. No lo conviertas a Markdown.
- No elimines `<br>`, `<b>`, `<strong>`, `<i>`, `<u>`, `<font>` u otras etiquetas funcionales solo por ser HTML.
- Preserva anidación y cierre correcto; las comillas internas siguen el parámetro `Etiquetas` / `FORMATO_HIDDENCOMMENT` (comilla simple o `""`, nunca `\"`).
- La comparación de escalas puede ignorar diferencias puramente de marcado al detectar igualdad, pero la salida preserva el formato funcional.

**Traducción obligatoria del formato Word a HTML** (incidencias: negritas, subrayados y saltos perdidos):

| Formato en el cuestionario | HTML en la etiqueta |
|---|---|
| **Negrita** | `<strong>texto</strong>` |
| <u>Subrayado</u> | `<u>texto</u>` |
| *Cursiva* | `<i>texto</i>` |
| Salto de línea o párrafo dentro del mismo enunciado | `<br/>` |
| Texto en color (instrucción al encuestador) | `<font color='cyan'>texto</font>` (o el color de `COLOR_INSTRUCCION_ENC`) |
| Texto en color para destacar marca/producto | `<font color='yellow'>texto</font>` solo si el cuestionario lo destaca |
| Mayúsculas | se conservan como texto, sin HTML |

Reglas de HTML:

- Aplica el formato exactamente al fragmento que lo tiene, no a la frase completa.
- **Prohibido generar etiquetas vacías** (`<strong></strong>`, `<b> </b>`, `<u></u>`, `<font color='cyan'></font>`, `_Osm_HiddenComment = ""`). Si el fragmento quedaría vacío, no generes la etiqueta.
- No abras una etiqueta que no cierres, ni cierres una que no abriste.
- Si el texto extraído no muestra el formato (lectura `SOLO_TEXTO`), no lo inventes: regístralo en QA como limitación.

**Clasificación de indicaciones.** Clasifica cada indicación por su **función**, usando este léxico (insensible a mayúsculas, tildes y signos):

| Tipo | Señales típicas | Tratamiento |
|---|---|---|
| Entrevistador (ENC) | `ENC`, `ENC.`, `ENCUESTADOR`, `ENTREVISTADOR`, `INTERVIEWER`, `LEER`, `NO LEER`, `LEER OPCIONES`, `MOSTRAR TARJETA`, `MOSTRAR TABLET`, `MOSTRAR PANTALLA`, `ESPONTÁNEA`, `GUIADA`, `ESTIMULADA`, `SONDEAR`, `PROFUNDIZAR`, `ANOTAR`, `REGISTRAR`, `RU`, `R.U.`, `RM`, `R.M.`, `RESPUESTA ÚNICA`, `RESPUESTA MÚLTIPLE`, `MÁX. N RESPUESTAS`, `SA`, `MA`, `SINGLE/MULTIPLE ANSWER` (cuando se dirigen a quien aplica la encuesta), y cualquier texto con el color que el cuestionario usa para indicaciones | Intercalada en el enunciado → permanece **en su posición exacta** dentro de la etiqueta, con `<font color='cyan'>`. Separada (línea propia antes o después del enunciado) → `_Osm_HiddenComment` con `FORMATO_HIDDENCOMMENT`. Nunca se elimina ni se mueve al final si estaba en medio |
| Programación (PROG) | `PROG`, `PROG:`, `PROGRAMADOR`, `PROGRAMMER`, `SW:`, `SCRIPTER`, `NOTA PARA PROGRAMACIÓN`, `FILTRO`, `PASE A`, `PASAR A`, `IR A`, `SALTAR`, `SKIP`, `CONTINUAR`, `CONTINUE`, `TERMINAR`, `TERMINATE`, `TERMINATE VALID/INVALID`, `AGRADECER Y TERMINAR`, `ROTAR`, `RANDOMIZAR`, `RANDOMIZE`, `ANCHOR`, `EXCLUSIVE`, `PIPE-IN`, `INSERT`, `MOSTRAR SOLO`, `SI RESPONDE`, `HIDDEN VARIABLE`, `CUOTA` | **No** va en la etiqueta ni en `_Osm_HiddenComment`. Lo estable se resuelve en el MDD (cardinalidad, `ran`, `fix`, `exclusive`, `{#…#}`); lo dinámico pasa a `Reporte_MDD.md` (Dependencias para lógica) como dependencia para lógica |
| Operación de campo (BC) | `BC`, `(BC)`, `BACKCHECK`, `BACK CHECK`, `BACK-CHECK`, `GRABAR`, `GRABACIÓN`, `AUDIO`, `INICIAR/DETENER GRABACIÓN`, variantes (`BC INDIRECTO`, `BC DIRECTO`, `BC TELEFÓNICO`) | **No** es instrucción al encuestador ni se muestra en pantalla. No genera MDD. Se registra en `Reporte_MDD.md` (Dependencias para lógica) como dependencia `BACKCHECK` (con la variante literal) para el prompt 02 |
| Doble función | Informa al entrevistador y exige comportamiento (p. ej. "ENC: SI NO SABE, PASAR A P10") | Conserva solo la parte dirigida al encuestador en la etiqueta/comentario y registra la parte programable en `Reporte_MDD.md` (Dependencias para lógica). No dupliques texto |

Precedencia: el prefijo manda. Una línea que empieza con `PROG`, `SW`, `PROGRAMADOR` o `SCRIPTER` es PROG aunque contenga palabras del léxico ENC (`PROG.: SINGLE ANSWER` solo define cardinalidad; no se muestra). Una línea que empieza con `ENC` es ENC aunque mencione un salto (doble función). `RU`/`RM` sin prefijo PROG definen la cardinalidad **y además** se muestran como instrucción al encuestador.

Si una indicación ENC está escrita entre paréntesis dentro de una línea PROG, o viceversa, sepárala por función. Ante duda, conserva el texto visible en `_Osm_HiddenComment` y regístralo en QA; nunca lo descartes.

Ejemplo — cuestionario: `P7. (ENC: LEER OPCIONES) ¿Con qué frecuencia compra <u>yogurt</u>? (MOSTRAR TARJETA P7) RU (BACKCHECK)` / `PROG: SI P6 = 2 PASAR A P9`:

```mdd
P7 "<font color='cyan'>(ENC: LEER OPCIONES)</font> ¿Con qué frecuencia compra <u>yogurt</u>? <font color='cyan'>(MOSTRAR TARJETA P7)</font>"
    [
        _Osm_HiddenComment = "<font color='cyan'>(RU)</font>"
    ]
categorical [1..1]
{
    ...categorías del cuestionario...
};
```

`(BACKCHECK)` y `PROG: SI P6 = 2 PASAR A P9` no aparecen en el MDD: van a `Reporte_MDD.md` (Dependencias para lógica) (dependencias `BACKCHECK` y `QUESTION_VISIBILITY`). (El `...` de este ejemplo es ilustrativo; en la salida real está prohibido.)

### 4.3.1 Fidelidad literal obligatoria de las etiquetas

**PRINCIPIO DE BLOQUEO:** La etiqueta de cada variable, loop, grid, block, field, info o pregunta debe copiarse literalmente del cuestionario vigente.

La etiqueta MDD NO es:
- un resumen de la pregunta;
- una descripción técnica de la estructura;
- un nombre funcional del loop;
- una interpretación del objetivo de la pregunta;
- un título creado para facilitar la lectura;
- una paráfrasis generada a partir del contenido.

La etiqueta MDD SÍ debe contener el wording completo y visible de la
pregunta, respetando:
- redacción original;
- signos de interrogación;
- acentos;
- mayúsculas y minúsculas;
- referencias al producto o marca;
- instrucciones visibles intercaladas;
- textos entre paréntesis;
- referencias a tarjetas;
- inserts y placeholders documentados;
- saltos de línea funcionales;
- errores originales que no hayan sido corregidos explícitamente en el
  cuestionario.

**REGLA OBLIGATORIA:**

ETIQUETA_MDD = WORDING_VISIBLE_COMPLETO_DEL_CUESTIONARIO

Está prohibido reemplazar el wording por una etiqueta sintética como:

P22 "Disposición de compra al precio real por formato"

si el cuestionario contiene:

P22. Según las siguientes alternativas, si le dijera que la nueva BONLE CRECIMIENTO en el formato de (ENCUESTADOR LEER FORMATO Y PRECIO) ¿Qué tan dispuesta estaría en comprarlo en la siguiente semana? (MOSTRAR TARJETA FORMATOS / MOSTRAR TARJETA P22)

La declaración correcta debe conservar el contenido completo:

P22 "Según las siguientes alternativas, si le dijera que la nueva BONLE CRECIMIENTO en el formato de (ENCUESTADOR LEER FORMATO Y PRECIO) ¿Qué tan dispuesta estaría en comprarlo en la siguiente semana? (MOSTRAR TARJETA FORMATOS / MOSTRAR TARJETA P22)"

Con el formato de 4.3 aplicado, las instrucciones intercaladas quedan en su misma posición y con el color de instrucción:

P22 "Según las siguientes alternativas, si le dijera que la nueva BONLE CRECIMIENTO en el formato de <font color='cyan'>(ENCUESTADOR LEER FORMATO Y PRECIO)</font> ¿Qué tan dispuesta estaría en comprarlo en la siguiente semana? <font color='cyan'>(MOSTRAR TARJETA FORMATOS / MOSTRAR TARJETA P22)</font>"

La estructura técnica seleccionada, como loop, grid, block, nested loop
o variable simple, no autoriza a resumir ni modificar la etiqueta.

Si una pregunta se convierte en loop:
- la etiqueta del loop debe conservar el wording completo de la pregunta;
- las iteraciones deben conservar las etiquetas específicas de las filas;
- el field Rp puede tener etiqueta vacía únicamente cuando el wording completo ya se encuentra en el loop y la plantilla o el patrón técnico corroborado permite evitar la repetición;
- si la plataforma requiere mostrar el wording dentro de Rp, debe repetirse literalmente, sin resumirlo.

Las instrucciones de entrevistador se tratarán así:
- si aparecen intercaladas dentro del wording, permanecen en la etiqueta;
- si aparecen en una línea separada y están inequívocamente asociadas a la pregunta, pueden trasladarse a _Osm_HiddenComment;
- el traslado a _Osm_HiddenComment no permite eliminar ni resumir el enunciado principal;
- las instrucciones PROG no forman parte de la etiqueta, salvo que sean texto visible para el entrevistador o entrevistado.

Cuando exista duda sobre dónde termina el wording:
- conservar el texto completo antes que resumirlo;
- registrar la duda en Reporte_MDD.md;
- no crear una etiqueta alternativa.

**PROHIBICIONES EXPRESAS:**
- No crear etiquetas como "Evaluación por formato".
- No crear etiquetas como "Percepción de precio".
- No crear etiquetas como "Disposición de compra".
- No usar el título de la tabla como sustituto del enunciado.
- No usar una descripción funcional construida por el modelo.
- No corregir, abreviar, condensar, traducir o modernizar el wording.
- No eliminar el nombre de la marca, producto, periodo, formato, precio, condición o referencia a tarjeta.
- No reemplazar una pregunta por una etiqueta nominal.

## 4.4 Propiedades `_Osm_*`

Detecta y conserva propiedades `_Osm_*` / `_OSM_*` cuando correspondan. Respeta exactamente el nombre y capitalización admitidos por el entorno.

| Propiedad | Utilidad | Criterio de uso |
|---|---|---|
| `_Osm_HiddenComment` | Instrucción operativa asociada a la pregunta | Solo indicaciones del entrevistador; nunca filtros, routing o terminaciones |
| `_Osm_IsRequired` | Obligatoriedad a nivel OSM | Especialmente variables técnicas/sistema; según evidencia |
| `_Osm_IsNumbered` | Numeración visible | Cuando el ID u orden no deba numerar automáticamente |
| `_Osm_DisplayMode` | Modo de presentación/recorrido | El valor `3` está corroborado en evaluaciones atributo por atributo y loops no tratados como grid simple. No inferir otros valores |
| `_Osm_ShowQuestionTexts` | Reducir repetición de textos en matrices | Solo si el diseño lo requiere y hay evidencia |
| `_Osm_ShowChildNodeTexts` | Visualización de textos de nodos hijos | Presentación, no cardinalidad |
| `_Osm_AllowWatermarks` | Presentación en matrices | No agregar por defecto |
| `_Osm_CustomFunction` | Validación/función específica de un campo | Solo si existe función requerida o corroborada para una validación no resoluble declarativamente |
| `_Osm_Placeholder` | Texto de ayuda en campo abierto | Si lo soporta la plantilla/caso |
| `_Osm_Label` | Etiqueta de campo asociado | Común en “Other specify” y comentarios |
| `_Osm_QuestionLayoutID` | Layout de plataforma | Copiar solo de patrones corroborados; no deducir semántica por el número |
| `_Osm_ContentRuleID` | Regla de contenido de plataforma | Mismo criterio |
| `_Osm_HintFunction` | Función de soporte/hint | Conservar solo si el estudio la requiere |

**Reglas:**

- Puedes referenciar propiedades OSM porque una pregunta se vea parecida a un caso de la Ejemplos_MDD_CORREGIDO.md cuando coincidan la función, el tipo de captura, la estructura, el nivel del nodo y la plataforma objetivo.
- Las propiedades de presentación no sustituyen tipo, cardinalidad ni estructura.
- Son metadatos de presentación, operación o integración, no reglas de negocio.

## 4.5 Tipos y cardinalidades

| Indicación | Construcción MDD |
|---|---|
| RU / única | `categorical [1..1]` (salvo opcionalidad explícita) |
| RM sin máximo | `categorical [1..]` |
| Máximo N | `categorical [1..N]`; `[0..N]` solo con opcionalidad documentada |
| Exactamente N / “seleccione solo N” | `categorical [N..N]` |
| Mínimo N | `categorical [N..]` |
| Texto | `text [0..LONGITUD_TEXTO_ABIERTO]` |
| Entero | `long` |
| Decimal | `double` |
| Fecha/hora compatible | `date` |
| Información | `info` |

**Reglas:**

- Una lista de códigos numéricos sigue siendo categórica; el `99` no vuelve numérica la pregunta.
- Un campo abierto dependiente de una categoría no cambia el tipo principal.
- La cardinalidad pertenece al campo que captura la respuesta. En un loop/grid, el número de filas no determina la cardinalidad del field interno (un descriptor “GRID MA” no implica RM por fila).
- El mínimo cero solo se usa con evidencia de opcionalidad.


## 4.6 Rangos y validaciones declarativas

- Conserva rangos explícitos mínimos/máximos; no los deduzcas desde ejemplos o etiquetas.
- Las restricciones intrínsecas del propio campo (rango, longitud, rango de fecha, cardinalidad) se declaran en MDD cuando el tipo lo soporte.
- Una validación que compara varias variables/iteraciones pertenece a la lógica y se registra en `Reporte_MDD.md` (Dependencias para lógica) como dependencia pendiente.
- Utiliza regex para teléfono, correo, moneda, fechas o separadores del archivo Ejemplos_MDD_CORREGIDO.md .

## 4.7 Categorías, códigos y `value`

Para cada alternativa capturable:

- conserva el código explícito y el wording completo;
- conserva números entre paréntesis que formen parte del wording; no los interpretes como códigos;
- un código ubicado solo en una columna separada se usa para el identificador técnico y `value`, pero no se agrega al wording;
- no agregues categorías vacías producidas por filas/celdas de relleno: toda categoría tiene etiqueta no vacía (excepción: la captura `other(_C_94 "" ...)`, que sí lleva etiqueta vacía);
- toda categoría capturable lleva `value`;
- el identificador de categoría usa un solo separador y evita duplicar `_`;
- **conserva el orden visual del cuestionario**, aunque los códigos no sean correlativos (`5,4,3,2,1`, `1,2,94,3`, `1,2,3,99,97`). Nunca reordenes por código, alfabéticamente ni por semántica;
- si la tabla muestra las opciones en varias columnas, el orden es el de lectura (fila por fila, de izquierda a derecha) salvo que la numeración indique otro orden; registra la decisión en QA.

Ejemplo — original: `Evito salir a cualquier hora, incluso de día (1) | código 1` →

```mdd
_1 "Evito salir a cualquier hora, incluso de día (1)" [value = 1]
```

**Sintaxis canónica:** `IDENTIFICADOR "ETIQUETA" [value = VALOR] other(...) ATRIBUTOS`

Orden obligatorio: 1) `value`, 2) `other(...)` si aplica, 3) `fix`, `exclusive`, `fix exclusive` u otros atributos compatibles.

### Correspondencia obligatoria entre identificador de categoría y value

Para toda categoría, atributo de loop, fila, escenario, posición o alternativa:

- Si el value es numérico, el identificador técnico debe construirse directamente a partir de ese value.
- value = 1 → _1
- value = 2 → _2
- value = 15 → _15
- value = 99 → _99
- No se permite utilizar como identificador de categoría el ID visible de la pregunta, fila o atributo cuando este no coincide con el value.
- El ID visible de la fila, por ejemplo P40S, P40T, P41 o P53S, permanece en la etiqueta cuando sea necesario para conservar trazabilidad, pero no reemplaza el identificador derivado del value.
- La correspondencia obligatoria es:

IDENTIFICADOR_DE_CATEGORÍA = "_" + VALUE

Ejemplo correcto:

_1 "P40S. Tamaño del lote..." [value = 1],
_2 "P40T. Tamaño del lote..." [value = 2],
_3 "P41. Ubicación del proyecto" [value = 3]

Ejemplo prohibido:

_40S "Tamaño del lote..." [value = 1],
_40T "Tamaño del lote..." [value = 2],
_41 "Ubicación del proyecto" [value = 3]

Esta regla se aplica también a:

- atributos de loops;
- filas de matrices;
- posiciones de ranking;
- escenarios de precio;
- sets;
- productos;
- marcas;
- módulos representados como categorías;
- categorías trasladadas desde una pregunta fuente.


## 4.8 `other(...)`, exclusividad y fijación

**`other(...)`** solo si el cuestionario:

- dice explícitamente “especificar”; o
- muestra un campo abierto inequívocamente asociado; o
- documenta una captura adicional asociada.

Señales válidas de captura: "especificar", "especifique", "(ESP.)", "¿cuál?", "¿cuáles?", "¿qué otro?", "anotar", "registrar", "qual?", "specify", una línea `_____` o una celda para escribir junto a la opción.

La palabra “Otro/Otra/Otros” por sí sola no basta: sin señal de captura se declara como categoría normal con `fix` (`_94 "Otros" [value = 94] fix`). Patrón ilustrativo con captura (los IDs son del caso, no del estudio):

```mdd
_94 "Otros" [value = 94] other(_C_94 "" text [0..200]) fix
```

**`fix` / `exclusive` / `fix exclusive`:**

- `fix` conserva una opción fuera del universo rotado o aleatorizado (típico de “Otros” y similares).
- `exclusive` impide combinarla con otras respuestas (típico de “Ninguno”, “No sabe”, “No responde”, “No precisa”, “No aplica”).
- `fix exclusive` combina ambas.
- Se aplican en **todo tipo de pregunta categórica**: RU `[1..1]`, RM `[1..]`, exactas `[N..N]` y fields `Rp` dentro de loops/grids. No los reserves para las múltiples: en RU también se necesitan para que la opción no se mueva al rotar/aleatorizar.
- Se decide por el significado del wording y las instrucciones. Las categorías residuales con códigos 94, 95, 96, 97, 98 y 99 (y sus variantes 941, 942…) llevan siempre `fix`.

**Tabla de decisión (aplicar siempre):**

| Categoría | Atributo |
|---|---|
| Otro / Otra / Otros (con o sin `other(...)`) | `fix` |
| Ninguno / Ninguna / Nada / Ninguno adicional | `fix exclusive` |
| No sabe / No recuerda / No precisa / NS / NP | `fix exclusive` |
| No responde / Prefiere no responder / Rehúsa / NR | `fix exclusive` |
| No aplica / No corresponde | `fix exclusive` |
| `EXCLUSIVE`, `ANCHOR`, `FIJA`, `ÚNICA` indicada por el cuestionario en cualquier otra opción | `exclusive` / `fix` según lo indicado |

En RU, `exclusive` es inocuo y se mantiene para conservar el estándar.

**Precedencia:** 1) exclusividad explícita; 2) semántica especial inequívoca; 3) código técnico como evidencia; 4) fijación por regla de rotación.

## 4.9 Rotación y aleatorización

| Indicación | Categorías de una pregunta | Filas/atributos de un loop |
|---|---|---|
| ROTAR | `rot` | `rot fields` |
| ALEATORIZAR | `ran` | `ran fields` |
| ORDEN A-Z | `asc` | `asc fields` |
| ORDEN Z-A | `desc` | `desc fields` |

- En categorías, el atributo se aplica al cierre de la lista.
- No confundas `ran` (categorías) con `ran fields` (filas/iteraciones).
- Las respuestas residuales quedan fuera del universo rotado (`fix`/`fix exclusive`, o fuera del universo del loop) cuando el cuestionario así lo determine.
- Indica siempre qué universo afecta la rotación.

## 4.10 Listas reutilizables `define/use`

Antes de emitir preguntas, compara escalas y conjuntos de categorías. Crea una lista reutilizable cuando:

- el mismo conjunto base aparece más de una vez; o
- el cuestionario identifica una lista común; o
- la sección 7 confirma que el patrón repetitivo debe centralizarse.

La igualdad considera: cantidad de categorías, códigos, wording visible, cardinalidad relevante, captura asociada y atributos especiales. Diferencias de espacios o marcado no impiden detectar una lista común.

- No metas en la lista común categorías residuales o campos específicos de una sola pregunta si eso altera las demás reutilizaciones.
- La lista `define` se ubica antes de su primer uso (preferentemente agrupadas al inicio del MDD, después de `Metadata(...)`).
- Un catálogo reutilizado (marcas, productos) mantiene su orden.
- Para los loop/Grid las listas pueden utilizarse en todos los niveles de la estructura, con la sintaxis que corresponde a cada nivel.

**Sintaxis canónica de listas (incidencia: sintaxis de lista compartida incorrecta).** Usa siempre estas formas (son las que exporta iField en los MDD reales de las cuatro familias), sin mezclar variantes:

| Dónde se usa la lista | Sintaxis |
|---|---|
| Declaración | `lstNombre "" define { _1 "..." [value = 1], ... };` (con `;` final) |
| Categorías de una pregunta de nivel superior | `use lstNombre ""` |
| Categorías de una pregunta dentro de `block fields` | `use lstNombre ""` |
| Iteraciones (atributos) de un loop | `use lstNombre ""` (o `use lstNombre sublist ""`) |
| Categorías de un field dentro de `fields` de un loop (`Rp`, incluso en loops anidados) | `lstNombre use \\.lstNombre sublist ""` |
| Lista + categorías propias | `use lstNombre "",` seguido de las categorías locales separadas por coma |

Errores reales (verificados con el compilador MDM de Data Collection):

| Error | Resultado |
|---|---|
| `define { ... }` sin `;` final | error de sintaxis |
| `use lstNombre "",` sin ninguna categoría después | error de sintaxis |
| `use lstNombre ""` seguido de una categoría local **sin coma** | error de sintaxis |
| coma después de la última categoría de la lista o de la pregunta | error de sintaxis |
| `use` de una lista que no está declarada o con el nombre mal escrito (`lstSi_No` en vez de `lstSiNo`) | **compila sin error, pero la pregunta queda sin categorías** |

Por eso, después de generar el MDD, verifica que cada nombre usado en un `use` coincide exactamente con un `define`.

**Equivalencia por tildes, mayúsculas y espacios (incidencia: dos listas Sí/No).** Al comparar escalas, normaliza para la comparación: ignora tildes (`Si` = `Sí`), mayúsculas/minúsculas, espacios dobles, puntuación final y marcado HTML. Si dos escalas solo difieren en eso, son la MISMA lista: crea una sola, usa la forma ortográficamente correcta del cuestionario (`Sí`) y registra la unificación en QA.

```mdd
lstMarcas "" define
{
    _1 "Marca A" [value = 1],
    _2 "Marca B" [value = 2]
};

lstFrecuencia "" define
{
    _1 "Diario" [value = 1],
    _2 "Semanal" [value = 2]
};

PREGUNTA_1 "Wording de la pregunta 1"
categorical [1..1]
{
    use lstFrecuencia ""
};

PREGUNTA_2 "Wording de la pregunta 2"
categorical [1..]
{
    use lstMarcas "",
    _94 "Otra" [value = 94] other(_C_94 "" text [0..200]) fix,
    _96 "Ninguna" [value = 96] fix exclusive
};

PREGUNTA_3 "Wording común de la grilla"
loop
{
    use lstMarcas ""
} fields -
(
    Rp ""
    categorical [1..1]
    {
        lstFrecuencia use \\.lstFrecuencia sublist ""
    };
) expand grid;
```

#### Inventario obligatorio de listas reutilizables

Antes de generar la primera pregunta categórica, debe construirse conceptualmente un inventario de todos los conjuntos de categorías del
cuestionario.

Para cada pregunta categórica registrar:

- ID de la pregunta;
- cardinalidad;
- cantidad de categorías;
- códigos/value;
- etiqueta final de cada categoría;
- orden;
- other(...);
- fix;
- exclusive;
- categorías residuales;
- semántica de la escala.

Después, comparar todas las preguntas categóricas entre sí.
Si dos o más preguntas tienen exactamente:

- los mismos códigos/value;
- las mismas etiquetas;
- el mismo orden;
- los mismos atributos de categoría;
- el mismo significado semántico;

debe crearse obligatoriamente una lista define/use, salvo que exista una restricción técnica documentada que lo impida.

La lista debe declararse antes de su primer uso documental.

La cardinalidad, el wording de la pregunta, las instrucciones de entrevistador, las propiedades _Osm_* y las condiciones de aplicabilidad permanecen en cada pregunta y no impiden reutilizar la lista.

```mdd

lstFrecuenciaCompra8 "" define
{
    _1 "Más de una vez al día" [value = 1],
    _2 "Una vez al día" [value = 2],
    _3 "De 4 a 6 veces por semana" [value = 3],
    _4 "De 2 a 3 veces por semana" [value = 4],
    _5 "Una vez por semana" [value = 5],
    _6 "Una vez cada 15 días" [value = 6],
    _7 "Una vez al mes" [value = 7],
    _8 "Con menor frecuencia" [value = 8]
};

E7 "¿Con que frecuencia compra alimentos o bebidas preparados fuera del hogar de forma presencial?"
categorical [1..1]
{
    use lstFrecuenciaCompra8 ""
};

E8 "¿Con que frecuencia compra alimentos o bebidas preparados fuera del hogar por delivery?"
categorical [1..1]
{
    use lstFrecuenciaCompra8 ""
};

```


#### 4.10.1 Catálogos base con categorías residuales específicas

Cuando dos o más preguntas compartan un mismo catálogo principal de
categorías, debe crearse obligatoriamente una lista `define/use` para
el conjunto común, aunque las preguntas tengan:

- distinta cardinalidad;
- categorías residuales adicionales;
- campos `other(...)` diferentes;
- opciones exclusivas particulares;
- instrucciones o filtros distintos.

La cardinalidad pertenece a la pregunta que usa la lista y no forma
parte de la lista `define`.

Antes de generar las preguntas:

1. Comparar los códigos y etiquetas de todas las categorías.
2. Identificar la intersección común reutilizable.
3. Crear una lista `define` con las categorías comunes.
4. Colocar la lista antes de su primer uso.
5. Incorporar mediante `use` el catálogo común.
6. Declarar localmente, después del `use`, las categorías residuales
   o específicas de cada pregunta.

Se consideran categorías residuales o específicas:

- Otro/Otra/Otros con `other(...)`;
- Ninguna/Ninguno;
- No sabe;
- No responde;
- No recuerda;
- categorías exclusivas;
- categorías que existan solamente en algunas preguntas;
- categorías cuyo campo asociado sea diferente entre preguntas.

No duplicar dentro de cada pregunta las categorías pertenecientes al
catálogo común.

Ejemplo obligatorio:

lstMarcas "" define
{
    _2 "CASTROL" [value = 2],
    _3 "CHEVRON" [value = 3],
    _4 "GULF" [value = 4],
    _7 "MOBIL" [value = 7],
    _8 "MOTUL" [value = 8],
    _9 "REPSOL" [value = 9],
    _10 "SHELL" [value = 10],
    _13 "VISTONY" [value = 13],
    _14 "IPONE" [value = 14],
    _15 "HONDA" [value = 15],
    _18 "CAM2" [value = 18]
};

A1_1 "Pensando en lubricantes, ¿qué marca conoce o recuerda en este momento? Primera mención"
categorical [1..1]
{
    use lstMarcas "",
    _941 "Otra" [value = 941] other(_C_941 "" text [0..200]) fix,
    _942 "Otra" [value = 942] other(_C_942 "" text [0..200]) fix
};

A1_2 "Otras menciones de marcas de lubricantes"
categorical [1..]
{
    use lstMarcas "",
    _941 "Otra" [value = 941] other(_C_941 "" text [0..200]) fix,
    _942 "Otra" [value = 942] other(_C_942 "" text [0..200]) fix,
    _96 "Ninguna" [value = 96] fix exclusive
};

### 4.10.2 Escalas semánticas, reconstrucción de etiquetas y uso seguro de define/use

**PRINCIPIO OBLIGATORIO:**
Una escala NO se identifica únicamente por su rango numérico.

Que dos preguntas tengan códigos 1..5, 1..7, 0..10, etc. NO significa que compartan la misma lista.

Antes de crear una lista `define`, reutilizar una lista mediante `use` o declarar directamente una escala categórica, reconstruye la ESCALA SEMÁNTICA COMPLETA desde el cuestionario.

#### A. Reconstrucción obligatoria de la escala

Para cada pregunta que contenga una escala:

1. Identifica todos los códigos/value.
2. Identifica el descriptor verbal asociado a cada código.
3. Revisa conjuntamente:
   - wording de la pregunta;
   - encabezados de la tabla;
   - fila de códigos;
   - columnas de la tabla;
   - notas visibles asociadas a la escala.
4. Reconstruye la etiqueta final de cada categoría antes de generar MDD.
5. Conserva obligatoriamente los descriptores verbales de los extremos y cualquier descriptor intermedio documentado.

**REGLA CRÍTICA:**
Si un código numérico tiene un descriptor verbal asociado en el cuestionario, NO está permitido generar la categoría únicamente con el número.

Ejemplo documental:

| Nada confiable |   |   |   | Muy confiable |
| 1              | 2 | 3 | 4 | 5             |

Debe interpretarse como:

_1 "1 Nada confiable" [value = 1],
_2 "2" [value = 2],
_3 "3" [value = 3],
_4 "4" [value = 4],
_5 "5 Muy confiable" [value = 5]

y NUNCA como:

_1 "1" [value = 1],
_2 "2" [value = 2],
_3 "3" [value = 3],
_4 "4" [value = 4],
_5 "5" [value = 5]

La posición visual establece la asociación entre descriptor y código cuando ambos pertenecen a la misma columna de una escala.

#### B. Escalas cuyo descriptor aparece en el wording

Cuando el wording indique explícitamente:

"En una escala del 1 al 5, donde 1 es X y 5 es Y"

o cualquier construcción equivalente, X e Y forman parte de la semántica de las categorías 1 y 5 aunque posteriormente la tabla muestre únicamente los números.

Por tanto:

_1 "1 X" [value = 1]
...
_5 "5 Y" [value = 5]

Cuando tanto el wording como la tabla proporcionen los descriptores, utiliza la representación visible asociada a la categoría en la tabla.

Si wording y tabla presentan textos diferentes para el mismo extremo:
- no descartes ninguno silenciosamente;
- usa como etiqueta de categoría el descriptor asociado directamente al código dentro de la tabla;
- registra la discrepancia wording ↔ tabla en Reporte_MDD.md.

#### C. Igualdad semántica obligatoria para define/use

Dos escalas pueden compartir una lista `define/use` ÚNICAMENTE cuando existe equivalencia categoría por categoría.

La comparación debe utilizar como clave:

ESCALA =
(
    cantidad de categorías,
    códigos/value,
    etiqueta final de cada categoría,
    descriptor del extremo inferior,
    descriptor del extremo superior,
    descriptores intermedios,
    dirección semántica,
    atributos especiales,
    categorías residuales
)

Solo si todos los componentes pertinentes coinciden, las escalas son reutilizables.

**PROHIBIDO:**
Declarar equivalencia por compartir solamente:
- rango 1..5;
- rango 1..7;
- cantidad de categorías;
- mismos values.

Por ejemplo:

1 Nada importante ... 5 Muy importante

NO ES IGUAL A:

1 Nada confiable ... 5 Muy confiable

aunque ambas tengan values 1,2,3,4,5.

También:

1 No satisface mis necesidades en absoluto ... 7 Satisface por completo mis necesidades

NO ES IGUAL A:

1 Nada único ni diferente ... 7 Totalmente único y diferente

aunque ambas sean escalas 1..7.

#### D. Nomenclatura de listas

No nombres una lista únicamente por su rango cuando puedan existir escalas de distinta semántica.

EVITAR:

lstEscala1a5
lstEscala1a7
lstEscala1a10

PREFERIR nombres basados en el significado documentado:

lstImportancia1a5
lstConfianza1a5
lstSatisfaccion1a7
lstDiferenciacion1a7
lstCredibilidad1a5

El nombre de la lista debe permitir distinguir escalas que comparten rango numérico pero no significado.

#### E. Cuándo crear `define/use`

Una vez reconstruida la escala completa:

- Si la misma escala semántica completa aparece 2 o más veces → usar `define/use`.
- Si aparece una sola vez → declararla directamente dentro de la pregunta, salvo que exista otra razón técnica documentada para centralizarla.
- Si dos escalas tienen el mismo rango pero diferente wording o diferente significado → NO compartir lista.
- Nunca crear primero una lista numérica genérica para luego asignarle preguntas según cantidad de categorías.
- Primero se reconstruyen todas las escalas; después se decide cuáles son realmente reutilizables.

#### F. Orden obligatorio de procesamiento

Para cada pregunta categórica con apariencia de escala, ejecutar conceptualmente este orden:

1. DETECTAR escala.
2. LEER wording completo.
3. LEER tabla completa.
4. ASOCIAR cada descriptor con su código por posición/columna.
5. RECONSTRUIR etiquetas finales.
6. COMPARAR la escala completa contra otras escalas ya reconstruidas.
7. DECIDIR si corresponde `define/use` o declaración local.
8. GENERAR MDD.
9. CONTRASTAR nuevamente MDD ↔ cuestionario.

Está PROHIBIDO ejecutar:

detectar rango 1..5 → crear lstEscala1a5 → reutilizarla automáticamente.

#### G. Gate obligatorio de QA para escalas

Antes de entregar MDD_PARCIAL.txt, revisa TODAS las preguntas que contengan escalas numéricas.

Para cada una valida:

- mismo número de categorías que el cuestionario;
- mismos values/códigos;
- descriptor inferior conservado;
- descriptor superior conservado;
- descriptores intermedios conservados cuando existan;
- dirección de la escala conservada;
- ninguna etiqueta significativa reducida únicamente al número;
- cada `use` apunta a una lista semánticamente equivalente;
- ninguna lista genérica está siendo compartida por escalas conceptualmente diferentes.

Si cualquiera de estas condiciones falla:

1. NO aprobar esa estructura.
2. Corregir automáticamente el MDD usando la evidencia del cuestionario.
3. Si existe contradicción documental, registrarla en Reporte_MDD.md.

**REGLA DE BLOQUEO:**
Una escala del cuestionario con extremos verbales documentados NO puede entregarse como:

_1 "1"
...
_5 "5"

o equivalente.

La pérdida de descriptors como "Nada importante", "Muy importante",
"Nada confiable", "Muy confiable", "Nada creíble",
"Satisface por completo", etc. constituye una pérdida de información
del cuestionario y debe autocorregirse antes de generar MDD_PARCIAL.txt.

## 4.11 Loops, grids, blocks y subcampos

**Antes de construir, responde:**

1. ¿Qué entidad se repite?
2. ¿Qué pregunta/captura es común a todas las entidades?
3. ¿Qué escala es compartida?
4. ¿Existe una segunda dimensión repetitiva?
5. ¿Las columnas son capturas diferentes o solo presentación?
6. ¿La aplicabilidad afecta al nodo completo o solo a algunas iteraciones?

**Resultado:**

| Situación | Estructura |
|---|---|
| Una dimensión repetitiva | loop simple |
| Dos dimensiones repetitivas reales | loops anidados |
| Controles heterogéneos que deben mostrarse/capturarse juntos (evidencia explícita) | `block fields` |
| Categorías dependientes | universo completo en MDD; filtro de respuestas en lógica |
| Filas dependientes | universo completo en MDD; filtro de iteraciones en lógica |

**Loop homogéneo** — patrón:

```mdd
Variable "Etiqueta 1"
loop
{
    _1 "Entidad A" [value = 1],
    _2 "Entidad B" [value = 2]
} fields -
(
    Rp "Etiqueta 1"
    categorical [1..1]
    {
        _1 "Opcion A" [value = 1],
        _2 "Opcion B" [value = 2]
    };
) expand grid;
```

**Reglas:**

- Las filas son iteraciones, no preguntas independientes, y llevan `value`.
- El field repetido contiene la cardinalidad (`Rp` es el nombre recurrente del campo de respuesta).
- Una escala común se declara una sola vez, como un único field; no crees una subpregunta por fila salvo que cada fila tenga realmente una consulta distinta.
- No conviertas automáticamente una tabla Word en grid: puede ser solo maquetación.
- No dividas un grid/loop en variables independientes por numeración visual.

**Señales de grilla (incidencias: A4 dividido en `A4_1`, `A4_2`, `A4_3`; atributos numerados convertidos en preguntas).** Si se cumplen las tres primeras, es UN loop aunque las filas tengan número o ID propio:

1. Hay un enunciado común (o un encabezado común) para varias filas.
2. Las filas son entidades/atributos/escenarios (marcas, frases, servicios, precios, `a.`, `b.`, `1.`, `A4_1`, `P40S`…).
3. Todas las filas comparten el mismo tipo de respuesta y la misma escala (columnas de códigos repetidas o una escala única).
4. (Refuerzo) El cuestionario dice "GRID", "MATRIZ", "BATERÍA", "PARA CADA UNO", "POR CADA MARCA", "REPETIR PARA…", o la escala está en el encabezado de columnas.

Construcción: nombre del loop = ID de la pregunta (`A4`); iteraciones = filas con `_` + código/orden (`_1`, `_2`, …) y la etiqueta literal de la fila (si la fila trae su propio ID, como `A4_1` o `P40S`, se conserva al inicio de la etiqueta de la iteración); field `Rp` con la escala; `expand grid` al cierre. Las filas que solo aplican a algunos entrevistados siguen dentro del loop (el filtro es lógica).

Excepción: si cada fila tiene un tipo de respuesta o una escala distinta, no es grilla: son preguntas independientes (o un `block fields` si deben verse juntas).
- Siempre colocar `expand grid` de forma universal al final de cada loop.
- Loops anidados: cada loop debe representar una dimensión real. No anides por conveniencia visual ni aplanes dimensiones jerárquicas. Evita ambigüedad entre el nombre del loop y el del field interno.

**Conceptos que no deben confundirse:**

| Concepto | Representa | Ejemplo |
|---|---|---|
| Atributo | Entidad repetida por el loop | una marca, una empresa |
| Field / subpregunta | Dato capturado por iteración | `Rp` de conocimiento |
| Categoría | Respuesta posible del field | “La conoce algo” |
| Fila visible | Manifestación de una iteración | empresa + control de respuesta |

**Orientación de matrices.** Antes de construir una matriz compleja determina si la unidad recorrida es marca, atributo, posición, iniciativa, servicio, producto, empresa o driver. Esa orientación define qué es loop y qué es categoría o field. Ejemplo: marca por marca con varias razones → loop de marcas + RM de razones; razón por razón con varias marcas → loop de razones + RM de marcas.

**Ranking por posiciones** (primera/segunda/tercera mención): loop de posiciones + `Rp categorical [1..1]` por posición (+ `_Osm_DisplayMode = 3` si es secuencial). Si el cuestionario prohíbe repetir alternativas entre posiciones, la RU individual no basta: registra la validación transversal en `Reporte_MDD.md` (Dependencias para lógica).

**Conocimiento y detalle en la misma fila.** Si el detalle se presenta en la misma grilla que el conocimiento, modela un loop con dos fields (ej. P7 y P8) y registra en `Reporte_MDD.md` (Dependencias para lógica) que el segundo depende del primero. Si se presentan en nodos separados, cada nodo conserva su propio loop con el universo equivalente y `objectName` comunes.

### Identificación obligatoria de preguntas “por marca”, “por producto” o “por elemento”

Cuando el cuestionario indique:

- RU por marca;
- una respuesta por marca;
- evaluar cada marca;
- mostrar una marca a la vez;
- repetir la escala para cada marca;
- rotar marcas;

las marcas no deben modelarse como categorías de una pregunta múltiple.

La estructura obligatoria es:

- loop = marcas o entidades evaluadas;
- Rp = respuesta capturada para cada marca;
- cardinalidad = aplicada al Rp;
- `rot fields` = cuando se ordena rotar marcas;
- `_Osm_DisplayMode = 3` = cuando se indica mostrar o evaluar una marca
  a la vez y el patrón está corroborado;
- `expand grid` = al cierre del loop.

### Rotación de módulos

Cuando el cuestionario indique “ROTAR MÓDULOS”, “ROTAR SECCIONES”,
“ROTAR BLOQUES”, "ROTAR/ALEATORIZAR PUBLICIDADES", "ROTAR CONCEPTOS", "ROTAR COMERCIALES" o una instrucción equivalente (incidencia: la publicidad que debía rotar quedó como un `info` con la indicación):

1. Identificar los límites completos de cada módulo.
2. Verificar si los módulos contienen preguntas heterogéneas.
3. Si cada módulo contiene diferentes cantidades o tipos de preguntas,
   crear:
   - un `block fields` exterior que agrupe el universo rotado;
   - un `block fields` interior por cada módulo.
4. Aplicar al bloque exterior la propiedad de orden rotatorio corroborada por la plataforma, por ejemplo: `_Osm_QuestionOrder = "I"`.
5. Mantener dentro de cada bloque interno todas sus preguntas, instrucciones, recursos y dependencias.
6. No convertir módulos heterogéneos en un loop.
7. No dejar los módulos como preguntas independientes fuera del bloque.
8. Los saltos “ir al siguiente módulo” deben interpretarse respecto del orden rotado, no necesariamente del orden documental.

REGLA DE BLOQUEO:
Si el cuestionario ordena rotar módulos y existe un patrón de bloques corroborado para la plataforma, el MDD no puede entregarse con los módulos declarados como nodos independientes fuera de un bloque rotatorio.

### Correspondencia obligatoria entre variable fuente y universo del loop

Cuando un loop se construya a partir de las respuestas de una pregunta anterior, debe realizarse una comparación código por código entre:
- las categorías declaradas en la pregunta fuente;
- las categorías que el cuestionario ordena trasladar;
- las categorías excluidas explícitamente;
- los atributos declarados dentro del loop.

El universo declarativo del loop debe contener todas las categorías de la pregunta fuente que puedan generar una iteración, aunque exista una sección posterior dedicada específicamente a alguna de ellas.
Una categoría no puede excluirse del loop por:
- tener tratamiento adicional en una sección posterior;
- pertenecer a un módulo temático específico;
- parecer conceptualmente distinta de las demás;
- tener preguntas adicionales asociadas;
- haberse omitido accidentalmente durante la construcción.

Solo pueden excluirse categorías cuando el cuestionario lo indique
explícitamente.

Ejemplo:

Pregunta fuente:
- 1 Empanada
- 2 Sándwich
- 3 Pizza
- 4 Café
- 94 Otro

Indicación: “REPETIR POR CADA CÓDIGO MARCADO, EXCEPTO EL CÓDIGO 94”.
Universo obligatorio del loop:
- código 1;
- código 2;
- código 3;
- código 4.

El código 94 debe excluirse porque existe evidencia explícita. El código 4 no puede excluirse aunque posteriormente exista una sección completa dedicada al café.
Antes de aprobar el loop, generar conceptualmente estos conjuntos:
FUENTE_APLICABLE = categorías de la pregunta fuente menos exclusiones expresas del cuestionario.
UNIVERSO_LOOP = categorías declaradas como atributos del loop.

### Baterías homogéneas con contingencias entre iteraciones

Cuando una tabla presente:

- un encabezado o wording común;
- varias filas de escenarios, precios, productos, cuotas, porcentajes
  o montos;
- el mismo tipo de respuesta para todas las filas;
- la misma cardinalidad para todas las filas;

debe construirse un único loop:

- el encabezado común forma la etiqueta del loop;
- cada escenario forma un atributo o iteración;
- el identificador del atributo se deriva de su código/value;
- la descripción específica de la fila forma la etiqueta del atributo;
- el field Rp contiene la respuesta común;
- el loop termina con expand grid.

No deben generarse preguntas independientes solamente porque cada fila tenga un ID visible como P52S, P53S, P54S, P55S o P56S.

Ejemplo correcto:

P52S_P56S "Pregunta común"
loop
{
    _1 "Escenario 1" [value = 1],
    _2 "Escenario 2" [value = 2],
    _3 "Escenario 3" [value = 3]
} fields -
(
    Rp ""
    categorical [1..1]
    {
        _1 "Sí" [value = 1],
        _2 "No" [value = 2]
    };
) expand grid;

Ejemplo prohibido:

P52S "Escenario 1"
categorical [1..1] { ... };

P53S "Escenario 2"
categorical [1..1] { ... };

La existencia de contingencias entre las filas no elimina la homogeneidad estructural del loop.
Si las instrucciones PROG determinan que una fila se muestra según la respuesta de una fila anterior:

- declarar todas las filas dentro del universo completo del loop;
- trasladar la condición a la lógica como filtro de iteraciones;
- conservar el orden documental requerido;
- no aplicar ran fields si la secuencia depende de respuestas anteriores;
- limpiar iteraciones posteriores cuando una respuesta anterior cambie
  y deje de cumplir la condición.


## 4.12 MaxDiff

Cuando el cuestionario documente MaxDiff:

- identifica el bloque completo como una sola estructura;
- conserva atributos, sets, columnas de elección y relaciones;
- reutiliza listas define/use cuando el conjunto de atributos lo permita;
- no inventes combinaciones ni sets; el diseño (versión × set × ítems) proviene de la tabla del cuestionario, no se genera;
- recurre al archvivo Ejemplos_MDD_CORREGIDO.md y busca referencias a las estructuras asociadas al MaxDiff
- modela la variable de versión como `categorical [1..1]` y cada set con el mismo patrón de respuesta;
- declara `_Osm_CustomFunction` solo si la función y su firma están respaldadas por el proyecto;
- registra en `Reporte_MDD.md` (Dependencias para lógica): asignación de ítems por set según versión, reordenamiento, variable de cuota/control de versión y la validación de que “más importante” y “menos importante” no sean la misma selección.

Si no hay sintaxis MDD corroborada para algún elemento del MaxDiff, no la inventes: regístralo en QA.

## 4.13 Cuotas y variables derivadas

- Identifica la variable fuente y la variable de cuota/derivada como entidades diferenciables.
- Conserva categorías, rangos y cruces documentados.
- **Toda tabla de cuotas genera variables** (incidencias: "no está creando las cuotas (tabla)", "CUOTA_RANGOEDAD_2 estaba como imagen"). Por cada dimensión de la tabla (edad, género, NSE, zona, región, ciudad, cliente, segmento, versión…) declara una variable `CUOTA_<DIMENSION>` `categorical [1..1]`, con una categoría por fila/tramo de la tabla, en el orden de la tabla, con su etiqueta literal (`"18 A 24"`). Si la tabla nombra la variable (`CUOTA_RANGOEDAD_2`), usa ese nombre normalizado.
- Las cuotas cruzadas (p. ej. NSE × ZONA) se representan con una `CUOTA_` por dimensión; si la tabla define celdas cruzadas con nombre propio, declara además `CUOTA_<D1>_<D2>` con una categoría por celda y registra la decisión en QA.
- Las variables `CUOTA_*` no llevan `_Osm_HiddenComment` ni wording inventado: la etiqueta es el nombre de la dimensión tal como aparece en la tabla (`"CUOTA RANGO DE EDAD"`).
- Ubicación: bloque técnico final, antes de `ELIMI` (4.20).
- La asignación de valores a las cuotas es lógica (prompt 02): regístrala en `Reporte_MDD.md` (Dependencias para lógica) con su fuente (`CUOTA_EDAD ← F2 (edad exacta) por tramos`).
- Si la tabla está en una imagen legible, se construye igual. Si no es legible, registra `BLOQUEO_DE_COBERTURA` indicando la sección/página de la imagen.
- Una variable derivada (recode, agrupación, cliente/no cliente, grupos de edad, versión) se declara con **dominio explícito e identidad propia**; nunca sobrescribe la fuente.
- Si la asignación es dinámica, declara las variables necesarias en MDD y registra la dependencia en `Reporte_MDD.md` (Dependencias para lógica).
- Si una definición derivada es ambigua (ej. “NO CLIENTE” con “y/o”), no la resuelvas: regístrala en QA.
- Si una variable derivada puede llevar varios grupos simultáneos, su cardinalidad debe admitir selección múltiple; si es RU, asignaciones sucesivas se sobrescriben. Registra la alerta en QA cuando la regla sea ambigua.
- No omitas variables de cuota insertadas como imagen.

## 4.14 Fechas y horas

- Usa `date` cuando el cuestionario capture fecha, hora o fecha-hora ("FECHA", "DD/MM/AAAA", "fecha de nacimiento", "hora de inicio", "¿cuándo…? (fecha)"); no la conviertas en `text` ni en tres preguntas día/mes/año por ausencia de un ejemplo idéntico.
- Rango propio de la fecha → MDD (`date ["2025-01-01" .. "2026-12-31"]`) solo si el cuestionario lo indica; si no, `date;` sin rango.
- Coherencia entre fecha y otra variable (ej. edad) → lógica futura; puede asociarse `_Osm_CustomFunction` si el proyecto la requiere.

```mdd
FN "¿Cuál es su fecha de nacimiento?"
date;

HORA_INICIO "Hora de inicio de la entrevista"
date;
```

## 4.15 Fotografías y attachments

En iField, una pregunta de fotografía es una **categórica `[1..1]`** con la opción documentada en el cuestionario ("Tomar foto", "Foto adjuntada", "Continuar"); el adjunto lo configura el scripter en iField/Survey Builder.

```mdd
FOTO1 "TOMAR FOTO DEL PRODUCTO"
categorical [1..1]
{
    _1 "Foto adjuntada" [value = 1]
};
```

- No inventes validación MDD ni JavaScript para comprobar el archivo adjunto (incidencia: "creó una forma de validar la respuesta en la pregunta de foto").
- No agregues `_Osm_IsAllowAttachments`, `_Osm_MinAttachmentsRequired` ni `_Osm_AttachmentNamingPattern` salvo que el proyecto lo pida; regístralo en `Reporte_MDD.md` (Dependencias para lógica) como "configurar adjunto en iField".

## 4.16 Intros e información

- Genera `info;` para intros/textos funcionales que deban mostrarse (títulos, introducciones, consentimientos, lecturas obligatorias y cierres visibles que no capturan respuesta).
- Conserva la posición documental; no desplaces los `info` al final (incidencia: el `info` de inicio quedó al final del MDD).
- No omitas una `INTRO` solo por no capturar respuesta si es parte funcional del flujo (incidencia: "no generó la variable de INTRO").
- Nombre: ID visible o `INTRO`, `INTRO_2`… (4.1). Nunca `INICIO`, `INFO_INICIO` ni `INFO_INTRO_1`.
- Los `info` llevan `[ _Osm_IsRequired = false ]`.

```mdd
INTRO "Buenos días/tardes, mi nombre es ... y trabajo para Ipsos. Estamos realizando un estudio sobre ..."
    [
        _Osm_IsRequired = false
    ]
info;
```

(En la salida real la etiqueta es el texto completo del cuestionario, sin `...`.)

### 4.16.1 Piping e inserts en el MDD

Cuando el cuestionario indique insertar, arrastrar, mostrar o repetir el texto de una respuesta previa ("INSERTAR RESPUESTA DE P5", "<PIPE-IN P5>", "[MARCA MENCIONADA EN P3]", "PIPE-IN CODES SELECTED IN S.85b", "la marca que mencionó"), el piping se declara en la etiqueta (incidencia: "no incorpora el piping para arrastrar el texto de respuesta"):

| Necesidad | Sintaxis en la etiqueta |
|---|---|
| Texto de la respuesta de una categórica previa | `{#P5#}` |
| Texto escrito en "Otro, especificar" | `{#P5._94._C_94#}` |
| Atributo/iteración actual dentro de un loop | `{@}` |
| Respuesta de otro field de la misma iteración | `{#../CAMPO#}` |
| Valor calculado o compuesto por lógica (varias fuentes, texto armado) | `{#nombreInsert#}` y registrar en `Reporte_MDD.md` (Dependencias para lógica) la dependencia `ANSWER_PIPING` para que el prompt 02 haga `OSM.Survey.setInsert('nombreInsert', ...)` |

```mdd
P6 "¿Por qué razones prefiere <font color='yellow'>{#P5#}</font> en vez de otras marcas?"
text [0..4000];
```

- La variable fuente debe existir en el MDD y estar antes en el flujo. Si no es inequívoca, no la adivines: regístrala en QA.
- Cuando el pipe trae la respuesta de "Otro", el loop/categoría que lo muestra usa `{#VAR._94._C_94#}` como etiqueta (Casos 7 y 8).

### 4.16.2 Opciones e instrucciones con imágenes

Cuando una pregunta tenga opciones que son imágenes (logos, empaques, conceptos, fotos de producto), genera una categoría por opción, con su código y un recurso editable (incidencia: "generar un ejemplo de cada opción indicando el código o estructura para luego editarse"):

```mdd
P8 "¿Cuál de estos empaques le gusta más?"
categorical [1..1]
{
    _1 "{#resource:'P8_1.jpg'#}<br/>Empaque 1" [value = 1],
    _2 "{#resource:'P8_2.jpg'#}<br/>Empaque 2" [value = 2],
    _3 "{#resource:'P8_3.jpg'#}<br/>Empaque 3" [value = 3]
};
```

- **Disparador:** "MOSTRAR IMÁGENES", "SHOW PRODUCT IMAGES", "MOSTRAR TARJETA CON IMÁGENES" o una tabla de opciones con fotos/logos. Aplica aunque el Word no incluya las imágenes o tu lectura sea `SOLO_TEXTO`: el recurso queda editable y se lista en el reporte. No basta con dejar la indicación en `_Osm_HiddenComment`.
- Una tarjeta física que el encuestador muestra para toda la pregunta ("PEDIR QUE VEA LA IMAGEN DE LA TARJETA A1") no crea recursos por opción: se conserva como instrucción (C04).
- Nombre del recurso: `<VARIABLE>_<CODIGO>.jpg`, salvo que el cuestionario indique el nombre del archivo.
- Texto después de `<br/>`: el texto visible bajo la imagen; si no hay, `Imagen <código>` y regístralo en QA.
- Una imagen que acompaña al enunciado (concepto, TELEPIC, tarjeta) va en `_Osm_HiddenComment = "{#resource:'NOMBRE'#}"` o en la etiqueta del `info` (Caso 21).
- Lista en `Reporte_MDD.md` todos los recursos que el scripter debe cargar.

## 4.17 Prueba de producto (estudios tipo INN)

Cuando el cuestionario indique productos, órdenes, celdas o secuencias de evaluación, conserva explícitamente las dimensiones de diseño. Revisa:

1. universo de productos;
2. número de productos evaluados por entrevistado;
3. orden o rotación de presentación;
4. celda experimental o grupo de asignación;
5. variables de producto por posición (`prod_1`, `prod_2`, … `prod_n`);
6. relación entre producto asignado, posición y preguntas evaluativas;
7. carry-forward del producto actual hacia el wording (`{@}` o insert inequívoco);
8. filtros de iteraciones para mostrar solo los productos asignados;
9. reglas de no repetición;
10. persistencia del orden para el análisis posterior.

Modelo conceptual: `CELDA` (diseño asignado), `ROTACION` (orden de exposición), `prod_n` (producto en la posición n) y un loop de producto que ejecuta las preguntas evaluativas.

- No crees `prod_n`, `CELDA` o `ROTACION` sin evidencia de diseño de productos.
- No deduzcas una rotación solo porque existan varios productos.
- Si celda y orden vienen precargados, manténlos como variables técnicas o derivadas según la arquitectura del estudio.
- Si las preguntas posteriores solo aplican a productos asignados, el filtrado es de iteraciones (lógica), no solo ocultar la pregunta.

## 4.18 Variables técnicas y de sistema


**Para iField:**

- usa siempre `Metadata(<IDIOMA_METADATA>, Question, Label, SystemVariables = false)` (incidencia: al compilar sin `SystemVariables = false` se agregan variables de sistema de Dimensions que iField no usa y el conversor las arrastra).

**Incluye una variable técnica solo si:** (1) aparece en el cuestionario/estructura requerida; (2) es necesaria para una regla explícita; o (3) pertenece a la lista blanca de 4.1. Todo lo de la lista negra de 4.1 está prohibido.

**Siempre crea `ELIMI` y `GRACIAS_ELIMI`**, ubicadas en el bloque técnico final (4.20), con estas definiciones autorizadas:

```mdd
ELIMI "ESTA ENCUESTA SERÁ ELIMINADA POR NO CUMPLIR CON FILTRO DE LA ENCUESTA"
text [0..200];

GRACIAS_ELIMI "Gracias por participar"
info;
```

No generalices al resto de variables Shell. Las variables de infraestructura (identificadores de caso, estado, grabación, flags de calidad, GPS, timestamps) no se confunden con preguntas sustantivas.

## 4.19 Separación MDD vs. lógica

**Principio maestro:** el MDD declara el contrato estable del dato; la lógica implementa lo que depende del estado de la entrevista. Declara primero, programa después.

**Cuatro capas:** cuestionario (qué debe ocurrir) → MDD (qué datos existen y cómo se estructuran) → lógica OSM (dependencias y comportamiento dinámico) → Shell/infraestructura (identificación, grabación, estado).

**No conviertas en MDD dinámico por imitación:**

- show/hide dependiente de otra respuesta;
- filtros de categorías por contexto;
- filtros de iteraciones (carry-forward);
- recodes derivados y asignación de cuotas;
- routing y terminación;
- cálculos y validaciones cruzadas;
- piping dinámico que requiere `setInsert`;
- inicio/detención de audio (BACKCHECK).

**Clasificación de cada dependencia** para la sección "Dependencias para lógica" de `Reporte_MDD.md` (determina qué objeto y evento usará la lógica):

| Nivel de la dependencia | Ejemplo de señal |
|---|---|
| Pregunta completa (mostrar/ocultar) | “solo si P31 = 1” |
| Categorías (filtro de respuestas) | “mostrar solo ciertas alternativas” |
| Iteraciones (filtro de filas) | “mostrar solo las mencionadas / seleccionadas” |
| Texto dinámico / piping | “insertar respuesta de X”, `{#VAR#}`, `{@}` |
| Recode / variable derivada | “crear variable”, cuota agrupada |
| Validación cruzada | “debe sumar 100”, “no repetir marca” |
| Routing / terminación | “terminar si…”, “saltar a…” |
| Operación de campo | BACKCHECK, GRABAR, PROFUNDIZAR |

Cada dependencia debe anotar, cuando el cuestionario lo permita: fuente → destino, nivel y qué debe ocurrir ante retroceso o cambio de la respuesta fuente (reset antes de refiltrar), y que en terminaciones se conserve respuesta, flags y motivo antes de navegar.

## 4.20 Encabezado y formato del MDD

- **iField:** `Metadata(<IDIOMA_METADATA>, Question, Label, SystemVariables = false)`.
- **Dimensions Online:** encabezado autorizado por la plantilla, sin `SystemVariables = false` cuando no corresponda.
- Una declaración lógica por línea; sangría consistente de 4 espacios; sin tabulaciones.
- Sin Markdown envolvente ni comentarios editoriales dentro del MDD.
- No escapes `_`.
- Llaves, paréntesis, comillas y puntos y coma balanceados; sin coma tras la última categoría.
- Comillas: la etiqueta va entre `"…"`; una comilla doble interna se escribe `""`; los atributos HTML usan `'…'` o `""…""`. Nunca `\"`.
- HTML dentro de cadenas/propiedades está permitido y se preserva cuando es funcional y compatible.
- Termina exactamente con `End Metadata`.

**Orden de los nodos (incidencias: preguntas desordenadas, `info` desplazados al final, preguntas cambiadas de lugar):**

1. `Metadata(...)`.
2. Listas `define` (todas, antes de su primer uso).
3. Todas las preguntas, `info`, loops y bloques **en el orden exacto del cuestionario**, sección por sección. Las variables derivadas visibles en el cuestionario (p. ej. rango de edad calculado) van en su posición documental.
4. Bloque técnico final: variables `CUOTA_*`, variables de diseño no ubicadas en el cuestionario, `ELIMI`, `GRACIAS_ELIMI`.
5. `End Metadata`.

Un bloque `block fields` de rotación ocupa la posición del primer módulo que contiene. Ninguna otra reubicación está permitida; si el cuestionario es ambiguo sobre el orden, conserva el orden de lectura y regístralo en QA.

## 4.21 Prohibiciones y antipatrones

Está prohibido:

- inventar variables, códigos, categorías, rangos, filtros, pipe-ins o HTML;
- copiar datos de los casos de la sección 7;
- omitir preguntas para conseguir un MDD que compile;
- usar la etiqueta completa como ID;
- crear categorías vacías de relleno;
- crear `other(...)` solo porque la opción diga “Otros”;
- dividir una grid/loop en variables independientes por numeración visual;
- convertir toda tabla Word en grid, o toda fila en pregunta independiente;
- interpretar “GRID MA” como RM por fila;
- usar `_Osm_HiddenComment` para guardar reglas de flujo;
- duplicar en lógica una regla ya expresada en el MDD (cardinalidad, rango);
- convertir lógica dinámica en propiedades MDD sin sustento;
- sobrescribir la variable fuente con su recode;
- agregar variables `SHELL_*`/System/Link ID sin justificación;
- promover a patrón un fragmento de caso cuyo ID, wording y códigos no correspondan entre sí, o con llaves/cierres incompletos (se conserva como evidencia conceptual, no como código);
- ocultar una discrepancia relevante mediante una corrección silenciosa no respaldada;
- declarar APROBADO si existe un bloqueo crítico;
- usar caracteres no ASCII, `/` o espacios en nombres técnicos;
- generar `__` en cualquier identificador;
- generar etiquetas HTML vacías;
- mostrar instrucciones PROG o BC como instrucciones al encuestador;
- mover instrucciones intercaladas al final de la etiqueta;
- reordenar categorías por código o preguntas por conveniencia;
- crear dos listas para la misma escala por diferencias de tildes o mayúsculas;
- referenciar con `use` una lista no declarada o con otro nombre;
- usar `\"` dentro de cadenas MDD;
- entregar el MDD truncado, con `...`, "etc." o comentarios del tipo "resto de categorías igual".

## 4.22 Módulo estándar NSE (`B_NSE`)

Es el bloque "Nivel Socioeconómico 2023" que usan los estudios reales del equipo (idéntico en OVN, Untables y Hyundai). Se inserta cuando aplica C22, en la posición del cuestionario donde se pide la ficha o el filtro NSE:

- Cópialo **tal cual**: mismos nombres (`B_NSE.N1`… `B_NSE.DETALLE`), códigos y textos. La lógica estándar del Prompt 02 (cálculo de `PTJE3`, `NIVEL3`, `NSEX` y filtro) depende de esos nombres.
- No crees además una variable `NSE`, `F4` u otra con las categorías de la tabla de cuotas. Si hay cuota de NSE, se crea `CUOTA_NSE` (C14) y la asigna la lógica.
- El filtro ("SOLO NSE ABC", "TERMINAR NSE D/E") no va en el MDD: regístralo en Dependencias para lógica con los niveles que terminan.
- Si el cuestionario trae su propia ficha NSE con otras preguntas o puntajes, no uses este bloque: programa la del cuestionario y regístralo en Diferencias y decisiones.

```mdd
    B_NSE "Nivel Socioeconómico 2023"
        [ _Osm_QuestionsCountTypeID = 0 ]
    block fields
    (
        info_NSE "<p><strong>(LEER)</strong> Con la finalidad de agrupar sus respuestas con las de otras personas de similares características a las de usted, nos gustaría que responda a las siguientes preguntas referentes al jefe de hogar:</p><p> </p><p><br/><font color='aquamarine'>JEFE DE HOGAR:</font> Aquella persona, hombre o mujer, de 15 a más, que aporta más económicamente en casa o toma las decisiones financieras de la familia, y vive en el hogar.<br/><br/><font color='aquamarine'> HOGAR:</font> conjunto de personas que, habitando en la misma vivienda, preparan y consumen sus alimentos en común.</p>"
            [ _Osm_QuestionLayoutID = 10, _Osm_IsRequired = false, _Osm_IsNumbered = false ]
        info;

        N1 "N1. ¿Cuál es el último año o grado de estudios y nivel que aprobó el jefe de hogar?"
            [ _Osm_HiddenComment = "<font color='aquamarine'>(E: ACLARAR “COMPLETA O INCOMPLETA”)</font>" ]
        categorical [1..1]
        {
            _0 "Sin educación/ Educación Inicial / Primaria Incompleta" [ value = 0 ],
            _1 "Primaria Completa / Secundaria Incompleta" [ value = 1 ],
            _2 "Secundaria Completa/ Superior Técnico Incompleta" [ value = 2 ],
            _3 "Superior Técnico Completa / Superior Univ. Incompleta" [ value = 3 ],
            _5 "Superior Univ. Completa" [ value = 5 ],
            _7 "Post-Grado Universitario" [ value = 7 ]
        };

        N2 "N2. ¿El jefe del hogar se encuentra afiliado a un..."
            [ _Osm_ShowQuestionTexts = false, _Osm_AllowWatermarks = true ]
        loop
        {
            _1 "Seguro de salud privado o EPS"
        } fields -
        (
            Rp "Respuestas"
            categorical [1..1]
            {
                _0 "NO",
                _7 "SI"
            };
        ) grid;

        N3 "N3. ¿Cuál de estos bienes tiene en su hogar?"
            [ _Osm_ShowQuestionTexts = false, _Osm_AllowWatermarks = true ]
        loop
        {
            _1 "Lavadora",
            _2 "Refrigeradora"
        } fields -
        (
            Rp "Respuestas"
            categorical [1..1]
            {
                _0 "NO",
                _1 "SI"
            };
        ) grid;

        N4 "N4. ¿Cuál de estos tipos de tecnología de comunicación (TIC) tiene en su hogar?"
            [ _Osm_ShowQuestionTexts = false, _Osm_AllowWatermarks = true ]
        loop
        {
            _1 "Computadora, laptop en funcionamiento",
            _2 "Internet (sin compartir por el celular)",
            _3 "Televisión por cable"
        } fields -
        (
            Rp "Respuestas"
            categorical [1..1]
            {
                _0 "NO",
                _1 "SI"
            };
        ) grid;

        N5 "N5. ¿Tiene en su hogar?"
            [ _Osm_ShowQuestionTexts = false, _Osm_AllowWatermarks = true ]
        loop
        {
            _1 "Auto y/o camioneta para uso particular",
            _2 "Servicio doméstico en el hogar pagado (MINIMO QUE VAYA AL HOGAR UNA VEZ POR SEMANA)"
        } fields -
        (
            Rp "Respuestas"
            categorical [1..1]
            {
                _0 "NO",
                _1 "SI"
            };
        ) grid;

        N6 "N6. ¿Cuál es el material predominante en los pisos de su vivienda?"
            [ _Osm_HiddenComment = "<font color='aquamarine'>(CONSIDERAR ÁREA CONSTRUIDA. RESPUESTA ÚNICA)</font>" ]
        categorical [1..1]
        {
            _0 "Tierra / Otro material (arena y tablones sin pulir)" [ value = 0 ],
            _2 "Madera (entablados)/ tapizón / Cemento sin pulir o pulido" [ value = 2 ],
            _5 "Losetas, terrazos, mayólicas, cerámicos / Láminas asfálticas o similares / vinílicos, mosaico o similares, / Laminado tipo madera" [ value = 5 ],
            _8 "Parquet o madera pulida y similares; porcelanato, alfombra, mármol" [ value = 8 ]
        };

        N7 "N7. ¿El baño o servicio higiénico que tiene en su hogar está CONECTADO a:"
        categorical [1..1]
        {
            _0 "No tiene baño/ No está conectado a una red pública" [ value = 0 ],
            _2 "Baño compartido fuera de la vivienda (Ejem: quintas, corralones, cuartos con baño compartido, etc)" [ value = 2 ],
            _5 "Baño dentro de la vivienda" [ value = 5 ]
        };

        PTJE3 "PTJE3. Nivel socioeconómico (puntaje)"
        long [0 .. 99]
        precision(10);

        NSEX "Nivel A B C D E"
        categorical [1..1]
        {
            _1 "A",
            _2 "B",
            _3 "C",
            _4 "D",
            _5 "E"
        };

        NIVEL3 "NIVEL3. Nivel socioeconómico"
        categorical [1..1]
        {
            _1 "A1" [ value = 1 ],
            _2 "A2" [ value = 2 ],
            _3 "B1" [ value = 3 ],
            _4 "B2" [ value = 4 ],
            _5 "C1" [ value = 5 ],
            _6 "C2" [ value = 6 ],
            _7 "D" [ value = 7 ],
            _8 "E" [ value = 8 ]
        };

        DETALLE "<p>{#B_NSE.NIVEL3#}</p><p>{#B_NSE.PTJE3#} puntos</p>"
            [ _Osm_QuestionLayoutID = 10, _Osm_IsRequired = false ]
        info;
    );
```

---

# 5. REVISIÓN DE DOCUMENTOS

## 5.A Antes de construir: revisión documental y visual del cuestionario

El cuestionario se revisa como contenido textual, estructural y visual. Recorre de arriba hacia abajo y de izquierda a derecha:

- párrafos;
- tablas y celdas;
- encabezados y pies;
- numeraciones automáticas;
- columnas;
- cuadros de texto, formas y SmartArt;
- imágenes y capturas;
- objetos flotantes;
- contenido oculto;
- saltos de página;
- formato relevante;
- etiquetas HTML literales;
- texto tachado, coloreado, sombreado o marcado como eliminado/deshabilitado;
- comentarios y control de cambios (identifícalos y exclúyelos de la estructura final).

**Reglas de vigencia:**

- Ignora contenido tachado cuando `IGNORAR_TEXTO_TACHADO = SI`.
- Ignora contenido en colores declarados no vigentes (`COLORES_NO_VIGENTES`, por defecto rojo).
- Si solo una parte está tachada/no vigente, ignora solo esa parte.
- Lo tachado tampoco pasa a Dependencias para lógica: un `BACKCHECK`, `TERMINAR`, filtro o automarcado tachado se lista en §7.1 "Instrucciones tachadas — NO programar" (C20).
- Si el cuestionario trae una leyenda de colores, aplícala antes que los parámetros por defecto (C21).
- No elimines otros colores o formatos si no están configurados como no vigentes.
- No omitas contenido programable por estar insertado como imagen: si una variable, cuota, escala, código o instrucción aparece visualmente y es legible, incorpórala en su posición documental.
- Si un elemento visual no puede leerse con certeza, no lo reconstruyas: regístralo como `BLOQUEO_DE_COBERTURA` en QA.

La extracción textual no reemplaza la revisión visual.

**Inventario de imágenes (obligatorio).** Recorre todas las imágenes, capturas, cuadros de texto y formas del documento y clasifícalas en `Reporte_MDD.md`: `PROGRAMABLE_INCORPORADA` (p. ej. tabla de cuotas, escala, opciones), `DECORATIVA` (logo, separador), `ESTÍMULO` (concepto, empaque, publicidad → recurso `{#resource:...#}`) o `NO_LEGIBLE` (`BLOQUEO_DE_COBERTURA`). Las tablas de cuotas y las escalas suelen venir como imagen: búscalas expresamente.

**Inventario funcional interno** (no se emite como archivo). Construye un inventario ordenado de:

- secciones e introducciones funcionales;
- preguntas y variables simples, preguntas auxiliares, variables padre y subcampos;
- categorías, códigos y etiquetas; escalas repetidas y listas comunes;
- cardinalidades (RU/RM/exact-N/mínimo/máximo), rangos y restricciones propias del campo;
- campos abiertos y `other specify`; exclusividad y fijación;
- rotación, randomización y orden;
- grids, loops, blocks y nested loops; MaxDiff;
- variables y tablas de cuota; variables derivadas o técnicas declaradas;
- fechas y horas; preguntas de fotografía/attachment;
- placeholders, pipe-ins e inserts declarados;
- instrucciones ENC/entrevistador e instrucciones PROG;
- filtros, saltos, terminaciones y dependencias para lógica; backcheck y grabación;
- HTML y propiedades `_Osm_*` existentes o justificadas;
- estructuras de prueba de producto (celda, orden/rotación, `prod_1`, `prod_2`…) cuando el estudio las documente.

Al clasificar cada elemento aplica el criterio **función → pertenencia → estructura → formato**, en ese orden, y asigna cada indicación, escala, alternativa o campo al **nodo más específico** al que pertenece.

## 5.B Después de construir

**1. Contraste directo Cuestionario ↔ MDD.** Para cada pregunta/bloque vigente verifica: existencia; ID y normalización; wording/HTML relevante; tipo; cardinalidad; categorías; códigos y `value`; other/comment; fix/exclusive; rangos; escala completa; lista reutilizable; padre/subcampos; loop/grid/block; orden; cuota; intro/info; propiedades `_Osm_*` justificadas; elementos necesarios para lógica posterior. En grids/loops compara fila por fila, subcampo por subcampo y escala por escala. Un MDD que “compila” no es correcto por ello: debe representar el cuestionario vigente.

**2. Comparación con los casos (sección 7).** Para cada caso identificado:

- identifica casos funcional y técnicamente similares y analiza el contexto en que se implementaron;
- compara variables, tipos, etiquetas, propiedades OSM, relaciones y estructuras;
- extrae solo los criterios consistentes y aplicables al estudio actual;
- adapta la estructura respetando las variables, códigos, categorías, dependencias e indicaciones del estudio;
- antes de reutilizar un caso verifica: misma función, misma granularidad, misma cardinalidad, mismo nivel de condición, misma relación entre nodos y misma convención de plataforma.

**3. Validación de HTML y propiedades OSM.**

- las etiquetas HTML están ubicadas donde corresponde según el contenido y formato del cuestionario;
- representan la intención visual o estructural indicada;
- hay correspondencia entre el formato observado y el HTML generado;
- cada propiedad `_Osm_*` está asociada al nodo correcto y justificada por el cuestionario, la plantilla o un caso corroborado.

**4. Gate de cobertura.** Clasifica las diferencias:

| Severidad | Criterio |
|---|---|
| `CRÍTICA` | Impide identificar/programar una pregunta, escala, categoría, grid, cuota, loop o variable necesaria; puede causar pérdida de datos o lógica imposible |
| `ALTA` | Cambia tipo, código, elegibilidad, cardinalidad o comportamiento estructural |
| `MEDIA` | Afecta presentación, rotación, instrucción o metadato importante |
| `BAJA` | Diferencia documental sin impacto operativo inmediato |

Estado global: `APROBADO_PARA_REVISION` si no quedan diferencias críticas detectables tras la autocorrección; `REQUIERE_CORRECCION` si existe al menos una diferencia crítica o bloqueo de cobertura.

El nombre `MDD_PARCIAL.txt` no autoriza omisiones conocidas: autocorrige todo lo sustentado por evidencia antes de entregar y reserva lo parcial para la revisión humana posterior.

**5. Loop interno de QA** (hasta cuatro pasadas, sin mostrar razonamiento):

1. Cobertura documental: preguntas, imágenes, escalas, cuotas e instrucciones.
2. Construcción: tipos, listas, loops, propiedades y sintaxis.
3. Contraste: cuestionario↔MDD, pregunta por pregunta y estructura por estructura.
4. Auditoría final: sintaxis, nomenclatura, HTML, `_Osm_*`, categorías, dependencias y gate.

**6. Validaciones finales obligatorias.** Confirma internamente:

- [ ] La respuesta empieza con la CONFIRMACIÓN DE LECTURA (clave, último caso, primera y última pregunta del cuestionario).
- [ ] 100 % del cuestionario revisado, incluido contenido visual; modalidad de lectura declarada.
- [ ] El orden de las variables en el MDD parcial es el mismo orden del cuestionario (4.20); las categorías respetan el orden visual.
- [ ] Ninguna pregunta vigente omitida sin aparecer en el reporte: el número de filas de la **Matriz de cobertura** (6.2) coincide con el número de preguntas/INFO del cuestionario.
- [ ] **Control de secuencia de IDs** (6.2, sección 3) hecho recorriendo el cuestionario: todo salto de numeración (P5 → P7) está explicado. Un salto sin explicación es una pregunta posiblemente omitida: vuelve a buscarla en el documento (cuadros de texto, tablas, imágenes, páginas finales) antes de entregar.
- [ ] Ninguna escala/opción omitida; toda pregunta categórica tiene categorías o `use`; ninguna categoría vacía espuria.
- [ ] Ningún `__` en identificadores; ningún nombre técnico con caracteres no ASCII, `/` o espacios.
- [ ] Ningún `SIN_CODIGO_###` asignado a una pregunta con número visible o automático.
- [ ] `other(...)` solo con evidencia de especificación.
- [ ] `fix/exclusive` aplicados con la tabla de 4.8 en todas las categóricas (RU, RM y `Rp`).
- [ ] Las grillas conservan padre, filas/atributos, escala e instrucciones; los loops no se fragmentan.
- [ ] Las escalas repetidas se evaluaron para `define/use` y la sintaxis de cada `use` corresponde a su nivel.
- [ ] Cuotas identificadas y representadas como `CUOTA_*` según la tabla (incluidas las que estaban en imagen).
- [ ] Intros en su posición; fechas como `date` cuando corresponde.
- [ ] Fotografías como categórica sin validación personalizada de attachment.
- [ ] Instrucciones ENC conservadas en su posición o en `_Osm_HiddenComment`; PROG y BC fuera de la pantalla y registradas en `Reporte_MDD.md` (Dependencias para lógica).
- [ ] HTML funcional preservado (negrita, subrayado, cursiva, saltos); sin etiquetas vacías; `_Osm_*` solo cuando corresponde.
- [ ] Variables de la lista negra ausentes; `ELIMI` y `GRACIAS_ELIMI` presentes.
- [ ] Nada tachado en el MDD ni como vigente en Dependencias para lógica; lo tachado está en §7.1 (C20). Leyenda de colores aplicada (C21).
- [ ] Si el cuestionario pide ficha/filtro NSE, `B_NSE` estándar insertado tal cual (C22).
- [ ] Encabezado con `SystemVariables = false` (iField); MDD sintácticamente balanceado y terminado en `End Metadata`.
- [ ] `Reporte_MDD.md` concuerda con `MDD_PARCIAL.txt` (mismos totales, mismos IDs).

**7 Gate obligatorio de correspondencia literal de etiquetas**

Antes de entregar MDD_PARCIAL.txt, comparar cada etiqueta MDD contra el
wording visible del cuestionario.

Para cada variable, loop, grid, block, field e info, validar:

- El texto sustantivo coincide literalmente con el cuestionario.
- No se utilizó una paráfrasis.
- No se utilizó un resumen semántico.
- No se utilizó un título funcional creado por el generador.
- Se conservaron marca, producto, periodo, formato, precio y contexto.
- Se conservaron las instrucciones visibles intercaladas.
- Se conservaron las referencias a tarjetas.
- Se conservaron los inserts documentados.
- No se eliminó ninguna oración del enunciado.
- No se agregó información que no aparece en el cuestionario.

**REGLA DE BLOQUEO:**

Si la etiqueta MDD no coincide con el wording del cuestionario, la
variable no puede aprobarse.

El generador debe:
1. reemplazar automáticamente la etiqueta resumida por el wording literal;
2. volver a comparar la etiqueta con el cuestionario;
3. registrar en Reporte_MDD.md cualquier fragmento cuya lectura no sea
   inequívoca.

Una etiqueta técnicamente clara pero documentalmente resumida se considera
una diferencia ALTA y debe corregirse antes de entregar el MDD.

**8. Autocontrol final de patrones prohibidos.** Antes de entregar, recorre el `MDD_PARCIAL.txt` completo buscando estos patrones. Cada aparición se corrige o se justifica en `Reporte_MDD.md`:

| Busca | Indica | Corrección |
|---|---|---|
| `__` en un identificador | error de normalización (`__1`, `_C__94`) | un solo `_` |
| `\"` | comillas inválidas en MDD | `'` o `""` |
| `""  [value` o `"" [value` en una categoría | categoría vacía | eliminar o poner etiqueta real |
| `<strong></strong>`, `<b></b>`, `<u></u>`, `<i></i>`, `<font ...></font>`, `_Osm_HiddenComment = ""` | HTML vacío | eliminar |
| un `use lstX` cuyo nombre no coincide con ningún `define` | pregunta sin categorías (compila sin error) | corregir el nombre |
| `define` sin `};`, `use lstX "",` sin nada después, `use lstX ""` + categoría sin coma, coma tras la última categoría | error de sintaxis | corregir la puntuación |
| `use lst` dentro de `fields -( ... )` sin la forma `lstX use \\.lstX sublist ""` | variante no estándar | usar la forma canónica |
| letras con tilde, ñ, ç, `/` o espacio en un nombre de variable/lista | nombre no ASCII (`/` además es error de compilación) | normalizar (4.2) |
| `SIN_CODIGO_` | posible ID no recuperado | aplicar el protocolo de 4.2 |
| `INICIO`, `INFO_LINK`, `LINK`, `ID_BASE`, `SOURCEPROJECTID`, `NWB_`, `System_`, `SHELL_` | variable no autorizada | eliminar |
| `PROG`, `SW:`, `BACKCHECK`, `(BC)`, `GRABAR` dentro de una etiqueta o `_Osm_HiddenComment` | instrucción no visible mostrada | quitar de la etiqueta y registrar en Dependencias para lógica |
| `...`, `etc.`, "resto igual", "mismas categorías" | salida truncada | completar |
| dos listas `define` con las mismas categorías | lista duplicada | unificar |
| loops/grillas: preguntas consecutivas `X_1`, `X_2`, `X_3` con la misma escala | grilla partida | un loop `X` |
| pregunta categórica sin categorías ni `use` | escala omitida | completar desde el cuestionario; si el catálogo está en otra parte del cuestionario (p. ej. la tabla de marcas), usar esa lista con `use` |
| `other(` al inicio de una línea, después de `fix`/`exclusive` o después de la última categoría | error de compilación verificado ("Error de sintaxis"): el MDD no carga en iField | `other(...)` va en la misma línea de su categoría, antes de `fix`: `_94 "Otros" [value = 94] other(_C_94 "" text [0..200]) fix` |
| la misma escala o catálogo (marcas, Sí/No, acuerdo 1–5) en 2+ preguntas y ningún `define` | listas no reutilizadas (C08) | crear `define` y `use` |
| `ELIMI` que no es `text [0..200]` o `GRACIAS_ELIMI` que no es `info` | definición no autorizada | copiar la definición de 4.18 |
| una pregunta, opción o instrucción tachada en el MDD o como vigente en Dependencias para lógica | contenido anulado programado (C20) | eliminar y listar en §7.1 |
| texto del color de programador o investigador (según la leyenda del cuestionario) dentro de una etiqueta | instrucción no visible mostrada (C21) | quitar y registrar en Dependencias para lógica |
| variable `NSE` o similar con las categorías de la tabla de cuotas cuando el cuestionario pide ficha NSE | módulo NSE inventado (C22) | insertar `B_NSE` de 4.22 |

Luego verifica una por una las reglas C01–C22 de la sección 0.

---

# 6. SALIDA

## 6.0 Protocolo de entrega completa (cuestionarios largos)

Entrega **exactamente** estos dos archivos y ningún otro, completos: `MDD_PARCIAL.txt` y `Reporte_MDD.md`. Si por longitud no caben en una sola respuesta (incidencias: "no agregó las escalas, se tuvo que ejecutar nuevamente", "omitió varias preguntas"):

1. Divide `MDD_PARCIAL.txt` en partes que terminen siempre en un nodo completo (nunca a mitad de una pregunta, loop, bloque o lista).
2. Encabeza cada parte con un comentario fuera del bloque de código: `PARTE n de N — desde <ID inicial> hasta <ID final>`. Al final de la parte indica: `Continúa con <ID siguiente>. Responde CONTINUAR.`
3. La primera parte empieza con `Metadata(...)` y las listas `define`; la última termina con el bloque técnico final y `End Metadata`.
4. Entrega `Reporte_MDD.md` después de la última parte del MDD.
5. Nunca resumas categorías ni reemplaces contenido por `...` para "ahorrar espacio": divide en más partes.
6. Al recibir CONTINUAR, retoma exactamente en el ID indicado, sin repetir ni saltar nodos.

## 6.1 `MDD_PARCIAL.txt`

Contiene únicamente MDD, desde `Metadata(...)` hasta `End Metadata`, conforme a las secciones 4.7 a 4.20.

## 6.2 `Reporte_MDD.md`

Reporte para que el scripter revise el MDD **en pocos minutos**: primero lo que necesita su atención, después el detalle. Sin razonamiento interno ni información inventada. Si una sección no tiene contenido, escribe `Sin pendientes` (no la rellenes).

```
# Reporte MDD — Autocontrol del Paso 1 (no es el QA final)

## 1. Qué revisar primero
(lista corta y priorizada; cada punto con ID y ubicación en el cuestionario. Solo pendientes reales)
0. Si la modalidad de lectura no es DOCX_COMPLETO: "No se pudieron verificar tachados ni colores: revisar a mano".
1. Elementos del cuestionario NO representados o bloqueados (y por qué).
2. Saltos de numeración sin explicar (ver sección 3).
3. Imágenes, cuadros de texto o tablas que no se pudieron leer.
4. Decisiones que el scripter debe confirmar (ambigüedades, IDs derivados, órdenes dudosos, correcciones temporales).
5. Recursos `{#resource:...#}` que hay que cargar.

## 2. Estado y cobertura
- Estado: APROBADO_PARA_REVISION | REQUIERE_CORRECCION
- Plataforma destino / parámetros aplicados: NUMERO_EN_ETIQUETA = …, IDIOMA_METADATA = …
- Modalidad de lectura del cuestionario: DOCX_COMPLETO | SOLO_TEXTO | PARCIAL
- Ejemplos consultados (código de estudio y estructura tomada):
- Preguntas/INFO en el cuestionario: N · representadas en el MDD: N · bloqueadas: N · omitidas: N
- Grillas/loops: N · listas `define`: N · cuotas: N · MaxDiff: N · fechas: N · fotos: N
- IDs derivados de numeración automática: N · SIN_CODIGO: N

## 3. Control de secuencia de IDs
(recorre los IDs del cuestionario por sección y lista cada salto de numeración o de letra: P5 → P7, A4 → A4b → A6, D2 → D4a)
| Salto | Explicación (NO EXISTE EN EL CUESTIONARIO / ESTABA TACHADO / NO SE PUDO LEER / OMITIDO) |

## 4. Matriz de cobertura
(una fila por cada pregunta, INFO/INTRO, grilla y tabla de cuotas del cuestionario, en orden documental)
| # | ID cuestionario | Elemento MDD | Tipo/estructura | Nº categorías u filas cuestionario → MDD | Lista usada | Estado (OK / DERIVADO / BLOQUEO / OMITIDO con motivo) |

## 5. Inventario de imágenes y objetos
| Ubicación | Contenido | Clasificación (PROGRAMABLE_INCORPORADA / ESTÍMULO / DECORATIVA / NO_LEGIBLE) | Representación en MDD |

## 6. Diferencias y decisiones
| Severidad | Elemento | Tipo de diferencia o decisión | Evidencia del cuestionario | Resultado MDD | Impacto | Estado |

## 7. Dependencias para lógica
(insumo opcional del Paso 2: una fila por cada instrucción PROG/BC que el MDD no implementa)
| Variable | Familia (filtro, terminación, visibilidad, piping, cuota, BACKCHECK, validación…) | Instrucción literal del cuestionario | Fuente → destino |
(solo instrucciones vigentes: nada tachado)

### 7.1 Instrucciones tachadas — NO programar
(una fila por cada instrucción o palabra de lógica tachada en el cuestionario, aunque esté junto a texto vigente; si no hay, `Sin pendientes`)
| Variable | Texto tachado (literal) | Qué NO debe programarse |

## 8. Dependencias técnicas del pipeline
(solo si aplica: compilador/conversor externo, librería faltante. No es un error de MDD)
```

Reglas del reporte:

- La sección 1 es lo único que el scripter debe leer si todo está bien: no la llenes de elementos correctos.
- La sección 3 es obligatoria y se construye **recorriendo el cuestionario**, no el MDD: así una pregunta que no se leyó aparece como salto sin explicar.
- Las secciones 2 y 4 deben cuadrar entre sí y con el `MDD_PARCIAL.txt` (mismos totales, mismos IDs).
- La sección 6 incluye, cuando existan: preguntas omitidas; duplicados; variables sin ID; escalas/opciones faltantes; grids divididos; listas no reutilizadas; cuotas faltantes; intros desplazadas; instrucciones de entrevistador perdidas; HTML perdido; uso dudoso de `other(...)`; listas unificadas por tildes/mayúsculas; ambigüedades y excepciones del cuestionario.

`Reporte_MDD.md` contiene únicamente la documentación definida aquí.

---

# 7. BASE CONCEPTUAL Y CASOS DE EJEMPLO

Esta sección es **referencia técnica**: explica por qué cada estructura es la correcta y muestra patrones corroborados. No es fuente de datos del estudio (véase 2.3). La lógica OSM (eventos, filtros, validaciones) se menciona solo para clasificar dependencias; su implementación no forma parte de este prompt.

## 7.1 Niveles de evidencia

Un patrón es reutilizable según el respaldo que tenga:

| Nivel | Evidencia | Uso permitido |
|---|---|---|
| A — extremo a extremo | Cuestionario + MDD + lógica vinculables por ID o función | Patrón fuerte y reutilizable, manteniendo sus condiciones |
| B — estructural | Cuestionario + MDD | Estándar declarativo |
| C — técnico contextual | MDD o lógica con función técnica observable, sin requisito funcional completo | Mecanismo, no regla de negocio universal |

Ante contradicción entre un referente resumido y la trazabilidad directa Cuestionario → MDD → Lógica del caso concreto, prevalece esta última. Las ausencias de correspondencia, contradicciones entre fuentes o ambigüedades se registran como excepción y reducen el nivel de evidencia; no se rellenan por intuición.

## 7.2 Estándares de interpretación

- **Función sobre apariencia.** La naturaleza de un elemento se decide por lo que hace y cómo se relaciona con otros nodos, no por su color, posición, tabla, columna o página. Una tabla puede mezclar atributos, escalas, instrucciones y códigos; un texto con aspecto de encabezado puede ser una instrucción de entrevistador.
- **Pertenencia al nodo más específico.** “ENC: LEER OPCIONES” de una pregunta no es un `info` general; “Otro, ¿cuál?” pertenece a la categoría “Otro”; una escala común de batería pertenece al field repetido; una restricción por fila pertenece a `Rp`, no al loop.
- **Fidelidad y separación wording/código/ID.** Son tres cosas distintas; no se fusionan salvo que el código sea parte visible del wording. No se corrige silenciosamente redacción, puntuación ni etiquetas.
- **Inferencia limitada.** Puede inferirse con evidencia inequívoca: que RU implica una selección; que RM implica varias; que “preguntar por cada marca” sugiere iteración; que “mostrar solo los seleccionados” exige una dependencia; que una escala común a varias filas es un patrón de matriz; `fix` por etiqueta tipo “Otros”; `fix exclusive` por etiqueta tipo “Ninguno”. **No** puede inferirse: límites no escritos, códigos faltantes, el significado de valores numéricos de `_Osm_QuestionLayoutID` o `_Osm_ContentRuleID`, ni un filtro/recode/terminación porque otro estudio lo use.

## 7.3 Reglas maestras

1. **Declarar primero, programar después:** lo que pertenece al contrato estable del dato se expresa en MDD.
2. **La lógica resuelve contexto, no reemplaza estructura.**
3. **La cardinalidad pertenece al field que captura.**
4. **Filtrar el nivel correcto:** pregunta → show/hide · categorías → filtro de respuestas · filas → filtro de iteraciones · texto → inserts/piping · derivación → variable separada · salida → routing/terminación.
5. **No confundir presentación con datos:** DropList, grid, expand grid, `_Osm_DisplayMode`, textos ocultos y watermarks no redefinen la semántica de respuesta.
6. **No convertir convenciones locales en universales:** códigos especiales, IDs de layout, reglas de contenido, BACKCHECK, colores y propiedades OSM dependen del proyecto.
7. **La evidencia manda sobre la analogía.**
8. **Preservar fuente y derivación:** variables derivadas, cuotas y clasificaciones se rastrean hasta la respuesta original.
9. **Toda excepción se documenta.**

## 7.4 Índice rápido: indicación → criterio MDD → dependencia para lógica

| Indicación o necesidad | Criterio MDD | Dependencia para lógica (`Reporte_MDD.md`) |
|---|---|---|
| RU / única | `categorical [1..1]` | solo si hay aplicabilidad, recode o terminación |
| RM | `categorical [1..]` | — |
| Máximo N | `[1..N]` (`[0..N]` solo si opcional) | no duplicar el máximo |
| Exactamente N | `[N..N]` | — |
| “Otro, especificar” | categoría + `other(...)` si la captura está indicada | — |
| “Ninguno / No precisa” | evaluar `fix exclusive` por semántica, no por código | — |
| Rotar alternativas | `rot` / `ran` al cierre de la lista | — |
| Rotar filas | `ran fields` / `rot fields` (el loop es el universo rotado) | — |
| Misma escala para muchas filas | loop + un field común | — |
| Mostrar matriz | grid / expand grid según presentación corroborada | — |
| Preguntar 1 por 1 | loop con `_Osm_DisplayMode = 3` (corroborado en casos afines) | — |
| Mostrar solo seleccionados/mencionados | loop con universo completo | filtro de iteraciones |
| Mostrar solo ciertas alternativas | universo completo de categorías | filtro de respuestas |
| “Solo si X” | pregunta con su estructura normal | show/hide o filtro del nivel correspondiente |
| Insertar respuesta previa | `{#VARIABLE#}` / `{@}` solo si la fuente es inequívoca | insert/piping |
| Recode, cuota agrupada | variable derivada con dominio explícito | asignación posterior a la fuente |
| Suma 100 / no repetir / coherencia entre respuestas | rangos y tipos locales | validación transversal |
| BACKCHECK / GRABAR | no es un tipo de dato; se conserva la indicación | operación (grabación), solo si el proyecto confirma la equivalencia |
| Mostrar tarjeta | `_Osm_HiddenComment` | ninguna (no crea filtros ni saltos) |
| Dos dimensiones repetidas | loops anidados | — |
| Mismo screen de preguntas distintas | `block` si la agrupación es explícita | — |
| Ranking por posiciones | loop de posiciones + RU | unicidad entre posiciones si aplica |
| Versión/sets MaxDiff | variable de versión + sets con igual patrón | asignación de ítems, reordenamiento, validación más/menos |

## 7.5 Casos de referencia

Los IDs, códigos y textos de estos casos pertenecen a otros estudios: sirven para elegir estructura, no para copiar datos.

Notas de lectura de los casos (V6):

- Muchos casos provienen de estudios con `NUMERO_EN_ETIQUETA = SI` y por eso la etiqueta empieza con `P18.`, `F21.`, `I2.`. Aplica siempre el parámetro del estudio actual (4.3): con `NO`, la etiqueta empieza directamente con el wording.
- Los colores de los casos (`aquamarine`, `cyan`, `hsl(...)`, `#00FFFF`) son del estudio original. Usa `COLOR_INSTRUCCION_ENC`.
- Donde un caso y la sección 0 o 4 discrepan, prevalecen la sección 0 y la 4.

### Caso 1 — Máximo tres respuestas
Indicación: `MÁX. 3 RESPUESTAS` → `categorical [1..3]`. La restricción es cardinalidad del campo; no requiere lógica. No usar `[0..3]` salvo evidencia de opcionalidad.

### Caso 2 — Mostrar tarjeta
```mdd
_Osm_HiddenComment = "<font color='cyan'>(MOSTRAR TARJETA S8)</font>"
```
Informa al entrevistador; por sí sola no crea filtros ni saltos. Las comillas internas del HTML van con comilla simple o duplicadas (`""cyan""`); `\"` no es válido en MDD.

### Caso 3 — Exactamente tres, con categorías dependientes de segmento
“Seleccione solo tres” → `categorical [3..3]`. Las categorías que solo aplican a un segmento (hogares vs. empresas) se declaran en el universo completo; el filtrado y el cambio de wording son lógica. Cardinalidad y aplicabilidad son dimensiones distintas. Del mismo modo, una pregunta RU cuyo universo se restringe por zona/segmento conserva el universo MDD completo.

### Caso 4 — Matriz RU por fila con filas aleatorias (M5)
```mdd
M5 "M5. Por lo general, ¿la minería formal beneficia o perjudica a (LEER OPCIONES)?"
loop
{
    _1 "La población de la comunidad o distrito donde se desarrolla la mina",
    _2 "La población de la región donde se desarrolla la mina",
    _3 "La población del país en general"
} ran fields -
(
    Rp ""
    categorical [1..1]
    {
        _1 "Beneficia" [value = 1],
        _2 "Perjudica" [value = 2],
        _99 "NP" [value = 99] fix exclusive
    };
) expand grid;
```
El loop contiene las entidades; `Rp` captura una respuesta por entidad; `ran fields` aleatoriza filas; “NP” es fija y exclusiva. El referente original añade `_Osm_AllowWatermarks = true` y `style(Control(Type = "DropList"))`: son presentación y solo se copian con respaldo del cuestionario o la plantilla.

### Caso 5 — Baterías sucesivas sobre el mismo universo (P1–P4)
P1 mide conocimiento; P2–P4 solo evalúan empresas con códigos 2–5 en P1. Cada pregunta conserva su propio loop de empresas y su escala (P1: conocimiento 1–5; P2–P4: escalas 1–5 más residual 99). Las filas pueden llevar `ran fields`. Dependencia para lógica: construir las empresas elegibles desde P1 y **filtrar iteraciones** de las baterías posteriores (no basta ocultar la pregunta completa). Reutilizable en embudos de marca, reputación, awareness→consideración.

### Caso 6 — Loops anidados (empresa × driver)
Dimensiones: Empresa → Driver → Calificación. Loop exterior de empresas, loop interior de drivers, `Rp` dentro del interior (escala 1–5 y residual 99; `_Osm_DisplayMode = 3` si el recorrido es secuencial por empresa). No aplanar. Reutilizable en producto × atributo, marca × dimensión, concepto × criterio.

```mdd
BRAND_CLOSENESS loop
{
    use MARCAS sublist ""
} fields -
(
    BC loop
    {
        _1 "."
    } fields -
    (
        Rp ""
        categorical [1..1]
        {
            lstCercania1a10 use \\.lstCercania1a10 sublist ""
        };
    ) expand grid;
) expand grid;
```
Usa las listas pertinentes en cualquier nivel de la estructura: iteraciones con `use LISTA sublist ""`; categorías de un field dentro de `fields` con `LISTA use \\.LISTA sublist ""` (4.10). Si una empresa evalúa solo un subconjunto de atributos, el MDD declara el universo completo y la lógica oculta iteraciones.

### Caso 7 — Loop filtrado por unión de variables previas
El universo completo del loop se declara en MDD; las iteraciones visibles se construyen luego con respuestas de varias variables fuente (marcas recordadas + adicionales + seleccionadas). Estructura MDD:

```mdd
P6_0 "P6_0"
loop
{
    use MARCAS sublist "",

    _94 "{#P3._94._C_94#}" [value = 94],
    _941 "{#P4._941._C_941#}" [value = 941],
    _95 "{#P4._95._C_95#}" [value = 95]

} fields -
(
    SL "¿Qué tan bien recuerda esta publicidad?" loop
    {
        _1 "."
    } fields -
    (
        Rp ""
        categorical [1..1]
        {
            lstRecuerdo1a10 use \\.lstRecuerdo1a10 sublist ""
        };
    ) expand grid;
) expand grid;

```
Aplica a “mostrar solo marcas mencionadas/recordadas/seleccionadas anteriormente” y a uniones de varias preguntas fuente. Declara el pipe `{#…#}` solo si la fuente es inequívoca.

### Caso 8 — RM seguida de evaluación solo de seleccionados (F21 → F22)
F21 es `categorical [1..]` de formas de consumo. F22 es un loop sobre las mismas formas con `_Osm_DisplayMode = 3` y un field RU de frecuencia que reutiliza una lista `define/use`. Aunque el descriptor diga “GRID MA”, cada fila es `[1..1]`. Dependencia para lógica: filtro de iteraciones con las respuestas de F21.

```mdd

    F21 "<strong>F21.</strong> ¿De qué manera consume la <strong>BEBIDA / LECHE DE ALMENDRA</strong>?"
        [
            _Osm_IsNumbered = false
        ]
    categorical [1..]
    {
        _1 "Sola / Directa FRÍA" [value = 1],
        _2 "Sola / Directa CALIENTE" [value = 2],
        _3 "Mezclada con café, té, cacao, etc" [value = 3],
        _4 "Con cereales, avena o granolas" [value = 4],
        _5 "En batidos / smoothies / jugos" [value = 5],
        _6 "Para repostería / postres (queques, flanes, etc.)" [value = 6],
        _7 "Para preparar platos salados" [value = 7],
        _8 "Para mis batidos de proteína" [value = 8],
        _94 "Otros ¿cuáles?" [value = 94] other(_C_94 "" [ _Osm_Placeholder = "Especifique",_Osm_Label = "Comment:"] text [0..200] ) fix
    };

    F22 "<strong>F22.</strong> <strong><font color='aquamarine'>(MOSTRAR TARJETA F22)</font></strong> ¿Con qué frecuencia suele consumir su <strong>BEBIDA / LECHE DE ALMENDRA {@}</strong> en su hogar ...?"
        [
            _Osm_IsNumbered = false,
            _Osm_DisplayMode = 3
        ]
    loop
    {
        _1 "Sola / Directa FRÍA" [value = 1],
        _2 "Sola / Directa CALIENTE" [value = 2],
        _3 "Mezclada con café, té, cacao, etc" [value = 3],
        _4 "Con cereales, avena o granolas" [value = 4],
        _5 "En batidos / smoothies / jugos" [value = 5],
        _6 "Para repostería / postres (queques, flanes, etc.)" [value = 6],
        _7 "Para preparar platos salados" [value = 7],
        _8 "Para mis batidos de proteína" [value = 8],
        _94 "{#F21._94._C_94#}" [value = 94] fix
    } fields -
    (
        Rp "<strong>F22.</strong> <strong><font color='aquamarine'>(MOSTRAR TARJETA F22)</font></strong> ¿Con qué frecuencia suele consumir su <strong>BEBIDA / LECHE DE ALMENDRA {@}</strong> en su hogar ...?"
            [
                _Osm_HiddenComment = "<span style=""color:aquamarine;""><strong>(RESPUESTA ÚNICA)</strong></span>",
                _Osm_IsNumbered = false
            ]
        categorical [1..1]
        {
            l_frecuencia_consumo use \\.l_frecuencia_consumo sublist ""
        };

    ) expand grid;

```

### Caso 9 — Conocimiento → detalle (I2 → I3)
Dos loops con el mismo universo y `objectName` comunes (I2 Sí/No; I3 empresa ejecutora); el requisito “solo código 1 en I2” afecta iteraciones, no categorías de I3. Si ambos datos se muestran en la misma fila: un loop con dos fields. Reutilizable en uso→satisfacción, selección→evaluación.

```mdd

I2 "I2. ¿Conoce o ha oído hablar acerca de ...?"
    [
        _Osm_AllowWatermarks = true,
        _Osm_IsNumbered = false,
        _Osm_ShowQuestionTexts = false
    ]
loop
{
    _1 "a. Campañas de salud para brindar atención médica y vacunación contra el covid-19" [value = 1],
    _2 "b. La implementación de plantas de oxígeno, donación de equipamiento médico, de ambulancias e insumos a diversos hospitales." [value = 2],
    _3 "c. El programa de Recursos Educativos que busca mejorar los niveles de aprendizaje de los escolares y capacitar a los profesores de las escuelas." [value = 3],
    _4 "d. El programa Aprendiendo en Comunidad que brinda vacaciones útiles a escolares, así como escuela para padres." [value = 4],
    _5 "e. El programa de becas que brinda estudios superiores a escolares que culminaron la secundaria, cubriendo los costos de alimentación, alojamiento, materiales de estudio, matrícula y pensión mensual." [value = 5],
    _19 "s. Las Campañas de Salud Comunitaria y servicios de atención especializados para grupos vulnerables" [value = 19],
    _6 "f. La entrega de tractores e implementos agrícolas para la comunidad con el objetivo de mejorar la producción agrícola" [value = 6],
    _7 "g. La construcción del Puente Kutuctay" [value = 7],
    _8 "h. La construcción y mejoramiento de canchas sintéticas en comunidades" [value = 8],
    _9 "i. La elaboración de planes de desarrollo comunal para mejorar las comunidades locales." [value = 9],
    _10 "j. El programa de capacitación y entrenamiento para operadores mineros y en especialidades técnicas o gestión empresarial." [value = 10],
    _11 "k. El programa de capacitación a los negocios en las comunidades para brindar servicios de calidad en alimentos frescos, transporte, uniformes, señalización y servicios de soldadura especializados." [value = 11],
    _12 "l. El programa Promoción de la agricultura familiar, que busca mejorar la producción agropecuaria de diferentes comunidades." [value = 12],
    _13 "m. El apoyo para mejorar la calidad de producción de carne, leche y lana de pequeños productores de las comunidades." [value = 13],
    _14 "n. El mantenimiento de caminos rurales en comunidades" [value = 14],
    _15 "o. El programa Capacitación Docente que busca contribuir a mejorar el desempeño de profesores de diversas escuelas." [value = 15],
    _16 "p. El Proyecto Viveros Forestales que tiene por objetivo generar puestos trabajo temporales a través de la actividad forestal en diferentes comunidades." [value = 16],
    _17 "q. Servicio de movilidad escolar para comunidades" [value = 17],
    _18 "r. Construcción de cocinas mejoradas en comunidades" [value = 18]
} ran fields -
(
    Rp "I2. ¿Conoce o ha oído hablar acerca de {@}?"
        [
            _Osm_IsNumbered = false
        ]
    categorical [1..1]
    {
        _1 "Sí" [value = 1],
        _2 "No" [value = 2]
    };

) expand grid;

I3 "I3. ¿Qué empresas o institución la lleva o llevó a cabo? <br />    <font color=""Cyan"">(MOSTRAR TARJETA I3)</font>"
    [
        _Osm_AllowWatermarks = true,
        _Osm_IsNumbered = false,
        _Osm_ShowChildNodeTexts = false,
        _Osm_ShowQuestionTexts = false
    ]
loop
{
    _1 "a. Campañas de salud para brindar atención médica y vacunación contra el covid-19" [value = 1],
    _2 "b. La implementación de plantas de oxígeno, donación de equipamiento médico, de ambulancias e insumos a diversos hospitales." [value = 2],
    _3 "c. El programa de Recursos Educativos que busca mejorar los niveles de aprendizaje de los escolares y capacitar a los profesores de las escuelas." [value = 3],
    _4 "d. El programa Aprendiendo en Comunidad que brinda vacaciones útiles a escolares, así como escuela para padres." [value = 4],
    _5 "e. El programa de becas que brinda estudios superiores a escolares que culminaron la secundaria, cubriendo los costos de alimentación, alojamiento, materiales de estudio, matrícula y pensión mensual." [value = 5],
    _19 "s. Las Campañas de Salud Comunitaria y servicios de atención especializados para grupos vulnerables" [value = 19],
    _6 "f. La entrega de tractores e implementos agrícolas para la comunidad con el objetivo de mejorar la producción agrícola" [value = 6],
    _7 "g. La construcción del Puente Kutuctay" [value = 7],
    _8 "h. La construcción y mejoramiento de canchas sintéticas en comunidades" [value = 8],
    _9 "i. La elaboración de planes de desarrollo comunal para mejorar las comunidades locales." [value = 9],
    _10 "j. El programa de capacitación y entrenamiento para operadores mineros y en especialidades técnicas o gestión empresarial." [value = 10],
    _11 "k. El programa de capacitación a los negocios en las comunidades para brindar servicios de calidad en alimentos frescos, transporte, uniformes, señalización y servicios de soldadura especializados." [value = 11],
    _12 "l. El programa Promoción de la agricultura familiar, que busca mejorar la producción agropecuaria de diferentes comunidades." [value = 12],
    _13 "m. El apoyo para mejorar la calidad de producción de carne, leche y lana de pequeños productores de las comunidades." [value = 13],
    _14 "n. El mantenimiento de caminos rurales en comunidades" [value = 14],
    _15 "o. El programa Capacitación Docente que busca contribuir a mejorar el desempeño de profesores de diversas escuelas." [value = 15],
    _16 "p. El Proyecto Viveros Forestales que tiene por objetivo generar ingresos económicos familiares por el pago de jornales en beneficio de actividad forestal en diferentes comunidades." [value = 16],
    _17 "q. Servicio de movilidad escolar para comunidades" [value = 17],
    _18 "r. Construcción de cocinas mejoradas en comunidades" [value = 18]
} ran fields -
(
    Rp "I3. ¿Qué empresas o institución la lleva o llevó a cabo? <br />    <font color=""Cyan"">(MOSTRAR TARJETA I3)</font>"
        [
            _Osm_IsNumbered = false
        ]
        style(
            Control(
                Type = "DropList"
            )
        )
    categorical [1..1]
    {
        _1 "1. Mina Las Bambas" [value = 1],
        _2 "2. Gobierno regional/municipal" [value = 2],
        _3 "3. Mina Constancia" [value = 3],
        _4 "4. Mina Antapaccay" [value = 4],
        _5 "5. El Gobierno Central" [value = 5],
        _94 "Otra empresa" [value = 94] fix,
        _99 "No precisa" [value = 99] fix exclusive
    };

) expand grid;


```


### Caso 10 — Ranking por menciones (P18)
Loop de posiciones (1.ª, 2.ª, 3.ª mención) + `Rp categorical [1..1]` + `_Osm_DisplayMode = 3`. “Ninguno adicional” puede habilitarse desde la segunda pantalla y “No sabe” puede generar salto desde la primera (lógica). La no repetición entre posiciones es validación transversal.

```mdd

P18 "P18. ¿A través de qué medios vio publicidad de la Franja Electoral? Seleccione del medio en el que más vio hasta en el que menos vio publicidad."
    [
        _Osm_AllowWatermarks = true,
        _Osm_HiddenComment = "<font color='aquamarine'>(RESPUESTA MÚLTIPLE) (MOSTRAR TARJETA P18)</font>",
        _Osm_DisplayMode = 3
    ]
loop
{
    _1 "1° MENCIÓN" [value = 1],
    _2 "2° MENCIÓN" [value = 2],
    _3 "3° MENCIÓN" [value = 3]
} fields -
(
    Rp "P18. ¿A través de qué medios vio publicidad de la Franja Electoral? Seleccione del medio en el que más vio hasta en el que menos vio publicidad. <font color='aquamarine'>(MOSTRAR TARJETA P18)</font>"
        [
            _Osm_HiddenComment = "<br/><font color='cyan'>{@}</font>",
            _Osm_IsNumbered = false
        ]
    categorical [1..1]
    {
        _1 "Televisión (1)" [value = 1],
        _2 "Radio (2)" [value = 2],
        _3 "Medios digitales (Facebook, Instagram, TikTok, YouTube, etc.) (3)" [value = 3],
        _94 "Otros" [value = 94] fix,
        _96 "Ninguno adicional" [value = 96] fix exclusive,
        _99 "No sabe / No precisa" [value = 99] fix exclusive
    };

) expand grid;

```


### Caso 11 — Porcentajes por marca con suma 100 (SOW)
Loop sobre marcas con `Rp long [1..100]`. El rango individual es MDD. `_Osm_CustomFunction = "ValSOW"` solo si la función está corroborada por el proyecto. La suma exacta de 100, el filtro de marcas elegibles (p. ej. códigos 4–6 de una pregunta previa), el autocompletado cuando hay una sola marca y la suma en vivo son lógica. No resolver la suma solo con el rango de cada campo.

```mdd

SOW "Piense SOLO en <u>la cantidad de operaciones o transacciones</u> que realiza con sus MEDIOS DE COBRO. Del total de operaciones que realiza ¿Qué porcentaje realiza con …? Asegúrese que el porcentaje asignado a cada medio de pago sume 100%." loop
    {
        use lstMarcas ""
    } fields -
    (
        Rp "Suma: {#msjSumaPorcentajes#}%"
            [
                _Osm_IsNumbered = false,
                _Osm_CustomFunction = "ValSOW"
            ]
        long [1 .. 100]
        precision(10);

    ) grid;

```

### Caso 12 — Variable fuente y recode (CLIENTE → cuota)
`CLIENTE` (códigos 1,3,4,5 → cliente; códigos 2 → no cliente).

```mdd

     CLIENTE "CLIENTE"
    [
        _Osm_IsRequired = false
    ]
    categorical
    {
        _1 "CLIENTE CLARO TOTAL" [value = 1],
        _2 "NO CLIENTE CLARO" [value = 2],
        _3 "CLIENTE CLARO PREPAGO" [value = 3],
        _4 "CLIENTE CLARO POSTPAGO" [value = 4],
        _5 "CLIENTE CLARO HOGAR" [value = 5]
    };

    CUOTA_CLIENTE "CUOTA CLIENTE"
    categorical [1..1]
    {
        _1 "Cliente CLARO" [value = 1],
        _2 "No Cliente CLARO" [value = 2]
    };

```

### Caso 13 — Informacion de hijo en loop (H3)


```mdd

    H3 "H3. ¿Cuántos hijos que viven con usted tienen ...?"
    [
        _Osm_AllowWatermarks = true,
        _Osm_ShowQuestionTexts = false,
        _Osm_ShowChildNodeTexts = false
    ]
    loop
    {
        _1 "Menos de 6 años" [value = 1],
        _2 "De 6 a 10 años" [value = 2],
        _3 "De 11 a 14 años" [value = 3],
        _4 "De 15 años a más" [value = 4]
    } fields -
    (
        Rp "H3. ¿Cuántos hijos que viven con usted tienen ...?"
            [
                _Osm_QuestionLayoutID = 2,
                _Osm_CustomFunction = "checkH3",
                _Osm_CommentRequirementRule = 16
            ]
        long [-2147483648 .. 2147483647]
        precision(10);

    ) expand grid;

```

### Caso 14 — Slider de cercanía de marca
Loop de marcas, `_Osm_DisplayMode = 3`, `Rp double` con códigos 1 a 10, y propiedades de plataforma (`_Osm_QuestionLayoutID`, `_Osm_Label`, `_Osm_IsGenericMultipleSelection = false`). El template y el layout dependen de la plataforma: cópialos solo si el recurso existe, la plantilla los soporta y escala y wording coinciden. La escala no se infiere de la apariencia del slider.

### Caso 15 — Abiertas por marca (BRANDREJ_2)
Loop de marcas, `_Osm_DisplayMode = 3`, `text` por marca (la longitud 4000 de este caso es específica del estudio) y `{@}` para insertar la marca actual. El universo es declarativo; el conjunto activo (marcas rechazadas o flag de consideración) es lógica.

```mdd

BRANDREJ_2 "BRANDREJ_2"
    [
        _Osm_AllowWatermarks = true,
        _Osm_IsNumbered = false,
        _Osm_DisplayMode = 3,
        _Osm_ShowChildNodeTexts = false
    ]
loop
{
    _1 "Arkadia" [value = 1],
    _2 "Los Molinos" [value = 2],
    _3 "Unicentro" [value = 3],
    _4 "Santafé" [value = 4],
    _5 "Oviedo" [value = 5],
    _6 "El Tesoro" [value = 6],
    _7 "Viva Laureles" [value = 7],
    _8 "Viva Envigado" [value = 8],
    _9 "Mayorca" [value = 9],
    _10 "Aves María" [value = 10],
    _11 "Monterrey" [value = 11],
    _12 "Puerta del Norte" [value = 12],
    _13 "San Diego" [value = 13],
    _14 "Premium Plaza" [value = 14],
    _15 "Florida Parque Comercial" [value = 15],
    _16 "Parque Fabricato" [value = 16],
    _89 "{#P01._89._89#}{#P02._89._89#}{#P04._89._89#}" [value = 89] fix
} fields -
(
    Rp "¿Por qué razón no visitaría <font color=""yellow"">{@}</font>?<br/><font color=""cyan"">ENC: ESPONTÁNEA, PROFUNDIZAR</font>"
        [
            _Osm_QuestionLayoutID = 2,
            _Osm_Type = 3
        ]
    text [0..4000];

) expand grid;

```

### Caso 16 — Atributos × marcas (P10) y barreras por marca
Loop de atributos con `ran fields`, `Rp` categórico múltiple con marcas como categorías y “Ninguno” `fix exclusive`; `_Osm_DisplayMode = 3` si se pregunta atributo por atributo. La disponibilidad de marcas es filtro de respuestas si son categorías, o de iteraciones si se modelaron como loop. Para barreras, la orientación (marca→barreras o barrera→marcas) sigue la experiencia requerida y el dato analítico esperado; “Otro, ¿cuál?” lleva `other(...)` si hay captura abierta.

```mdd

P10 "P10"
    [
        _Osm_AllowWatermarks = true,
        _Osm_IsNumbered = false,
        _Osm_DisplayMode = 3
    ]
loop
{
    _1 "Es el mejor lugar para parchar (pasar el rato)" [value = 1],
    _2 "Ofrece actividades de entretenimiento únicas" [value = 2],
    _4 "Tiene las mejores actividades para niños" [value = 4],
    _5 "Tiene las mejores actividades para adolescentes/jóvenes" [value = 5],
    _6 "Tiene las mejores actividades para Adultos" [value = 6],
    _7 "Tiene el mejor Cine" [value = 7],
    _8 "Es donde me siento más a gusto" [value = 8],
    _9 "Es el Centro Comercial con el que me identifico" [value = 9],
    _12 "Es un Centro Comercial cercano / me queda cerca" [value = 12],
    _13 "Es un lugar donde me siento seguro" [value = 13],
    _14 "Es mi primera opción cuando voy a comprar Moda (Ropa y Calzado)" [value = 14],
    _15 "Es mi primera opción cuando quiero comer en una Plazoleta de comidas" [value = 15],
    _16 "Es mi primera opción cuando quiero comer en Restaurante con atención a la mesa" [value = 16],
    _17 "Es mi primera opción para diligencias en bancos" [value = 17],
    _18 "Es mi primera opción para servicios de Salud" [value = 18],
    _19 "Ofrece diferentes opciones de pago para el parqueadero" [value = 19],
    _20 "Es el lugar que prefiere mi familia/pareja" [value = 20],
    _21 "Es el lugar donde siempre están ofreciendo cosas nuevas" [value = 21],
    _22 "Es el lugar donde encuentro los mejores precios" [value = 22],
    _23 "Tiene zonas amplias y suficientes para trabajar" [value = 23],
    _24 "Es un lugar que premia mi fidelidad con premios, puntos, etc." [value = 24],
    _25 "Ofrece los mejores servicios médicos / IPS integrados" [value = 25],
    _26 "Es la mejor opción para visitar con mascotas (Pet friendly)" [value = 26]
} ran fields -
(
    Rp "P10. Ahora le voy a mencionar algunas características que los Centros Comerciales pueden o no tener. ¿Cuáles Centros Comerciales considera que tienen las siguientes características?<br/><font color=""cyan"">RM (ENC: MOSTRAR TABLET)</font> ¿ALGUNA OTRA?<br/><font color=""yellow"">{@}</font>"
        [
            _Osm_IsNumbered = false
        ]
    categorical
    {
        _1 "Arkadia" [value = 1],
        _2 "Los Molinos" [value = 2],
        _3 "Unicentro" [value = 3],
        _4 "Santafé" [value = 4],
        _5 "Oviedo" [value = 5],
        _6 "El Tesoro" [value = 6],
        _7 "Viva Laureles" [value = 7],
        _8 "Viva Envigado" [value = 8],
        _9 "Mayorca" [value = 9],
        _10 "Aves María" [value = 10],
        _11 "Monterrey" [value = 11],
        _12 "Puerta del Norte" [value = 12],
        _13 "San Diego" [value = 13],
        _14 "Premium Plaza" [value = 14],
        _15 "Florida Parque Comercial" [value = 15],
        _16 "Parque Fabricato" [value = 16],
        _89 "{#P01._89._89#}{#P02._89._89#}{#P04._89._89#}" [value = 89] fix,
        _90 "Ninguno" [value = 90] fix exclusive
    };

) expand grid;

```

### Caso 17 — Servicios y proveedores (X1 → X2, S1 → S2)
La pregunta de proveedor es un loop cuyo universo equivale al de servicios utilizados; se filtran iteraciones. Variables derivadas (`CLIENTE TOTAL`, `PREPAGO`, `POSTPAGO`, `HOGAR`…) se declaran con dominio propio. Alerta: una definición como “NO CLIENTE” con “y/o” puede producir universos distintos; regístrala en QA sin resolverla. En grabación por iteración, el nombre del archivo debe incorporar pregunta e iteración (lógica).

```mdd

X1 "¿Cuáles de los siguientes servicios de telecomunicaciones tiene usted actualmente contratados o utiliza en su hogar?<br/><span style='color: #00FFFF'>(MOSTRAR TARJETA 14)(R. MÚLTIPLE) (SI TIENE MÁS DE UN SERVICIO, EVALUAR POR EL QUE CONSIDERE PRINCIPAL)</span>"
    [
        _Osm_ShowQuestionTexts = false,
        _Osm_AllowWatermarks = true
    ]
loop
{
    use lstServicios ""
} ran fields -
(
    Rp ""
    categorical [1..1]
    {
        _1 "Sí" [value = 1],
        _2 "No" [value = 2],
        _99 "No precisa" [value = 99] fix exclusive
    };

) expand grid;

X2 "¿Y con qué empresa tiene contratado/provee el servicio actualmente?"
    [
        _Osm_ShowQuestionTexts = false,
        _Osm_AllowWatermarks = true
    ]
loop
{
    use lstServicios ""
} ran fields -
(
    Rp ""
    categorical [1..1]
    {
        _1 "Claro" [value = 1],
        _2 "Otra empresa" [value = 2],
        _99 "No precisa" [value = 99] fix exclusive
    };

) expand grid;

```



### Caso 18 — Prueba de producto (INN)

Se crearan la variables y opciones dependiendo de la cantidad de productos a probar y la cantidad de rotaciones y celdas que se evidencien en el cuestionario

```mdd
CELDA "Celda experimental"
categorical [1..1]
{
    _1 "Celda 1" [value = 1],
    _2 "Celda 2" [value = 2]
};

ROTACION "Orden de presentación"
categorical [1..1]
{
    _1 "Orden A-B" [value = 1],
    _2 "Orden B-A" [value = 2]
};

prod_1 "Producto en primera posición"
categorical [1..1]
{
    _1 "Producto A" [value = 1],
    _2 "Producto B" [value = 2]
};
```


### Caso 19 — MaxDiff por versión y set
`VERSION` es `categorical [1..1]`; los nodos `SET1…SETn` comparten el mismo patrón de respuesta (típicamente cuatro ítems por set). Dependencias para lógica: seleccionar el diseño de la versión, reordenar y mostrar solo los ítems del set, guardar la versión en una variable de cuota/control y validar que “más importante” y “menos importante” sean distintos. El diseño proviene de la tabla autorizada; no se genera en la entrevista.

```mdd

lstMaxDiff "" define
{
    _1 "1. Que sea la opción de cobro preferida por la mayoría de negocios." [value = 1],
    _2 "2. Que me permita pagar servicios (ej. Agua, luz, teléfono)" [value = 2],
    _3 "3. Sentir que la marca me entiende/entiende las necesidades de mi negocio" [value = 3],
    _4 "4. Que sea una marca segura y confiable" [value = 4],
    _5 "5. Que cuente con respaldo financiero" [value = 5],
    _6 "6. Que cuente con tecnología de vanguardia" [value = 6],
    _7 "7. Cobre comisiones bajas" [value = 7],
    _8 "8. Deposite/abone mis ventas rápidamente" [value = 8],
    _9 "9. Que sus dispositivos sean fáciles de usar" [value = 9],
    _10 "10. Que me ofrezca medios de cobro e-commerce (Ejem. Link de pago, botón de pago, etc.)" [value = 10],
    _11 "11. Que me permita cobrar de múltiple maneras (Ejem: aceptar pago con tarjeta desde el celular, QR, Pago efectivo, etc.) a través de su aplicativo." [value = 11],
    _12 "12. Resuelva mis consultas post venta a tiempo" [value = 12],
    _13 "13. Cuente con canales de atención eficientes para resolver mis consultas" [value = 13],
    _14 "14. Me ofrezca un reporte completo de mis ventas y en tiempo real" [value = 14],
    _15 "15. Me ofrezca todos los medios de cobro que necesito (tarjeta, QR, cobro desde el celular, Apple pay, etc.)" [value = 15],
    _16 "16. Me ofrezca servicios adicionales que faciliten la gestión de mi negocio (Ejem: reportería en línea, Ari, cobro a moneda extranjera, etc.)" [value = 16],
    _17 "17. Cuente con las mejores promociones y beneficios" [value = 17],
    _18 "18. Cuente con productos de buena calidad" [value = 18],
    _19 "19. Que me permita enviar el voucher por correo / mensaje de texto" [value = 19],
    _20 "20. Que cuente con un sistema estable: que no presente fallas, no se caiga la red" [value = 20],
    _21 "21. Que tenga los equipos (POS) más modernos y en buenas condiciones" [value = 21],
    _22 "22. Que me brinde capacitación e información útil para mi negocio" [value = 22]
};


SET1 "<p style=""margin-left:0cm;text-align:justify;"">A continuación, se presentan cuatro atributos relacionados con la contratación de su proveedor de MEDIOS DE COBRO.</p><p style=""margin-left:0cm;text-align:justify;"">Por favor:</p><p style=""margin-left:0cm;text-align:justify;"">- <strong>Marque el atributo MÁS IMPORTANTE</strong> para usted.</p><p style=""margin-left:0cm;text-align:justify;"">- <strong>Marque el atributo MENOS IMPORTANTE</strong> para usted.</p><p style=""margin-left:0cm;text-align:justify;"">&nbsp;</p><p style=""margin-left:0cm;text-align:justify;"">OJO: Algunos atributos que se presentarán a continuación pueden repetirse de manera aleatoria en los grupos a evaluar</p><p style=""margin-left:0cm;text-align:justify;"">RECUERDE marcar solo<strong> UN ATRIBUTO POR COLUMNA</strong>.</p>"
    [
        _Osm_ShowQuestionTexts = false
    ]
loop
{
    _1 "MÁS IMPORTANTE" [value = 1],
    _2 "MENOS IMPORTANTE" [value = 2]
} fields -
(
    Rp ""
        [
            _Osm_IsNumbered = false,
            _Osm_CustomFunction = "validaMaxDiff"
        ]
    categorical [1..1]
    {
        lstMaxDiff use \\.lstMaxDiff sublist ""
    };

) column grid;

SET2 "<p style=""margin-left:0cm;text-align:justify;"">A continuación, se presentan cuatro atributos relacionados con la contratación de su proveedor de MEDIOS DE COBRO.</p><p style=""margin-left:0cm;text-align:justify;"">Por favor:</p><p style=""margin-left:0cm;text-align:justify;"">- <strong>Marque el atributo MÁS IMPORTANTE</strong> para usted.</p><p style=""margin-left:0cm;text-align:justify;"">- <strong>Marque el atributo MENOS IMPORTANTE</strong> para usted.</p><p style=""margin-left:0cm;text-align:justify;"">&nbsp;</p><p style=""margin-left:0cm;text-align:justify;"">OJO: Algunos atributos que se presentarán a continuación pueden repetirse de manera aleatoria en los grupos a evaluar</p><p style=""margin-left:0cm;text-align:justify;"">RECUERDE marcar solo<strong> UN ATRIBUTO POR COLUMNA</strong>.</p>"
    [
        _Osm_ShowQuestionTexts = false
    ]
loop
{
    _1 "MÁS IMPORTANTE" [value = 1],
    _2 "MENOS IMPORTANTE" [value = 2]
} fields -
(
    Rp ""
        [
            _Osm_IsNumbered = false,
            _Osm_CustomFunction = "validaMaxDiff"
        ]
    categorical [1..1]
    {
        lstMaxDiff use \\.lstMaxDiff sublist ""
    };

) column grid;

SET3 "<p style=""margin-left:0cm;text-align:justify;"">A continuación, se presentan cuatro atributos relacionados con la contratación de su proveedor de MEDIOS DE COBRO.</p><p style=""margin-left:0cm;text-align:justify;"">Por favor:</p><p style=""margin-left:0cm;text-align:justify;"">- <strong>Marque el atributo MÁS IMPORTANTE</strong> para usted.</p><p style=""margin-left:0cm;text-align:justify;"">- <strong>Marque el atributo MENOS IMPORTANTE</strong> para usted.</p><p style=""margin-left:0cm;text-align:justify;"">&nbsp;</p><p style=""margin-left:0cm;text-align:justify;"">OJO: Algunos atributos que se presentarán a continuación pueden repetirse de manera aleatoria en los grupos a evaluar</p><p style=""margin-left:0cm;text-align:justify;"">RECUERDE marcar solo<strong> UN ATRIBUTO POR COLUMNA</strong>.</p>"
    [
        _Osm_ShowQuestionTexts = false
    ]
loop
{
    _1 "MÁS IMPORTANTE" [value = 1],
    _2 "MENOS IMPORTANTE" [value = 2]
} fields -
(
    Rp ""
        [
            _Osm_IsNumbered = false,
            _Osm_CustomFunction = "validaMaxDiff"
        ]
    categorical [1..1]
    {
        lstMaxDiff use \\.lstMaxDiff sublist ""
    };

) column grid;

CUOTA_VERSION "VERSION"
    [
        _Osm_IsNumbered = false
    ]
categorical [1..1]
{
    _1 "1" [value = 1],
    _2 "2" [value = 2],
    _3 "3" [value = 3]
};

```

### Caso 20 — Manejo del Loop de Prueba de Productos

Cuando en los cuestionarios veamos un bloque de prueba de porducto debemos usar un loop  y dentro del loop agrupar las variables que se van evaluar por cada producto

```mdd

R100 "ROTACIONES: <span style=""color:hsl(180,75%,60%);"">ENCUESTADOR SELECCIONE LA CELDA</span>"
    categorical [1..1]
    {
        _1 "Rotación 1 - FWP vs ZBL" [value = 1],
        _2 "Rotación 2 - ZBL vs TXD" [value = 2]
    };

PROD_1 "Producto en primera posición"
categorical [1..1]
{
    _1 "FWP" [value = 1],
    _2 "ZBL" [value = 2],
    _3 "TXD" [value = 3]
};

PROD_2 "Producto en segunda posición"
categorical [1..1]
{
    _1 "FWP" [value = 1],
    _2 "ZBL" [value = 2],
    _3 "TXD" [value = 3]
};

EV2 "EVALUACIÓN"
    [
        _Osm_AllowWatermarks = true,
        _Osm_DisplayMode = 3
    ]
loop
{
    _1 "FWP" [value = 1],
    _2 "ZBL" [value = 2],
    _3 "TXD" [value = 3]
} fields -
(
    ORDEN "ORDEN"
    categorical [1..1]
    {
        _1 "1" [value = 1],
        _2 "2" [value = 2]
    };

    NOMBRE "NOMBRE"
    categorical [1..1]
    {
        _1 "Polar Prototipo" [value = 1],
        _2 "Prototipo 1" [value = 2],
        _3 "Producto de la competencia" [value = 3]
    };

    MARCA "MARCA"
    categorical [1..1]
    {
        _1 "Polar" [value = 1],
        _2 "Polar" [value = 2],
        _3 "Aguila" [value = 3]
    };

    PRODUCTO "PRODUCTO"
    categorical [1..1]
    {
        _1 "FWP" [value = 1],
        _2 "ZBL" [value = 2],
        _3 "TXD" [value = 3]
    };

    PRECIO "PRECIO"
    categorical [1..1]
    {
        _1 "$3.000" [value = 1],
        _2 "$3.000" [value = 2],
        _3 "$3.500" [value = 3]
    };

    ML "PRECIO"
    categorical [1..1]
    {
        _1 "310 ml" [value = 1],
        _2 "310 ml" [value = 2],
        _3 "330 ml" [value = 3]
    };

    INT3 "ENCUESTADOR PIDA AL LOGISTICO QUE LE ENTREGUE EL DUMMIE-EMPAQUE DEL PRODUCTO TXD - Aguila"
        [
            _Osm_IsRequired = false
        ]
    info;

    Texto1 "<font color=""Cyan"">ENC.LEER:</font>  Ahora le voy a mostrar el empaque de la cerveza <font color='yellow'><strong>Aguila</strong></font>, para que me responda unas preguntas, por favor tome el empaque y obsérvelo detenidamente por 30 segundos. <br/><br/><font color=""Cyan"">ENC:</font> Mostrar el empaque de la cerveza <font color='yellow'><strong>Aguila</strong></font>, con código TXD. No permita que el encuestado maltrate el empaque, después de algunos segundos pida que lo deje nuevamente en la mesa."
        [
            _Osm_IsRequired = false
        ]
    info;

    INT_2 "ENCUESTADOR PIDA AL LOGISTICO QUE LE ENTREGUE EL DUMMIE-EMPAQUE DEL PRODUCTO <font color='yellow'><strong>{#../PRODUCTO}</strong></font> - <font color='yellow'><strong>Polar</strong></font>"
        [
            _Osm_IsRequired = false
        ]
    info;

    Texto2 "<font color=""Cyan"">ENC.LEER:</font> Ahora le mostraremos un prototipo de empaque de la cerveza <font color='yellow'><strong>{#../MARCA}</strong></font> que nos servirá para conocer su opinión sobre el diseño y la información que aparece. Le pedimos que lo evalúe como si fuera un producto que está en el mercado. Por favor tome el empaque y obsérvelo detenidamente por 30 segundos.<br/><br/><font color=""Cyan"">ENC:</font> Mostrar el prototipo del empaque de la cerveza <font color='yellow'><strong>{#../MARCA}</strong></font> <font color='yellow'><strong>{#../PRODUCTO}</strong></font>. No permita que el encuestado maltrate el empaque, después de algunos segundos pida que lo deje nuevamente en la mesa."
        [
            _Osm_IsRequired = false
        ]
    info;

    INFO_INI "<font color=""Cyan"">ENC:</font> Mostrar el prototipo del empaque de la cerveza <font color='yellow'><strong>{#txtMarca#}</strong></font> <font color='yellow'><strong>{#../PRODUCTO}</strong></font>. No permita que el encuestado maltrate el empaque, después de algunos segundos pida que deje lo deje nuevamente en la mesa."
        [
            _Osm_IsRequired = false
        ]
    info;

    P56 "P56. <font color=""Cyan"">ENC: MOSTRAR TARJETA P56</font> ¿Qué tanto le gusta el DISEÑO de este empaque? De acuerdo con la escala de la tarjeta P56."
        [
            _Osm_HiddenComment = "<font color=""Cyan"">ENC. LEER OPCIONES</font>"
        ]
    categorical [1..1]
    {
        _7 "Me gusta mucho" [value = 7],
        _6 "Me gusta" [value = 6],
        _5 "Me gusta un poco" [value = 5],
        _4 "Ni me gusta, ni me disgusta" [value = 4],
        _3 "Me disgusta un poco" [value = 3],
        _2 "Me disgusta" [value = 2],
        _1 "Me disgusta mucho" [value = 1]
    };

    P57 "P57. ¿Por qué razón indica que este empaque {#../P56#}? ¿Qué más?"
        [
            _Osm_HiddenComment = "<font color=""Cyan"">ENC. PROFUNDIZAR AL MÁXIMO</font>",
            _Osm_Type = 3
        ]
    text [20..4000];

    P58 "P58. ¿Le cambiaría algo a este empaque? ¿Qué le cambiaría? ¿Algo más?"
        [
            _Osm_HiddenComment = "<font color=""Cyan"">ENC. PROFUNDIZAR AL MÁXIMO</font>",
            _Osm_Type = 3
        ]
    text [20..4000];

    P59 "P59. <font color=""Cyan"">ENC: MOSTRAR TARJETA P59</font> Después de haber visto el empaque y de acuerdo con la escala de la tarjeta P59. ¿Qué tan interesado estaría en comprar cerveza <font color='yellow'><strong>{#../MARCA}</strong></font>?"
        [
            _Osm_HiddenComment = "<font color=""Cyan"">ENC. LEER OPCIONES</font>"
        ]
    categorical [1..1]
    {
        _5 "Definitivamente la compraría" [value = 5],
        _4 "Probablemente la compraría" [value = 4],
        _3 "Podría o no comprarla" [value = 3],
        _2 "Probablemente no la compraría" [value = 2],
        _1 "Definitivamente no la compraría" [value = 1]
    };

    P60 "P60. <font color=""Cyan"">ENC: MOSTRAR TARJETA P60</font> ¿Qué tan DIFERENTE es este empaque de <font color='yellow'><strong>{#../MARCA}</strong></font> frente a las cervezas que hay en el mercado? De acuerdo con la escala de la tarjeta P60."
        [
            _Osm_HiddenComment = "<font color=""Cyan"">ENC. LEER OPCIONES</font>"
        ]
    categorical [1..1]
    {
        _5 "Muy diferente" [value = 5],
        _4 "Diferente" [value = 4],
        _3 "Algo diferente" [value = 3],
        _2 "Poco diferente" [value = 2],
        _1 "Nada diferente" [value = 1]
    };

    P61 "P61. <font color=""Cyan"">ENC: MOSTRAR TARJETA P61.</font> Pensando en lo ATRACTIVO DE ESTE EMPAQUE DE <font color='yellow'><strong>{#../MARCA}</strong></font> en comparación con los otros empaques de cerveza que hay en el mercado y de acuerdo con la escala de la tarjeta P61, usted diría que este empaque es…"
        [
            _Osm_HiddenComment = "<font color=""Cyan"">ENC. LEER OPCIONES</font>"
        ]
    categorical [1..1]
    {
        _5 "Muy atractivo" [value = 5],
        _4 "Atractivo" [value = 4],
        _3 "Algo atractivo" [value = 3],
        _2 "Poco atractivo" [value = 2],
        _1 "Nada atractivo" [value = 1]
    };

    Msj_finDummie "<font color=""Cyan"">ENC:</font> Retire el DUMMIE-EMPAQUE de la cerveza <font color='yellow'><strong>{#../MARCA}</strong></font>"
        [
            _Osm_IsRequired = false
        ]
    info;

    Msj_PSM "Pensando en el precio que podría tener esta cerveza <font color='yellow'><strong>{#../MARCA}</strong></font> que acaba de probar y si la encontrara en lugares como tiendas, licoreras y supermercados en presentación en lata de <font color='yellow'><strong>{#../ML#}</strong></font> quisiera que por favor me respondiera las siguientes preguntas:"
        [
            _Osm_IsRequired = false
        ]
    info;

    PSM1 "PSM1. ¿A qué precio comenzaría a percibir que esta cerveza <font color='yellow'><strong>{#../MARCA}</strong></font> en lata de <font color='yellow'><strong>{#../ML#}</strong></font> es tan cara, que no consideraría comprarla? Por favor, indique el precio en pesos."
        [
            _Osm_HiddenComment = "<font color='cyan'>ENC: REGISTRAR EL MONTO EXACTO DECLARADO POR EL ENTREVISTADO SIN PUNTOS NI COMAS</font>"
        ]
    long [1000 .. 25000]
    precision(10);

    PSM2 "PSM2. ¿A qué precio comenzaría a percibir que esta cerveza <font color='yellow'><strong>{#../MARCA}</strong></font> en lata de <font color='yellow'><strong>{#../ML#}</strong></font> es cara, pero igual consideraría comprarla? Por favor, indique el precio en pesos."
        [
            _Osm_HiddenComment = "<font color='cyan'>ENC: REGISTRAR EL MONTO EXACTO DECLARADO POR EL ENTREVISTADO SIN PUNTOS NI COMAS</font>",
            _Osm_CustomFunction = "valCaro"
        ]
    long [800 .. 24900]
    precision(10);

    PSM3 "PSM3. ¿A qué precio comenzaría a percibir que esta cerveza <font color='yellow'><strong>{#../MARCA}</strong></font> en lata de <font color='yellow'><strong>{#../ML#}</strong></font> es tan barata, que sería una ganga y la compraría? Por favor, indique el precio en pesos."
        [
            _Osm_HiddenComment = "<font color='cyan'>ENC: REGISTRAR EL MONTO EXACTO DECLARADO POR EL ENTREVISTADO SIN PUNTOS NI COMAS</font>",
            _Osm_CustomFunction = "valbarata"
        ]
    long [700 .. 24800]
    precision(10);

    PSM4 "PSM4. ¿A qué precio comenzaría a percibir que esta cerveza <font color='yellow'><strong>{#../MARCA}</strong></font> en lata de <font color='yellow'><strong>{#../ML#}</strong></font> es tan barata, que dudaría de la calidad de esta y no la compraría? Por favor, indique el precio en pesos."
        [
            _Osm_HiddenComment = "<font color='cyan'>ENC: REGISTRAR EL MONTO EXACTO DECLARADO POR EL ENTREVISTADO SIN PUNTOS NI COMAS</font>",
            _Osm_CustomFunction = "valTbarata"
        ]
    long [600 .. 24700]
    precision(10);

    PSM5 "PSM5. ¿Cuál diría usted que es el precio justo para esta cerveza <font color='yellow'><strong>{#../MARCA}</strong></font> en lata de <font color='yellow'><strong>{#../ML#}</strong></font>?"
        [
            _Osm_HiddenComment = "<font color='cyan'>ENC: REGISTRAR EL MONTO EXACTO DECLARADO POR EL ENTREVISTADO SIN PUNTOS NI COMAS</font>",
            _Osm_CustomFunction = "valPSM5"
        ]
    long [1000 .. 25000]
    precision(10);

    P66 "P66. Si esta lata de cerveza <font color='yellow'><strong>{#../MARCA}</strong></font> de <font color='yellow'><strong>{#../ML#}</strong></font> estuviera disponible a un precio <font color='yellow'><strong>{#../PRECIO#}</strong></font>  en el lugar donde compra cerveza usualmente ¿Qué tan interesado estaría en comprarla?"
        [
            _Osm_HiddenComment = "<font color=""Cyan"">ENC. LEER OPCIONES DE RESPUESTA</font>"
        ]
    categorical [1..1]
    {
        _5 "Definitivamente la compraría" [value = 5],
        _4 "Probablemente la compraría" [value = 4],
        _3 "Podría o no comprarla" [value = 3],
        _2 "Probablemente no la compraría" [value = 2],
        _1 "Definitivamente no la compraría" [value = 1]
    };
) expand grid;

```

### Caso 21 — Uso de bloques
Para casos donde se indica que se van rotar modulos usamos los bloques como en el siguiente ejemplo 

```mdd

    INTRO_ROTACION_C2_C5 "ROTACIÓN DE MÓDULOS C2-C5: C2 Digital Video madre; C3 Digital 2; C4 OOH; C5 Radio."
        [
            _Osm_IsRequired = false
        ]
    info;

    Msj_1 "<font color='cyan'>(LEER)</font> Ahora nos gustaría mostrarle unas imágenes de una publicidad que puede haber visto o no, revise con detenimiento todas las imágenes."
        [
            _Osm_IsRequired = false
        ]
    info;

    
    C2_C5 "Publicidad"
        [
            _Osm_IsNumbered = false,
            _Osm_QuestionOrder = "I"
        ]
    block fields
    (
        C2 "C2"
            [
                _Osm_IsNumbered = false
            ]
        block fields
        (
            C2_1 "C2.1. ¿Ha visto recientemente está publicidad en redes sociales o no? <br/><font color='cyan'>(MOSTRAR TELEPIC C2)<br/></font>"
                [
                    _Osm_HiddenComment = "{#resource:'TELEPIC_C2'#}",
                    _Osm_IsNumbered = false
                ]
            categorical [1..1]
            {
                _1 "Sí" [value = 1],
                _2 "No" [value = 2]
            };

            C2_2 "C2.2. ¿De qué marca era esta publicidad?"
                [
                    _Osm_HiddenComment = "ESPONTÁNEA",
                    _Osm_IsNumbered = false
                ]
            categorical [1..1]
            {
                _2 "Castrol" [value = 2],
                _7 "Mobil" [value = 7],
                _8 "Motul" [value = 8],
                _9 "Repsol" [value = 9],
                _10 "Shell" [value = 10],
                _13 "Vistony" [value = 13],
                _94 "Otros" [value = 94] other(_C_94 "" [_Osm_Label = "Comment:"] text [0..200] ) fix,
                _99 "No recuerdo" [value = 99] fix exclusive
            };

            C2_3 "C2.3. Dónde recuerda haber visto esta publicidad? <br/>Mencione todos los medios en donde recuerda haberlo visto."
                [
                    _Osm_IsNumbered = false
                ]
            categorical [1..]
            {
                _1 "Facebook" [value = 1],
                _2 "YouTube" [value = 2],
                _3 "Instagram" [value = 3],
                _4 "TikTok" [value = 4],
                _94 "Otro" [value = 94] other(_C_94 "" [_Osm_Label = "Comment:"] text [0..200] ) fix,
                _941 "Otro" [value = 941] other(_C_941 "" [_Osm_Label = "Comment:"] text [0..200] ) fix,
                _99 "No recuerda" [value = 99] fix exclusive
            };

            C2_4 "C2.4. ¿Cuál cree que es el mensaje principal de este comercial? ¿Algún otro mensaje que recuerde de esta publicidad? Por favor, detalle su respuesta.<br/>Mencione todas las ideas que le transmitió el comercial"
                [
                    _Osm_Type = 3,
                    _Osm_IsNumbered = false
                ]
            text [0..4000];

            C2_5 "C2.5. Pensando en una escala del 1 al 5, donde 1 es “No me gustó para nada” y 5 “Me gustó mucho” ¿Cuánto diría que le gustó esta publicidad?"
                [
                    _Osm_HiddenComment = "ENC: MOSTRAR TARJETA",
                    _Osm_IsNumbered = false
                ]
            categorical [1..1]
            {
                _5 "5. Me gustó mucho" [value = 5],
                _4 "4. Me gustó" [value = 4],
                _3 "3. No me gustó ni me disgustó" [value = 3],
                _2 "2. No me gustó" [value = 2],
                _1 "1. No me gustó para nada" [value = 1],
                _99 "No contesta" [value = 99] fix exclusive
            };

            C2_6 "C2.6. ¿Qué es lo que más le gusta o lo que no le gusta de esta publicidad? ¿algo más? - Detalle su respuesta"
                [
                    _Osm_Type = 3,
                    _Osm_IsNumbered = false
                ]
            text [0..4000];

            C2_7 "C2.7. Después de haber visto esta publicidad y de acuerdo con sus necesidades, ¿Qué tan probable es que compre ESTA MARCA en su próxima compra?"
                [
                    _Osm_HiddenComment = "ENC: MOSTRAR TARJETA",
                    _Osm_IsNumbered = false
                ]
            categorical [1..1]
            {
                _5 "5. Definitivamente sí" [value = 5],
                _4 "4. Probablemente sí" [value = 4],
                _3 "3. No estoy seguro" [value = 3],
                _2 "2. Probablemente no" [value = 2],
                _1 "1. Definitivamente no" [value = 1]
            };

            C2_8 "C2.8. De acuerdo con la siguiente escala ¿Qué OPINIÓN tiene de LA MARCA luego de haber visto esta publicidad?"
                [
                    _Osm_HiddenComment = "ENC: MOSTRAR TARJETA",
                    _Osm_IsNumbered = false
                ]
            categorical [1..1]
            {
                _5 "5.Una opinión mucho mejor" [value = 5],
                _4 "4.Una opinión un poco mejor" [value = 4],
                _3 "3.La misma opinión que antes" [value = 3],
                _2 "2.Una opinión un poco peor" [value = 2],
                _1 "1.Una opinión mucho peor" [value = 1]
            };

            C2_9 "C2.9. En una escala del 1 al 3 donde 1 es “En desacuerdo”, 2 “Algo de acuerdo” y 3 “Totalmente de acuerdo” ¿Qué tan de acuerdo esta con las siguientes frases que describen esta publicidad?"
                [
                    _Osm_HiddenComment = "ENC: LEER ESCALA",
                    _Osm_ShowQuestionTexts = false,
                    _Osm_IsNumbered = false
                ]
            loop
            {
                _1 "Es para gente como yo" [value = 1],
                _2 "Me dice algo que me interesa" [value = 2],
                _3 "Es único y diferente" [value = 3],
                _4 "Es entretenido" [value = 4],
                _5 "Tiene un mensaje creíble" [value = 5],
                _6 "Muestra lo que una marca de LUBRICANTES realmente buena debería ser" [value = 6],
                _7 "Hace que la marca se vea diferente de otras marcas" [value = 7],
                _8 "Me dice algo nuevo de la marca" [value = 8],
                _9 "Aumentó mi interés hacia la marca" [value = 9],
                _10 "Hizo que quisiera hablar sobre la publicidad con otros" [value = 10],
                _11 "Despertó mis emociones" [value = 11],
                _12 "Es confuso" [value = 12],
                _13 "Es una publicidad que hace que la marca se diferencie de otras" [value = 13],
                _14 "Me dice algo nuevo" [value = 14],
                _15 "Me da ganas de volver a ver a verlo" [value = 15],
                _16 "Tiene humor" [value = 16]
            } ran fields -
            (
                Rp ""
                    [
                        _Osm_IsNumbered = false
                    ]
                categorical [1..1]
                {
                    _1 "1_En desacuerdo" [value = 1],
                    _2 "2_Algo de acuerdo" [value = 2],
                    _3 "3_Totalmente de acuerdo" [value = 3]
                };

            ) grid;

        );

        C3 "C3"
            [
                _Osm_IsNumbered = false
            ]
        block fields
        (
            C3_1 "C3.1. ¿Ha visto recientemente está publicidad en redes sociales o no?<br/><font color='cyan'>(MOSTRAR TELEPIC C3)<br/></font>"
                [
                    _Osm_HiddenComment = "{#resource:'TELEPIC_C3'#}",
                    _Osm_IsNumbered = false
                ]
            categorical [1..1]
            {
                _1 "Sí" [value = 1],
                _2 "No" [value = 2]
            };

            C3_2 "C3.2. ¿De qué marca era esta publicidad?"
                [
                    _Osm_HiddenComment = "ESPONTÁNEA",
                    _Osm_IsNumbered = false
                ]
            categorical [1..1]
            {
                _2 "Castrol" [value = 2],
                _7 "Mobil" [value = 7],
                _8 "Motul" [value = 8],
                _9 "Repsol" [value = 9],
                _10 "Shell" [value = 10],
                _13 "Vistony" [value = 13],
                _94 "Otros" [value = 94] other(_C_94 "" [_Osm_Label = "Comment:"] text [0..200] ) fix,
                _99 "No recuerdo" [value = 99] fix exclusive
            };

            C3_3 "C3.3. Dónde recuerda haber visto esta publicidad? Mencione todos los medios en donde recuerda haberlo visto."
                [
                    _Osm_IsNumbered = false
                ]
            categorical [1..]
            {
                _1 "Facebook" [value = 1],
                _2 "YouTube" [value = 2],
                _3 "Instagram" [value = 3],
                _4 "TikTok" [value = 4],
                _94 "Otro" [value = 94] other(_C_94 "" [_Osm_Label = "Comment:"] text [0..200] ) fix,
                _941 "Otro" [value = 941] other(_C_941 "" [_Osm_Label = "Comment:"] text [0..200] ) fix,
                _99 "No recuerda" [value = 99] fix exclusive
            };

            C3_4 "C3.4. Pensando en una escala del 1 al 5, donde 1 es “No me gustó para nada” y 5 “Me gustó mucho” ¿Cuánto diría que le gustó esta publicidad?"
                [
                    _Osm_HiddenComment = "ENC: MOSTRAR TARJETA",
                    _Osm_IsNumbered = false
                ]
            categorical [1..1]
            {
                _5 "5. Me gustó mucho" [value = 5],
                _4 "4. Me gustó" [value = 4],
                _3 "3. No me gustó ni me disgustó" [value = 3],
                _2 "2. No me gustó" [value = 2],
                _1 "1. No me gustó para nada" [value = 1],
                _99 "No contesta" [value = 99] fix exclusive
            };

        );

        C4 "C4"
            [
                _Osm_IsNumbered = false
            ]
        block fields
        (
            C4_1 "C4.1. ¿Ha visto recientemente alguna de estas publicidades en algún cartel, panel o valla de la vía pública?<br/><font color='cyan'>(MOSTRAR TELEPIC C4)<br/></font>"
                [
                    _Osm_HiddenComment = "{#resource:'TELEPIC_C4'#}",
                    _Osm_IsNumbered = false
                ]
            categorical [1..1]
            {
                _1 "Sí" [value = 1],
                _2 "No" [value = 2]
            };

            C4_2 "C4.2. ¿De qué marca era esa publicidad?"
                [
                    _Osm_HiddenComment = "ESPONTANEA",
                    _Osm_IsNumbered = false
                ]
            categorical [1..1]
            {
                _2 "Castrol" [value = 2],
                _7 "Mobil" [value = 7],
                _8 "Motul" [value = 8],
                _9 "Repsol" [value = 9],
                _10 "Shell" [value = 10],
                _13 "Vistony" [value = 13],
                _94 "Otros" [value = 94] other(_C_94 "" [_Osm_Label = "Comment:"] text [0..200] ) fix,
                _99 "No recuerdo" [value = 99] fix exclusive
            };

            CP4 "CP4. Pensando en esta publicidad que Ud. vio, ¿Cuánto diría que le agradó?"
                [
                    _Osm_IsNumbered = false
                ]
            categorical [1..1]
            {
                _5 "5. Me gustó mucho" [value = 5],
                _4 "4. Me gustó" [value = 4],
                _3 "3. No me gustó ni me disgustó" [value = 3],
                _2 "2. No me gustó" [value = 2],
                _1 "1. No me gustó para nada" [value = 1]
            };

        );

        C5 "C5"
            [
                _Osm_IsNumbered = false
            ]
        block fields
        (
            C5_1 "C5.1. ¿Ha escuchado recientemente esta publicidad en radio? #audio#{#resource:'MOBIL.mp3'#}"
                [
                    _Osm_QuestionLayoutID = 10,
                    _Osm_IsNumbered = false,
                    _Osm_InstanceSubType = "A",
                    _Osm_IsMedia = true
                ]
            categorical [1..1]
            {
                _1 "Sí" [value = 1],
                _2 "No" [value = 2]
            };

            C5_2 "C5.2. ¿De qué marca era esta publicidad?"
                [
                    _Osm_HiddenComment = "ESPONTÁNEA",
                    _Osm_IsNumbered = false
                ]
            categorical [1..1]
            {
                _2 "Castrol" [value = 2],
                _7 "Mobil" [value = 7],
                _8 "Motul" [value = 8],
                _9 "Repsol" [value = 9],
                _10 "Shell" [value = 10],
                _13 "Vistony" [value = 13],
                _94 "Otros" [value = 94] other(_C_94 "" [_Osm_Label = "Comment:"] text [0..200] ) fix,
                _99 "No recuerdo" [value = 99] fix exclusive
            };

            C5_3 "C5.3. ¿En qué emisoras de radio recuerda haber escuchado la publicidad?"
                [
                    _Osm_IsNumbered = false
                ]
            categorical [1..]
            {
                _1 "Radio Mágica" [value = 1],
                _2 "América" [value = 2],
                _3 "Corazón" [value = 3],
                _4 "Disney" [value = 4],
                _5 "Doble Nueve" [value = 5],
                _6 "Exitosa" [value = 6],
                _7 "Filarmonía" [value = 7],
                _8 "Karibeña" [value = 8],
                _9 "La Inolvidable" [value = 9],
                _10 "La Kalle" [value = 10],
                _11 "La Mega" [value = 11],
                _12 "La Zona" [value = 12],
                _13 "Moda" [value = 13],
                _14 "Nacional" [value = 14],
                _15 "Nueva Q" [value = 15],
                _16 "Oasis" [value = 16],
                _17 "Onda Cero" [value = 17],
                _18 "Oxígeno" [value = 18],
                _19 "Panaméricana" [value = 19],
                _20 "PBO Radio" [value = 20],
                _21 "Planeta" [value = 21],
                _22 "Radio Felicidad" [value = 22],
                _23 "Radiomar" [value = 23],
                _24 "Ritmo Romántica" [value = 24],
                _25 "RPP" [value = 25],
                _26 "Studio 92" [value = 26],
                _27 "Union" [value = 27],
                _28 "Antena" [value = 28],
                _29 "Fiesta" [value = 29],
                _30 "FM Bravaza" [value = 30],
                _31 "Frecuencia 100" [value = 31],
                _32 "Girasol" [value = 32],
                _33 "Nova" [value = 33],
                _94 "Otra" [value = 94] other(_C_94 "" [_Osm_Label = "Comment:"] text [0..200] ) fix,
                _941 "Otra" [value = 941] other(_C_941 "" [_Osm_Label = "Comment:"] text [0..200] ) fix,
                _942 "Otra" [value = 942] other(_C_942 "" [_Osm_Label = "Comment:"] text [0..200] ) fix,
                _99 "No Recuerda" [value = 99] fix exclusive
            };

        );

    );


```
### Caso 25 — Ranking con atributos como filas
Cuando el cuestionario presenta atributos en las filas y posiciones en las columnas, cada atributo es una iteración del loop y Rp registra la posición asignada.

```mdd

ATRIBUTOS_RANKING "Ordene las características de mayor a menor" loop
{
    _1 "Atributo A" [value = 1],
    _2 "Atributo B" [value = 2],
    _3 "Atributo C" [value = 3]
} fields -
(
    Rp ""
    categorical [1..1]
    {
        _1 "1° posición" [value = 1],
        _2 "2° posición" [value = 2],
        _3 "3° posición" [value = 3],
        _99 "No precisa" [value = 99] fix exclusive
    };
) expand grid;

```
### Caso 26 — Batería homogénea de escenarios con respuesta Sí/No

Cuando un enunciado común introduce varias filas de precios, productos, montos o escenarios y todas comparten Sí/No, las filas forman el universo del loop y Sí/No es la respuesta de Rp.

```mdd

P52S_P56S "Por favor, en base a la descripción del proyecto inmobiliario, ¿Estaría dispuesto a comprar el lote previamente mencionado de 90 m2 al precio de…"
loop
{
    _1 "P52S. 72,000 soles (800 soles el m2)" [value = 1],
    _2 "P53S. 70,000 soles (778 soles el m2)" [value = 2],
    _3 "P54S. 65,000 soles (722 soles el m2)" [value = 3],
    _4 "P55S. 60,000 soles (667 soles el m2)" [value = 4],
    _5 "P56S. 55,000 soles (611 soles el m2)" [value = 5]
} fields -
(
Rp ""
categorical [1..1]
{
    _1 "Sí" [value = 1],
    _2 "No" [value = 2]
};
) expand grid;

```

### Caso 27 — Variables que se encuentran en una sola matriz
Si vemos que las variables se declaran en una misma tabla podemos darle una estructura MDD si comparten las mismas opciones y colocando el nombre de la variable dentro de la etiqueta

```mdd
    P40_P53 "¿Cuáles de las características mencionadas de la idea valora más? Por favor, ordénelas de mayor a menor atractivo para usted"
loop
{
    _1 "P40S. Tamaño del lote (entre 90 a 95 m2, con conexión a luz, agua y desagüe, con fuente propia o directamente de la EPS)" [value = 1],
    _2 "P40T. Tamaño del lote (entre 90 a 120 m2, con conexión a luz, agua y desagüe, con fuente propia o directamente de la EPS)" [value = 2],
    _3 "P41. Ubicación del proyecto" [value = 3],
    _4 "P42. Que tenga acceso a diversos servicios e infraestructura cercanas (educación, salud, supermercados, etc.)" [value = 4],
    _5 "P43. Que cuente con vías asfaltadas" [value = 5],
    _6 "P44. Pórtico de ingreso con nombre de la Habilitación Urbana (del proyecto)" [value = 6],
    _7 "P45. Que cuente con áreas verdes" [value = 7],
    _8 "P46. Que cuente con cerco perimétrico" [value = 8],
    _9 "P47. Seguridad" [value = 9],
    _10 "P48. Que sea de una empresa inmobiliaria reconocida y de confianza" [value = 10],
    _11 "P49. Tamaño total del lote (en m2)" [value = 11],
    _12 "P50. Precio del lote" [value = 12],
    _13 "P51. Opciones de financiamiento y tasa de interés" [value = 13],
    _14 "P52. Cuotas de pago mensuales" [value = 14],
    _15 "P53S. Cercanía a la playa o al mar" [value = 15],
    _16 "P53T. Cercanía a zonas turísticas" [value = 16]
} ran fields -
(
    Rp "Posición"
    categorical [1..1]
    {
        _1 "1° posición" [value = 1],
        _2 "2° posición" [value = 2],
        _3 "3° posición" [value = 3],
        _4 "4° posición" [value = 4],
        _5 "5° posición" [value = 5],
        _99 "No precisa" [value = 99] fix exclusive
    };
) expand grid;

```



### Caso 28 — Control de calidad por inconsistencia
Si se identifica alguna inconsistencia en el cuestionario, esta debe ser señalada y documentada en el reporte de QA, indicando claramente el error encontrado.
La estructura MDD debe construirse igualmente, aplicando una corrección temporal o criterio técnico provisional cuando sea necesario para completar la construcción. Esta corrección debe quedar explícitamente registrada en el reporte de QA, indicando que se trata de una solución temporal y cuál fue el criterio aplicado.
No se debe omitir la creación de ninguna estructura MDD debido a una inconsistencia detectada en el cuestionario.

### Caso 29 — Uso de la base de ejemplos MDD
Revisemos la base de ejemplos MDD para identificar otros casos de uso y compararlos con el cuestionario actual. Esto permitirá encontrar estructuras similares y utilizar esos antecedentes como referencia para facilitar y la construcción de las estructuras MDD.
Cuando exista diferencia entre la sección 7 y Ejemplos_MDD_CORREGIDO.md, prevalece la sección 7 de este documento. El archivo externo se utiliza únicamente para localizar ejemplos adicionales compatibles.

### Caso 30 — Idioma
Se mantiene el idioma en el que se encuentra el cuestionario. No se traduce el wording, las categorías ni las instrucciones. Los nombres técnicos sí se normalizan a ASCII (4.2).

### Caso 31 — Tabla de cuotas (incluida la que viene como imagen)
Cuestionario: tabla "CUOTAS" con dos dimensiones: rango de edad (18 a 24 / 25 a 44 / 45 a más) y NSE (A/B, C, D/E). La etiqueta de la tabla de edad dice `CUOTA_RANGOEDAD_2`.

```mdd
CUOTA_RANGOEDAD_2 "CUOTA RANGO DE EDAD"
categorical [1..1]
{
    _1 "18 A 24" [value = 1],
    _2 "25 A 44" [value = 2],
    _3 "45 A MÁS" [value = 3]
};

CUOTA_NSE "CUOTA NSE"
categorical [1..1]
{
    _1 "A/B" [value = 1],
    _2 "C" [value = 2],
    _3 "D/E" [value = 3]
};
```
Van en el bloque técnico final, antes de `ELIMI`. `Reporte_MDD.md` (Dependencias para lógica) registra: `CUOTA_RANGOEDAD_2 ← edad exacta (F2) por tramos; CUOTA_NSE ← NSE calculado`.

### Caso 32 — Grilla con atributos numerados (no dividir)
Cuestionario: `A4. ¿Qué tan de acuerdo está con las siguientes frases?` y una tabla con filas `A4_1 Es confiable`, `A4_2 Es moderna`, `A4_3 Es cercana` y columnas 1 a 5 (Nada de acuerdo … Totalmente de acuerdo).

Correcto (un loop):

```mdd
A4 "¿Qué tan de acuerdo está con las siguientes frases?"
loop
{
    _1 "A4_1 Es confiable" [value = 1],
    _2 "A4_2 Es moderna" [value = 2],
    _3 "A4_3 Es cercana" [value = 3]
} fields -
(
    Rp ""
    categorical [1..1]
    {
        _1 "1 Nada de acuerdo" [value = 1],
        _2 "2" [value = 2],
        _3 "3" [value = 3],
        _4 "4" [value = 4],
        _5 "5 Totalmente de acuerdo" [value = 5]
    };
) expand grid;
```

Prohibido: `A4_1 "Es confiable" categorical [1..1] {...}; A4_2 "Es moderna" categorical [1..1] {...}; A4_3 ...`.

### Caso 33 — Pregunta auxiliar sin ID asociada a una respuesta
Cuestionario: `F3. ¿Qué marcas conoce?` con opción `1. Marca A` y, debajo de esa opción, sin ID: `¿Desde cuándo la conoce?` (texto abierto).

```mdd
F3_1 "¿Desde cuándo la conoce?"
text [0..200];
```
Nombre `IDPADRE_CODIGO`. La etiqueta es el wording de la auxiliar; nunca queda vacía ni se usa el wording como nombre.

### Caso 34 — Escala Sí/No escrita con y sin tilde
Cuestionario: P3 tiene `1 Sí / 2 No`; P9 tiene `1 Si / 2 No`; P15 tiene `1 SÍ / 2 NO`.

```mdd
lstSiNo "" define
{
    _1 "Sí" [value = 1],
    _2 "No" [value = 2]
};
```
P3, P9 y P15 usan `use lstSiNo ""`. QA registra: "Unificada escala Sí/No (P9 sin tilde, P15 en mayúsculas)".

### Caso 35 — Instrucción al entrevistado dentro de la pregunta (cuestionario en portugués)
Cuestionario: `S.90b Qual dessas marcas de <u>cerveja com álcool</u> você **compra com mais frequência**?` / *Selecione apenas uma resposta* / `PROG.: SINGLE ANSWER` / `PROG: IF CODE 6 NOT SELECTED TERMINATE VALID`.

```mdd
S_90b "Qual dessas marcas de <u><strong>cerveja com álcool</strong></u> você <strong>compra com mais frequência</strong>?<br/><i>Selecione apenas uma resposta</i>"
categorical [1..1]
{
    ...categorías del cuestionario...
};
```
`PROG.: SINGLE ANSWER` define `[1..1]` y no se muestra; `TERMINATE VALID` va a `Reporte_MDD.md` (Dependencias para lógica) como `FILTER_TERMINATE`. (El `...` es ilustrativo; en la salida real está prohibido.)




## 7.6 Glosario mínimo

- **MDD:** modelo declarativo del dato y de la estructura: tipos, categorías, cardinalidades, loops, fields, listas, blocks y metadatos OSM.
- **iField/OSM:** entorno de ejecución donde el MDD se presenta y la lógica opera sobre el estado de la entrevista.
- **Loop:** repite un conjunto de fields por cada atributo/entidad del universo.
- **Field (`Rp`):** dato capturado dentro de una iteración.
- **Grid / expand grid:** presentación matricial de un loop y sus fields; no cambia la semántica.
- **`ran fields`:** aleatorización del orden de las iteraciones de un loop.
- **Block:** agrupación funcional de nodos distintos; no representa repetición.
- **Carry-forward:** uso de respuestas previas para definir contenido, alternativas o iteraciones posteriores.
- **Piping:** inserción de contenido de otra variable (`{#VARIABLE#}`) o del atributo actual (`{@}`) en el wording.
- **Recode:** variable derivada que agrupa o transforma una respuesta fuente sin reemplazarla.
- **Filtro de respuestas / de iteraciones:** restricción dinámica de categorías / de filas de un loop.
- **BACKCHECK:** marca operativa que, en casos corroborados, activa grabación de la interacción; su equivalencia debe confirmarse por proyecto.

---

**FIN DEL PROMPT 01 — EASYSCRIPT V6**

CLAVE DE LECTURA DEL PROMPT 01: MDD-V6-QUINUA-4718
