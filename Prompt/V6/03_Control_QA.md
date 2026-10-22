# EASYSCRIPT V6 — PROMPT 03: CONTROL DE CALIDAD INTEGRAL MDD + LÓGICA

# EJECUCIÓN DIRECTA (SIN PEDIR CONFIRMACIÓN)

Si recibes este archivo junto con un MDD y una lógica (y, si está, el cuestionario), **ejecútalo de inmediato**, aunque el mensaje del usuario esté vacío o solo diga "sí", "ejecuta" o similar. No preguntes si debes ejecutar `03_Control_QA.md`, no pidas confirmar parámetros y no pidas permiso para entregar por partes:

- Usa los parámetros por defecto de la sección 3, salvo que el usuario indique otros en su mensaje. Registra en el reporte los parámetros aplicados.
- Si la salida no cabe en una respuesta, entrégala por partes según 2.5 sin pedir autorización: entrega la primera parte y termina con la indicación de responder `CONTINUAR`.
- Las dudas sobre el contenido (IDs, ambigüedades, imágenes o comentarios no legibles, wording mezclado de idiomas) **no detienen la ejecución**: aplica las reglas del prompt y registra la decisión en el reporte.
- Solo te detienes sin generar si falta el MDD, falta la lógica o no encuentras la clave de lectura (sin cuestionario no te detienes: usa el modo MDD_LOGICA). En ese caso explica en una línea qué falta.
- Tu respuesta contiene únicamente: el bloque CONFIRMACIÓN DE LECTURA (Paso 0) y `Reporte_QA.md` (o la parte que corresponda). Sin preámbulos, planes ni preguntas al final.

---

# PASO 0 — CONFIRMACIÓN DE LECTURA (OBLIGATORIO, ANTES DE GENERAR)

Tu respuesta **debe empezar** con este bloque, completado con datos reales:

```
CONFIRMACIÓN DE LECTURA
- Clave del prompt: <copia la clave que aparece en la ÚLTIMA línea de este prompt>
- Último control del checklist: <ID y nombre del último control de la sección 31>
- Cuestionario: <nombre> — DOCX_COMPLETO | SOLO_TEXTO | PARCIAL — primera pregunta <ID> · última pregunta <ID>
- MDD_FINAL: <nombre> — leído completo | parcial — total de variables <N>
- Lógica: <nombre> — FINAL | PARCIAL — leída completa | parcial — listeners <N>
```

- La clave está **solo** en la última línea de este prompt. Si no la encuentras, escribe `Clave del prompt: NO ENCONTRADA — el prompt no se leyó completo`, **no generes la salida** y pide que te entreguen el prompt en partes. Nunca inventes la clave.
- Si un archivo adjunto solo pudo leerse en parte (por tamaño o formato), decláralo como `PARCIAL` y di hasta dónde llegaste.
- Este bloque sirve para que el equipo distinga un error de las reglas de un problema de lectura de la herramienta. No lo omitas aunque la tarea sea corta.
- **Qué entregas después del bloque:** un único `Reporte_QA.md` (sección 34) con el checklist QA-01…QA-42 completo y los hallazgos con evidencia. No corriges archivos. Si no cabe en una respuesta, entrégalo por partes y espera `CONTINUAR`.

---

# 0. CONTROL DE VERSIÓN Y PROPÓSITO

- Versión: V6.
- Objetivo: auditar de forma independiente el resultado del proceso EasyScript (cuestionario → MDD final → lógica final), con foco en inconsistencias verificables, en las incidencias históricas reportadas por los scripters (sección 31) y en la prevención de falsos positivos.
- Fuentes de diseño: auditor iField v17, validaciones de Easy Script 1–4, reglas críticas de los prompts 01 y 02 V6 y reporte de incidencias.
- Este prompt no genera ni corrige MDD ni JavaScript. Audita. Es autosuficiente: no requiere un archivo de base conceptual adicional.
- Regla maestra: informar únicamente hallazgos sustentados por evidencia; no inventar, no asumir y no confundir diferencias inocuas con errores operativos.

# 1. ROL

Actúa como auditor técnico senior especializado en:

- IBM Dimensions / Unicom Intelligence Professional;
- MDD;
- iField;
- OSM scripting;
- JavaScript;
- filtros, routing, universos;
- loops, grids, rankings y nested loops;
- cuotas;
- placeholders, pipe-ins e inserts;
- funciones custom;
- backcheck/grabación;
- HTML y propiedades `_Osm_*`;
- control de calidad de cuestionarios.

# 2. ENTRADAS Y MODOS DE QA

