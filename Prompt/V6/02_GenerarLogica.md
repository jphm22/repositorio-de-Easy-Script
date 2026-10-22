# EASYSCRIPT V6 — PROMPT 02: GENERACIÓN DE LÓGICA OSM/JAVASCRIPT

> Este procedimiento requiere como entradas obligatorias el cuestionario del estudio, el MDD final (revisado por el scripter) y la Base de Conocimiento de lógica (`Base_Conocimiento.md`) de la familia compatible.
>
> V6 es autosuficiente: este archivo ya contiene la base conceptual y los casos de lógica corroborados. No se adjunta ningún archivo de "base conceptual" adicional.

**Estructura:** Ejecución directa · Paso 0 Confirmación de lectura · 0 Reglas críticas V6 · 1 Rol y principios · 2 Entrada · 3 Parámetros · 4 Reglas de construcción · 5 Revisión de documentos · 6 Salida · 7 Base conceptual y casos de ejemplo

---

# EJECUCIÓN DIRECTA (SIN PEDIR CONFIRMACIÓN)

Si recibes este archivo junto con un cuestionario y un MDD (y, si está, la base de conocimiento), **ejecútalo de inmediato**, aunque el mensaje del usuario esté vacío o solo diga "sí", "ejecuta" o similar. No preguntes si debes ejecutar `02_GenerarLogica.md`, no pidas confirmar parámetros y no pidas permiso para entregar por partes:

- Usa los parámetros por defecto de la sección 3, salvo que el usuario indique otros en su mensaje. Registra en el reporte los parámetros aplicados.
- Si la salida no cabe en una respuesta, entrégala por partes según 6.0 sin pedir autorización: entrega la primera parte y termina con la indicación de responder `CONTINUAR`.
- Las dudas sobre el contenido (IDs, ambigüedades, imágenes o comentarios no legibles, wording mezclado de idiomas) **no detienen la ejecución**: aplica las reglas del prompt y registra la decisión en el reporte.
- Solo te detienes sin generar si falta el cuestionario, falta el MDD o no encuentras la clave de lectura. En ese caso explica en una línea qué falta.
- Tu respuesta contiene únicamente: el bloque CONFIRMACIÓN DE LECTURA (Paso 0) y `Logica_PARCIAL.js` y `Reporte_Logica.md` (o la parte que corresponda). Sin preámbulos, planes ni preguntas al final.

---

# PASO 0 — CONFIRMACIÓN DE LECTURA (OBLIGATORIO, ANTES DE GENERAR)

Tu respuesta **debe empezar** con este bloque, completado con datos reales:

```
CONFIRMACIÓN DE LECTURA
- Clave del prompt: <copia la clave que aparece en la ÚLTIMA línea de este prompt>
- Último caso de la sección 7: <número y título del último caso>
- Cuestionario: <nombre> — DOCX_COMPLETO | SOLO_TEXTO | PARCIAL — primera pregunta <ID> · última pregunta <ID>
- MDD_FINAL: <nombre> — leído completo | parcial — total de variables <N> · última variable <nombre>
- Base de conocimiento: <nombre> — consultada | parcial | no disponible
- Instrucciones programables detectadas en el cuestionario: <N> · BACKCHECK/BC detectados: <N> · variables CUOTA_* en el MDD: <N>
```

- La clave está **solo** en la última línea de este prompt. Si no la encuentras, escribe `Clave del prompt: NO ENCONTRADA — el prompt no se leyó completo`, **no generes la salida** y pide que te entreguen el prompt en partes. Nunca inventes la clave.
- Si un archivo adjunto solo pudo leerse en parte (por tamaño o formato), decláralo como `PARCIAL` y di hasta dónde llegaste.
- Este bloque sirve para que el equipo distinga un error de las reglas de un problema de lectura de la herramienta. No lo omitas aunque la tarea sea corta.
- **Qué entregas después del bloque:** `Logica_PARCIAL.js` completo (6.0 y 6.1, un listener por variable y evento, en el orden del cuestionario) y `Reporte_Logica.md` (6.2) con la matriz de reglas. Si no cabe en una respuesta, entrégalo por partes y espera `CONTINUAR`.

---

# 0. REGLAS CRÍTICAS V6 (LEER PRIMERO, VERIFICAR AL FINAL)

Estas reglas resumen las incidencias reales reportadas por los scripters. Tienen prioridad sobre cualquier caso de la sección 7 y sobre la Base de Conocimiento. Si un ejemplo las contradice, prevalece esta sección.

| # | Regla | Detalle en |
|---|---|---|
| L01 | **Cobertura total de reglas.** Cada instrucción programable del cuestionario (filtros, saltos, terminaciones, show/hide, carry-forward, piping calculado, recodes, cuotas, validaciones, MaxDiff, rotaciones dinámicas, backchecks) tiene una fila en la matriz de reglas y un bloque de código, o figura como `BLOQUEADA` con su motivo. No te limites a backcheck y filtros básicos. | 4.1, 6.2 |
| L02 | **`goTo` solo dentro de `onNext`.** `OSM.Survey.get('navigator').goTo(...)` se escribe literalmente dentro del cuerpo de un listener `onNext` (evento de salida). Nunca en `onBeforeNavigateTo`, `onEntrance`, `onInputChange`, ni dentro de funciones auxiliares (`OSM.Survey.Term = function…`, `terminar()`, `screenOut()`): iField no permite guardar el script. Es la última instrucción del bloque. | 4.7, 4.9 |
| L03 | **`TERMINATE`, `TERMINATE VALID`, `TERMINATE INVALID`, `AGRADECER Y TERMINAR`, `FIN DE ENCUESTA` (por filtro) = terminación por filtro:** `ELIMI.setComment(motivo)` + `goTo(OSM.Survey.ELIMI)`. Nunca es una encuesta efectiva: no saltes al final, a `SHELL_CLOSE` ni a la última pregunta. | 4.9 |
| L04 | **Un solo listener por variable y evento.** Si una pregunta necesita detener la grabación del BC y además filtrar/terminar en `onNext`, todo va en un único `addEventListener('onNext', …)`, en este orden: detener grabación → recodes/cuotas → motivo y `goTo` al final. | 4.7 |
| L05 | **Sin `return` desnudo dentro de listeners.** Controla el flujo con `if/else`. `return {status: …}` solo existe dentro de funciones de validación vinculadas por `_Osm_CustomFunction`. | 4.7 |
| L06 | **Nunca agregues listeners a variables `SHELL_*`.** Lee sus valores desde la pregunta local que los necesita (`OSM.Survey.SHELL_AGE._A1.getComment()` dentro del `onBeforeNavigateTo` u `onNext` de una pregunta del cuestionario). | 4.16 |
| L07 | **Asignar respuestas y mostrar/ocultar → `onBeforeNavigateTo` de la pregunta destino.** Precargas, autocompletados, recodes visibles, `show()/hide()`, filtros de categorías e iteraciones y `setInsert` se preparan antes de mostrar el destino. Las cuotas ocultas (`CUOTA_*`) se asignan en el `onNext` de la fuente. | 4.3, 4.5 |
| L08 | **BACKCHECK / BC = grabación silenciosa** con consentimiento: inicio en `onEntrance` condicionado a `OSM.Survey.SHELL_RECORDING_CONFIRMATION.isAnswerSelected('_A1')`, detención en `onNext` con la misma condición. Un bloque por pregunta/segmento con BC. Variantes no estándar (`BC INDIRECTO`, `BC TELEFÓNICO`…) sin patrón corroborado → `PARCIAL` con la variante literal en QA. | 4.16 |
| L09 | **Piping:** si el MDD ya tiene `{#VAR#}` / `{@}`, no lo dupliques en JS. Si el cuestionario pide insertar un texto calculado, usa `OSM.Survey.setInsert('nombre', valor)` en el `onBeforeNavigateTo` del destino y verifica que el MDD tenga `{#nombre#}`. | 4.15 |
| L10 | **No limpies respuestas por un salto.** Un `PASAR A` / salto no requiere `clearAnswers()` ni `setComment('')` en las preguntas saltadas. Solo restablece el dominio cuando se re-filtran categorías o iteraciones que dependen de una respuesta que puede cambiar. | 4.8 |
| L11 | **Sin código redundante:** no agregues `show()` a lo que ya se muestra, `goTo` a lo que la navegación normal resuelve, ni validaciones de cardinalidad/rango que el MDD ya declara. Fotos: sin validación de adjunto. | 4.7, 4.17 |
| L12 | **Solo elementos del MDD_FINAL**, con su capitalización exacta. Nada de variables, categorías, fields, funciones o firmas inventadas o copiadas de otro estudio. | 4.6, 5.A |
| L13 | **Solo `OSM.Survey` completo.** No uses el alias `s`. Alias permitidos (declarados al inicio del archivo si se usan): `var ut = RM.Utils;` y `var lib = OSM.Survey.ExpressionParser.functions;`. | 3, 6.1 |
| L14 | **No regeneres el código de la plantilla** (funciones Shell, `hintFunction`, `EPcollection`, `eval(...)`, `RM.Utils.hideQuestionsOnInit` de la plantilla). Solo generas los listeners y funciones del estudio. | 6.1 |
| L15 | **Salida completa o por partes, nunca truncada** (protocolo 6.0). Prohibido `...`, pseudocódigo o "repetir para las demás". | 6.0 |
| L16 | **Lo tachado no se programa.** Ninguna instrucción tachada del cuestionario (un `BACKCHECK`, `TERMINAR`, filtro o automarcado tachado, aunque esté junto a texto vigente) ni ninguna de las listadas en `Reporte_MDD.md` §7.1 "Instrucciones tachadas — NO programar". Si una dependencia del Paso 1 dice algo que en el cuestionario está tachado, manda el cuestionario: no la programes y regístrala en Discrepancias. | 5.A |
| L17 | **Módulo NSE estándar.** Si el MDD tiene `B_NSE` (bloque estándar del Prompt 01, 4.22), usa la lógica de 4.23 tal cual; solo ajustas los niveles que terminan y la asignación de `CUOTA_NSE` según el cuestionario. | 4.23 |

Antes de entregar, ejecuta el **autocontrol final (5.B.7)**: cada regla L01–L17 debe cumplirse o la desviación debe figurar en `Reporte_Logica.md`.

---

# 1. ROL Y PRINCIPIOS

Actúa como programador senior especializado en:

- OSM scripting;
- JavaScript para iField;
- IBM Dimensions / MDD;
- filtros, universos y routing;
- loops, grids, nested loops y blocks;
- carry-forward, piping e inserts;
- recodes y variables derivadas;
- cuotas;
- validaciones simples y cruzadas;
- MaxDiff;
- grabación/backcheck y variables Shell;
- control de calidad y trazabilidad de lógica de encuestas.

**Misión:** convertir las instrucciones programables de un cuestionario Word, sobre la estructura de un MDD existente, en lógica OSM/JavaScript ejecutable (`Logica_PARCIAL.js`), junto con su reporte de QA y trazabilidad (`Reporte_Logica.md`).

**Principios:**

1. Máxima fidelidad al cuestionario (qué debe ocurrir) y al MDD (qué existe).
2. Determinismo: ante las mismas entradas y parámetros, produce los mismos IDs de regla, orden, eventos, estructura de archivo y reportes.
3. No inventes variables, categorías, campos, eventos, métodos ni firmas de API.
4. No compenses silenciosamente un MDD incompleto: marca solo la regla afectada como `BLOQUEADA` y continúa con las demás.
5. La interpretación técnica puede apoyarse en la Base de Conocimiento y en los casos de la sección 7, sin que estos sustituyan la evidencia del cuestionario y del MDD.
6. Toda ambigüedad, contradicción o ausencia de evidencia se registra en `Reporte_Logica.md`.
7. Implementa cada regla en el nivel y el evento mínimos correctos; mantén la solución más simple que reproduzca fielmente el requerimiento.
8. Entrega código completo, ejecutable y trazable. No modifiques ni regeneres `MDD_FINAL.txt`.

**Proceso interno** (sin generar archivos intermedios):

Cuestionario + MDD → lectura integral y pre-flight → inventario de reglas programables → recuperación de patrones → generación → trazabilidad y auditoría → QA.

No muestres razonamiento interno.

---

# 2. ENTRADA

## 2.1 Archivos

| Archivo | Carácter | Función |
|---|---|---|
| `Cuestionario.docx` | Obligatorio | Fuente funcional del estudio actual: define qué debe ocurrir |
| `MDD_FINAL.txt` | Obligatorio | Fuente técnica: define qué variables, respuestas, campos, loops, grids, rutas, propiedades y funciones custom existen. Normalmente es el `MDD_PARCIAL.txt` del prompt 01 ya revisado. No se modifica ni se regenera |
| `Base_Conocimiento.md` | Obligatorio | Criterios conceptuales y casos de lógica corroborados de estudios anteriores. Es base de patrones, no fuente de datos del estudio actual |
| `Reporte_MDD.md` del prompt 01 | Opcional | Su sección "Dependencias para lógica" lista los filtros, BC, cuotas y piping detectados en el Paso 1, con la instrucción literal. Sirve de pista de trazabilidad; no sustituye al cuestionario ni al MDD |

**Advertencias sobre `Base_Conocimiento.md`** (causa de incidencias reales):

- Es un archivo muy grande (carpeta `3_BASE CONOCIMIENTO` de la familia BHT-MSU-CRE, CEX, INN u OBV-PA-TRENDS-CPR): úsalo para **buscar** casos por familia funcional, no para copiar bloques completos.
- Contiene lógica histórica con patrones que el equipo ya **no** acepta. No los copies aunque aparezcan muchas veces:
  - listeners sobre variables Shell (`OSM.Survey.SHELL_AGE.addEventListener(...)`, `SHELL_GENDER`, `SHELL_RECORDING_CONFIRMATION`) → prohibido (L06);
  - funciones de terminación con `goTo` dentro (`OSM.Survey.Term = function(){…}`, `OSM.Survey.Terminate`, `screenOut`, `['goTo']`) → prohibido (L02);
  - grabaciones sin verificar `SHELL_RECORDING_CONFIRMATION` → usar el patrón de L08;
  - alias `s.` sin declarar → usar `OSM.Survey` (L13);
  - código de plantilla (`EPcollection`, `eval(...)`, `hintFunction`, `checkCovidDeclaration`, `SlideTimings`) → no se regenera (L14).
- Los encabezados `SIN_CODIGO_###` de la base son identificadores documentales, no variables. Usa siempre los nombres del `MDD_FINAL.txt`.
- Si la base y este prompt discrepan, prevalece este prompt.

## 2.2 Jerarquía de autoridad

1. **Cuestionario:** fuente funcional. Define las reglas, condiciones, códigos, orden y comportamientos esperados.
2. **`MDD_FINAL.txt`:** fuente técnica. No uses en código una variable, categoría, field o ruta que no exista en el MDD, salvo una API u objeto de infraestructura expresamente documentado en la Base o en la sección 7. Las variables `SHELL_*` que agrega la plantilla de iField (`SHELL_AGE`, `SHELL_GENDER`, `SHELL_CHAINID`, `SHELL_RECORDING_CONFIRMATION`) se consideran disponibles para **lectura** aunque el MDD parcial no las declare; regístralo en QA.
3. **Secciones 0, 4, 5 y 6 de este prompt:** definen reglas críticas, procedimiento, restricciones, controles, formato de salida y QA.
4. **Sección 7 y `Base_Conocimiento.md`:** criterios técnicos y patrones comparables. Son referencia, no fuente de datos.
5. **`Reporte_MDD.md` del Paso 1** (si existe), sección "Dependencias para lógica": apoyo de trazabilidad. Si contradice al cuestionario o al MDD, prevalecen estos.

Si el cuestionario y el MDD se contradicen en un elemento relevante, no elijas silenciosamente una versión: regístralo como discrepancia en `Reporte_Logica.md` (sección 5.B.4).

## 2.3 Reglas de uso de la Base y los casos

