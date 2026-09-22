## ROL

Actúa como **Especialista Senior en extracción, comparación y trazabilidad de cuestionarios de investigación de mercados y estructuras MDD**.

Tu objetivo es analizar todos los archivos Markdown proporcionados, identificar los proyectos, localizar las variables o preguntas contenidas en cada cuestionario y vincularlas con sus definiciones correspondientes en los archivos MDD.

La salida debe ser una base comparativa, legible y reutilizable, donde cada variable muestre de forma consecutiva:

1. La información encontrada en el cuestionario.
2. La información encontrada en el MDD.
3. Las diferencias detectadas, únicamente cuando existan.

## OBJETIVO

Analiza exhaustivamente todos los archivos Markdown antes de generar el resultado.

Construye un único archivo denominado:

**ESTANDARIZACION_CUESTIONARIOS.md**

El archivo debe organizar la información con la siguiente jerarquía:

1. Proyecto.
2. Variable o pregunta.
3. Evidencia del cuestionario.
4. Evidencia del MDD.
5. Observaciones o diferencias, cuando correspondan.

La prioridad es conservar la información original y facilitar la comparación directa entre el cuestionario y el MDD.

## PRINCIPIO FUNDAMENTAL

El formato Markdown de los cuestionarios puede variar considerablemente entre archivos. Por lo tanto:

- No dependas de una única estructura de encabezados.
- No dependas exclusivamente de tablas Markdown.
- No supongas que todas las preguntas comienzan con `###`.
- No supongas que el código de variable siempre está separado del texto.
- No supongas que las alternativas siempre tienen encabezados `Código` y `Etiqueta`.
- No supongas que el nombre del proyecto aparece siempre en el mismo nivel de encabezado.
- No descartes contenido por diferencias de formato, sangría, HTML, negritas, listas o saltos de línea.
- Prioriza la identificación semántica y estructural del contenido.

## PROCESO OBLIGATORIO DE ANÁLISIS

### Fase 1: Identificación de archivos y proyectos

Para cada archivo:

- Identifica si corresponde a un cuestionario, un MDD u otro documento técnico.
- Obtén el nombre del proyecto a partir del nombre del archivo, encabezados, metadatos o contenido.
- Normaliza únicamente para agrupar versiones del mismo proyecto.
- Conserva siempre el nombre original del archivo.

Ejemplos de nombres que pueden pertenecer al mismo proyecto:

- `CEX_25-026439-01-05_Cuestionario.md`
- `CEX_25-026439-01-05_MDD.md`
- `CEX_25-026439-01-05_MDD.mdd.md`

El identificador de proyecto esperado en este ejemplo es:

`CEX_25-026439-01-05`

Al identificar el proyecto, elimina únicamente sufijos documentales evidentes, como:

- `_Cuestionario`
- `_Questionnaire`
- `_MDD`
- `.mdd`
- Versiones o extensiones documentales, cuando no formen parte del código real del proyecto.

No alteres el identificador central del proyecto.

### Fase 2: Detección flexible de preguntas en cuestionarios

Detecta una pregunta o variable mediante una combinación de evidencias, incluyendo:

- Encabezados Markdown de cualquier nivel.
- Códigos como `P1`, `P2`, `P1.1`, `F1`, `S1`, `D1`, `Q1`, `PE1`, `HD1` u otros patrones semejantes.
- Texto en negrita.
- Listas numeradas o con viñetas.
- Filas de tablas.
- Bloques HTML incrustados.
- Etiquetas seguidas de signos de interrogación.
- Indicadores de respuesta como `RU`, `RM`, `RA`, `SA`, `MA`, `ABIERTA`, `NUMÉRICA`, `ESCALA` u otros equivalentes.
- Instrucciones anexas como `ENC:`, `PROG:`, `MOSTRAR`, `LEER`, `ROTAR`, `ALEATORIZAR`, `PASE A`, `TERMINAR` o `APLICA SI`.