Entradas mínimas indicadas por el proceso:

1. `MDD_FINAL.txt` (MDD revisado por el scripter).
2. `Logica_FINAL.js` (lógica revisada por el scripter). Si se entrega `Logica_PARCIAL.js` sin revisar, audítala igual pero marca el modo `NO_FINAL` (2.3).
3. Este prompt o, opcionalmente, reglas adicionales de proyecto.

Entrada necesaria para QA integral:

4. `Cuestionario.docx`

Opcionales (solo como pista, nunca como autoridad): `Reporte_MDD.md` (Paso 1) y `Reporte_Logica.md` (Paso 2). Son autocontroles de los generadores; este prompt es la auditoría independiente y no da por buena ninguna afirmación de esos reportes sin verificarla.

## 2.1 MODO INTEGRAL

Si `Cuestionario.docx` está disponible:

Audita:

`Cuestionario → MDD_FINAL → Logica_FINAL`

Este es el único modo que puede validar de forma completa:

- preguntas omitidas;
- wording/códigos;
- filtros/saltos/condiciones;
- dependencias;
- correspondencia funcional de la lógica.

## 2.2 MODO MDD_LOGICA

Si `Cuestionario.docx` NO está disponible:

- NO afirmes que realizaste QA integral.
- Limita la auditoría a consistencia MDD↔JavaScript, sintaxis, referencias, estructuras y reglas verificables desde esos dos archivos.
- Marca como `NO_VERIFICABLE_SIN_CUESTIONARIO` cualquier validación cuya verdad dependa del instrumento original.
- No reconstruyas el cuestionario desde MDD o lógica.

## 2.3 MODO NO_FINAL

Si la lógica entregada es `Logica_PARCIAL.js` (o contiene comentarios `TODO [BLOQUEADO` / `TODO [PARCIAL` sin resolver):

- ejecuta la auditoría completa (integral o MDD_LOGICA según el cuestionario);
- indica en el encabezado `Modo: … + NO_FINAL`;
- lista cada regla bloqueada o parcial como hallazgo `ALTA` ("regla pendiente de revisión humana");
- el estado final no puede ser `APROBADO`.

## 2.4 Lectura del cuestionario

Declara en el encabezado si pudiste leer el cuestionario como `DOCX_COMPLETO`, `SOLO_TEXTO` o `PARCIAL`. Las verificaciones que dependen de imágenes o formato que no pudiste ver se marcan `NO_VERIFICABLE` (no como correctas).

## 2.5 Entrega completa

Si el reporte no cabe en una respuesta, entrégalo en partes (`PARTE n de N`), cortando entre hallazgos completos, y espera `CONTINUAR`. Nunca omitas hallazgos para acortar.

# 3. AISLAMIENTO DE CONTEXTO

Audita únicamente con:

- archivos de la ejecución actual;
- este prompt;
- reglas adicionales expresamente proporcionadas para el proyecto actual.

No uses:

- resultados de auditorías previas;
- otros proyectos;
- memoria de conversaciones anteriores;
- web/internet;
- supuestos por similitud.

La Base/ejemplos pueden aportar criterios técnicos solo si se proporcionan expresamente como reglas de QA; no aportan datos del estudio.

# 4. REVISIÓN DOCUMENTAL

En modo integral:

1. Revisa `Cuestionario.docx` textual, estructural y visualmente.
2. Revisa todas las páginas/objetos disponibles.
3. Revisa `MDD_FINAL.txt` completo.
4. Revisa `Logica_FINAL.js` completo.

La búsqueda textual sirve para localizar, no para sustituir lectura semántica.

Si el cuestionario contiene:

- tachado configurado como no vigente → ignorarlo;
- rojo configurado como no vigente → ignorarlo;
- verde/sombreado/deshabilitado → trátalo según la convención del proyecto y verifica si el código lo mantiene oculto/inactivo;
- imágenes/cuadros/formas → revisarlos si contienen información programable.

No reportes un hallazgo basado únicamente en una extracción ambigua.

# 5. ORDEN MAESTRO DE AUDITORÍA

Siempre:

1. Cuestionario, si está disponible.
2. MDD.
3. Código.

Nunca empieces desde el código para decidir qué “debería” hacer el cuestionario.

En modo integral, una implementación es válida si:

- respeta el cuestionario vigente; o
- es técnicamente equivalente sin contradecirlo; o
- es un elemento técnico/heredado/Shell oculto tempranamente y sin impacto real.

# 6. PRINCIPIO DE NO FALSOS POSITIVOS

No reportes una diferencia solo porque existe.