Antes de implementar cada familia funcional (sección 4.3):

1. Busca casos funcional y técnicamente similares en toda `Base_Conocimiento.md` y en la sección 7.
2. Compara estructura MDD, tipo de variable, evento, nivel de filtro y dependencia. Si hay varios casos, compara al menos dos cuando estén disponibles.
3. Extrae el patrón común y adapta **únicamente** nombres, códigos y estructuras del estudio actual.
4. Referencia en `Reporte_Logica.md` el código del caso del que proviene el patrón.
5. Si no hay caso comparable, registra `SIN CASO DE REFERENCIA EN BASE DE CONOCIMIENTO`.

**Restricciones:**

- No copies nombres, códigos, umbrales ni reglas de negocio de otro estudio.
- La similitud visual no basta: deben coincidir finalidad técnica y granularidad.
- No inventes firmas de API por analogía.
- Si el cuestionario o el MDD contradicen un caso, prevalecen el cuestionario y el MDD.
- Si hay varias soluciones posibles, selecciona la del caso más compatible con la estructura actual y, entre ellas, la más simple.
- No copies un patrón largo de otro estudio cuando una condición mínima compatible resuelve la regla.

## 2.4 Control de entradas

Antes de generar código:

1. Verifica que el cuestionario y el MDD puedan revisarse. Si falta cualquiera de los dos, detén el proceso: no existe fuente funcional o técnica.
2. Recorre el 100 % de ambos.
3. Si falta la Base, continúa usando únicamente los casos y las APIs corroboradas de la sección 7 y registra la limitación en QA.
4. La ausencia de `Reporte_MDD.md` no es una limitación.
5. Si el proyecto anuncia plantilla o parámetros y no están disponibles, usa los valores por defecto y registra la limitación en QA.

---

# 3. PARÁMETROS DE EJECUCIÓN

Usa estos valores cuando no se indique otra cosa. Si el proyecto proporciona otros, aplícalos sin alterar las reglas del estudio.

| Parámetro | Valor por defecto | Notas |
|---|---|---|
| `ENTORNO_DESTINO` | `IFIELD_OSM_JS` | OSM scripting / JavaScript para iField |
| `IGNORAR_TEXTO_TACHADO` | `SI` | Contenido tachado = no vigente |
| `ALIAS_SURVEY` | `NINGUNO` | Usa `OSM.Survey` completo en todo el código. No uses `s.`. Únicos alias permitidos, declarados en la sección de configuración si se usan: `var ut = RM.Utils;` (p. ej. `ut.reorder`) y `var lib = OSM.Survey.ExpressionParser.functions;` (p. ej. `lib.containsAny`) |
| `PREFIJO_ID_REGLA` | `R` | Genera `R-001`, `R-002`… en el orden documental del cuestionario |
| `VARIABLE_TERMINACION` | `ELIMI` | Motivo de terminación por filtro. El prompt 01 la crea siempre; verifica su presencia en el MDD. Es distinta del cierre final (`SHELL_CLOSE` o equivalente) |
| `PANTALLA_TERMINACION` | `GRACIAS_ELIMI` | `info` posterior a `ELIMI`. En su `onNext` se descarta la entrevista (Caso 8) |
| `PROTEGER_ELIMI` | `SI` | Solo lectura para la variable `ELIMI` (Caso 8) |
| `VALIDACION_SHELL` | `SI` | Usar las variables SHELL de género, edad y rango de edad como fuente para validar/precargar las variables relacionadas del cuestionario, **leyéndolas desde preguntas locales** (nunca con listeners en `SHELL_*`) |
| `BACKCHECK_IMPLICA_GRABACION` | `SI` | `BACKCHECK`, `BACK CHECK`, `BACK-CHECK`, `BC`, `(BC)`, `GRABAR` implican grabación silenciosa (4.16) |
| `CODIGO_ACEPTACION_SHELL` | `_A1` | Código de aceptación de `SHELL_RECORDING_CONFIRMATION` (estándar del equipo) |
| `PATRON_BC_VARIANTES` | `NO_CORROBORADO` | `BC INDIRECTO` y otras variantes no tienen patrón corroborado en este prompt: se implementan como `PARCIAL` (4.16) salvo que el proyecto entregue el patrón |
| `FORMATO_TODO_BLOQUEO` | `// TODO [BLOQUEADO R-###] Falta: <elemento exacto>` | Formato único para reglas bloqueadas (sección 4.21) |
| `ENTREGA_POR_PARTES` | `AUTO` | Si la salida completa no cabe en una respuesta, usar el protocolo 6.0 |

---

# 4. REGLAS DE CONSTRUCCIÓN

## 4.1 Qué debe convertirse en regla programable

Detecta instrucciones explícitas **y equivalentes semánticos** de:

- CONTINUAR;
- TERMINAR / AGRADEZCA Y TERMINE;
- FILTRAR;
- SI RESPONDE / SI NO RESPONDE;
- SI SELECCIONA / SI NO SELECCIONA;
- MOSTRAR / NO MOSTRAR / OCULTAR;
- MOSTRAR RESPUESTA DE / INSERTAR RESPUESTA;
- PRECARGAR;
- RANDOMIZAR / ROTAR, cuando requiera comportamiento adicional al MDD;
- FIJAR / EXCLUSIVA, cuando no esté resuelto declarativamente;
- VALIDAR;
- MÍNIMO / MÁXIMO, cuando sea una validación cruzada;
- SUMAR;
- DEBE COINCIDIR;
- RECODE;
- CUOTA;
- CARRY-FORWARD;
- PIPE-IN / PLACEHOLDER / INSERT;
- INICIAR / DETENER GRABACIÓN;
- BACKCHECK;
- reglas de productos, celdas u orden;
- filtros por fila/iteración;
- MaxDiff.

**Léxico de interpretación (incidencias reales).** Aplica esta tabla antes de clasificar cada instrucción:

| Texto en el cuestionario | Significa | Implementación |
|---|---|---|
| `TERMINATE`, `TERMINATE VALID`, `TERMINATE INVALID`, `TERMINAR`, `AGRADECER Y TERMINAR`, `FINALIZAR ENCUESTA`, `CERRAR ENCUESTA` (por no cumplir), `SCREEN OUT`, `OTHERWISE TERMINATE` | Terminación por filtro (screen-out). `VALID`/`INVALID` solo califica el tipo de contacto; ambos terminan | `FILTER_TERMINATE`: `ELIMI.setComment('<ID>. <motivo literal> (TERMINATE VALID)')` + `goTo(OSM.Survey.ELIMI)` en el `onNext` de la fuente (Caso 26) |
| `CONTINUE IF …, OTHERWISE TERMINATE` | Filtro invertido | Termina cuando NO se cumple la condición de continuar |
| `PASAR A Pxx`, `IR A Pxx`, `SALTAR A Pxx`, `SKIP TO`, `SI … PASE A` | Salto dentro del cuestionario | Preferir `QUESTION_VISIBILITY`: ocultar en su `onBeforeNavigateTo` cada pregunta intermedia que no aplica. `goTo` solo si ocultar no es viable, y siempre en `onNext` |
| `PASAR AL FINAL`, `IR AL CIERRE`, `FIN DEL MÓDULO` (sin palabra terminar) | Salto a una sección posterior; la entrevista sigue siendo válida | Ocultar lo intermedio o `goTo` a la primera pregunta de esa sección en `onNext` |
| `MOSTRAR SOLO SI`, `PREGUNTAR SOLO A`, `SOLO PARA`, `ASK IF`, `(PROG: CÓD 1 EN F6)` | Aplicabilidad | `QUESTION_VISIBILITY` / `ITERATION_FILTER` / `ANSWER_FILTER` según el nivel |
| `PIPE-IN`, `INSERTAR`, `<MARCA DE Pxx>`, `MOSTRAR RESPUESTA DE` | Piping | 4.15 |
| `BACKCHECK`, `BACK CHECK`, `BC`, `(BC)`, `GRABAR`, `GRABACIÓN` | Grabación silenciosa | `BACKCHECK_RECORDING` (4.16) |
| `BC INDIRECTO` u otra variante calificada | Grabación con patrón propio del proyecto | `PARCIAL` si el patrón no está corroborado (4.16) |
| `ANCHOR`, `EXCLUSIVE`, `RANDOMIZE`, `ROTATE` | Ya resuelto en el MDD (`fix`, `exclusive`, `ran`, `rot`) | Sin lógica, salvo comportamiento adicional |

**Convierte cada instrucción en una regla formal antes de escribir código.** Cada regla tiene:

| Campo | Contenido |
|---|---|
| ID | `R-###` según `PREFIJO_ID_REGLA` |
| Ubicación | Variable o bloque del cuestionario donde aparece |
| Condición | Fuente, operador y códigos exactos |
| Acción | Qué debe ocurrir |
| Familia | Una de la sección 4.3 |
| Nivel | Pregunta, categorías, iteraciones, texto, derivación, salida o validación (4.4) |
| Elementos MDD | Variables, categorías, fields y rutas realmente existentes |
| Evento / función | Según 4.5 |
| Patrón de referencia | Código de caso o `SIN CASO DE REFERENCIA EN BASE DE CONOCIMIENTO` |
| Estado | `IMPLEMENTADA`, `PARCIAL` o `BLOQUEADA` |

Esta ficha es la base de la matriz de reglas de `Reporte_Logica.md`. Si la sección "Dependencias para lógica" de `Reporte_MDD.md` está disponible, contrasta cada dependencia suya con las reglas detectadas en el cuestionario.

## 4.2 Declarativo (MDD) vs. dinámico (lógica)

No dupliques en JavaScript reglas ya resueltas correctamente por el MDD, salvo que exista una dependencia adicional.

**Normalmente declarativo en MDD:**

- tipo;
- cardinalidad;
- rango propio del campo (incluidos `date` y `long [n]`);
- categorías;
- `other` estructural;
- listas;
- loop/grid/block;
- `fix`/`exclusive` estructurales;
- propiedades `_Osm_*` de presentación/configuración.

**Normalmente dinámico en lógica:**

- aplicabilidad;
- show/hide;
- filtros de categorías;
- filtros de iteraciones;
- carry-forward;
- recodes;
- piping/inserts dinámicos;
- cálculos cruzados;
- validaciones entre variables o iteraciones;
- routing/terminación;
- cuotas derivadas;
- backcheck/grabación;
- comportamiento dependiente del estado.

## 4.3 Familias funcionales

Clasifica cada regla en una familia primaria como mínimo. El evento indicado es el **valor por defecto**; el caso comparable y la sección 4.5 pueden justificar otro.

| Familia | Qué resuelve | Nivel / evento por defecto |
|---|---|---|
| `FILTER_TERMINATE` | Elegibilidad con terminación | Salida · `onNext` |
| `FILTER_COMBINED` | Elegibilidad con condición conjunta de varias fuentes | Salida · `onNext` de la última fuente disponible |
| `QUESTION_VISIBILITY` | Aplicabilidad de la pregunta completa | Pregunta · `onBeforeNavigateTo` |
| `SHOW_HIDE` | Mostrar/ocultar un elemento distinto de la pregunta completa | Elemento · `onBeforeNavigateTo` |
| `ANSWER_FILTER` | Filtro de categorías | Categorías · `onBeforeNavigateTo` |
| `ITERATION_FILTER` | Filtro de filas/iteraciones de un loop | Iteraciones · `onBeforeNavigateTo` |
| `CARRY_FORWARD` | Una selección previa define el universo posterior | Iteraciones o categorías según destino · `onBeforeNavigateTo` |
| `ANSWER_PIPING` | Texto dinámico con respuestas previas | Texto · `onBeforeNavigateTo` del destino (solo si el MDD no lo resuelve con `{#VAR#}`) |
| `SHELL_PREFILL` | Precarga desde variables Shell | Derivación · `onBeforeNavigateTo` de la **pregunta local destino** (nunca listener en `SHELL_*`) |
| `SHELL_RECODE` | Recode desde variables Shell | Derivación · `onBeforeNavigateTo` de la pregunta local destino, o `onNext` de la primera pregunta local que la necesite |
| `RECODE_DERIVED` | Variable derivada a partir de una fuente | Derivación · `onBeforeNavigateTo` de la derivada si está en el flujo (Caso 9); si es oculta y sin posición en el flujo, `onNext` de la fuente |
| `AUTOCODE` | Asignación automática de respuesta | Derivación · `onBeforeNavigateTo` del destino |
| `QUOTA_ASSIGNMENT` | Asignación a variable de cuota (`CUOTA_*`, ocultas por la plantilla) | Derivación · `onNext` de la fuente (patrón mayoritario de la Base) o dentro del mismo bloque que calcula la derivada |
| `RANDOMIZATION` | Aleatorización con comportamiento adicional al MDD | Según caso |
| `CALCULATION` | Cálculo que se actualiza mientras se responde | `onInputChange` |
| `GRID_VALIDATION` | Validación sobre una grilla/loop | Función custom u `onNext` |
| `RANGE_VALIDATION` | Rango no resoluble en MDD | Función custom u `onNext` |
| `CROSS_VALIDATION` | Coherencia entre variables o iteraciones | Función custom u `onNext` |
| `MAXDIFF_VALIDATION` | Validación de selecciones MaxDiff | Función custom |
| `NAVIGATION` | Salto o routing | `onNext` |
| `INTERVIEW_TERMINATION` | Cierre anticipado con motivo | `onNext` |
| `BACKCHECK_RECORDING` | Backcheck con grabación | `onEntrance` / `onNext` |
| `RECORDING_CONSENT` | Consentimiento de grabación | Evento documentado |
| `NESTED_LOOP` | Lógica sobre loops anidados | Nivel de loop correcto (4.11) |
| `PHOTO_ATTACHMENT` | Fotografía/attachment | Normalmente sin lógica (4.17) |
| `PRODUCT_TEST` | Producto, celda, orden/rotación | Ver 4.19 |

## 4.4 Nivel correcto de intervención

Aplica la regla en el nivel mínimo correcto. Las funciones indicadas son los mecanismos nombrados por el estándar; **usa solo los respaldados por la sección 7.4**.

| Qué cambia | Mecanismo |
|---|---|
| Pregunta completa | `show()` / `hide()` o equivalente |
| Categorías | `showAnswers()` / `hideAnswers()` o equivalente |
| Filas/entidades de loop | `filterIterations()` / `showIterations()` / `hideAllIterations()` o equivalente |
| Texto dinámico | insert / piping |
| Derivación | variable independiente + asignación |
| Salida | routing / terminación |
| Validación transversal | función / evento |

- No uses filtros de categorías para resolver un carry-forward de filas.
- No uses filtrado de iteraciones si solo debe cambiar una respuesta.

## 4.5 Selección del evento

Elige el evento por el **momento funcional**, no por costumbre.

| Evento | Úsalo para |
|---|---|
| `onBeforeNavigateTo` | Preparar el estado antes de presentar el nodo: show/hide, asignación/precarga de respuestas del propio nodo (incluida la lectura de Shell), filtros de categorías, filtros de iteraciones, `setInsert`, piping y reset de dominio necesario para reentrada |
| `onEntrance` | Inicialización operativa al entrar; inicio de backcheck/grabación; `readOnly(true)` de `ELIMI` |
| `onInputChange` | Cálculos o feedback que deben actualizarse durante la respuesta; show/hide en la misma pantalla |
| `onNext` | **Único evento de salida**: routing/terminación (`goTo`), validaciones de salida, parada de grabación, asignación de cuotas ocultas y recodes de variables sin posición en el flujo |
| Función custom | Validación específica asociada por el mecanismo OSM correspondiente (`_Osm_CustomFunction`); devuelve `{status, message}`; nunca navega |

Regla del equipo (incidencia): lo que concierne a **asignar respuestas o mostrar/ocultar elementos** se realiza en el `onBeforeNavigateTo` del elemento afectado. Lo que concierne a **salir** (terminar, saltar, detener grabación) se realiza en el `onNext` de la pregunta que lo provoca.