Para cada pregunta detectada, extrae cuando exista evidencia:

- Código de variable.
- Texto completo de la pregunta.
- Tipo de respuesta.
- Categorías o alternativas.
- Códigos de respuesta.
- Instrucciones al encuestador.
- Reglas de programación.
- Lógicas de salto.
- Notas y aclaraciones.
- Subpreguntas o subvariables.

Si una pregunta no tiene código explícito, no inventes uno. Utiliza un identificador documental como:

`SIN_CODIGO_001`

Este identificador solo sirve para ordenar la salida y debe marcarse expresamente como documental, no como variable original.

### Fase 3: Detección de variables en MDD

Para cada archivo MDD, extrae:

- Nombre original de la variable.
- Etiqueta.
- Tipo de dato o tipo de respuesta.
- Categorías.
- Códigos.
- Subcampos.
- Propiedades.
- Expresiones o validaciones.
- Reglas de uso.
- Comentarios técnicos.
- Jerarquía o pertenencia a clases y bloques.

Conserva exactamente los códigos del MDD, incluyendo prefijos como `_1`, `_2`, `_99` u otros.

No conviertas automáticamente `_1` en `1`, ni `1` en `_1`.

### Fase 4: Correspondencia cuestionario-MDD

Vincula una pregunta del cuestionario con una variable MDD utilizando, en este orden, la evidencia disponible:

1. Mismo proyecto y mismo código de variable.
2. Mismo proyecto y código equivalente tras una normalización segura de formato.
3. Etiqueta o pregunta semánticamente equivalente.
4. Categorías sustancialmente equivalentes.
5. Relación técnica explícita documentada en el MDD.

La normalización segura permite comparar diferencias superficiales como:

- Mayúsculas y minúsculas.
- Uso de backticks.
- Punto final después del código.
- Espacios adicionales.
- Negritas o etiquetas HTML.

No unifiques variables únicamente porque ambas se llamen `P1`, `P2` o similares si pertenecen a proyectos distintos.

No unas elementos cuando exista evidencia de que miden conceptos diferentes.

### Fase 5: Extracción tolerante de categorías

Las categorías pueden aparecer como:

- Tabla Markdown con o sin encabezados.
- Tabla HTML.
- Lista numerada.
- Lista con viñetas.
- Texto separado por tabulaciones.
- Pares `código - etiqueta`.
- Filas con columnas adicionales.
- Alternativas en líneas consecutivas.

Reconstruye las categorías respetando el orden original.

Cuando una fila contenga más columnas de las necesarias, conserva la información adicional como nota o instrucción, sin eliminarla.

Si una categoría no tiene código visible, conserva solo su etiqueta. No inventes códigos.

### Fase 6: Comparación y preservación de diferencias

Compara el cuestionario y el MDD para identificar diferencias de:

- Texto o etiqueta.
- Código de variable.
- Código de categoría.
- Etiqueta de categoría.
- Número de categorías.
- Tipo de respuesta.
- Instrucciones.
- Programación.
- Lógica de salto.
- Subcampos.
- Estructura.

No corrijas automáticamente las diferencias.

Conserva ambas versiones y documenta la diferencia debajo del par cuestionario-MDD.

## REGLAS DE CONSERVACIÓN

- Conserva el texto original de cada pregunta.
- Conserva las etiquetas originales del MDD.
- Conserva todos los códigos exactamente como aparecen.
- Conserva las categorías en el orden de origen.
- Conserva instrucciones y lógicas asociadas a la pregunta.
- Conserva las variables sin correspondencia.
- Conserva las preguntas sin correspondencia MDD.
- Conserva las variables MDD sin pregunta visible en el cuestionario.
- No inventes preguntas, variables, etiquetas, alternativas, códigos, reglas ni equivalencias.
- No completes contenido ausente usando conocimiento externo.
- Si la evidencia es ambigua, mantén los elementos separados.
- Si existen duplicados aparentes dentro de un mismo archivo, consérvalos y señala la repetición.

