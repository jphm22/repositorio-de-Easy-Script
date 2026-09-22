# PROMPT PARA GENERAR BASE DE CONOCIMIENTO CONSOLIDADA TIPO EASY SCRIPT

## ROL

Actúa como **Especialista Senior en cuestionarios, estructuras MDD, lógica JavaScript de encuestas y consolidación documental**.

Debes analizar conjuntamente, por proyecto, los siguientes archivos:

1. `01_CUESTIONARIO_UNIDO.md`
2. `02_LOGICA_UNIDA.txt`
3. `03_MDD_UNIDO.txt`

Tu tarea es generar una base de conocimiento con una estructura, nivel de detalle y forma de presentación semejantes a `Base_conocimiento_Easy_Script_Mixta.md`.

La unidad principal de salida debe ser el **elemento del cuestionario o variable**, no la regla lógica aislada.

Para cada elemento debes presentar juntas estas tres capas:

```text
PREGUNTA DEL CUESTIONARIO
        ↓
ESTRUCTURA DE LA VARIABLE MDD
        ↓
LÓGICA JAVASCRIPT ASOCIADA
```

No generes un nuevo MDD. No corrijas los archivos originales. No inventes información, relaciones, reglas, variables, categorías ni fragmentos técnicos.

## OBJETIVO

Genera un único archivo llamado:

`BASE_CONOCIMIENTO.MD`

El resultado debe funcionar como una base consolidada de consulta técnica y debe parecerse a la referencia `Base_conocimiento_Easy_Script_Mixta.md` en estos aspectos:

- Organización por proyecto o estudio.
- Organización interna por elemento o variable.
- Presentación consecutiva de cuestionario, MDD y JavaScript.
- Conservación de fragmentos originales.
- Inclusión de elementos aunque no tengan lógica JavaScript.
- Descripción explícita de ausencias, sin inventar implementación.
- Tratamiento completo de variables simples, bloques, loops, grids, matrices, campos y validaciones.
- Lectura clara y directa, sin fichas abstractas por `LOGICA_001`, salvo que una regla no pueda asociarse a ningún elemento.

## PRINCIPIO CENTRAL DE GRANULARIDAD

La unidad documental principal es el **elemento**.

Un elemento puede ser:

- Pregunta.
- Variable.
- Variable oculta.
- Variable derivada.
- Variable auxiliar.
- Info.
- Bloque.
- Loop.
- Grid.
- Matriz.
- Campo interno.
- Variable de control.
- Variable de estado.
- Variable de cuota.

Cada elemento debe aparecer **una sola vez por proyecto** y reunir toda la evidencia asociada de las tres fuentes.

Si un elemento tiene varios eventos o funciones JavaScript, inclúyelos juntos en la sección `Lógica JavaScript`, respetando el orden original del archivo.

No dividas automáticamente cada `addEventListener`, condición `if` o función auxiliar en fichas independientes.

## PRIORIDAD DE LAS FUENTES

### `01_CUESTIONARIO_UNIDO.md`

Usa esta fuente para documentar:

- Identificador.
- Enunciado.
- Contenido complementario.
- Opciones o categorías visibles.
- Instrucciones al encuestador.
- Indicaciones de programación.
- Filtros.
- Saltos.
- Terminaciones.
- Validaciones.
- Rotaciones.
- Aleatorizaciones.
- Exclusividades.
- Dependencias.
- Matrices, escalas y loops.

### `03_MDD_UNIDO.txt`

Usa esta fuente para documentar la declaración técnica del elemento:

- Nombre exacto.
- Texto exacto.
- Tipo.
- Rango.
- Categorías.
- Valores.
- Propiedades.
- `fix`, `exclusive`, `ran`, `asc`, `desc`.
- `loop`, `fields`, `block fields`, `expand grid`.
- Validaciones.
- Subcampos.
- Propiedades `_Osm_*`.
- Referencias e inserts.

### `02_LOGICA_UNIDA.txt`

Usa esta fuente para documentar toda la lógica JavaScript directamente asociada al elemento:

- `addEventListener`.
- `onNext`.
- `onEntrance`.
- `onBeforeNavigateTo`.
- `onInputChange`.
- Funciones `check_*`.
- Funciones de validación vinculadas mediante propiedades MDD.
- Autocompletados.
- Recodificaciones.
- Filtros y terminaciones.
- Mostrar u ocultar preguntas, respuestas o iteraciones.
- Cálculos.
- Grabación.
- Navegación.
- Asignaciones.

## VALIDACIÓN PREVIA OBLIGATORIA

Antes de generar la salida:

1. Verifica que existan los tres archivos requeridos.
2. Verifica que puedan leerse completamente.
3. Identifica todos los proyectos internos.
4. Asocia las secciones de cuestionario, MDD y lógica solo mediante evidencia verificable.
5. Construye un inventario interno de elementos por proyecto.

Si falta un archivo, devuelve exclusivamente:

```text
No se puede generar BASE_CONOCIMIENTO.MD porque falta el archivo: [NOMBRE_DEL_ARCHIVO]
```

## IDENTIFICACIÓN DE PROYECTOS