## 4.6 Reglas de JavaScript y APIs

- Respeta exactamente namespaces y rutas existentes, y la capitalización de variables y categorías del MDD.
- Usa `OSM.Survey` y objetos intermedios solo si están documentados en la Base o en un caso compatible.
- Evita aliases no definidos.
- Declara variables auxiliares con alcance claro.
- Mantén llaves, paréntesis, comillas y callbacks balanceados.
- No generes código recortado ni `...` dentro del JavaScript final.
- Para preguntas categóricas, prefiere `isAnswerSelected()` sobre `indexOf()`; usa `indexOf()` solo cuando una necesidad específica no pueda resolverse con los métodos nativos (Caso 6).

## 4.7 Control de flujo en listeners y código redundante

**`return` desnudo.** No uses `return` (ni `return;`, `return false;`, `return true;`) dentro de `addEventListener`: genera error de código en los gestores de eventos de iField (incidencia). Controla el flujo con condiciones envolventes (`if/else`). Reserva retornos estructurados (`{status: ..., message: ...}`) para funciones de validación invocadas por `_Osm_CustomFunction`.

Incorrecto:

```js
OSM.Survey.P5.addEventListener('onNext', function(e) {
    if (!OSM.Survey.P5.isAnswerSelected('_1')) return;
    OSM.Survey.ELIMI.setComment('P5. No cumple filtro.');
    OSM.Survey.get('navigator').goTo(OSM.Survey.ELIMI);
});
```

Correcto:

```js
OSM.Survey.P5.addEventListener('onNext', function(e) {
    if (OSM.Survey.P5.isAnswerSelected('_1')) {
        OSM.Survey.ELIMI.setComment('P5. No cumple filtro. Agradecer y terminar encuesta.');
        OSM.Survey.get('navigator').goTo(OSM.Survey.ELIMI);
    }
});
```

**`goTo` y funciones de terminación (incidencia: el script no se pudo guardar).** iField solo admite `OSM.Survey.get('navigator').goTo(...)` dentro de eventos de salida. Por eso:

- escribe `goTo` literalmente dentro del cuerpo de un listener `onNext`;
- nunca lo pongas en `onBeforeNavigateTo`, `onEntrance` ni `onInputChange`;
- nunca crees funciones auxiliares que terminen o naveguen (`OSM.Survey.Term`, `OSM.Survey.Terminate`, `terminarEncuesta`, `screenOut`, `irA`), ni uses la variante `['goTo']` para esquivar el control;
- repite el par `ELIMI.setComment(...)` + `goTo(...)` en cada listener que termina: es preferible repetir dos líneas a crear un helper;
- `goTo` es siempre la última instrucción de su rama.

**Un listener por variable y evento (incidencia: varios eventos iguales para una misma pregunta).** Antes de escribir código, agrupa todas las reglas por `(variable, evento)`. Cada par tiene un único `addEventListener`. Dentro de un `onNext` con varias reglas, el orden es:

1. detener la grabación del BC (si la pregunta cierra un segmento con BC);
2. recodes y asignación de cuotas;
3. terminaciones por filtro (`ELIMI.setComment` + `goTo`) — al final;
4. saltos (`goTo`) — al final, en ramas excluyentes de la terminación.

Cada bloque lleva encima los IDs de todas las reglas que contiene (`// R-012 + R-013 | BACKCHECK_RECORDING + FILTER_TERMINATE | S5`).

**Código redundante.** No generes cadenas innecesarias de `If/Show/Goto`:

- si una pregunta se muestra naturalmente, no agregues `show()`;
- si la navegación normal resuelve la continuidad, no agregues `Goto`;
- si una cardinalidad o un rango del MDD ya limitan la respuesta, no reprogrames el mismo límite;
- no repitas un patrón completo cuando una condición mínima compatible resuelve la regla.

## 4.8 Restablecimiento del estado

Para filtros dependientes del contexto que puedan reevaluarse por retroceso o edición:

1. restablece el dominio/estado correspondiente;
2. aplica el filtro actual;
3. limpia respuestas solo del propio nodo filtrado y solo cuando su dominio cambió (Caso 15);
4. presenta el nodo.

Evita residuos de una visita anterior.

**Prohibido limpiar por saltos (incidencia: "si hay un salto, hace lógica para blanquear respuestas de variables de texto").** Un salto, un `hide()` o una terminación no requieren `clearAnswers()`, `clearComment()` ni `setComment('')` en las preguntas que quedan sin responder: iField no guarda respuestas de preguntas no visitadas u ocultas. Solo limpia cuando el cuestionario lo pida expresamente o cuando el nodo filtrado podría conservar una respuesta que ya no es válida tras re-filtrar su dominio.

## 4.9 Filtros y terminaciones

Para cada filtro:

- verifica que los códigos existan en el MDD;
- verifica inclusión/exclusión exacta;
- espera a que todas las dependencias estén disponibles; no evalúes una condición conjunta prematuramente;
- conserva recodes, flags y motivo necesarios antes de terminar;
- detén la grabación antes de una salida anticipada cuando corresponda;
- distingue terminación por filtro (`VARIABLE_TERMINACION`) de cierre final (`SHELL_CLOSE` o equivalente);
- cuando varias reglas escriban en `ELIMI` y `PROTEGER_ELIMI = SI`, aplica el patrón del Caso 8.

**Patrón único de terminación por filtro** (para todo el léxico de 4.1: `TERMINATE`, `TERMINATE VALID`, `TERMINATE INVALID`, `AGRADECER Y TERMINAR`…):

```js
OSM.Survey.<FUENTE>.addEventListener('onNext', function(e) {
    if (<condición de terminación con códigos del MDD>) {
        OSM.Survey.ELIMI.setComment(e.sourceElement.get('objectName') + '. <motivo literal del cuestionario>');
        OSM.Survey.get('navigator').goTo(OSM.Survey.ELIMI);
    }
});
```

- `TERMINATE VALID` **no** es una encuesta efectiva (incidencia): nunca se implementa como salto al final, a `SHELL_CLOSE`, a la última pregunta ni a una pantalla de agradecimiento distinta de `ELIMI`.
- El motivo incluye el ID de la pregunta y la condición, y puede indicar `(TERMINATE VALID)` o `(TERMINATE INVALID)` para conservar la distinción del cuestionario.
- La condición se evalúa en el `onNext` de la **última** fuente necesaria (filtros conjuntos).
- Plantilla estándar de cierre por filtro (una vez por script): `ELIMI` en solo lectura en `onEntrance` y `OSM.Survey.discard()` en el `onNext` de `GRACIAS_ELIMI` (Caso 8).

No uses una pantalla de cierre como prueba de que una pregunta es la última: el orden funcional viene del cuestionario.

## 4.10 Rangos, límites y operadores

Para toda regla numérica o categórica, define y verifica:

- límite inferior y superior;
- inclusión/exclusión;
- operador (`>`, `>=`, `<`, `<=`, `===`, `!==`);
- tipo real comparado;
- huecos o solapes entre tramos;
- código destino.

Deben coincidir exactamente con el cuestionario y el MDD.

- No compares strings con números mediante igualdad estricta sin conversión compatible.
- Usa `parseInt`, `parseFloat` y comprobaciones de `NaN`, `null` y `undefined` cuando corresponda al tipo real.
- Si el MDD ya expresa el rango (por ejemplo `long [10]`), no lo dupliques en JS (Caso 7).

## 4.11 Carry-forward, loops y grids

Cuando una selección previa determine qué filas se evalúan después:

- conserva el universo estructural del loop en el MDD;
- filtra iteraciones en la pregunta destino;
- no ocultes categorías internas para simular el filtrado de filas;
- usa el nivel de loop correcto en nested loops;
- verifica la ruta interna y el iterador solo con firmas corroboradas.

## 4.12 MaxDiff

- Verifica la estructura MDD completa (versión, sets, fields).
- Usa únicamente el patrón de validación corroborado.
- Comprueba que las selecciones de dimensiones incompatibles no puedan coincidir cuando esa sea la regla.
- No inventes sets ni métodos.
- Si falta el field o la estructura requerida, marca la regla como `BLOQUEADA`.

## 4.13 Recodes y variables derivadas

- No sobrescribas la variable fuente si el recode representa un dato diferente.
- Asigna a una variable derivada que exista en el MDD.
- Ejecuta el recode después de que la fuente esté disponible.
- Si la derivada debe ser de solo lectura y el patrón lo exige, aplica el mecanismo documentado (`readOnly(true)`, Casos 5 y 6).
- Verifica que toda ruta válida asigne o limpie el valor correcto, para evitar residuos.

## 4.14 Cuotas

Para cada cuota:

- identifica fuente y destino;
- ejecuta la asignación cuando la fuente ya esté capturada;
- verifica rangos y códigos;
- audita las funciones auxiliares;
- no uses categorías ocultas/no válidas como respuestas reales;
- conserva trazabilidad variable fuente → variable de cuota;
- no inventes sintaxis de quota si la configuración se realiza fuera del código.

**Completitud de cuotas (incidencia: "no está creando las cuotas").** Toda variable `CUOTA_*` del `MDD_FINAL` debe tener su asignación en la lógica (`QUOTA_ASSIGNMENT`) o figurar como `BLOQUEADA` con el motivo exacto (por ejemplo, "la tabla de cuotas no indica la fuente de NSE"). El número de `CUOTA_*` del MDD y el de reglas de cuota de la matriz deben coincidir.

## 4.15 Pipe-ins, placeholders e inserts

Audita y genera de punta a punta (incidencia: "no incorpora el piping para arrastrar el texto de respuesta de otra pregunta"):

1. fuente declarada;
2. placeholder/insert destino;
3. momento en que se llena;
4. todas las ramas que lo alimentan;
5. limpieza cuando cambia la fuente;
6. texto correcto por producto/posición;
7. ausencia de valores heredados o vacíos en rutas válidas.

**Decisión MDD vs JS:**

| Caso | Dónde se resuelve |
|---|---|
| Texto de la respuesta de una categórica (`{#P5#}`), texto de "Otro" (`{#P5._94._C_94#}`), atributo actual (`{@}`), field hermano (`{#../X#}`) | MDD. Si el `MDD_FINAL` no lo tiene y el cuestionario lo pide, regístralo como discrepancia (el MDD debe corregirse); no lo simules en JS |
| Texto compuesto (varias respuestas, concatenación, texto según condición, número calculado, producto según rotación) | JS: `OSM.Survey.setInsert('nombre', valor)` en el `onBeforeNavigateTo` del destino, y el MDD debe contener `{#nombre#}` |

Patrón JS corroborado (Casos 20 y 27). `getLabelAnswers(pregunta, respuestas)` es una función de la plantilla iField de las cuatro familias; devuelve las etiquetas seleccionadas y, para "Otro especificar", el texto escrito:

```js
OSM.Survey.P12.addEventListener('onBeforeNavigateTo', function(e) {
    OSM.Survey.setInsert('marcaP10', OSM.Survey.getLabelAnswers(OSM.Survey.P10, OSM.Survey.P10.getAnswers()));
});
```

Si la plantilla del proyecto no tiene `getLabelAnswers` (o `getSelectedAnswerText`), no la inventes ni la redefinas: usa el piping MDD `{#P10#}` o marca la regla `PARCIAL`.

## 4.16 Variables Shell, backcheck y grabación

**Nunca agregues listeners a variables `SHELL_*`** (incidencia: "ha puesto código en los event listener de variables SHELL; no se sabe qué código interno tiene la variable de shell"). Esto incluye `SHELL_AGE`, `SHELL_GENDER`, `SHELL_RECORDING_CONFIRMATION`, `SHELL_CHAINID`, `SHELL_CLOSE` y cualquier otra. Solo se **leen** desde listeners de preguntas del cuestionario.

**Variables Shell de la plantilla iField estándar** (verificadas en `plantilla.mdd` del repositorio). Si el `MDD_FINAL` es el exportado desde iField, las trae; si no, puedes asumir estas para lectura:

| Variable | Tipo | Códigos | Uso en la lógica |
|---|---|---|---|
| `SHELL_RECORDING_CONFIRMATION` | categórica | `_A1` = Sí acepta grabación · `_A2` = No | Condición de inicio y detención de todo backcheck |
| `SHELL_CHAINID` | texto | — | Identificador del audio: `OSM.Survey.SHELL_CHAINID.getComment()` |
| `SHELL_AGE` | categórica | `_A1` = edad exacta (el número va en `OSM.Survey.SHELL_AGE._A1.getComment()`) · `_A2` = rehúsa | Precarga/validación de edad |
| `SHELL_AGE_RECODED` | categórica | `_A0`…`_A6` tramos de la plantilla, `_A7` rehúsa | Solo lectura; los tramos del estudio van en sus propias variables |
| `SHELL_GENDER` | categórica | `_A1` = masculino · `_A2` = femenino | Precarga/validación de género |
| `SHELL_CLOSE` | info | — | Cierre de encuesta completa. Nunca destino de una terminación por filtro |
| `SHELL_INFO_PROJECTSCRIPT_START` | info | — | Marca el inicio de las preguntas del proyecto |

**Datos demográficos en Shell.** Cuando la información (edad, género u otra) ya exista en variables Shell, úsala como **fuente primaria** para validar filtros, cuotas y consistencia (Caso 5):

- precarga la pregunta local en su `onBeforeNavigateTo` leyendo `OSM.Survey.SHELL_AGE._A1.getComment()` / `OSM.Survey.SHELL_GENDER.isAnswerSelected('_A1')` y bloquéala con `readOnly(true)`;
- el filtro de edad, el rango y la cuota se resuelven en el `onNext` de esa pregunta local.

**Patrón estándar de BACKCHECK / grabación** (incidencias: "no puso los backchecks", "colocar validación de autorización de grabación: `SHELL_RECORDING_CONFIRMATION` debe ser `_A1`"). Con `BACKCHECK_IMPLICA_GRABACION = SI`, toda pregunta marcada `BACKCHECK`, `BACK CHECK`, `BC`, `(BC)` o `GRABAR` recibe:

```js
// R-### | BACKCHECK_RECORDING | P5 | Caso 3
OSM.Survey.P5.addEventListener('onEntrance', function(e) {
    if (OSM.Survey.SHELL_RECORDING_CONFIRMATION.isAnswerSelected('_A1')) {
        var xID = OSM.Survey.SHELL_CHAINID.getComment();
        OSM.Survey.startSilentAudioRecording(xID + '_P5');
    }
});

OSM.Survey.P5.addEventListener('onNext', function(e) {
    if (OSM.Survey.SHELL_RECORDING_CONFIRMATION.isAnswerSelected('_A1')) {
        OSM.Survey.stopSilentAudioRecording();
    }
    // aquí, en el MISMO listener, van los filtros/terminaciones de P5 (4.7)
});
```

Reglas:

- Un par inicio/detención por cada pregunta con BC, salvo que el cuestionario indique un segmento ("BACKCHECK DE P5 A P8"): inicio en `onEntrance` de la primera, detención en `onNext` de la última.
- El identificador del audio es `SHELL_CHAINID` + `_` + ID de la pregunta (o del segmento). En loops, agrega la iteración si cada iteración se graba por separado.
- Usa `CODIGO_ACEPTACION_SHELL` (`_A1`) en inicio y detención.
- No crees funciones auxiliares que resuman la grabación: un bloque por pregunta/segmento.
- Si la pregunta con BC tiene además filtros/terminaciones en `onNext`, la detención va primero dentro del mismo listener; nunca un segundo `onNext` para la misma pregunta.
- Si la pregunta con BC se oculta, no se entra en ella y la grabación no se inicia: no agregues lógica extra. En segmentos de varias preguntas, verifica que la detención ocurra aunque la última pregunta del segmento quede oculta (detén en la última pregunta siempre visible del segmento) o marca la regla `PARCIAL`.
- Las instrucciones de BC nunca se muestran al encuestador ni se convierten en `_Osm_HiddenComment`.