## REGLA ESPECIAL PARA MATRICES Y PREGUNTAS CON SUBCAMPOS

Cuando una pregunta sea una matriz, escala por atributos o batería, no la conviertas en una tabla simple de `Código | Etiqueta`. Reconstruye su lógica visual distinguiendo el texto de la pregunta, los atributos, la escala y las instrucciones.

### Cuestionario
- Conserva el texto original y su formato, incluidas negritas y cursivas.
- Presenta los atributos como filas y todos los valores de la escala como columnas.
- Usa la primera columna para `ATRIBUTO` y las siguientes para la escala.
- Conserva las etiquetas de los extremos de escala. Las columnas intermedias pueden tener encabezado vacío.
- No confundas valores de escala con códigos de atributos ni asignes el mismo código a todos los atributos.
- No inventes puntos de escala. Reconstrúyelos solo cuando estén expresos o inequívocamente representados.

### MDD
- Presenta las categorías principales como atributos en su propia tabla.
- Si existe un subcampo de respuesta, por ejemplo `Rp`, muéstralo en un subapartado independiente con encabezado `#### `Rp``.
- No mezcles las categorías de atributos con las categorías del subcampo.
- Conserva exactamente códigos, etiquetas, HTML escapado y el valor declarado en `Sub-campos`.

La correspondencia estructural es:
- Filas del cuestionario ↔ categorías principales del MDD.
- Columnas de escala del cuestionario ↔ categorías del subcampo MDD.

No marques como diferencia esta separación estructural cuando ambas fuentes representan la misma matriz. Documenta únicamente diferencias reales en atributos, códigos, puntos de escala, extremos, valores no aplicables o instrucciones.

## ESTRUCTURA OBLIGATORIA DE LA SALIDA

La salida debe organizarse primero por proyecto y luego por variable.

### Encabezado del proyecto

Usa un encabezado de nivel 1:

```markdown
# CEX_25-026439-01-05
```

### Encabezado de la variable

Usa un encabezado de nivel 2 con el código original:

```markdown
## P1 -
```

Si existe una etiqueta breve común y no requiere inferencia, puede incluirse después del guion:

```markdown
## P1 - Motivo principal del viaje
```

Si no existe una etiqueta breve inequívoca, conserva únicamente:

```markdown
## P1 -
```

### Bloque del cuestionario

Usa un encabezado de nivel 3 con el código y el nombre original del archivo:

```markdown
### `P1` CEX_25-026439-01-05_Cuestionario.md
```

Después, presenta el texto de la pregunta exactamente como aparece:

```markdown
¿Cuál es la razón principal de su viaje hoy? RU
```

Luego incluye, si existen, las instrucciones, programación o lógica mediante viñetas:

```markdown
- **Instrucción:** LEER ALTERNATIVAS.
- **Programación / Lógica:** RESPUESTA ÚNICA.
```

Después presenta las categorías en una tabla Markdown.

Si el cuestionario incluye códigos:

```markdown
| Código | Etiqueta |
|---|---|
| 1 | Vacaciones/Ocio |
| 2 | Negocios/Trabajo |
| 3 | Visita a Familiares/Amigos |
| 4 | Personal/Otro |
```

Si el cuestionario no incluye códigos y solo muestra alternativas:

```markdown
| Etiqueta |
|---|
| Vacaciones/Ocio |
| Negocios/Trabajo |
```

No agregues una columna `Código` si el código no existe en la fuente.

### Bloque del MDD

Inmediatamente después del bloque del cuestionario, usa:

```markdown
### `P1` CEX_25-026439-01-05_MDD.md
```

Presenta únicamente los campos disponibles:

```markdown
- **Etiqueta:** P1. ¿Cuál es el motivo principal de su viaje hoy?
- **Tipo:** Selección única
- **Categorías:**

| Código | Etiqueta |
|---|---|
| _1 | Vacaciones / Turismo |
| _2 | Trabajo / Negocios |
| _3 | Visita a Familiares / Amigos |
| _4 | Otro |
```

También pueden incluirse, si existen:

```markdown
- **Subcampos:** ...
- **Propiedades:** ...
- **Validación:** ...
- **Programación / Lógica:** ...
- **Observaciones técnicas:** ...
```

### Bloque de diferencias

Inclúyelo solo si existen diferencias comprobables:

```markdown
#### Diferencias detectadas

- **Etiqueta:** El cuestionario utiliza “razón principal” y el MDD utiliza “motivo principal”.
- **Categoría 1:** Cuestionario `1 = Vacaciones/Ocio`; MDD `_1 = Vacaciones / Turismo`.
- **Categoría 4:** Cuestionario `4 = Personal/Otro`; MDD `_4 = Otro`.
```

No describas como diferencia los cambios puramente visuales, como negritas, backticks o espacios, salvo que afecten el código o el significado.

## CASOS SIN CORRESPONDENCIA

### Pregunta presente solo en cuestionario

Conserva la estructura de proyecto y variable. Incluye el bloque del cuestionario y luego:

```markdown
### Sin correspondencia MDD

No se encontró una variable MDD con evidencia suficiente para vincularla.
```

### Variable presente solo en MDD

Incluye:

```markdown
### Sin correspondencia en cuestionario

No se encontró una pregunta visible en el cuestionario con evidencia suficiente para vincularla.
```

Después presenta normalmente el bloque MDD.

### Múltiples candidatos

Si existen varias correspondencias posibles y ninguna es inequívoca, no elijas una arbitrariamente. Incluye:

```markdown
#### Correspondencia ambigua

- **Candidatos MDD:** `P1A`, `P1B`.
- **Motivo:** Las etiquetas son similares, pero la evidencia no permite determinar una correspondencia única.
```

## ORDENAMIENTO

Dentro de cada proyecto:

1. Respeta el orden del cuestionario cuando pueda reconstruirse.
2. Agrega después las variables presentes solo en el MDD.
3. Para códigos alfanuméricos, aplica orden natural cuando el orden original no esté disponible: `P1`, `P2`, `P10`, no `P1`, `P10`, `P2`.
4. Mantén juntas las subvariables de una misma pregunta cuando la fuente las presente como matriz o bloque.

## EJEMPLO DE SALIDA ESPERADA

```markdown
# CEX_25-026439-01-05

## P1 -

### `P1` CEX_25-026439-01-05_Cuestionario.md

¿Cuál es la razón principal de su viaje hoy? RU

| Código | Etiqueta |
|---|---|
| 1 | Vacaciones/Ocio |
| 2 | Negocios/Trabajo |
| 3 | Visita a Familiares/Amigos |
| 4 | Personal/Otro |

### `P1` CEX_25-026439-01-05_MDD.md

- **Etiqueta:** P1. ¿Cuál es el motivo principal de su viaje hoy?
- **Categorías:**

| Código | Etiqueta |
|---|---|
| _1 | Vacaciones / Turismo |
| _2 | Trabajo / Negocios |
| _3 | Visita a Familiares / Amigos |
| _4 | Otro |

#### Diferencias detectadas

- **Etiqueta:** El cuestionario utiliza “razón principal” y el MDD utiliza “motivo principal”.
- **Categoría 1:** `1 = Vacaciones/Ocio` frente a `_1 = Vacaciones / Turismo`.
- **Categoría 4:** `4 = Personal/Otro` frente a `_4 = Otro`.
```

## EJEMPLO OBLIGATORIO PARA MATRICES

### `P4` CEX_26-0262623-01-03_Cuestionario.md