Separa proyectos mediante:

1. Identificador explícito.
2. Nombre del archivo original.
3. Encabezados y separadores.
4. Metadatos.
5. Coincidencia exacta del identificador en las tres fuentes.
6. Conjuntos consistentes de variables.

No combines proyectos diferentes.

Para cada proyecto registra:

- Identificador.
- Sigla o metodología, si aparece.
- Archivo de cuestionario original, si aparece.
- Archivo MDD original, si aparece.
- Archivo de lógica original, si aparece.
- Cantidad real de elementos documentados.

## INVENTARIO MAESTRO DE ELEMENTOS

Construye primero un inventario unificado por proyecto.

Incluye en el inventario todo elemento encontrado en al menos una fuente. Usa como clave principal el nombre exacto de la variable o estructura.

Para evitar omisiones:

1. Extrae elementos del cuestionario.
2. Extrae declaraciones del MDD.
3. Extrae elementos con lógica JavaScript.
4. Une los tres inventarios por proyecto.
5. Conserva elementos presentes solo en una o dos fuentes.
6. No descartes un elemento por no tener JavaScript.

### Regla de correspondencia

La asociación entre fuentes puede considerarse directa cuando existe:

- Mismo proyecto y mismo identificador exacto.
- Referencia explícita del elemento en la lógica.
- Función `check_*` vinculada explícitamente en el MDD.
- Subcampo o iteración inequívocamente perteneciente a un loop.

No uses similitud aproximada del nombre como única evidencia.

## ESTRUCTURA OBLIGATORIA DE LA SALIDA

El archivo debe comenzar exactamente con:

```markdown
# Base de conocimiento consolidada — Lógica MDD

Este archivo consolida los estudios proporcionados. Cada elemento mantiene tres capas: **pregunta del cuestionario**, **estructura MDD** y **lógica JavaScript**. Cuando una capa no fue identificada, se declara explícitamente su ausencia en lugar de inventar contenido.
```

Luego incluye:

```markdown
## Estudios incluidos

- **[PROYECTO 1]** — [cantidad real] elementos
- **[PROYECTO 2]** — [cantidad real] elementos
```

## ESTRUCTURA POR PROYECTO

Para cada proyecto utiliza:

```markdown
## [IDENTIFICADOR DEL PROYECTO]

- Cuestionario: [nombre exacto o “No identificado”]
- MDD: [nombre exacto o “No identificado”]
- Lógica: [nombre exacto o “No identificado”]

### Elementos
```

## ESTRUCTURA OBLIGATORIA POR ELEMENTO

Para cada elemento utiliza exactamente este orden:

```markdown
### [PROYECTO] — [IDENTIFICADOR DEL ELEMENTO]

#### 1. Pregunta del cuestionario

##### Identificador

[identificador exacto]

##### Enunciado / contenido principal

[texto original o extracto completo pertinente]

##### Contenido complementario

[contenido complementario, si existe]

##### Opciones / categorías / estructura visible

- [opción o estructura]

##### Indicaciones / reglas del cuestionario

- [instrucción, filtro, salto, terminación, validación, rotación, etc.]

#### 2. Estructura de la variable MDD

```text
[declaración MDD completa y exacta]
```

#### 3. Lógica JavaScript

```javascript
[todos los fragmentos JavaScript asociados al elemento, en el orden original]
```
```

Omite solamente los subtítulos vacíos `Contenido complementario`, `Opciones` o `Indicaciones` cuando realmente no existan.

No omitas ninguna de las tres secciones numeradas.

## TEXTO OBLIGATORIO PARA AUSENCIAS

### Sin elemento en el cuestionario

```text
No se identificó una pregunta o instrucción del cuestionario directamente asociada a este elemento.
```

### Sin declaración MDD

```text
No se identificó una declaración MDD directamente asociada a este elemento.
```

### Sin lógica JavaScript

```text
No se identificó lógica JavaScript directamente asociada a este elemento mediante un addEventListener, una función check_*, una función de validación vinculada o una referencia técnica inequívoca.
```

No reemplaces estas ausencias con contenido inferido.

## REGLAS PARA ASOCIAR JAVASCRIPT A UN ELEMENTO

Incluye como lógica del elemento:

1. Todos los `OSM.Survey.[ELEMENTO].addEventListener(...)`.
2. Funciones `check_[ELEMENTO]`, `check[ELEMENTO]`, `fn_[ELEMENTO]` u otras cuando exista referencia explícita.
3. Funciones declaradas en propiedades del MDD, por ejemplo `_Osm_ValidateFunction`, `_Osm_HintFunction` o propiedades equivalentes.
4. Funciones auxiliares únicamente cuando su uso por el elemento sea explícito.
5. Eventos que afectan al elemento desde otra variable, si la referencia es directa. En ese caso conserva la lógica en el elemento propietario del evento y agrega una nota breve en el elemento afectado, sin duplicar todo el código.

### Lógica comentada

- Conserva el comentario si forma parte del fragmento asociado.
- No presentes código totalmente comentado como lógica activa.
- Añade antes del bloque: `Nota: el fragmento asociado está comentado en el archivo original.`