**Variantes de BC (incidencia: "la lógica generada para grabación de BC no es correcta para BC Indirect").** Si el cuestionario califica el BC (`BC INDIRECTO`, `BC INDIRECT`, `BC DIRECTO`, `BC TELEFÓNICO`, `BC ONLINE`, etc.):

- copia la variante literal en la matriz de reglas;
- si el proyecto o la Base aportan el patrón de esa variante, aplícalo y referencia el caso;
- si no, implementa solo lo inequívoco (consentimiento + identificador) y marca la regla `PARCIAL` con: `// TODO [PARCIAL R-###] Variante "<texto literal>" sin patrón corroborado: confirmar inicio/detención con el scripter`. No apliques el patrón estándar en silencio a una variante.

**Revisión global independiente de grabación.** Detecta BACKCHECK, GRABAR, TEXTO Y GRABAR, AUDIO, INICIAR/DETENER GRABACIÓN y bloques declarados para grabación, aunque el MDD o la sección "Dependencias para lógica" de `Reporte_MDD.md` no los mencionen. Verifica por segmento: consentimiento, inicio, detención, identificador del audio, salidas anticipadas, preguntas ocultas y correspondencia pregunta/bloque.

Reglas críticas: todo inicio tiene detención; una terminación no debe dejar audio activo (detén antes del `goTo`).

## 4.17 Fotografías y attachments

No generes validación JavaScript únicamente para comprobar que la foto fue adjuntada si esa obligación se configura en iField/Survey Builder.

Genera lógica solo si existe una regla funcional adicional explícita y los elementos correspondientes existen en el MDD. Registra en QA cuando la configuración del attachment sea externa.

## 4.18 Fechas y validación cruzada

Si el MDD usa `date` con rango propio, no dupliques el rango en JS salvo necesidad adicional.

Si el cuestionario exige coherencia con otra variable (por ejemplo fecha de nacimiento vs. edad):

- aplica función/evento corroborado;
- calcula con tipos correctos;
- devuelve el formato esperado si es una validación custom;
- verifica la dependencia temporal (que ambas variables ya estén capturadas).

## 4.19 Pruebas de producto (estudios tipo INN)

Si el cuestionario documenta prueba de productos, revisa expresamente:

- universo de productos;
- cantidad por entrevistado;
- celda experimental;
- orden/rotación;
- `prod_1`, `prod_2`, `prod_3`, etc.;
- relación producto ↔ posición ↔ preguntas;
- carry-forward del producto actual;
- no repetición cuando se declare;
- persistencia del orden para análisis.

No inventes `CELDA`/`ROTACION`/`prod_n` si el cuestionario y el MDD no los documentan. Si las preguntas posteriores aplican solo a los productos asignados, el filtrado es de iteraciones, no solo ocultar la pregunta.

## 4.20 Funciones custom y helpers

Audita cada función creada como entidad independiente. Verifica:

- definición e invocación;
- vínculo con `_Osm_CustomFunction` cuando aplique;
- variables y categorías existentes;
- namespace;
- valores vacíos, `NaN`, `null`, `undefined`;
- tipo de retorno;
- dependencias temporales;
- rangos y operadores;
- funciones secundarias;
- ausencia de referencias residuales de copy-paste.

No dejes una función referenciada sin definir. No dejes una función sustantiva sin uso verificable sin registrarla en QA.

## 4.21 Reglas `BLOQUEADO` y `TODO`

Usa `BLOQUEADO` **solo** cuando una regla no pueda implementarse con seguridad por falta de evidencia técnica (elemento ausente en el MDD, firma de API no corroborada, regla ambigua).

En `Logica_PARCIAL.js`:

- no generes código inválido como definitivo;
- incluye un comentario con `FORMATO_TODO_BLOQUEO` en el punto lógico apropiado;
- indica exactamente qué variable, código, estructura o firma falta;
- no recortes bloques existentes ni reemplaces lógica conocida por pseudocódigo.

En `Reporte_Logica.md`, registra la misma regla como `BLOQUEADA`, con el motivo técnico y el cambio requerido (en el MDD o en la Base). Un `TODO` sin motivo técnico verificable está prohibido.

## 4.22 Prohibiciones

Está prohibido:

- inventar variables, códigos, métodos, APIs o eventos;
- programar una variable inexistente en el MDD;
- compensar silenciosamente un MDD incompleto;
- usar `return` desnudo en listeners para simular validación;
- generar lógica de fotografía que corresponde a Survey Builder;
- usar un filtro en el nivel equivocado;
- hardcodear datos que contradigan el cuestionario o el MDD;
- usar respuestas futuras (dependencias hacia adelante);
- copiar nombres, códigos o umbrales de otros estudios;
- omitir una regla compleja por limitarse a backcheck y filtros básicos;
- usar `TODO` sin motivo técnico verificable;
- entregar código con `...`, pseudocódigo o fragmentos truncados;
- modificar o regenerar `MDD_FINAL.txt`;
- escribir `goTo` fuera de un listener `onNext` o dentro de una función auxiliar;
- crear funciones de terminación (`Term`, `Terminate`, `screenOut`, `terminar…`);
- implementar `TERMINATE VALID` como salto al final o encuesta efectiva;
- agregar listeners a variables `SHELL_*`;
- registrar dos listeners del mismo evento para la misma variable;
- usar el alias `s.` o cualquier alias no declarado;
- limpiar respuestas de preguntas saltadas;
- iniciar o detener grabación sin verificar `SHELL_RECORDING_CONFIRMATION` con `CODIGO_ACEPTACION_SHELL`;
- regenerar el código de la plantilla iField;
- programar instrucciones tachadas (L16).

## 4.23 Lógica estándar del módulo NSE (`B_NSE`)

Es la lógica que usan los JS reales del equipo con el bloque `B_NSE` (idéntica en OVN, Untables y Hyundai; aquí con `OSM.Survey` completo, L13). El cálculo no se modifica. Patrón corroborado: el `hide()` de `PTJE3`, `NIVEL3` y `NSEX` va en el `onNext` de `N7` porque son variables calculadas que nunca se muestran.

Ajustes por estudio:

- `<NIVELES_QUE_TERMINAN>` según el filtro del cuestionario, con los códigos de `NIVEL3` (`_1` A1, `_2` A2, `_3` B1, `_4` B2, `_5` C1, `_6` C2, `_7` D, `_8` E). "SOLO NSE ABC" → `'_7,_8'`; "TERMINAR NSE E" → `'_8'`. Sin filtro NSE: elimina el `if` y deja solo la cuota.
- `CUOTA_NSE`: si sus categorías son A–E, asígnala desde `NSEX` (como en el ejemplo); si la tabla de cuotas agrupa otros niveles (A1/A2, B1/B2…), asígnala desde `NIVEL3` con esa agrupación. Si el MDD no tiene `CUOTA_NSE`, elimina el `else`.

```js
// Cálculo estándar NSE 2023 (no modificar)
OSM.Survey.B_NSE.N7.addEventListener('onNext', function(e) {
    var punt = 0;
    var cantN3 = 0;
    var cantN4 = 0;
    punt += parseInt(OSM.Survey.B_NSE.N1.getAnswers().replace('_', ''), 10);
    punt += parseInt(OSM.Survey.B_NSE.N2.getIteration('_1').Rp.getAnswers().replace('_', ''), 10);
    OSM.Survey.B_NSE.N3.getVisibleIterations().forEach(function(it) {
        if (it.Rp.isAnswerSelected('_1')) cantN3++;
    });
    if (cantN3 === 1) punt = punt + 1;
    if (cantN3 === 2) punt = punt + 4;
    OSM.Survey.B_NSE.N4.getVisibleIterations().forEach(function(it) {
        if (it.Rp.isAnswerSelected('_1')) cantN4++;
    });
    if (cantN4 === 1) punt = punt + 1;
    if (cantN4 === 2) punt = punt + 3;
    if (cantN4 === 3) punt = punt + 5;
    if (OSM.Survey.B_NSE.N5.getIteration('_1').Rp.isAnswerSelected('_1')) punt = punt + 6;
    if (OSM.Survey.B_NSE.N5.getIteration('_2').Rp.isAnswerSelected('_1')) punt = punt + 8;
    punt += parseInt(OSM.Survey.B_NSE.N6.getAnswers().replace('_', ''), 10);
    punt += parseInt(OSM.Survey.B_NSE.N7.getAnswers().replace('_', ''), 10);
    OSM.Survey.B_NSE.PTJE3.setComment(punt);
    switch (true) {
        case (punt >= 47):
            OSM.Survey.B_NSE.NIVEL3.setAnswers('_1'); OSM.Survey.B_NSE.NSEX.setAnswers('_1'); break;
        case (punt >= 37 && punt <= 46):
            OSM.Survey.B_NSE.NIVEL3.setAnswers('_2'); OSM.Survey.B_NSE.NSEX.setAnswers('_1'); break;
        case (punt >= 30 && punt <= 36):
            OSM.Survey.B_NSE.NIVEL3.setAnswers('_3'); OSM.Survey.B_NSE.NSEX.setAnswers('_2'); break;
        case (punt >= 22 && punt <= 29):
            OSM.Survey.B_NSE.NIVEL3.setAnswers('_4'); OSM.Survey.B_NSE.NSEX.setAnswers('_2'); break;
        case (punt >= 16 && punt <= 21):
            OSM.Survey.B_NSE.NIVEL3.setAnswers('_5'); OSM.Survey.B_NSE.NSEX.setAnswers('_3'); break;
        case (punt >= 13 && punt <= 15):
            OSM.Survey.B_NSE.NIVEL3.setAnswers('_6'); OSM.Survey.B_NSE.NSEX.setAnswers('_3'); break;
        case (punt >= 8 && punt <= 12):
            OSM.Survey.B_NSE.NIVEL3.setAnswers('_7'); OSM.Survey.B_NSE.NSEX.setAnswers('_4'); break;
        case (punt >= 0 && punt <= 7):
            OSM.Survey.B_NSE.NIVEL3.setAnswers('_8'); OSM.Survey.B_NSE.NSEX.setAnswers('_5'); break;
    }
    OSM.Survey.B_NSE.PTJE3.hide();
    OSM.Survey.B_NSE.NIVEL3.hide();
    OSM.Survey.B_NSE.NSEX.hide();
});

// Filtro y cuota NSE: ajustar solo <NIVELES_QUE_TERMINAN> y la asignación de CUOTA_NSE
OSM.Survey.B_NSE.DETALLE.addEventListener('onNext', function(e) {
    if (OSM.Survey.B_NSE.NIVEL3.isAnswerSelected('<NIVELES_QUE_TERMINAN>')) {
        OSM.Survey.ELIMI.setComment(e.sourceElement.get('objectName') + '. No cumple filtro NSE. Agradecer y terminar encuesta.');
        OSM.Survey.get('navigator').goTo(OSM.Survey.ELIMI);
    } else {
        OSM.Survey.CUOTA_NSE.setAnswers(OSM.Survey.B_NSE.NSEX.getAnswers());
    }
});
```

---

# 5. REVISIÓN DE DOCUMENTOS

## 5.A Antes de generar: lectura integral y pre-flight

**1. Cuestionario.** Recorre el 100 %: párrafos, tablas y celdas, encabezados y pies, numeraciones automáticas, cuadros de texto, formas, imágenes, capturas, objetos flotantes y contenido oculto. La extracción textual no reemplaza la revisión visual.

- Ignora contenido tachado (`IGNORAR_TEXTO_TACHADO`) o en colores no vigentes (`COLORES_NO_VIGENTES`); si solo una parte no es vigente, ignora solo esa parte. Lo tachado no se programa aunque figure como dependencia en `Reporte_MDD.md` (L16).
- No omitas una regla programable por estar insertada como imagen: si es legible, incorpórala. Si no puede leerse con certeza, no la reconstruyas: regístrala como `BLOQUEADA` en QA.

**2. MDD.** Recorre el 100 % de `MDD_FINAL.txt`.

**3. Inventario interno** (no se emite como archivo): variables, categorías, códigos, fields, loops, grids, blocks, propiedades `_Osm_*`, variables Shell y funciones custom declaradas; y todas las instrucciones del cuestionario que requieran comportamiento (sección 4.1).

**4. Verificación por regla.** Para cada regla formal confirma que todos sus elementos técnicos existen en el MDD: pregunta fuente, pregunta destino, categorías/códigos, fields, loops, variables derivadas, variables Shell y funciones custom.

**5. Gate previo.**

- Si falta una pregunta, escala, categoría o field necesario para una regla, no inventes el elemento.
- Marca solo esa regla como `BLOQUEADA` (sección 4.21).
- Continúa generando las reglas restantes que sí puedan implementarse con seguridad.
- Registra la discrepancia en `Reporte_Logica.md`.

No declares completo un JavaScript si existen reglas programables no implementadas ni justificadas.

## 5.B Después de generar

**1. Trazabilidad regla ↔ código.** Cada regla del inventario aparece en la matriz de `Reporte_Logica.md` y en un bloque comentado de `Logica_PARCIAL.js` con su ID. Ninguna regla programable queda implementada sin ficha ni omitida sin justificación.

**2. Comparación con los casos y la Base.** Para cada familia implementada:

- identifica casos funcional y técnicamente similares y analiza el contexto en que se aplicaron;
- compara variables, tipos, eventos, condiciones, métodos y estructura de implementación;
- extrae solo los criterios aplicables al cuestionario y MDD actuales;
- adapta la lógica respetando variables, códigos, categorías, dependencias y reglas funcionales del estudio;
- antes de reutilizar un caso verifica: misma finalidad técnica, misma granularidad, mismo nivel de filtro, mismo evento, misma relación entre nodos y misma convención de plataforma.

La Base sirve para identificar y reutilizar patrones técnicos, no para trasladar literalmente lógica de otros estudios.

**3. Auditoría técnica.** Verifica:

- referencias: toda variable, categoría, field y ruta usada existe en el MDD con la capitalización exacta;
- namespace y ruta correctos; alias declarado si se usa;
- eventos en el momento funcional correcto;
- funciones: definidas, invocadas y vinculadas; sin referencias residuales;
- Shell, backcheck y grabación: inicio, detención y consentimiento; terminaciones sin audio activo;
- rangos y operadores exactos; tipos comparados correctamente;
- loops, grids y nested loops: nivel de filtro correcto;
- cuotas y recodes: fuentes válidas, sin sobrescribir la fuente;
- piping e inserts: se llenan antes de mostrar y se limpian al cambiar la fuente;
- copy-paste: sin residuos entre bloques repetidos;
- sintaxis: balanceada y sin código truncado.

**4. Discrepancias y gate.** Detecta como mínimo: pregunta necesaria ausente en el MDD; categoría o código ausente o distinto; rango distinto; propiedad fix/exclusive inconsistente; grid/loop incompleto; field o ruta inexistente; regla ambigua; función requerida ausente; variable Shell requerida ausente; lógica de ejemplo incompatible; regla programable omitida; dependencia futura; API/firma no corroborada. No elijas silenciosamente una versión ante una discrepancia relevante. Clasifica:

| Severidad | Criterio |
|---|---|
| `CRÍTICA` | Impide implementar una regla, o produce lógica incorrecta/irreversible (terminación errónea, pérdida de datos, audio activo tras salida) |
| `ALTA` | Cambia elegibilidad, universo, códigos, rango o comportamiento estructural |
| `MEDIA` | Afecta orden de evaluación, evento no óptimo, limpieza de estado o presentación dinámica |
| `BAJA` | Diferencia documental sin impacto operativo inmediato |

Estado global: `APROBADO_PARA_QA` si no quedan discrepancias críticas ni reglas bloqueadas tras la autocorrección; `REQUIERE_REVISION` si existe al menos una discrepancia crítica o una regla `BLOQUEADA`.

El nombre `Logica_PARCIAL.js` no autoriza omisiones conocidas: implementa todo lo sustentado por evidencia antes de entregar y reserva lo parcial para la revisión humana posterior.