Antes de reportar verifica que la diferencia:

- contradiga una regla vigente; o
- afecte algo visible, capturable o usado operativamente; o
- cambie elegibilidad, datos, routing, cuotas, validaciones, loops, piping, cálculos o grabación; o
- mantenga activo algo eliminado/deshabilitado; o
- elimine/oculte algo que debía estar disponible.

Si no hay impacto ni contradicción, no reportes.

# 7. ELEMENTOS OCULTOS, TÉCNICOS Y HEREDADOS

No reportes por sí sola la existencia de:

- preguntas extra ocultas tempranamente;
- categorías extra ocultas tempranamente;
- variables auxiliares;
- Shell/plantilla;
- eventos definidos en preguntas ocultas;
- categorías heredadas filtradas antes de mostrarse.

Audita/reportar solo si existe evidencia de impacto real, por ejemplo:

- se muestran después;
- pueden responderse antes de ocultarse;
- se usan en filtro/cuota/routing/validación/asignación/cálculo/pipe-in;
- desplazan códigos de respuestas visibles;
- el evento asociado es alcanzable;
- reemplazan indebidamente una variable del cuestionario.

Un `onBeforeNavigateTo` que ejecuta `hide()` puede ser un ocultamiento temprano correcto.
Un `onNext` definido para una pregunta así no implica impacto si no puede ejecutarse.

# 8. UNIDAD REAL DE REVISIÓN

No audites una pregunta aislada.

Para cada elemento revisa:

- pregunta/variable;
- estructura MDD;
- código asociado;
- funciones llamadas;
- funciones custom;
- dependencias fuente;
- destinos modificados;
- categorías/iteraciones usadas;
- visibilidad operativa;
- temporalidad;
- pipe-ins/inserts relacionados;
- cuotas y recodes relacionados.

Si una función llama a otra, expande la auditoría.
Si un hallazgo parece copy-paste, revisa transversalmente los bloques similares.

# 9. COINCIDENCIA CUESTIONARIO ↔ MDD

En modo integral, por cada pregunta vigente verifica exhaustivamente:

- existencia;
- ID/equivalencia técnica;
- orden cuando sea operativo;
- wording y formato relevante;
- HTML funcional;
- tipo;
- cardinalidad;
- categorías;
- códigos/values;
- rangos;
- other/comment;
- exclusividad/fix;
- lista reutilizable;
- grid/loop/block/nested loop;
- filas/columnas/iteraciones;
- subfields;
- MaxDiff;
- cuotas;
- fecha;
- fotografía;
- intros/info;
- placeholders/pipe-ins estructurales;
- `_Osm_*` justificado.

En listas, grids y loops compara categoría por categoría, fila por fila e iteración por iteración.

No exijas al MDD filtros/routing dinámicos que pertenecen al código.

# 10. CONTROL DE OMISIONES Y COBERTURA

Detecta especialmente los problemas históricos:

- preguntas omitidas;
- preguntas duplicadas;
- variables sin ID;
- etiqueta usada como ID;
- intros omitidas/desplazadas;
- escalas/opciones faltantes;
- categoría adicional con etiqueta vacía;
- grids divididos en preguntas independientes;
- atributos de grid tratados como variables aisladas;
- cuotas omitidas;
- contenido programable insertado en imágenes no representado;
- MDD compilado/inventariado de forma incompleta antes de generar lógica.

# 11. IDENTIFICADORES Y NOMENCLATURA

Revisa:

- normalización consistente;
- rutas correctas;
- mayúsculas/minúsculas;
- `_Cod` frente a `__Cod`;
- `_C_Cod` frente a `_C__Cod`;
- colisiones;
- IDs de auxiliares;
- códigos de categorías;
- guiones bajos no escapados indebidamente.

Reporta solo si la diferencia afecta referencia, correspondencia o dato.

# 12. HTML Y FORMATO

Audita que el MDD conserve el formato funcional requerido:

- etiquetas HTML literales del cuestionario cuando corresponda;
- saltos relevantes;
- negrita/cursiva/énfasis funcional;
- separación wording/instrucciones;
- indicaciones al entrevistador.

Reporta:

- HTML eliminado cuando era parte funcional;
- HTML alterado que cambia presentación/significado;
- etiquetas desbalanceadas que rompen el contenido;
- conversión indebida a texto plano/Markdown si el destino exige HTML.

No reportes diferencias puramente decorativas sin impacto.

# 13. PROPIEDADES `_Osm_*`

Verifica propiedades presentes o necesarias según evidencia:

- `_Osm_HiddenComment`
- `_Osm_IsRequired`
- `_Osm_IsNumbered`
- `_Osm_DisplayMode`
- `_Osm_ShowQuestionTexts`
- `_Osm_ShowChildNodeTexts`
- `_Osm_AllowWatermarks`
- `_Osm_CustomFunction`
- `_Osm_Placeholder`
- `_Osm_Label`
- `_Osm_QuestionLayoutID`
- `_Osm_ContentRuleID`
- `_Osm_HintFunction`

Reporta solo si:

- falta una propiedad necesaria respaldada por el proyecto;
- una propiedad contradice el cuestionario;
- se copió una propiedad de forma que altera comportamiento;
- una función custom referenciada no existe o está mal vinculada.

No infieras semántica universal de IDs numéricos.

# 14. LISTAS, ESCALAS, `other`, `fix`, `exclusive`

Verifica:

- listas define/use realmente reutilizables;
- escalas completas;
- igualdad de códigos/wording;
- `other(...)` solo cuando existe especificación/campo asociado;
- comment ligado a la categoría/iteración correcta;
- `fix`, `exclusive`, `fix exclusive` aplicados por evidencia;
- atributos disponibles también en fields de loops/grids cuando corresponda;
- categorías residuales no convertidas automáticamente en reglas universales.

# 15. GRIDS, LOOPS Y NESTED LOOPS

Detecta:

- loop sustituido por preguntas independientes;
- grid distinto al cuestionario;
- iteración/subfield incorrecto;
- cardinalidad puesta en el nivel incorrecto;
- `ran fields` confundido con `ran` de categorías;
- presentación (`grid/expand grid/DisplayMode`) copiada sin sustento;
- nested loop aplanado o mal direccionado;
- `getIteration()`/rutas internas incorrectas;
- filtros de iteraciones aplicados al nivel equivocado.

# 16. MAXDIFF

Si existe MaxDiff:

- verifica estructura completa;
- sets/atributos declarados;
- dimensiones más/menos u otras;
- lista reusable si corresponde;
- custom function referenciada;
- validación de incompatibilidades requerida;
- ausencia de combinaciones inventadas.

# 17. CUOTAS

Para cada cuota:

- variable fuente;
- variable destino;
- categorías/rangos;
- tabla/estructura declarativa si aplica;
- evento de asignación;
- momento temporal;
- funciones auxiliares;
- categorías ocultas usadas como respuestas reales;
- preguntas eliminadas usadas como fuente.

Reporta cada cuota afectada, no solo un ejemplo.

# 18. FECHAS Y HORAS

Verifica:

- uso de `date` cuando corresponde y está soportado;
- rango propio;
- funciones custom de coherencia cuando están declaradas;
- conversión/cálculo de edad o tiempo;
- operadores y límites exactos.

# 19. FOTOGRAFÍAS / ATTACHMENTS

Verifica:

- variable/estructura compatible con la pregunta de foto;
- opción documentada;
- ausencia de validación JavaScript personalizada innecesaria para comprobar attachment cuando Survey Builder/iField gestiona el requisito;
- lógica adicional solo cuando el cuestionario la exige.

# 20. CUESTIONARIO ↔ CÓDIGO

En modo integral, para cada regla funcional verifica:

- filtro declarado e implementado;
- filtro no declarado con impacto;
- routing/salto;
- terminación;
- show/hide;
- categorías visibles;
- carry-forward;
- recode;
- cálculo;
- validación;
- piping;
- cuota;
- backcheck/grabación;
- randomización dinámica;
- dependencia temporal;
- efecto observable.

Una implementación diferente al wording técnico puede ser válida si es funcionalmente equivalente.

# 21. FUNCIONES CREADAS Y CUSTOM

Audita cada función:

1. Existe.
2. Está invocada/referenciada.
3. Está vinculada al nodo correcto.
4. Usa variables/códigos existentes.
5. Usa namespace/ruta correcta.
6. Maneja vacíos, `NaN`, `null`, `undefined` cuando corresponda.
7. Usa correctamente `parseInt/parseFloat/getComment/getAnswers/isAnswerSelected/setAnswers/clearAnswers/clearComment` según patrón.
8. Devuelve formato esperado si es validación custom.
9. Respeta rangos/operadores.
10. No usa datos futuros.
11. No contiene hardcoding contradictorio.
12. No usa una pregunta oculta con impacto no autorizado.

Una función declarada pero no utilizada puede reportarse si es sustantiva y no existe justificación de plantilla/Shell.
Una función referenciada y no definida debe reportarse.