### Funciones globales

Las funciones globales sin elemento propio, como utilidades, generadores aleatorios o funciones comunes, deben ir al final del proyecto en:

```markdown
### Funciones globales y utilidades
```

No las conviertas en preguntas ficticias.

## REGLAS PARA CUESTIONARIO

Para cada elemento:

- Conserva el identificador exacto.
- Conserva el enunciado relevante.
- Separa contenido complementario de opciones.
- Presenta opciones como lista legible.
- Conserva códigos visibles.
- Conserva instrucciones `PROG`, `PN`, `ENC`, filtros, saltos y terminaciones.
- No combines contenido de preguntas distintas aunque aparezcan cerca.
- Si una extracción incluye accidentalmente preguntas posteriores, recorta el contenido al límite del elemento actual.

## REGLAS PARA MDD

- Incluye la declaración completa del elemento.
- Para loops o grids incluye iteradores, categorías, `fields`, subcampos y cierre de la estructura.
- Conserva exactamente `_1`, `_A1`, valores, propiedades, comillas, rangos, mayúsculas y minúsculas.
- No escapes ni alteres sintaxis salvo lo necesario para un bloque Markdown válido.
- No resumas listas de categorías con puntos suspensivos.
- No atribuyas al MDD la lógica JavaScript. El MDD describe la estructura declarativa; JavaScript describe el comportamiento ejecutable, salvo que la regla esté expresada directamente en una propiedad MDD.

## REGLAS PARA JAVASCRIPT

- Conserva el fragmento completo.
- Incluye todos los eventos asociados al elemento.
- Conserva operadores, comentarios, funciones, mensajes y orden.
- No simplifiques condiciones.
- No sustituyas `s` por `OSM.Survey` ni viceversa.
- No cambies comillas ni códigos.
- No clasifiques como variable real nombres de métodos como `discard`, `screenOut`, `setInsert`, `randomGenerator` o `stopSilentAudioRecording`.

## ELEMENTOS COMPLEJOS

### Loops, matrices y grids

En el cuestionario documenta pregunta principal, filas, columnas, escala e instrucciones.

En el MDD conserva toda la estructura `loop`, iteraciones, `fields`, subcampos y propiedades.

En JavaScript agrupa las reglas de filtrado de iteraciones, validaciones por celda, rankings, ordenamiento y visibilidad.

### Variables derivadas y recodificadas

Mantén juntas:

- Variable de salida.
- Entrada funcional del cuestionario.
- Declaración MDD.
- Fórmula o asignación JavaScript.
- Condiciones y rangos exactos.

### Elementos con varias reglas

No crees una ficha por regla. Incluye todos los eventos y funciones asociados dentro de la misma ficha del elemento.

## SECCIONES FINALES

Después de todos los proyectos, incluye:

```markdown
# Índice consolidado de elementos
```

Agrupa por proyecto y lista los identificadores documentados.

Luego incluye:

```markdown
# Patrones técnicos observados
```

Incluye únicamente patrones sustentados por dos o más elementos, por ejemplo:

- Terminación por filtro.
- Visibilidad condicionada.
- Autocompletado con variables `SHELL_*`.
- Recodificación de rangos.
- Validación mediante `check_*`.
- Filtrado de respuestas.
- Filtrado de iteraciones.
- Grabación por consentimiento.

Para cada patrón indica:

- Descripción.
- Proyectos.
- Elementos de ejemplo.
- Implementación observada.
- Variantes.
- Limitaciones.

No conviertas casos únicos en patrones generales.

## CONTROL DE CALIDAD

Antes de entregar, verifica:

- Todos los proyectos fueron separados correctamente.
- Todos los elementos del inventario unificado fueron documentados.
- Cada elemento aparece una sola vez por proyecto.
- Cada elemento contiene las tres secciones numeradas.
- Los fragmentos MDD están completos y balanceados.
- Los fragmentos JavaScript están completos y balanceados.
- Los eventos de una misma variable están agrupados.
- Los loops incluyen sus campos internos.
- No se confundieron métodos con variables.
- El código comentado no se presentó como activo.
- Las ausencias se declararon explícitamente.
- No se inventó ninguna correspondencia.
- Las cantidades del inventario coinciden con las fichas generadas.
- El Markdown es válido y todos los bloques de código están cerrados.

## SALIDA OBLIGATORIA

Genera exclusivamente el archivo:

`BASE_CONOCIMIENTO.MD`

No generes explicaciones externas, metodología, recomendaciones ni archivos adicionales.

El documento debe finalizar con:

```markdown
# Control final

- **Proyectos procesados:** [cantidad real]
- **Elementos documentados:** [cantidad real]
- **Elementos con las tres capas:** [cantidad real]
- **Elementos sin cuestionario asociado:** [cantidad real]
- **Elementos sin estructura MDD:** [cantidad real]
- **Elementos sin lógica JavaScript:** [cantidad real]
- **Loops, matrices o grids documentados:** [cantidad real]
- **Funciones globales documentadas:** [cantidad real]
- **Patrones técnicos respaldados:** [cantidad real]
```

Todas las cantidades deben derivarse del contenido procesado.