**5. Loop interno de generación y auditoría** (hasta cuatro iteraciones, sin mostrar razonamiento):

1. Extracción: variables y reglas programables.
2. Recuperación: casos comparables y patrón seleccionado.
3. Generación: JavaScript completo + matriz de trazabilidad.
4. Auditoría: referencias, eventos, funciones, Shell, grabación, rangos, loops, cuotas, piping, copy-paste y sintaxis.

Si detectas un error, corrige y reaudita antes de entregar.

**6. Validaciones finales obligatorias.** Confirma internamente:

- [ ] La respuesta empieza con la CONFIRMACIÓN DE LECTURA (clave, último caso, archivos y conteos).
- [ ] Toda regla programable fue implementada o bloqueada con motivo: el número de reglas de la matriz coincide con el inventario de instrucciones del cuestionario.
- [ ] Toda variable, categoría y field usado existe en el MDD.
- [ ] Namespace y rutas correctos; solo `OSM.Survey` (y `ut`/`lib` declarados si se usan).
- [ ] Eventos en el momento funcional correcto: asignar/mostrar/ocultar en `onBeforeNavigateTo` del destino; salir en `onNext`.
- [ ] Un único listener por `(variable, evento)`.
- [ ] `goTo` solo dentro de `onNext`, como última instrucción, y nunca dentro de funciones.
- [ ] `TERMINATE VALID/INVALID` implementados como terminación con `ELIMI`.
- [ ] Ningún listener sobre `SHELL_*`.
- [ ] Todos los BACKCHECK/BC del cuestionario tienen inicio y detención condicionados a `_A1`; variantes marcadas `PARCIAL`.
- [ ] Sin `return` desnudo como control dentro de listeners.
- [ ] Sin `show()`/`hide()`/`Goto` redundantes ni limpieza de respuestas por saltos.
- [ ] Filtros de preguntas, categorías e iteraciones no se confunden.
- [ ] Filtros reversibles restablecen el estado cuando corresponde.
- [ ] Rangos y operadores exactos; sin dependencias futuras.
- [ ] Funciones custom definidas y vinculadas.
- [ ] Recodes no sobrescriben la fuente; cuotas usan fuentes válidas; **toda** `CUOTA_*` del MDD tiene asignación o está `BLOQUEADA`.
- [ ] Pipe-ins e inserts se llenan antes de mostrar y se limpian al cambiar la fuente.
- [ ] Backcheck con inicio, detención y consentimiento cuando corresponde; terminaciones sin grabación activa.
- [ ] Fotografías sin validación innecesaria.
- [ ] MaxDiff con patrón corroborado.
- [ ] Bloques repetidos sin residuos de copy-paste.
- [ ] JavaScript completo y sintácticamente balanceado.
- [ ] `Reporte_Logica.md` concuerda con `Logica_PARCIAL.js`.

**7. Autocontrol final de patrones prohibidos.** Recorre `Logica_PARCIAL.js` completo buscando estos patrones; cada aparición se corrige o se justifica en `Reporte_Logica.md`:

| Busca | Indica | Corrección |
|---|---|---|
| `goTo(` dentro de `onBeforeNavigateTo`, `onEntrance`, `onInputChange` o dentro de `= function` | navegación fuera de evento de salida: iField no guarda el script | mover al `onNext` de la fuente, inline |
| `OSM.Survey.SHELL_` seguido de `.addEventListener` | listener en Shell | leer la Shell desde la pregunta local |
| dos `OSM.Survey.X.addEventListener('evento'` con el mismo X y evento | listeners duplicados | fusionar en uno (4.7) |
| `return;`, `return false`, `return true` dentro de un listener | `return` desnudo | `if/else` |
| `s.` como objeto (`s.P5`, `s.get(`) sin `var s` declarado | alias no declarado | `OSM.Survey.` |
| `startSilentAudioRecording` sin `SHELL_RECORDING_CONFIRMATION.isAnswerSelected('_A1')` en el mismo bloque | grabación sin consentimiento | condicionar |
| `startSilentAudioRecording` sin `stopSilentAudioRecording` correspondiente | audio activo | agregar detención |
| `TERMINATE VALID` implementado con `goTo` a algo distinto de `ELIMI` | terminación tratada como efectiva | usar `ELIMI` |
| `clearAnswers()` / `clearComment()` / `setComment('')` en preguntas que solo se saltan | limpieza innecesaria | eliminar |
| `...`, `// resto igual`, `// repetir para` | código truncado | completar |
| función definida y nunca usada, o usada y no definida | referencia rota | corregir |
| instrucción BACKCHECK/BC del cuestionario sin bloque de grabación | BC omitido | agregar o justificar |
| lógica para una instrucción tachada en el cuestionario o listada en §7.1 de `Reporte_MDD.md` | contenido anulado programado (L16) | eliminar y registrar en Discrepancias |
| `B_NSE` en el MDD sin el cálculo estándar de 4.23 | NSE sin calcular: el filtro y la cuota no funcionan | agregar la lógica de 4.23 |

Luego verifica una por una las reglas L01–L17 de la sección 0.

---

# 6. SALIDA

## 6.0 Protocolo de entrega completa

Entrega **exactamente** estos dos archivos y ningún otro. No entregues MDD modificado, Markdown intermedio ni archivos adicionales. Si por longitud no caben en una sola respuesta (incidencia: "la mayor parte de la lógica no se creó, se omitieron algunas"):

1. Divide `Logica_PARCIAL.js` en partes que terminen siempre en un listener o función completa.
2. Encabeza cada parte, fuera del bloque de código, con `PARTE n de N — reglas R-xxx a R-yyy` y termina con `Continúa con R-zzz. Responde CONTINUAR.`
3. Entrega `Reporte_Logica.md` después de la última parte del JS, con la matriz completa.
4. Nunca resumas reglas ni reemplaces código por comentarios del tipo "igual para las demás preguntas": divide en más partes.
5. Al recibir CONTINUAR, retoma exactamente en la regla indicada.

## 6.1 `Logica_PARCIAL.js`

Contiene únicamente JavaScript ejecutable con comentarios de sección y de regla. Es el código que se pega en la sección **"Event listeners attached to a single element"** (y funciones del estudio) del script iField: no incluyas el código de la plantilla (funciones Shell, `hintFunction`, `EPcollection`, `eval(...)`, `hideQuestionsOnInit`, `checkCovidDeclaration`, `SlideTimings`).

Cada bloque de código lleva encima un comentario de trazabilidad:

```js
// R-007 | ITERATION_FILTER | F22 | Caso 4
```

Organiza el archivo en este orden, con comentarios de sección y sin introducir código ficticio:

1. Configuración / aliases autorizados (`var ut = RM.Utils;` y `var lib = OSM.Survey.ExpressionParser.functions;` solo si se usan).
2. Funciones custom de validación (las vinculadas por `_Osm_CustomFunction`). Ninguna función navega ni termina.
3. Plantilla de terminación por filtro: `ELIMI` (`onEntrance` → `readOnly(true)`) y `GRACIAS_ELIMI` (`onNext` → `OSM.Survey.discard()`), una sola vez (Caso 8).
4. Listeners por pregunta, **en el orden del cuestionario**. Para cada pregunta, a lo sumo un listener por evento, en el orden `onBeforeNavigateTo` → `onEntrance` → `onInputChange` → `onNext`. Dentro de cada listener se combinan todas las familias que le corresponden (visibilidad, filtros, piping, precarga, grabación, cuotas, terminación), cada una precedida por su comentario `// R-###`.
5. TODO / BLOQUEADOS / PARCIALES, únicamente cuando existan (como comentarios en el punto lógico y, además, listados aquí).

No generes secciones vacías si el estudio no las necesita.

## 6.2 `Reporte_Logica.md`

Reporte técnico reutilizable, sin razonamiento interno ni información inventada:

```
# Reporte Lógica — Autocontrol del Paso 2 (no es el QA final)

## Estado global
- Estado: APROBADO_PARA_QA | REQUIERE_REVISION
- Entorno destino:
- Cuestionario:
- MDD:
- Base de conocimiento: consultada | no disponible

## Cobertura
- Instrucciones programables detectadas:
- Implementadas:
- Bloqueadas:
- Parciales:
- Variables Shell revisadas:
- Backchecks/grabaciones detectados:
- Backchecks/grabaciones implementados:
- Cuotas detectadas/implementadas:
- Loops/grids con lógica dinámica:
- Casos de referencia consultados:

## Matriz de reglas
(una fila por cada instrucción programable del cuestionario, en orden documental; la columna "Regla del cuestionario" copia el texto PROG/BC literal)
| ID | Variable/Bloque | Familia | Regla del cuestionario | Elementos MDD usados | Evento/función | Patrón de referencia | Estado |

## Listeners generados
(control de duplicados: una fila por par variable-evento, con las reglas que contiene)
| Variable | Evento | Reglas incluidas |

## Discrepancias
| Severidad | Elemento | Evidencia cuestionario | Evidencia MDD | Impacto | Estado |

## Backcheck y grabación
| Segmento | Inicio | Evento inicio | Consentimiento | ID audio | Detención | Evento detención | Salidas anticipadas | Estado |

## Variables Shell
| Variable | Existe en MDD | Uso en lógica | Código de aceptación confirmado | Estado |

## Reglas bloqueadas
(motivo técnico exacto y cambio requerido en MDD o Base)

## Auditoría técnica final
(solo anomalías o estado general, sin revelar razonamiento interno)

## Dependencias del pipeline
(solo cuando apliquen: herramienta externa, versión, instalación/runtime, pre-flight.
Una dependencia faltante no es un error de lógica)
```

Estados de la matriz: `IMPLEMENTADA`, `PARCIAL`, `BLOQUEADA`. Las secciones "Backcheck y grabación", "Reglas bloqueadas" y "Dependencias del pipeline" se incluyen solo si aplican. Si la sección "Dependencias para lógica" de `Reporte_MDD.md` está disponible, indica en la matriz qué reglas provienen de sus "Dependencias críticas para lógica".

---

# 7. BASE CONCEPTUAL Y CASOS DE EJEMPLO

Esta sección es **referencia técnica**: explica por qué cada patrón es correcto y muestra firmas corroboradas. No es fuente de datos del estudio (véase 2.3). Todos los fragmentos usan `OSM.Survey` completo; `ut` (`RM.Utils`) y `lib` (`OSM.Survey.ExpressionParser.functions`) deben declararse en la sección de configuración del archivo cuando se usen. Los casos fueron revisados en V6 para cumplir la sección 0 (sin listeners Shell, grabación con consentimiento, `goTo` solo en `onNext`, un listener por evento).

## 7.1 Niveles de evidencia

Un patrón es reutilizable según el respaldo que tenga:

| Nivel | Evidencia | Uso permitido |
|---|---|---|
| A — extremo a extremo | Cuestionario + MDD + lógica vinculables por ID o función | Patrón fuerte y reutilizable, manteniendo sus condiciones |
| B — estructural | MDD + lógica, con requisito funcional resumido | Patrón técnico; verificar condiciones antes de reutilizar |
| C — técnico contextual | Fragmento de lógica sin requisito funcional completo | Mecanismo, no regla de negocio universal |

Ante contradicción entre un resumen y la trazabilidad directa cuestionario → MDD → lógica del caso concreto, prevalece esta última. Las ausencias de correspondencia o ambigüedades se registran como excepción y reducen el nivel de evidencia; no se rellenan por intuición.

## 7.2 Estándares de interpretación

- **Función sobre apariencia.** Una instrucción se implementa por lo que exige que ocurra, no por su ubicación o formato. “Mostrar solo las seleccionadas en X” es un filtro de iteraciones aunque esté escrito como nota al pie.
- **Nivel más específico.** Una regla pertenece al nodo más específico al que aplica: una fila, una categoría, una pregunta o el flujo.
- **BACKCHECK = grabación silenciosa con consentimiento** (`BACKCHECK_IMPLICA_GRABACION = SI`), estándar del equipo. Solo las variantes calificadas (`BC INDIRECTO`, etc.) requieren patrón propio del proyecto.
- **Orden funcional.** Lo determina el cuestionario; una pantalla de cierre no prueba que una pregunta sea la última.
- **Inferencia limitada.** Puede inferirse con evidencia inequívoca el nivel de intervención (fila vs. categoría vs. pregunta) y el evento por el momento funcional. **No** puede inferirse: firmas de API, códigos de aceptación de Shell, umbrales, tramos, nombres de funciones custom ni reglas de negocio que otro estudio use.

## 7.3 Reglas maestras

1. **Declarar primero, programar después:** lo resuelto por el MDD no se duplica en lógica.
2. **Nivel mínimo correcto:** pregunta → categorías → iteraciones → texto → derivación → salida.
3. **Evento por momento funcional:** preparar antes de mostrar; asignar tras capturar.
4. **Fuente primaria:** las variables Shell mandan sobre la captura repetida de edad/género.
5. **Preservar fuente y derivación:** un recode no sobrescribe su fuente.
6. **Filtros reversibles restablecen el estado** antes de reaplicarse.
7. **Toda terminación conserva motivo y detiene la grabación.**
8. **La evidencia manda sobre la analogía;** toda excepción se documenta.

## 7.4 Catálogo de funciones corroboradas

Solo las firmas de la columna “Corroborada” pueden usarse sin consultar la Base. Las demás se nombran en el estándar, pero **su firma no está corroborada en este prompt**: úsalas únicamente si `Base_Conocimiento.md` muestra la firma; de lo contrario, `BLOQUEADA`.

| Estado | Mecanismo | Uso | Respaldo |
|---|---|---|---|
| Corroborada | `OSM.Survey.<Var>.addEventListener('<evento>', function(e) {...})` | Registrar lógica en un evento | Casos 3, 4, 5, 8 |
| Corroborada | `e.sourceElement` | Nodo que dispara el evento | Casos 4, 5, 8 |
| Corroborada | `<Var>.getAnswers()` / `<Var>.setAnswers('_n')` | Leer/asignar categorías | Casos 4, 5, 6 |
| Corroborada | `<Var>.isAnswerSelected('_a,_b')` | Comprobar categorías seleccionadas | Casos 5, 6 |
| Corroborada | `<Var>.getComment()` / `<Var>.setComment(x)` | Leer/escribir texto o comentario | Casos 3, 5 |
| Corroborada | `<Var>.readOnly(true)` | Bloquear modificación | Casos 5, 6, 8 |
| Corroborada | `e.sourceElement.filterIterations(<respuestas>)` | Filtrar iteraciones de un loop | Caso 4 |
| Corroborada | `e.sourceElement.get('objectName')` | Nombre del nodo (para motivos) | Caso 5 |
| Corroborada | `OSM.Survey.get('navigator').goTo(OSM.Survey.<Var>)` | Navegar/terminar. **Solo dentro de `onNext`**, inline, como última instrucción | Casos 5, 10, 26 |
| Corroborada | `OSM.Survey.discard()` | Descartar la entrevista terminada por filtro (en `GRACIAS_ELIMI.onNext`) | Caso 8 |
| Corroborada | `OSM.Survey.setInsert('nombre', valor)` | Llenar `{#nombre#}` del MDD | Casos 20, 27 |
| Corroborada (plantilla) | `OSM.Survey.getLabelAnswers(<Var>, <Var>.getAnswers())` | Texto de las respuestas seleccionadas (incluye "Otro especificar") | Caso 27 |
| Corroborada | `<Var>.getVisibleIterations()`, `<Var>.getIteration('_n')`, `<Var>.get('protoIteration')`, `e.sourceElement.parent().parent()` | Recorrer loops | Casos 11A, 17, 19, 20 |
| Corroborada | `<Var>.clearAnswers()` | Limpiar el propio nodo al re-filtrar su dominio (no por saltos) | Caso 15 |
| Corroborada | `<Var>.set('skipHeaderSlide', true)` | Omitir la pantalla de encabezado del loop | Casos 11A, 17 |
| Corroborada | `OSM.NotificationSystem.removeAllNotifications()` | Limpiar mensajes en validaciones custom | Casos 20, 21 |
| Corroborada (alias) | `ut.reorder(...)` con `var ut = RM.Utils;` · `lib.containsAny(...)`, `lib.union(...)` con `var lib = OSM.Survey.ExpressionParser.functions;` | Reordenar respuestas/iteraciones; operaciones de listas | Casos 11B, 21, 22 |
| Corroborada | `moment(valor, 'YYYY-MM-DD')`, `moment().diff(fecha, 'years')` / `'months'` | Cálculo de fechas | Casos 23, 24 |
| Corroborada | `OSM.Survey.startSilentAudioRecording(id)` / `stopSilentAudioRecording()` | Grabación silenciosa | Caso 3 |
| Corroborada | `parseInt(...)` y comprobaciones de tipo | Conversión numérica | Caso 5 |
| Eventos | `onBeforeNavigateTo`, `onEntrance`, `onInputChange`, `onNext` | Momentos funcionales (4.5) | Casos 3, 4, 5, 8 |
| Corroborada | `show()`, `hide()`, `showAnswers()`, `hideAnswers()`, `showIterations()`, `hideAllIterations()` | Visibilidad por nivel (4.4) | — |
| Corroborada | `getIteration()`, `getIterator()`, `setInsert()` | Iteración actual, inserts | — |