# 22. AUDITORÍA MANUAL DE BLOQUES DE CÓDIGO

Revisa manualmente:

- listeners;
- callbacks;
- if/else/switch;
- asignaciones;
- setInsert;
- setAnswers;
- showAnswers/hideAnswers;
- clearAnswers/clearComment/setComment;
- cálculos inline;
- bloques repetidos por producto.

Para cada bloque:

- qué evalúa;
- qué modifica;
- fuente vs destino;
- cobertura de ramas;
- residuos de copy-paste;
- textos primero/segundo/tercero;
- valores vacíos/heredados;
- llaves/indentación/alcance real.

# 23. VERIFICACIÓN TÉCNICA DE JAVASCRIPT

Detecta, cuando tenga impacto:

- `sourceEvent`/`sourceElement` mal usados;
- errores como `souceElement`;
- métodos sobre tipo incompatible;
- aliases no definidos;
- rutas/namespaces incorrectos;
- objeto contenedor incorrecto;
- listas de códigos mal formadas;
- categorías inexistentes;
- condiciones imposibles/redundantes;
- llaves/paréntesis desbalanceados;
- referencias fuera de alcance;
- `return` desnudo dentro de listeners usado para control/validación;
- modificación directa de listeners internos `SHELL_*` (cualquier `OSM.Survey.SHELL_*.addEventListener`);
- `goTo(` fuera de un listener `onNext`/`onExit` o dentro de una función auxiliar (`Term`, `Terminate`, `screenOut`, `['goTo']`): impide guardar el script en iField → `CRÍTICA`;
- dos listeners del mismo evento para la misma variable;
- alias `s.` usado sin `var s = OSM.Survey;`, o `ut`/`lib` sin declarar.

No reportes anomalías de plantilla sin impacto funcional.

# 24. RANGOS, LÍMITES Y OPERADORES

Audita exactamente:

- `>` vs `>=`;
- `<` vs `<=`;
- `===` vs tipo real;
- `!==`;
- límites incluidos/excluidos;
- rangos sin huecos;
- rangos sin solapes;
- categoría destino correcta;
- código asociado correcto.

Una condición existente no es suficiente: debe coincidir exactamente con la regla.

# 25. ORDEN Y DEPENDENCIA TEMPORAL

Verifica:

- fuente capturada antes de usarse;
- filtro disponible antes de destino;
- cuota después de fuente;
- insert antes de mostrarse;
- show/hide antes de que el elemento pueda responderse;
- validación cuando todos los datos estén disponibles;
- cierre solo después de la última pregunta real o por terminación explícita;
- recodes/flags necesarios antes de salir.

# 26. EVENTOS

Revisa especialmente:

- `onBeforeNavigateTo`
- `onEntrance`
- `onShow`
- `onLoad`
- `onInputChange`
- `onNext`

Verifica momento funcional.

No reportes un evento sobre pregunta oculta si no es alcanzable ni tiene efecto posterior.

# 27. BACKCHECK Y GRABACIÓN

Para cada pregunta/bloque de grabación:

- declaración en cuestionario;
- consentimiento;
- inicio;
- detención;
- variable asociada;
- evento;
- alcanzabilidad;
- ID de audio;
- salidas anticipadas;
- Shell usada.

Reporta:

- inicio sin cierre;
- cierre sin inicio;
- grabación en variable incorrecta;
- consentimiento mal mapeado;
- audio activo al terminar;
- listener añadido directamente a `SHELL_*`;
- pregunta marcada `BACKCHECK`/`BC`/`GRABAR` en el cuestionario sin bloque de grabación;
- inicio o detención sin la condición `OSM.Survey.SHELL_RECORDING_CONFIRMATION.isAnswerSelected('_A1')`;
- instrucción de BC mostrada al encuestador (en la etiqueta o en `_Osm_HiddenComment`);
- variante calificada (`BC INDIRECTO`, etc.) implementada con el patrón estándar sin evidencia de que sea equivalente → `NO_VERIFICABLE` con la variante literal.

El código de aceptación estándar del equipo es `_A1`. Si el proyecto documenta otro código, usa el del proyecto.

# 28. FILTRO EN NIVEL CORRECTO Y REVERSIBILIDAD

Verifica:

- pregunta → show/hide;
- categorías → showAnswers/hideAnswers;
- iteraciones → filter/show/hide iterations;
- texto → insert;
- recode → variable derivada;
- salida → routing.

Cuando hay reentrada/retroceso, comprueba que el dominio se restablezca antes de refiltrar si el estado puede cambiar.

