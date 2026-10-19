# Guía de diagnóstico de ventas de una sola tienda

Guía propia de razonamiento comercial. Los patrones sirven para priorizar verificaciones; no prueban causas. Cada sección se recupera por separado. Usar solamente cifras calculadas por pandas y fuentes disponibles: la guía no autoriza calcular métricas nuevas ni completar datos ausentes.

## Caída concentrada en una categoría
Patrón: disminuyen las unidades o el importe de una categoría mientras las demás permanecen relativamente estables. Una explicación específica de esa categoría merece investigarse antes que una crisis general de la tienda.

Hipótesis: faltantes de productos, cambio de surtido, fin de una promoción, menor visibilidad o cambio en preferencias. Para Botanas, por ejemplo, revisar si faltaron presentaciones habituales; el nombre de la categoría no demuestra ese faltante.

Comprobar días comparables, registro por categoría, existencias, entregas y cambios comerciales. Si se confirma falta de disponibilidad, corregir reposición; si no, revisar surtido y promociones. No atribuir toda la caída a una única causa ni afirmar que las otras categorías están estables sin revisar sus métricas.

## Caída general entre meses
Patrón: varias categorías pierden unidades o importe en el mismo periodo. Primero revisar un factor compartido: menos días registrados o abiertos, cierre temporal, falla de captura, horario reducido o una base anterior excepcional.

Menor afluencia, cambios del entorno y pérdida de demanda son hipótesis posteriores, no conclusiones del JSON. Solicitar días de apertura, incidencias, promociones y, si existe, conteo de visitas. Si solo hay ventas agregadas no se puede distinguir menos clientes de una compra diferente por cliente.

Acción inicial: verificar integridad y cobertura antes de proponer descuentos generales. Comparar la evolución de cada categoría con el total; una categoría grande puede explicar la caída global sin que todas empeoren.

## Unidades suben pero importe baja
Patrón: aumenta la cantidad vendida de una categoría, pero disminuye su importe respecto del mismo periodo anterior. Se vende más volumen y se ingresa menos; no describirlo simplemente como crecimiento de ventas.

Hipótesis: mayor peso de productos económicos, descuentos, promociones por volumen o cambios de presentación. Esto es compatible con menor valor medio efectivo de las unidades, pero no prueba que cada producto haya bajado de precio. Solo citar un valor medio si pandas lo proporciona; no calcularlo en la respuesta.

Pedir precios, descuentos, mezcla por producto y costos. Revisar una promoción si se confirma que explica el patrón. No concluir pérdida de margen: faltan costos, mermas y condiciones de compra.

## Unidades bajan pero importe sube
Patrón: la categoría vende menos unidades y registra mayor importe. El aumento monetario no demuestra una recuperación de volumen ni mayor afluencia.

Hipótesis: mayor participación de productos de más valor, menor descuento, cambio de presentaciones o aumento de precios. Revisar precios y ventas por producto antes de elegir una explicación. Unidades de categorías distintas pueden representar objetos muy diferentes: no tratarlas como una medida homogénea del consumo.

Acción: identificar si se están perdiendo productos de compra frecuente o alternativas económicas. Mantener opciones de acceso si la evidencia lo justifica. No afirmar que mejoró la rentabilidad ni atribuir el cambio a inflación sin datos externos y costos.

## Unidades e importe bajan a la vez
Patrón: ambas métricas disminuyen. Es compatible con menor volumen registrado, pero no identifica su causa. Diferenciar si el movimiento se limita a una categoría o aparece en toda la tienda.

Hipótesis: faltantes, menos días comparables, fin de una promoción, cambio de horarios o menor demanda. Verificar primero cobertura, registros e inventario; después contrastar decisiones comerciales y contexto local.

Priorizar la investigación usando las diferencias absolutas por categoría ya calculadas, además de los porcentajes. Una caída porcentual grande en una categoría pequeña puede tener menor impacto monetario que una caída moderada en otra. No crear rankings de impacto ni sumas nuevas si no están incluidos en las métricas.

## Unidades estables e importe cambia
Patrón: las unidades varían poco mientras el importe sube o baja. Revisar mezcla de productos, presentaciones, precios efectivos y descuentos, antes de interpretar un cambio en cantidad demandada.

Estabilidad requiere leer la variación observada; la guía no establece un umbral universal. Un porcentaje pequeño con una base grande puede tener importancia operativa. No confundir unidades con tickets ni con clientes.