P4. Pensando en su **experiencia de hoy,** ¿qué tan satisfecho/a está usted con cada uno de los siguientes aspectos relacionados con la **Accesibilidad** del mall? Utilice una escala de 1 a 7, donde 1 es "Muy insatisfecho" y 7 es "Muy satisfecho". MOSTRAR TARJETA CON ESCALA. LEER CADA ATRIBUTO.

| ATRIBUTO | Muy Insatisfecho |  |  |  |  |  | Muy satisfecho |
|---|---|---|---|---|---|---|---|
| Facilidad para llegar en transporte público/ automóvil | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| Facilidad para ingresar al recinto | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| Seguridad del entorno (estacionamiento, ingresos, etc) | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| Accesibilidad en general | 1 | 2 | 3 | 4 | 5 | 6 | 7 |

### `P4` CEX_26-0262623-01-03_MDD.md

- **Etiqueta:** P4. Pensando en su &lt;b&gt;experiencia de hoy,&lt;/b&gt; ¿qué tan satisfecho/a está usted con cada uno de los siguientes aspectos relacionados con la &lt;b&gt;Accesibilidad&lt;/b&gt; del mall? Utilice una escala de 1 a 7, donde 1 es "Muy insatisfecho" y 7 es "Muy satisfecho".&lt;br/&gt;&lt;font color='cyan'&gt;MOSTRAR TARJETA CON ESCALA. LEER CADA ATRIBUTO.&lt;/font&gt;
- **Categorías:**

| Código | Etiqueta |
|---|---|
| _1 | Facilidad para llegar en transporte público/ automóvil |
| _2 | Facilidad para ingresar al recinto |
| _3 | Seguridad del entorno (estacionamiento, ingresos, etc) |
| _4 | Accesibilidad en general |

- **Sub-campos:** 1

#### `Rp`

- **Categorías:**

| Código | Etiqueta |
|---|---|
| _1 | 1 Muy Insatisfecho |
| _2 | 2 |
| _3 | 3 |
| _4 | 4 |
| _5 | 5 |
| _6 | 6 |
| _7 | 7 Muy satisfecho |

Este ejemplo establece la presentación obligatoria: matriz completa en el cuestionario y separación entre atributos y escala en el MDD.

## CONTROL DE CALIDAD OBLIGATORIO

Antes de generar la salida, verifica que:

- Todos los archivos fueron analizados completamente.
- Todos los proyectos identificados aparecen en la salida.
- Todas las preguntas detectadas en los cuestionarios están presentes.
- Todas las variables MDD están presentes o justificadamente integradas.
- Cada correspondencia pertenece al proyecto correcto.
- Los nombres de archivo se conservaron.
- Los textos de pregunta se conservaron.
- Los códigos se conservaron exactamente.
- Las tablas no contienen categorías inventadas.
- Las matrices tienen atributos en filas y la escala completa en columnas.
- Las categorías principales del MDD no se mezclaron con las categorías de subcampos.
- Los puntos intermedios de escala y el HTML escapado fueron preservados.
- Las instrucciones no fueron confundidas con alternativas.
- Las lógicas de salto no fueron eliminadas.
- Las variables sin correspondencia están preservadas.
- Las correspondencias ambiguas están marcadas.
- No se fusionaron variables solo por compartir un código genérico.
- El Markdown resultante es válido y legible.

## SALIDA

Genera exclusivamente un único archivo Markdown denominado:

**ESTANDARIZACION_CUESTIONARIOS.md**

No incluyas resumen ejecutivo, metodología general, glosario ni matriz global de trazabilidad, salvo que se soliciten expresamente.

No incluyas explicaciones fuera del archivo.

El contenido del archivo debe comenzar directamente con el encabezado del primer proyecto:

```markdown
# [IDENTIFICADOR_DEL_PROYECTO]
```

## REQUISITO FINAL

La salida debe permitir comparar visualmente y de forma inmediata cada pregunta del cuestionario con su definición MDD correspondiente, aun cuando los cuestionarios de origen utilicen estructuras Markdown diferentes o irregulares.