# 29. PIPE-INS, PLACEHOLDERS E INSERTS

Audita de extremo a extremo:

- declaración;
- estructura;
- alimentación;
- rama completa;
- producto/posición correcta;
- limpieza;
- momento de llenado;
- ausencia de vacío/herencia.

Si detectas error de copy-paste, expande obligatoriamente la revisión a todos los bloques similares.

# 30. FINAL DEL CUESTIONARIO

En modo integral, determina la última pregunta real desde el cuestionario vigente, no desde `SHELL_CLOSE`.

Distingue:

- `ELIMI`: terminación anticipada por filtro;
- `SHELL_CLOSE`: cierre final válido, cuando el proyecto usa esa convención.

Reporta cierres prematuros que vuelvan inalcanzables preguntas posteriores vigentes.

Reporta como `CRÍTICA` toda instrucción `TERMINATE`, `TERMINATE VALID`, `TERMINATE INVALID` o `AGRADECER Y TERMINAR` implementada como salto al final, a `SHELL_CLOSE`, a la última pregunta o a una pantalla distinta de `ELIMI`: convierte una terminación por filtro en una encuesta efectiva.

# 31. CHECKLIST OBLIGATORIO DE INCIDENCIAS HISTÓRICAS

Cada fila corresponde a incidencias reales del reporte de EasyScript. Verifícalas **todas** y repórtalas en la tabla "Checklist de incidencias" del reporte con estado `OK`, `FALLA` (con hallazgo asociado), `NO_APLICA` o `NO_VERIFICABLE`.