Solicitar historial de precios y promociones por producto. Si una rebaja se confirma, valorar sus resultados usando unidades e importe por separado y costos externos. Sin ese historial, presentar explicaciones alternativas y no afirmar que el dueño cambió precios.

## Crecimiento simultáneo de unidades e importe
Patrón: ambas métricas aumentan. Puede ser una mejora comercial, más días registrados o un evento excepcional. Revisar cobertura y repetición del crecimiento antes de extrapolarlo.

Hipótesis: mayor disponibilidad, promoción efectiva, surtido más adecuado o demanda temporal. Comprobar registros de reposición y acciones comerciales. No prometer que el crecimiento continuará ni aumentar compras solo por un mes favorable.

Acción: identificar categorías que crecen con consistencia y verificar capacidad de reposición y costos. Una mejora de importe no prueba beneficio; una promoción puede aumentar ventas y reducir margen. No se pueden obtener tickets medios ni tasas de conversión con este JSON.

## Categorías que se compensan entre sí
Patrón: el total cambia poco, pero unas categorías bajan y otras suben. La estabilidad del total puede ocultar una modificación importante del negocio.

Hipótesis: sustitución entre opciones, cambios de surtido, disponibilidad desigual o promociones dirigidas. La evolución opuesta no demuestra que los mismos clientes hayan sustituido un producto por otro: faltan tickets y detalle de productos.

Comprobar cambios de exhibición, precios y faltantes. Revisar las categorías por separado antes de intervenir. No recomendar eliminar una categoría solo por su menor importe: puede aportar compras complementarias y no se conocen costos ni margen. Las contribuciones numéricas al total requieren métricas precalculadas.

## Picos y días de semana
Los picos diarios son los mayores importes observados, no anomalías estadísticas demostradas. Un evento, una venta extraordinaria, compras agrupadas o una captura duplicada son explicaciones alternativas a contrastar.

Un día de semana con mayor importe acumulado puede tener más fechas registradas. Usar el promedio por día observado cuando pandas lo aporte; tampoco ese promedio garantiza días completos ni separa efectos de promociones.

Revisar comprobantes, calendario de acciones y apertura de los días destacados. Preparar reposición solo si el patrón se repite y existe capacidad de venta. Un pico aislado no justifica cambios permanentes de horarios, plantilla o compras.

## Recuperación después de una caída
Patrón: la categoría vuelve a crecer después de un periodo bajo. Una subida desde una base deprimida puede parecer grande sin recuperar el nivel previo.

Leer los importes y unidades de los periodos disponibles, no solo el último porcentaje. Si pandas no incluye la comparación requerida, indicar que falta esa métrica; no calcular una recuperación acumulada ni encadenar porcentajes mentalmente.

Hipótesis: reposición tras faltantes, reanudación de horarios o final de una incidencia. Comprobar su registro antes de atribuir la recuperación a una acción. Mantener seguimiento en periodos comparables y evitar presentar un rebote puntual como tendencia sostenida.

## Datos insuficientes y base cero
Sin mes anterior consecutivo no hay variación mensual comparable. Con base anterior cero no existe porcentaje finito; un valor null no equivale a cambio de cero por ciento. No traducirlo como estabilidad.

Un día o categoría ausente puede significar ventas no registradas, cierre o ausencia de operaciones; el JSON no permite elegir entre ellos. Revisar también posibles duplicados y categorías escritas de formas distintas antes de interpretar un salto.

La ausencia de inventario, costos, tickets, productos y visitas impide confirmar faltantes, rentabilidad, ticket medio o conversión. Si faltan datos para elegir una causa, explicar lo observado, ofrecer hipótesis diferenciadas y pedir el registro mínimo que permitiría comprobarlas.

## Importe nominal, volumen y causalidad
El importe es el valor monetario registrado, sin moneda especificada ni ajuste por inflación. Unidades refleja cantidad registrada, no clientes ni volumen físico homogéneo. No etiquetar el importe con una divisa que no está en los datos.

Separar tres niveles al explicar: hecho medido, hipótesis compatible y verificación pendiente. Coincidencia temporal no demuestra causalidad. No usar un indicador nacional para afirmar lo que pasó en esta tienda.

Cuando varias hipótesis encajen, priorizar revisiones de registro y operación que puedan comprobarse rápidamente. No asignar probabilidades, porcentajes de responsabilidad ni niveles de certeza numéricos sin evidencia. Para cuantificar nuevas relaciones se necesita un cálculo de pandas, no una inferencia verbal del modelo.