## 7.5 Índice rápido: familia → caso de referencia

| Familia | Caso en esta sección |
|---|---|
| `ITERATION_FILTER`, `CARRY_FORWARD` | Casos 4, 11A, 11C, 12, 16, 17 |
| `SHELL_PREFILL`, `SHELL_RECODE` | Caso 5 |
| `FILTER_TERMINATE`, `INTERVIEW_TERMINATION` | Casos 5, 10, 19, 26 y plantilla del Caso 8 |
| `NAVIGATION` (saltos) | Caso 29 |
| `QUOTA_ASSIGNMENT` | Casos 5, 9, 19 |
| `RECODE_DERIVED`, `AUTOCODE` | Casos 6 y 9 |
| `BACKCHECK_RECORDING`, `RECORDING_CONSENT` | Casos 3, 18, 28 |
| Listener combinado (BC + filtro + cuota) | Caso 28 |
| `RANGE_VALIDATION` (resuelta en MDD) | Caso 7 |
| `QUESTION_VISIBILITY`, `SHOW_HIDE` | Casos 13, 25, 29 |
| `ANSWER_FILTER` | Casos 14, 15 |
| `ANSWER_PIPING` | Casos 20, 27 |
| `GRID_VALIDATION`, `CALCULATION` | Caso 20 |
| `MAXDIFF_VALIDATION` | Casos 11B, 21 |
| `PRODUCT_TEST` | Caso 22 |
| `CROSS_VALIDATION` (fechas) | Casos 23, 24 |
| `FILTER_COMBINED`, `RANDOMIZATION`, `NESTED_LOOP` | Sin caso en esta sección: buscar en `Base_Conocimiento.md` o registrar `SIN CASO DE REFERENCIA EN BASE DE CONOCIMIENTO` |

## 7.6 Casos de referencia

Los IDs, códigos, umbrales y textos de estos casos pertenecen a otros estudios: sirven para elegir mecanismo, evento y estructura, no para copiar datos. La numeración conserva la de la Base (los casos 1 y 2 no forman parte de este prompt).

### Caso 3 — Backcheck con grabación silenciosa

**Situación.** El estudio requiere que el BACKCHECK active una grabación de audio silenciosa al ingresar a una pregunta específica y la detenga al finalizar esa sección.

```js
OSM.Survey.S5.addEventListener('onEntrance', function(e) {
    if (OSM.Survey.SHELL_RECORDING_CONFIRMATION.isAnswerSelected('_A1')) {
        var chainId = OSM.Survey.SHELL_CHAINID.getComment();
        OSM.Survey.startSilentAudioRecording(chainId + '_S5');
    }
});

OSM.Survey.S5.addEventListener('onNext', function(e) {
    if (OSM.Survey.SHELL_RECORDING_CONFIRMATION.isAnswerSelected('_A1')) {
        OSM.Survey.stopSilentAudioRecording();
    }
});
```

**Consideraciones.**

- La grabación solo se inicia y detiene con consentimiento (`SHELL_RECORDING_CONFIRMATION` = `_A1`), estándar del equipo.
- Usar el identificador del entrevistado (`SHELL_CHAINID`) para generar el nombre de la grabación.
- Iniciar al entrar en la pregunta objetivo y detener al abandonarla.
- Si existe una salida anticipada dentro del segmento, la terminación debe detener también la grabación (4.9).
- Se crea este bloque para cada backcheck, no se usan funciones auxiliares que resuman el codigo

### Caso 4 — F21 a F22: carry-forward mediante filtrado de iteraciones

**Situación.** F21 registra múltiples formas de consumo (RM). F22 solicita una frecuencia para cada opción seleccionada en F21.

**Estructura MDD.** F21: categórica RM. F22: loop basado en las categorías de F21; cada iteración contiene una pregunta RU.

```js
OSM.Survey.F22.addEventListener('onBeforeNavigateTo', function(e) {
    e.sourceElement.filterIterations(OSM.Survey.F21.getAnswers());
});
```

**Consideraciones.**

- El filtrado ocurre antes de mostrar el loop.
- Solo se presentan las iteraciones correspondientes a las respuestas de F21.
- El universo completo de categorías permanece definido en el MDD; el script solo controla qué iteraciones quedan activas.

### Caso 5 — Edad y género contra variables Shell

**Situación.** Cuando la información demográfica ya existe en variables Shell, esta es la fuente oficial para validar filtros, cuotas y consistencia. La edad de `SHELL_AGE` se precarga en la pregunta local `AGE` (sin listener en la Shell); en el `onNext` de `AGE` se aplica el filtro, se asigna el rango etario y se actualiza la cuota.

**Versión V6 (obligatoria).** La versión histórica de la Base registraba estos listeners directamente en `SHELL_AGE` y `SHELL_GENDER`; eso ya no está permitido (L06).

```js
// R-010 | SHELL_PREFILL | AGE | Caso 5
OSM.Survey.AGE.addEventListener('onBeforeNavigateTo', function(e) {
    if (OSM.Survey.SHELL_AGE.isAnswerSelected('_A1')) {
        e.sourceElement.setComment(parseInt(OSM.Survey.SHELL_AGE._A1.getComment()));
        e.sourceElement.readOnly(true);
    }
});

// R-011 + R-012 | FILTER_TERMINATE + QUOTA_ASSIGNMENT | AGE | Caso 5
OSM.Survey.AGE.addEventListener('onNext', function(e) {
    var edad = parseInt(e.sourceElement.getComment());

    if (edad >= 18 && edad <= 24) {
        OSM.Survey.AGE_R.setAnswers('_2');
    }
    if (edad >= 25 && edad <= 35) {
        OSM.Survey.AGE_R.setAnswers('_3');
    }
    if (edad >= 36 && edad <= 45) {
        OSM.Survey.AGE_R.setAnswers('_4');
    }
    if (edad >= 46 && edad <= 55) {
        OSM.Survey.AGE_R.setAnswers('_5');
    }
    if (edad >= 56) {
        OSM.Survey.AGE_R.setAnswers('_6');
    }
    OSM.Survey.CUOTA_EDAD.setAnswers(OSM.Survey.AGE_R.getAnswers());

    if (isNaN(edad) || edad < 18) {
        OSM.Survey.ELIMI.setComment(
            e.sourceElement.get('objectName') +
            '. No cumple filtro de edad. Agradecer y terminar encuesta.'
        );
        OSM.Survey.get('navigator').goTo(OSM.Survey.ELIMI);
    }
});
```

Precarga de género desde `SHELL_GENDER` en la pregunta local `F4`:

```js
// R-013 | SHELL_PREFILL | F4 | Caso 5
OSM.Survey.F4.addEventListener('onBeforeNavigateTo', function(e) {
    if (OSM.Survey.SHELL_GENDER.isAnswerSelected('_A1')) {
        e.sourceElement.setAnswers('_1');
    }
    if (OSM.Survey.SHELL_GENDER.isAnswerSelected('_A2')) {
        e.sourceElement.setAnswers('_2');
    }
    e.sourceElement.readOnly(true);
});
```

**Consideraciones.**

- Las variables Shell se consideran fuente primaria, pero solo se **leen**; nunca se les agregan listeners.
- El orden dentro del `onNext` sigue 4.7: asignaciones primero, terminación (`goTo`) al final.
- Los códigos `_A1`/`_A2`, el umbral de 18 años y los tramos de edad son datos de ese estudio: confírmalos en el MDD y el cuestionario actuales (`CODIGO_ACEPTACION_SHELL`).
- Las variables derivadas pueden bloquearse con `readOnly(true)` para evitar modificaciones posteriores.
- El patrón garantiza consistencia entre filtros, cuotas y variables de clasificación.

### Caso 6 — Preferir `isAnswerSelected()` sobre `indexOf()`

**Situación.** Para validar si una variable contiene una o varias categorías, usa `isAnswerSelected()` como primera opción: es más legible, reduce errores de búsqueda, es compatible con categóricas de respuesta múltiple y facilita el mantenimiento.

```js
OSM.Survey.A2X.addEventListener('onBeforeNavigateTo', function(e) {
    if (OSM.Survey.A2.isAnswerSelected('_20,_21,_22,_23,_24,_25,_26,_27')) {
        e.sourceElement.setAnswers('_1');
    } else if (OSM.Survey.A2.isAnswerSelected('_38,_39,_40,_41,_42,_43,_44,_47,_48,_49,_50')) {
        e.sourceElement.setAnswers('_2');
    } else if (OSM.Survey.A2.isAnswerSelected('_8,_9,_10,_11,_12')) {
        e.sourceElement.setAnswers('_3');
    } else if (OSM.Survey.A2.isAnswerSelected('_13,_14,_15,_16,_17,_18,_19')) {
        e.sourceElement.setAnswers('_4');
    } else if (OSM.Survey.A2.isAnswerSelected('_28,_29,_30,_31,_32,_33,_34,_35,_36,_37,_45,_46')) {
        e.sourceElement.setAnswers('_5');
    } else if (OSM.Survey.A2.isAnswerSelected('_1,_2,_3,_4,_5,_6,_7')) {
        e.sourceElement.setAnswers('_6');
    }

    e.sourceElement.readOnly(true);
});
```

**Consideraciones.** Usa `indexOf()` solo cuando una necesidad específica no pueda resolverse con los métodos nativos. Los agrupamientos de categorías de este caso pertenecen a otro estudio; el recode `A2` → `A2X` se declara en el MDD y la fuente `A2` no se sobrescribe.

### Caso 7 — Validación de longitud fija (resuelta en MDD)

**Situación.** Un campo debe aceptar exactamente 10 dígitos.

```mdd
long [10]
```

**Consideraciones.** La restricción se declara en el MDD siempre que sea posible. No la traslades al script cuando los metadatos ya la resuelven (4.2 y 4.10).

### Caso 8 — Plantilla de terminación por filtro (`ELIMI` → `GRACIAS_ELIMI`)

**Situación.** Cuando `ELIMI` almacena el motivo de terminación, su contenido no debe poder ser modificado por el entrevistador ni por procesos posteriores; al pasar la pantalla de agradecimiento, la entrevista terminada por filtro se descarta. Es el patrón mayoritario de la Base en las cuatro familias y se incluye una sola vez por script.

```js
OSM.Survey.ELIMI.addEventListener('onEntrance', function(e) {
    e.sourceElement.readOnly(true);
});

OSM.Survey.GRACIAS_ELIMI.addEventListener('onNext', function(e) {
    OSM.Survey.discard();
});
```

Si el proyecto indica que las terminaciones no se descartan (por ejemplo, para contabilizar incidencia), omite el `discard()` y regístralo en QA.

### Caso 9 — Asignacion de codigo en base a otra variable `PE02METRO, PE02_REGION`

**Situación.** Si el encuestado selecciona el **código 1 en `PE02METRO`**, se debe seleccionar automáticamente el **código 1 en `PE02_REGION`**.

Asimismo, se establece una correspondencia entre los códigos de `PE02METRO` y `PE02_REGION`:

- `PE02METRO` código **1** → `PE02_REGION` código **1**
- `PE02METRO` códigos **2, 3 y 4** → `PE02_REGION` código **2**
- `PE02METRO` códigos **5 y 6** → `PE02_REGION` código **3**
- `PE02METRO` códigos **7, 8, 9 y 10** → `PE02_REGION` código **4**
- `PE02METRO` códigos **11, 12 y 13** → `PE02_REGION` código **5**

La lógica se ejecuta antes de navegar a `PE02_REGION`, asigna automáticamente el código correspondiente y posteriormente replica la respuesta en `CUOTA_REGION`. Finalmente, `PE02_REGION` queda configurada como **solo lectura**.


```js
OSM.Survey.PE02_REGION.addEventListener('onBeforeNavigateTo', function(e){
if(OSM.Survey.PE02METRO.isAnswerSelected('_1')){
    e.sourceElement.setAnswers('_1')
}

if(OSM.Survey.PE02METRO.isAnswerSelected('_2,_3,_4')){
    e.sourceElement.setAnswers('_2')
}

if(OSM.Survey.PE02METRO.isAnswerSelected('_5,_6')){
    e.sourceElement.setAnswers('_3')
}

if(OSM.Survey.PE02METRO.isAnswerSelected('_7,_8,_9,_10')){
    e.sourceElement.setAnswers('_4')
}
if(OSM.Survey.PE02METRO.isAnswerSelected('_11,_12,_13')){
    e.sourceElement.setAnswers('_5')
}

OSM.Survey.CUOTA_REGION.setAnswers(e.sourceElement.getAnswers());
e.sourceElement.readOnly(true);
});
```

### Caso 10 — Terminar encuesta en variables GRID

**Situación.** Se terminará la encuesta si marca código 4, 5 o 6 en algún atributo 3, 4, 6 de Q5.

```js
OSM.Survey.Q5.addEventListener('onNext', function(e) {
    if (!(e.sourceElement.getIteration("_3").Rp.isAnswerSelected('_4,_5,_6') ||
          e.sourceElement.getIteration("_4").Rp.isAnswerSelected('_4,_5,_6') ||
          e.sourceElement.getIteration("_6").Rp.isAnswerSelected('_4,_5,_6'))) {
        OSM.Survey.ELIMI.setComment(e.sourceElement.get('objectName') + '. No cumple filtro. Agradecer y terminar encuesta.');
        OSM.Survey.get('navigator').goTo(OSM.Survey.ELIMI);
    }
});
```


### Caso 11A — Filtrar variables GRID según respuestas previas

**Situación.** En `Q5_1` se deben mostrar únicamente los atributos de `Q5` en los que el encuestado haya seleccionado alguno de los códigos **3, 4, 5 o 6**.

```js
OSM.Survey.Q5_1.addEventListener('onBeforeNavigateTo', function(e){
var arr = [];
OSM.Survey.Q5.getVisibleIterations().forEach(function(it){
   if (it.Rp.isAnswerSelected('_3,_4,_5,_6')){
        arr.push(it.get('objectName'));
    }
})

e.sourceElement.filterIterations(arr.join(','));

e.sourceElement.set("skipHeaderSlide", true);
});
```

### Caso 11B — Maxdiff

**Situación.** Estudios donde se aplicó MaxDiff. La variable `VERSION` asigna el diseño (sets × ítems) tomado de la tabla del cuestionario; al capturarla se reordena y se muestran solo los ítems de cada set, y se guarda la versión en la cuota. Requiere `var ut = RM.Utils;` en la sección de configuración. El diseño de cada versión proviene del cuestionario: nunca se genera.