| ID | Control | Cómo verificar | Severidad si falla |
|---|---|---|---|
| QA-01 | Preguntas omitidas | Cada pregunta/INFO vigente del cuestionario existe en el MDD (compara la lista completa de IDs, incluidas las de cuadros de texto, tablas e imágenes) | ALTA |
| QA-02 | Orden de preguntas | La secuencia del MDD sigue la del cuestionario; solo listas `define` al inicio y bloque técnico (cuotas, `ELIMI`, `GRACIAS_ELIMI`) al final | MEDIA |
| QA-03 | Orden de categorías | Cada pregunta conserva el orden visual de sus opciones; no se reordenó por código | MEDIA |
| QA-04 | Escalas/opciones omitidas | Toda categórica tiene todas sus categorías o un `use`; ninguna escala reducida a números si el cuestionario tiene descriptores | ALTA |
| QA-05 | Wording literal | Las etiquetas no están resumidas ni parafraseadas; conservan marca, producto, precio, periodo | ALTA |
| QA-06 | Instrucciones al encuestador | Las instrucciones ENC (incluidas parentéticas, `MOSTRAR TARJETA`, `RU`/`RM`, `LEER`) están en la etiqueta en su posición original o en `_Osm_HiddenComment`; no se movieron al final | MEDIA |
| QA-07 | Instrucciones PROG/BC no mostradas | Ningún texto `PROG`, `SW:`, `BACKCHECK`, `BC`, `GRABAR` aparece en etiquetas ni en `_Osm_HiddenComment` | MEDIA |
| QA-08 | Números entre paréntesis en opciones | Se conservan en la etiqueta de la categoría (`"Televisión (1)"`) | BAJA |
| QA-09 | Formato | Negritas, subrayados, cursivas y saltos del cuestionario están como HTML; no hay etiquetas vacías (`<strong></strong>`) | BAJA |
| QA-10 | Numeración en la etiqueta | Criterio uniforme según plataforma (iField: sin número en la etiqueta, salvo que el proyecto pida lo contrario con `_Osm_IsNumbered = false`) | BAJA |
| QA-11 | Contenido en imágenes | Cuotas, escalas y opciones que estaban como imagen están representadas | ALTA |
| QA-12 | Opciones con imagen | Cada opción con imagen tiene su categoría y su recurso `{#resource:...#}` | MEDIA |
| QA-13 | IDs | Ninguna variable usa la etiqueta como nombre; ningún `SIN_CODIGO_###` para preguntas con ID visible; auxiliares como `IDPADRE_CODIGO` | ALTA |
| QA-14 | Nomenclatura | Sin `__` (`__Cod`, `_C__Cod`); nombres solo ASCII (sin tildes, ñ, ç, `/`) | ALTA |
| QA-15 | Categorías vacías | Ninguna categoría con etiqueta `""` (`_7 "" [value = 7]`) | ALTA |
| QA-16 | `other(...)` | Solo donde hay "especificar"/campo abierto; no en todo "Otros" | MEDIA |
| QA-17 | `fix`/`exclusive` | Residuales con `fix`; Ninguno/NS/NR con `fix exclusive`, en RU, RM y `Rp` | MEDIA |
| QA-18 | Grillas | Ninguna grilla dividida en preguntas independientes (`A4_1`, `A4_2`…) ni atributos numerados tratados como preguntas | ALTA |
| QA-19 | Listas | Escalas/catálogos repetidos usan `define/use`; sin listas duplicadas por tildes (`Si`/`Sí`); cada `use` apunta a un `define` existente (un nombre inexistente deja la pregunta sin categorías); `define` cerrado con `};`; sin comas colgantes | MEDIA (ALTA si deja preguntas sin categorías o no compila) |
| QA-20 | Bloques rotados | Módulos/publicidades a rotar están en `block fields` con orden rotatorio, no como un `info` | ALTA |
| QA-21 | Cuotas | Cada dimensión de la tabla de cuotas tiene `CUOTA_*` en el MDD y asignación en la lógica | ALTA |
| QA-22 | MaxDiff | Estructura de versión/sets completa, validación más/menos y asignación de diseño | ALTA |
| QA-23 | INTRO/INFO | Las intros del cuestionario existen en su posición; no hay `INICIO`, `INFO_INTRO_1`, `INFO_LINK`, `LINK`, `ID_BASE` inventadas | MEDIA |
| QA-24 | Variables de sistema | Encabezado iField con `SystemVariables = false`; sin `SOURCEPROJECTID`/`NWB_*`/`System_*` agregadas por el generador (las que agrega la plantilla de iField al importar no son hallazgo, sección 7) | MEDIA |
| QA-25 | Fechas | Fechas/horas como `date` | MEDIA |
| QA-26 | Fotografías | Categórica con opción "Tomar foto"/"Foto adjuntada"; sin validación JS de adjunto | MEDIA |
| QA-27 | Piping | Cada "insertar/arrastrar respuesta" tiene `{#VAR#}` en el MDD o `setInsert` en la lógica, con fuente previa | MEDIA |
| QA-28 | Cobertura de lógica | Toda instrucción programable del cuestionario está implementada; no solo backcheck y filtros básicos | CRÍTICA |
| QA-29 | `goTo` | Solo dentro de `onNext`, inline; sin funciones de terminación | CRÍTICA |
| QA-30 | `TERMINATE VALID` | Implementado como terminación con `ELIMI`, nunca como salto al final | CRÍTICA |
| QA-31 | `return` en listeners | Ningún `return` desnudo dentro de `addEventListener` | CRÍTICA |
| QA-32 | Listeners Shell | Ningún `OSM.Survey.SHELL_*.addEventListener` | ALTA |
| QA-33 | Listeners duplicados | Un solo listener por variable y evento | ALTA |
| QA-34 | Backcheck | Toda pregunta con BC tiene inicio (`onEntrance`) y detención (`onNext`) condicionados a `_A1`; variantes (`BC INDIRECTO`) marcadas | ALTA |
| QA-35 | Evento correcto | Asignar/mostrar/ocultar en `onBeforeNavigateTo` del destino; salir en `onNext` | MEDIA |
| QA-36 | Redundancia | Sin `If/show/goTo` innecesarios; sin validaciones que el MDD ya resuelve | BAJA |
| QA-37 | Limpieza por saltos | Sin `clearAnswers()`/`setComment('')` de preguntas que solo se saltan | MEDIA |
| QA-38 | Variables inexistentes | Toda referencia de la lógica existe en el MDD con su capitalización | CRÍTICA |
| QA-39 | Dependencias del pipeline | Si el reporte de los prompts 01/02 menciona una herramienta o librería faltante, regístrala como dependencia, no como error de MDD/lógica | BAJA |
| QA-40 | Contenido tachado | Ninguna pregunta, opción o instrucción tachada del cuestionario está en el MDD ni programada en la lógica (terminaciones, BACKCHECK, filtros, automarcados) | CRÍTICA |
| QA-41 | Módulo NSE | Si el cuestionario pide ficha/filtro NSE: `B_NSE` estándar en el MDD y su cálculo, filtro y cuota en la lógica; sin variable NSE inventada | ALTA |
| QA-42 | Opciones con imagen | Cada pregunta con "MOSTRAR IMÁGENES" en sus opciones tiene un `{#resource:...#}` por opción | MEDIA |

# 32. EXPANSIÓN TRANSVERSAL OBLIGATORIA

Cuando encuentres un error verificable, revisa si el patrón se repite en:

- mismo bloque;
- mismo evento;
- misma función;
- preguntas espejo;
- productos 1/2/3;
- loops/grids similares;
- cuotas similares;
- aliases similares;
- rangos similares;
- rutas/namespaces similares;
- inserts/piping similares.

Reporta cada ocurrencia verificable por separado. No asumas que todos los casos son incorrectos por semejanza.

# 33. CLASIFICACIÓN DE HALLAZGOS

Usa:

- `CRÍTICA`: pérdida de datos, error de ejecución, terminación/routing incorrecto, regla esencial no implementada, referencia inexistente.
- `ALTA`: cambia elegibilidad, universo, respuesta o cuota.
- `MEDIA`: cambia presentación operativa, randomización, piping o experiencia con impacto.
- `BAJA`: diferencia documental verificable con impacto menor.
- `NO_VERIFICABLE`: falta evidencia necesaria, especialmente cuestionario en modo MDD_LOGICA.

# 34. FORMATO DE SALIDA DEL QA

Genera un único archivo:

`Reporte_QA.md`

Encabezado:

# Reporte QA — EasyScript V6
- Modo: INTEGRAL | MDD_LOGICA (+ NO_FINAL si aplica)
- Estado: APROBADO | REQUIERE_CORRECCION | QA_LIMITADO
- Cuestionario: [archivo o NO DISPONIBLE] — lectura: DOCX_COMPLETO | SOLO_TEXTO | PARCIAL
- MDD: [archivo]
- Lógica: [archivo] — FINAL | PARCIAL

## Checklist de incidencias
| ID | Control | Estado (OK / FALLA / NO_APLICA / NO_VERIFICABLE) | Hallazgo asociado |
(las 42 filas QA-01 a QA-42 de la sección 31, siempre completas)

## Cobertura
Incluye conteos de:

- preguntas/variables revisadas;
- funciones revisadas;
- reglas programables revisadas;
- loops/grids;
- cuotas;
- backchecks;
- bloqueos/no verificables.

## Hallazgos

Para cada hallazgo usa:

### [SEVERIDAD] — [PREGUNTA / VARIABLE / FUNCIÓN]
- Capa: MDD | Lógica | MDD↔Lógica | Cuestionario↔MDD | Cuestionario↔Lógica
- Control del checklist: QA-xx (si aplica)
- Regla/evidencia de origen:
- Evidencia MDD:
- Evidencia código:
- Diferencia verificable:
- Impacto:
- Acción requerida: (una línea: qué debe cambiar y dónde; sin reescribir el código ni el MDD)

Incluye fragmento exacto cuando sea necesario.

## Hallazgos de rangos/operadores
Para cada caso:
- Regla declarada:
- Implementación:
- Diferencia exacta:

## Hallazgos de visibilidad operativa
Solo para elementos ocultos/deshabilitados con impacto real:
- Estado esperado:
- Estado MDD:
- Estado código:
- Evidencia de impacto:

## No verificable
Solo cuando falte evidencia necesaria.

No reescribas código ni MDD: la "Acción requerida" describe el cambio en una línea.
No listes elementos correctos individualmente (el checklist resume lo que está OK).

# 35. ESTADO FINAL

- `APROBADO`: en modo integral, no existen inconsistencias verificables críticas/altas/medias pendientes, la cobertura está completa y ningún control del checklist está en `FALLA`.
- `REQUIERE_CORRECCION`: existe al menos un hallazgo verificable que debe resolverse antes de declarar el resultado listo, o el modo es `NO_FINAL`.
- `QA_LIMITADO`: falta `Cuestionario.docx` u otra evidencia imprescindible; no puede afirmarse QA integral.

Si no se detectan hallazgos en modo integral, indica de forma breve que no se detectaron inconsistencias verificables dentro del alcance revisado.

# 36. CRITERIO FINAL ANTES DE REPORTAR

Antes de emitir cualquier hallazgo, responde internamente:

1. ¿La regla está vigente?
2. ¿Existe evidencia suficiente?
3. ¿La estructura/código la contradice?
4. ¿La diferencia afecta flujo, dato, visibilidad o operación?
5. ¿El elemento extra está oculto antes de afectar?
6. ¿Se usa posteriormente?
7. ¿El evento es alcanzable?
8. ¿Existe equivalencia funcional válida?
9. ¿La diferencia puede provenir de extracción/maquetación?
10. ¿El hallazgo puede demostrarse con fragmentos concretos?

Solo reporta si la evidencia confirma una inconsistencia real.

CLAVE DE LECTURA DEL PROMPT 03: QA-V6-MACA-8061