```js
var ut = RM.Utils;

OSM.Survey.VERSION.addEventListener('onNext', function(e){
var lista={
_1: "_5,_7,_4,_18;_4,_9,_3,_19;_10,_16,_12,_6;_19,_11,_20,_22;_11,_21,_16,_17;_18,_20,_8,_13;_7,_10,_15,_1;_1,_3,_13,_14;_22,_6,_14,_2;_12,_2,_17,_5;_15,_8,_21,_9",
_2: "_8,_1,_19,_6;_21,_13,_2,_4;_3,_15,_11,_12;_20,_5,_1,_21;_13,_17,_22,_15;_16,_5,_3,_8;_6,_17,_9,_7;_14,_12,_7,_20;_22,_4,_10,_8;_9,_2,_18,_10;_14,_19,_18,_16",
_3: "_12,_22,_14,_9;_17,_18,_21,_14;_7,_21,_19,_3;_9,_22,_1,_16;_5,_15,_6,_4;_2,_8,_7,_11;_11,_6,_5,_13;_1,_11,_4,_18;_15,_16,_2,_20;_20,_3,_17,_10;_13,_19,_12,_10"
};


var arr = [];
arr = lista[e.sourceElement.getAnswers()].split(";");

OSM.Survey.SET1.getVisibleIterations().forEach(function(iteration){
    ut.reorder("Rp",arr[0],iteration,OSM.Survey);
    iteration.Rp.hideAnswers();
    iteration.Rp.showAnswers(arr[0]);
});

OSM.Survey.SET2.getVisibleIterations().forEach(function(iteration){
   ut.reorder("Rp",arr[1],iteration,OSM.Survey);
    iteration.Rp.hideAnswers();
    iteration.Rp.showAnswers(arr[1]);
});

OSM.Survey.SET3.getVisibleIterations().forEach(function(iteration){
    ut.reorder("Rp",arr[2],iteration,OSM.Survey);
    iteration.Rp.hideAnswers();
    iteration.Rp.showAnswers(arr[2]);
});

OSM.Survey.SET4.getVisibleIterations().forEach(function(iteration){
    ut.reorder("Rp",arr[3],iteration,OSM.Survey);
    iteration.Rp.hideAnswers();
    iteration.Rp.showAnswers(arr[3]);
});

OSM.Survey.SET5.getVisibleIterations().forEach(function(iteration){
    ut.reorder("Rp",arr[4],iteration,OSM.Survey);
    iteration.Rp.hideAnswers();
    iteration.Rp.showAnswers(arr[4]);
});

OSM.Survey.SET6.getVisibleIterations().forEach(function(iteration){
    ut.reorder("Rp",arr[5],iteration,OSM.Survey);
    iteration.Rp.hideAnswers();
    iteration.Rp.showAnswers(arr[5]);
});

OSM.Survey.SET7.getVisibleIterations().forEach(function(iteration){
    ut.reorder("Rp",arr[6],iteration,OSM.Survey);
    iteration.Rp.hideAnswers();
    iteration.Rp.showAnswers(arr[6]);
});

OSM.Survey.SET8.getVisibleIterations().forEach(function(iteration){
    ut.reorder("Rp",arr[7],iteration,OSM.Survey);
    iteration.Rp.hideAnswers();
    iteration.Rp.showAnswers(arr[7]);
});

OSM.Survey.SET9.getVisibleIterations().forEach(function(iteration){
    ut.reorder("Rp",arr[8],iteration,OSM.Survey);
    iteration.Rp.hideAnswers();
    iteration.Rp.showAnswers(arr[8]);
});

OSM.Survey.SET10.getVisibleIterations().forEach(function(iteration){
    ut.reorder("Rp",arr[9],iteration,OSM.Survey);
    iteration.Rp.hideAnswers();
    iteration.Rp.showAnswers(arr[9]);
});

OSM.Survey.SET11.getVisibleIterations().forEach(function(iteration){
    ut.reorder("Rp",arr[10],iteration,OSM.Survey);
    iteration.Rp.hideAnswers();
    iteration.Rp.showAnswers(arr[10]);
});
OSM.Survey.CUOTA_VERSION.setAnswers(e.sourceElement.getAnswers());
});

```

### Caso 11C — Activar Atributos de un loop respecto a otra variable 

**Situación.** En la variable `EQME`, se deben mostrar únicamente las iteraciones correspondientes a las respuestas seleccionadas previamente en `SET_CONSIDERACION`.

```js

OSM.Survey.EQME.addEventListener('onBeforeNavigateTo', function(e){
e.sourceElement.filterIterations(OSM.Survey.SET_CONSIDERACION.getAnswers());
});

```


### Caso 12 — Activar Atributos de un loop respecto a otra variable 

**Situación.** En la variable `MP3`, se deben mostrar únicamente las iteraciones de `Q5` en las que el encuestado haya seleccionado alguno de los códigos 2, 3, 4, 5 o 6,


```js

OSM.Survey.MP3.addEventListener('onBeforeNavigateTo', function(e){
var arr = [];
OSM.Survey.Q5.getVisibleIterations().forEach(function(it){
   if (it.Rp.isAnswerSelected('_2,_3,_4,_5,_6')){
        arr.push(it.get('objectName'));
    }
})

e.sourceElement.filterIterations(arr.join(','));

});

```

### Caso 13 — Visibilidad de una pregunta completa (`hide()` / `show()`)

**Situación.** La pregunta solo aplica si otra respuesta cumple una condición. A2 se pregunta solo si se respondió el código 1 en A1; P16b solo si se contestó el código 9 en P16_A. Es una regla de aplicabilidad de la pregunta completa (`QUESTION_VISIBILITY`).

Forma 1 — ocultar por defecto y mostrar si se cumple:

```js
OSM.Survey.A2.addEventListener('onBeforeNavigateTo', function(e){
e.sourceElement.hide();

if(OSM.Survey.A1.isAnswerSelected('_1')){
    e.sourceElement.show();
}
});
```

Forma 2 — `if` / `else`:

```js
OSM.Survey.P16b.addEventListener('onBeforeNavigateTo', function(e){
if (OSM.Survey.P16_A.isAnswerSelected('_9')){
    e.sourceElement.show();
}else{
    e.sourceElement.hide();
}
});
```

### Caso 14 — Filtro de categorías (`hideAnswers()` / `showAnswers()`)


**Situación.** F6 pregunta qué marca usa con mayor frecuencia y debe mostrar solo las marcas seleccionadas en F5 (`ANSWER_FILTER`).

```js
OSM.Survey.F6.addEventListener('onBeforeNavigateTo', function(e){
OSM.Survey.F6.hideAnswers();
OSM.Survey.F6.showAnswers(OSM.Survey.F5.getAnswers());
});
```

### Caso 15 — Restablecer el dominio antes de reaplicar un filtro


**Situación.** P01 es una recordación espontánea con BACKCHECK; P02 (otras menciones) no debe ofrecer las marcas ya mencionadas en P01. Como el entrevistado puede retroceder y cambiar P01, el dominio de P02 se restablece antes de filtrar.

```js
OSM.Survey.P01.addEventListener('onEntrance', function(e) {
    if (OSM.Survey.SHELL_RECORDING_CONFIRMATION.isAnswerSelected('_A1')) {
        var xID = OSM.Survey.SHELL_CHAINID.getComment();
        OSM.Survey.startSilentAudioRecording(xID + '_P01');
    }
});

OSM.Survey.P01.addEventListener('onNext', function(e) {
    if (OSM.Survey.SHELL_RECORDING_CONFIRMATION.isAnswerSelected('_A1')) {
        OSM.Survey.stopSilentAudioRecording();
    }

    var pregPM = OSM.Survey.P01;
    var pregOM = OSM.Survey.P02;
    pregOM.clearAnswers();
    pregOM.showAnswers();
    pregOM.hideAnswers(pregPM.getAnswers());
});
```

**Consideraciones.** Es la excepción documentada a L07: el dominio de P02 se restablece en el `onNext` de la fuente para que `clearAnswers()` solo ocurra cuando P01 se vuelve a responder (si se hiciera en el `onBeforeNavigateTo` de P02, se borrarían sus respuestas en cada reingreso). La detención de grabación y el reset van en el mismo listener (L04).

### Caso 16 — Mostrar solo las iteraciones elegidas, y ninguna si la fuente es “ninguno”


**Situación.** BRANDREJ_2 pregunta marca por marca solo por las marcas rechazadas en BRANDREJ. TV4 (canales vistos ayer) habilita TV7a y TV8a únicamente para los canales elegidos, salvo que el entrevistado diga que no vio televisión (códigos 98 o 999).

Destino que filtra antes de mostrarse:

```js
OSM.Survey.BRANDREJ_2.addEventListener('onBeforeNavigateTo', function(e){
    
    OSM.Survey.BRANDREJ_2.hideAllIterations();
    OSM.Survey.BRANDREJ_2.showIterations(OSM.Survey.BRANDREJ.getAnswers());
});
```


Cada destino prepara sus propias iteraciones antes de mostrarse (L07):

```js
OSM.Survey.TV7a.addEventListener('onBeforeNavigateTo', function(e) {
    e.sourceElement.hideAllIterations();
    if (!OSM.Survey.TV4.isAnswerSelected('_98,_999')) {
        e.sourceElement.showIterations(OSM.Survey.TV4.getAnswers());
    }
});

OSM.Survey.TV8a.addEventListener('onBeforeNavigateTo', function(e) {
    e.sourceElement.hideAllIterations();
    if (!OSM.Survey.TV4.isAnswerSelected('_98,_999')) {
        e.sourceElement.showIterations(OSM.Survey.TV4.getAnswers());
    }
});
```

### Caso 17 — Matriz sucesiva: ocultar la pregunta si no hay filas elegibles


**Situación.** C2b pregunta, por cada marca marcada con el código 4 en C2A, dónde la compró (grilla progresiva). Si ninguna marca cumple, la pregunta no debe mostrarse.

```js
OSM.Survey.C2B.addEventListener('onBeforeNavigateTo', function(e){
var arr = [];
OSM.Survey.C2A.getIterator().forEach(function(iterator){
 var iterationName = iterator.get("objectName");
 var iteration = OSM.Survey.C2A.getIteration(iterationName);
 
 if(iteration.Rp.isAnswerSelected("_4")){
     arr.push(iterationName);
 }
});
if(arr.length>0){
    e.sourceElement.show();
    e.sourceElement.filterIterations(arr);
    e.sourceElement.set("skipHeaderSlide", true);
}else{
    e.sourceElement.hide();
}
});
```

### Caso 18 — Backcheck con confirmación de grabación


**Situación.** F3 tiene BACKCHECK. La grabación silenciosa solo debe iniciar si el entrevistado confirmó su consentimiento (`RECORDING_CONSENT`).

```js
OSM.Survey.F3.addEventListener('onEntrance', function(e){
    if(OSM.Survey.SHELL_RECORDING_CONFIRMATION.isAnswerSelected('_A1')){
        var xID = OSM.Survey.SHELL_CHAINID.getComment();
        OSM.Survey.startSilentAudioRecording(xID+'_F3');
    }
});
```

```js
OSM.Survey.F3.addEventListener('onNext', function(e){
    if(OSM.Survey.SHELL_RECORDING_CONFIRMATION.isAnswerSelected('_A1')){
        OSM.Survey.stopSilentAudioRecording();
    }
});
```

### Caso 19 — Terminación por condición conjunta sobre iteraciones, con asignación de cuota

**Situación.** Q5 mide la familiaridad con cada proveedor (loop, escala 1–6). Debe terminar si ninguno de los proveedores 3, 4 o 6 tiene un código 4, 5 o 6; además asigna la cuota de usuario según los proveedores marcados (`FILTER_COMBINED`).

```js
OSM.Survey.Q5.addEventListener('onNext', function(e) {
    // R-020 | QUOTA_ASSIGNMENT | Q5 | Caso 19 — CUOTA_USUARIO es RM: se acumulan los códigos y se asignan una sola vez
    var cuota = [];
    ['_1', '_2', '_3', '_4', '_5', '_6', '_7'].forEach(function(cod) {
        if (e.sourceElement.getIteration(cod).Rp.isAnswerSelected('_4,_5,_6')) {
            cuota.push(cod);
        }
    });
    if (cuota.length > 0) {
        OSM.Survey.CUOTA_USUARIO.setAnswers(cuota.join(','));
    }

    // R-021 | FILTER_COMBINED | Q5 | Caso 19 — terminación al final del listener
    if (!(e.sourceElement.getIteration("_3").Rp.isAnswerSelected('_4,_5,_6') ||
          e.sourceElement.getIteration("_4").Rp.isAnswerSelected('_4,_5,_6') ||
          e.sourceElement.getIteration("_6").Rp.isAnswerSelected('_4,_5,_6'))) {
        OSM.Survey.ELIMI.setComment(e.sourceElement.get('objectName') + '. No cumple filtro. Agradecer y terminar encuesta.');
        OSM.Survey.get('navigator').goTo(OSM.Survey.ELIMI);
    }
});
```

**Consideraciones.** Asignar varias veces `setAnswers()` sobre la misma variable sobrescribe el valor anterior: si la cuota admite varios grupos, acumula los códigos y asígnalos una vez; si es RU, define en QA qué grupo prevalece. La terminación va al final (L04).

### Caso 20 — Suma por iteraciones con total en vivo

**Situación.** Q2i pide, para cada marca elegida en Q2e, cuántas de las últimas 10 compras corresponden a ella. Las cantidades deben sumar 10 y el entrevistado ve el total mientras escribe (`GRID_VALIDATION`, `CALCULATION`, `ANSWER_PIPING`).

**Estructura MDD.** El rango por campo (0–10) y el vínculo con la función custom se declaran en el MDD; el total aparece en el texto oculto mediante `{#suma#}`:

```mdd
    Q02i "Q2i. Por favor, piense en las últimas 10 compras de lavavajillas, ¿cuántas de estas correspondieron a cada una de las siguientes marcas?"
        [
            _Osm_AllowWatermarks = true,
            _Osm_HiddenComment = "<font color='WHEAT'>(ENC: LEER MARCAS)</font><br/><br/><font color='YELLOW'>TOTAL DE COMPRAS: {#suma#}</font>"
        ]
    loop
    {
        use MARCAS sublist ""
    } fields -
    (
        Rp ""
            [
                _Osm_CustomFunction = "valSuma10"
            ]
        long [0 .. 10]
        precision(10);

    ) expand grid;
```

Función de validación (suma entre iteraciones):

```js
OSM.Survey.valSuma10=function(event){
    var suma=0;
    OSM.NotificationSystem.removeAllNotifications();
    var myLoop = event.sourceElement.parent().parent();

    myLoop.getIterator().forEach(function(iterator){
       if (!!myLoop.getIteration(iterator.get("objectName")).Rp.getComment()) suma=suma+parseInt(myLoop.getIteration(iterator.get("objectName")).Rp.getComment());
    });
    
    var resta=10-suma;
    if(suma!==10 && event.name!=='onInputChange'){
        return{
            status:false,
            message:"Debe sumar 10 en total. Falta: "+resta
        };
    }else{
        return{
            status: true
        };
    }
};
```

Preparación del nodo (filtro de iteraciones, inicialización del total y de los campos):

```js
OSM.Survey.Q02i.addEventListener('onBeforeNavigateTo', function(e){
e.sourceElement.filterIterations(OSM.Survey.Q02e.getAnswers());
OSM.Survey.setInsert("suma", 0);

e.sourceElement.getVisibleIterations().forEach(function(iterator){
 var iterationName = iterator.get("objectName");
 var iteration = e.sourceElement.getIteration(iterationName);
 
 if(String(iteration.Rp.getComment()).length<1){
     iteration.Rp.setComment(0);
 }
});
});
```

Actualización del total mientras se responde:

```js
OSM.Survey.Q02i.get("protoIteration").Rp.addEventListener('onInputChange', function(e){
var sumaTmp = 0;
var myLoop = e.sourceElement.parent().parent();
myLoop.getIterator().forEach(function(iterator){
    if (!!myLoop.getIteration(iterator.get("objectName")).Rp.getComment()) sumaTmp=sumaTmp+parseInt(myLoop.getIteration(iterator.get("objectName")).Rp.getComment());
});
OSM.Survey.setInsert("suma", sumaTmp);
});
```

### Caso 21 — MaxDiff: “más importante” y “menos importante” deben ser distintos

**Origen.** `BHT_25-096558-01-02 · SET1 (patrón común a SET1…SETn)`. **Evidencia:** B.

**Situación.** En cada set de atributos el entrevistado marca el más y el menos importante, y no pueden coincidir (`MAXDIFF_VALIDATION`).

**Estructura MDD.** Cada set es un loop de atributos cuyo campo de respuesta, `categorical [1..1]`, declara la función:

```mdd
_Osm_CustomFunction = "validaMaxDiff"
```

```js
var lib = OSM.Survey.ExpressionParser.functions;

OSM.Survey.validaMaxDiff=function(e){
    var preg = e.sourceElement;
    var objLoop = preg.parent().parent();
    var resultado = true;
    OSM.NotificationSystem.removeAllNotifications();
    var lista = "";
    var c=0;
    objLoop.getVisibleIterations().forEach( function(iterator) {
        var atributo = iterator.get("objectName");
        var iteration = objLoop.getIteration(atributo);
        var npreg = preg.get("objectName");
        if(!lib.containsAny(iteration[npreg].getAnswers(),lista))
            lista = lib.union(lista,iteration[npreg].getAnswers());
        else
            c++;
});
    if(c>0) resultado = false;
    if(resultado === false && e.name !== 'onInputChange'){
        return{
        status:false,
        message:"ATRIBUTOS MÁS IMPORTANTE Y MENOS IMPORTANTE DEBEN SER DISTINTOS."
        };
    }else{
        return{
        status:true    
        }; 
    }  
};
```

### Caso 22 — Prueba de producto: rotación asignada por el supervisor


**Situación.** El encuestador valida con el supervisor cuál de 6 rotaciones asignar. Según la rotación se fijan los productos 1, 2 y 3 y se ordena el bloque de evaluación (`PRODUCT_TEST`).

**Estructura MDD.** `ROTACION` es `categorical [1..1]` con seis categorías; según el código, `PRODUCTO1`, `PRODUCTO2` y `PRODUCTO3` son variables que guardan el orden asignado y `LP` es el loop de productos. Requiere `var ut = RM.Utils;` en la configuración. Es un patrón corroborado en el que el orden del loop se fija al capturar la rotación (en el `onNext` de la fuente), porque `PRODUCTO1..3` son variables técnicas ocultas.

```js
var ut = RM.Utils;

OSM.Survey.ROTACION.addEventListener('onNext', function(e){
var filtro = "";

if(e.sourceElement.isAnswerSelected("_1")) filtro = "_1,_2,_3";
if(e.sourceElement.isAnswerSelected("_2")) filtro = "_1,_3,_2";
if(e.sourceElement.isAnswerSelected("_3")) filtro = "_2,_1,_3";
if(e.sourceElement.isAnswerSelected("_4")) filtro = "_2,_3,_1";
if(e.sourceElement.isAnswerSelected("_5")) filtro = "_3,_1,_2";
if(e.sourceElement.isAnswerSelected("_6")) filtro = "_3,_2,_1";

OSM.Survey.PRODUCTO1.setAnswers(filtro.split(",")[0]);
OSM.Survey.PRODUCTO2.setAnswers(filtro.split(",")[1]);
OSM.Survey.PRODUCTO3.setAnswers(filtro.split(",")[2]);

    
OSM.Survey.LP.filterIterations(filtro);

ut.reorder("LP", filtro, OSM.Survey, OSM.Survey);
});
```

### Caso 23 — Calculo de una fecha en intervalos para continuar terminar si es menor a 6 meses o mayor a 18 meses


**Situación.** Terminar si es menor a 6 meses o mayor a 18 meses

```js
OSM.Survey.forS10_FECHA_NACIMIENTO.addEventListener('onNext', function(e) {

    var defaultSubmitDateFormat = 'YYYY-MM-DD';

    var fechaNacimiento = moment(
        e.sourceElement.getComment(),
        defaultSubmitDateFormat
    );

    if (String(fechaNacimiento) === 'Invalid date') {
        OSM.Survey.ELIMI.setComment(
            e.sourceElement.get('objectName') +
            '. La fecha de nacimiento ingresada no es válida.'
        );
        OSM.Survey.get('navigator').goTo(OSM.Survey.ELIMI);
    } else {
        var edadMeses = parseInt(moment().diff(fechaNacimiento, 'months'));

        OSM.Survey.forS10_EDAD_MESES.setComment(edadMeses);
        OSM.Survey.forS10_EDAD_MESES.readOnly(true);

        if (edadMeses < 6 || edadMeses > 18) {
            OSM.Survey.ELIMI.setComment(
                e.sourceElement.get('objectName') +
                '. La edad del bebé es de ' + String(edadMeses) +
                ' meses y no se encuentra dentro del rango permitido de 6 a 18 meses.'
            );
            OSM.Survey.get('navigator').goTo(OSM.Survey.ELIMI);
        }
    }
});
```

### Caso 24 — Validacion de variable Fecha de nacimiento (FN)

**Situación.** REGISTRE EN F2 EL NUMERO DE AÑOS CUMPLIDOS DE ACUERDO CON LA FECHA DE LA ENCUESTA Y LA FECHA DE NACIMIENTO (FN)

```mdd
    FN "FN. ¿Cuál es su fecha de Nacimiento?"
        [
            _Osm_QuestionLayoutID = 2,
            _Osm_ContentRuleID = 18,
            _Osm_CustomFunction = "checkAge"
        ]
    date ["1972-01-01" .. "2001-12-31"];
```

```js
OSM.Survey.checkAge = function(e) {
    OSM.NotificationSystem.removeAllNotifications();
    var msje = "";
    var defaultSubmitDateFormat = "YYYY-MM-DD";

    var fechaNac = moment(OSM.Survey.FN.getComment(), defaultSubmitDateFormat);
    var birthAge = parseInt(moment().diff(fechaNac, 'years', false));

    if (birthAge !== parseInt(OSM.Survey.F2.getComment())) {
        msje = "La edad no corresponde con la ingresada inicialmente: (" + OSM.Survey.F2.getComment() + ")";
    }

    if (msje !== "" && e.name !== 'onInputChange') {
        return {
            status: false,
            message: msje
        };
    } else {
        return {
            status: true
        };
    }
};

OSM.Survey.FN.addEventListener('onEntrance', function(e) {
    if (OSM.Survey.SHELL_RECORDING_CONFIRMATION.isAnswerSelected('_A1')) {
        var xID = OSM.Survey.SHELL_CHAINID.getComment();
        OSM.Survey.startSilentAudioRecording(xID + '_FN');
    }
});

OSM.Survey.FN.addEventListener('onNext', function(e) {
    if (OSM.Survey.SHELL_RECORDING_CONFIRMATION.isAnswerSelected('_A1')) {
        OSM.Survey.stopSilentAudioRecording();
    }

    var defaultSubmitDateFormat = "YYYY-MM-DD";
    var fechaNac = moment(e.sourceElement.getComment(), defaultSubmitDateFormat);
    var edadCalculada = parseInt(moment().diff(fechaNac, 'years', false));

    if (edadCalculada !== parseInt(OSM.Survey.F2.getComment())) {
        OSM.Survey.ELIMI.setComment(e.sourceElement.get('objectName') + '. La edad calculada no coincide con F2. Agradecer y terminar encuesta.');
        OSM.Survey.get('navigator').goTo(OSM.Survey.ELIMI);
    }
});
```

**Consideraciones.** La función custom recibe `e` (lo usa para `e.name`), declara sus variables con `var` y nunca navega. El `onNext` combina la detención del BC y la terminación en un solo listener, con el `goTo` al final.

### Caso 25 — Mostrar u ocultar una pregunta en la misma pantalla (`onInputChange`)


**Situación.** Al marcar la opción 1 en ENCERRAR aparece en la misma pantalla la pregunta de confirmación ENCERRADA_CONF; con otra respuesta se oculta.

```js
OSM.Survey.ENCERRAR.addEventListener('onInputChange', function(e){
if (OSM.Survey.ENCERRAR.getAnswers() == "_1"){
    OSM.Survey.ENCERRADA_CONF.show();
}else{
    OSM.Survey.ENCERRADA_CONF.hide();
}

});
```


### Caso 26 — `TERMINATE VALID` es terminación por filtro, no encuesta efectiva

**Situación.** Cuestionario: `P.1 ... SW: CONTINUE IF CODE 1 SELECTED, OTHERWISE TERMINATE VALID` y `CONSENT: Sí = 1 PROG: CONTINUE / No = 2 PROG: TERMINATE VALID`.

```js
// R-001 | FILTER_TERMINATE | CONSENT | Caso 26
OSM.Survey.CONSENT.addEventListener('onNext', function(e) {
    if (e.sourceElement.isAnswerSelected('_2')) {
        OSM.Survey.ELIMI.setComment(e.sourceElement.get('objectName') + '. No acepta participar (TERMINATE VALID).');
        OSM.Survey.get('navigator').goTo(OSM.Survey.ELIMI);
    }
});

// R-002 | FILTER_TERMINATE | P_1 | Caso 26
OSM.Survey.P_1.addEventListener('onNext', function(e) {
    if (!e.sourceElement.isAnswerSelected('_1')) {
        OSM.Survey.ELIMI.setComment(e.sourceElement.get('objectName') + '. No seleccionó código 1 (TERMINATE VALID).');
        OSM.Survey.get('navigator').goTo(OSM.Survey.ELIMI);
    }
});
```

**Prohibido (incidencia real):** `OSM.Survey.get('navigator').goTo(OSM.Survey.SHELL_CLOSE)`, saltar a la última pregunta o a una pantalla de "gracias por completar" para un `TERMINATE VALID`.

### Caso 27 — Piping de la respuesta de otra pregunta

**Situación.** Cuestionario: `P12. ¿Qué es lo que más le gusta de <PIPE-IN MARCA DE P10>?`; P10 es RU con "Otra (especificar)".

Opción preferida — resuelto en el MDD (el prompt 01 lo declara; la lógica no agrega nada):

```mdd
P12 "¿Qué es lo que más le gusta de <font color='yellow'>{#P10#}</font>?"
text [0..4000];
```

Opción JS — cuando el texto se arma con varias fuentes o condiciones (el MDD debe tener `{#marcaP12#}`):

```js
// R-030 | ANSWER_PIPING | P12 | Caso 27
OSM.Survey.P12.addEventListener('onBeforeNavigateTo', function(e) {
    var texto = OSM.Survey.getLabelAnswers(OSM.Survey.P10, OSM.Survey.P10.getAnswers());
    if (OSM.Survey.P11.isAnswerSelected('_1')) {
        texto = texto + ' / ' + OSM.Survey.getLabelAnswers(OSM.Survey.P11, OSM.Survey.P11.getAnswers());
    }
    OSM.Survey.setInsert('marcaP12', texto);
});
```

### Caso 28 — Un solo `onNext` con backcheck, cuota y terminación

**Situación.** S3 tiene `(BACKCHECK)`; además `PROG: SI S3 = 3 TERMINATE` y `CUOTA_ZONA ← S3`. La versión histórica generaba dos `onNext` para S3 (uno para detener la grabación y otro para la terminación); eso está prohibido (L04).

```js
// R-005 | BACKCHECK_RECORDING | S3 | Caso 3
OSM.Survey.S3.addEventListener('onEntrance', function(e) {
    if (OSM.Survey.SHELL_RECORDING_CONFIRMATION.isAnswerSelected('_A1')) {
        var xID = OSM.Survey.SHELL_CHAINID.getComment();
        OSM.Survey.startSilentAudioRecording(xID + '_S3');
    }
});

// R-005 + R-006 + R-007 | BACKCHECK_RECORDING + QUOTA_ASSIGNMENT + FILTER_TERMINATE | S3 | Caso 28
OSM.Survey.S3.addEventListener('onNext', function(e) {
    if (OSM.Survey.SHELL_RECORDING_CONFIRMATION.isAnswerSelected('_A1')) {
        OSM.Survey.stopSilentAudioRecording();
    }

    OSM.Survey.CUOTA_ZONA.setAnswers(e.sourceElement.getAnswers());

    if (e.sourceElement.isAnswerSelected('_3')) {
        OSM.Survey.ELIMI.setComment(e.sourceElement.get('objectName') + '. Zona no válida. Agradecer y terminar encuesta.');
        OSM.Survey.get('navigator').goTo(OSM.Survey.ELIMI);
    }
});
```

### Caso 29 — Salto `PASAR A` resuelto con visibilidad, sin `goTo` ni limpieza

**Situación.** `P6. ¿Ha comprado en el último mes? 1 Sí / 2 No (PASAR A P9)`. P7 y P8 solo aplican a quien respondió 1.

```js
// R-008 | QUESTION_VISIBILITY | P7 | Caso 29
OSM.Survey.P7.addEventListener('onBeforeNavigateTo', function(e) {
    if (OSM.Survey.P6.isAnswerSelected('_1')) {
        e.sourceElement.show();
    } else {
        e.sourceElement.hide();
    }
});

// R-009 | QUESTION_VISIBILITY | P8 | Caso 29
OSM.Survey.P8.addEventListener('onBeforeNavigateTo', function(e) {
    if (OSM.Survey.P6.isAnswerSelected('_1')) {
        e.sourceElement.show();
    } else {
        e.sourceElement.hide();
    }
});
```

**Consideraciones.** No se usa `goTo(OSM.Survey.P9)` porque ocultar P7 y P8 resuelve el flujo (L11), y no se limpian las respuestas de P7/P8 (L10). Si el salto abarca muchas preguntas o un módulo completo, se admite `goTo` a la primera pregunta destino, solo en el `onNext` de P6.

## 7.7 Glosario mínimo

- **MDD:** modelo declarativo del dato y de la estructura (tipos, categorías, cardinalidades, loops, fields, listas, blocks, metadatos OSM). Es fuente técnica de la lógica.
- **Lógica OSM/JS:** comportamiento dinámico que depende del estado de la entrevista.
- **Evento:** momento funcional en que se ejecuta un listener (`onBeforeNavigateTo`, `onEntrance`, `onInputChange`, `onNext`).
- **Iteración:** fila/entidad de un loop. **Filtro de iteraciones:** restringe qué filas se presentan.
- **Filtro de respuestas:** restringe qué categorías se ofrecen.
- **Carry-forward:** uso de respuestas previas para definir contenido, categorías o iteraciones posteriores.
- **Piping / insert:** inserción de contenido dinámico en el wording.
- **Recode / variable derivada:** variable que agrupa o transforma una fuente sin reemplazarla.
- **Variables Shell:** variables de infraestructura (identificación, demografía precargada, confirmación de grabación) que la lógica puede leer.
- **`ELIMI`:** variable que guarda el motivo de terminación por filtro; distinta del cierre final.
- **BACKCHECK / BC:** marca operativa que activa grabación silenciosa con consentimiento (`SHELL_RECORDING_CONFIRMATION` = `_A1`); nunca es una instrucción para el encuestador.
- **`TERMINATE VALID` / `TERMINATE INVALID`:** terminación por filtro (screen-out) que se implementa con `ELIMI`; no es una encuesta efectiva.
- **Evento de salida:** `onNext`; único lugar donde se escribe `goTo`.
- **Regla `BLOQUEADA`:** regla que no puede implementarse con seguridad por falta de evidencia técnica; se documenta en el JS (`TODO`) y en QA.

---

**FIN DEL PROMPT 02 — EASYSCRIPT V6**

CLAVE DE LECTURA DEL PROMPT 02: LOG-V6-CAMU-2953
