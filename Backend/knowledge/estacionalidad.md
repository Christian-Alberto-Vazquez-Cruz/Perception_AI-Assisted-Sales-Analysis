# Estacionalidad y calendario de una tienda

Guía de hipótesis para comercio local, con ejemplos de México cuando resulte pertinente. No contiene el calendario verificado de la localidad ni pronósticos. Ninguna festividad, pago o condición meteorológica se considera ocurrida o causal solo porque el nombre del mes coincida. La fuente principal para conocer el comportamiento de la tienda sigue siendo su propio historial.

## Estacionalidad frente a calendario y tendencia
La estacionalidad describe movimientos que se repiten en épocas comparables; un cambio aislado no demuestra ese patrón. El calendario también cambia la duración de los meses y su composición de días. Tendencia y variación mensual no son lo mismo: una caída puntual puede ocurrir dentro de una serie que antes crecía.

INEGI distingue efectos de calendario, estacionales y tendencia en series económicas: [explicación metodológica](https://www.inegi.org.mx/app/tablero/). Esa metodología aporta contexto, no demuestra un efecto en esta tienda ni convierte su resumen en una serie ajustada.

Con un solo año no confirmar recurrencia anual. No afirmar que pandas ha desestacionalizado, ajustado por inflación o elaborado un pronóstico: esas funciones no están disponibles en el resumen actual.

## Meses de distinta duración y cobertura
Un mes corto puede registrar menor importe total simplemente porque incluye menos días potenciales de venta. También importa cuántos días estuvo abierta la tienda y cuáles fueron capturados. Un mes con registros hasta una fecha temprana puede estar incompleto, pero no asumirlo sin confirmación del dueño.

Antes de interpretar una caída mensual, revisar las fechas y días con registros que proporciona pandas. Tener registros en todos los días no garantiza que cada día esté completamente capturado. No inventar ventas de días faltantes.

Comparaciones por día abierto o por periodos equivalentes solo pueden cuantificarse si pandas aporta esas métricas. No normalizar mentalmente los totales ni tratar el número de registros como número de días o de tickets.

## Fines de semana y composición del mes
Viernes, sábados y domingos pueden tener patrones distintos según horarios, ubicación y clientes. Una tienda cercana a oficinas puede comportarse de otra forma que una tienda residencial; la ubicación no está incluida en el JSON.

Dos meses pueden contener diferente cantidad de fines de semana. Por ello, un cambio de importe total no confirma por sí solo pérdida de demanda. Revisar el promedio por día de semana observado y su cobertura cuando estén disponibles en las métricas.

Para considerar ajustes de reposición, buscar repetición en días comparables y confirmar eventos. No extrapolar un sábado fuerte a todos los sábados ni afirmar que abrir más horas será rentable sin datos de horarios y costos.

## Marzo y fechas móviles
Si las ventas bajan en marzo o cambian entre marzo y abril, considerar como hipótesis un desplazamiento de rutinas por vacaciones o celebraciones de fecha móvil. Semana Santa puede caer en marzo o abril; comprobar las fechas del año y el calendario local antes de mencionarla como explicación específica.

El efecto puede tener direcciones distintas: salida de residentes, visitantes o cambios en asistencia escolar y laboral. No afirmar que siempre reduce ventas ni que afecta igual a Botanas, Bebidas y Abarrotes.

Contrastar días abiertos, categorías afectadas, fechas concretas e historial propio. El resumen mensual no identifica ventas por vacaciones ni permite aislar su efecto. Una caída concentrada también requiere descartar faltantes y cambios comerciales.

## Quincenas, festividades y clima
Pagos, celebraciones y clima son hipótesis de contexto, no variables observadas en el JSON. Su efecto depende de la clientela, localidad, surtido, apertura y coincidencia con otras acciones.

Si el dueño menciona una quincena, festividad o episodio climático, solicitar la fecha y el registro que lo respalda. Contrastar el patrón por categoría y días comparables. No dar por hecho el día de pago de todos los clientes ni condiciones meteorológicas por el nombre del mes.

Cuando no haya calendario ni datos externos, presentar este contexto como posibilidad de menor certeza. Una cifra agregada nacional o una guía general no identifica la causa de una caída local. No cuantificar el efecto atribuible al evento.

## Vacaciones y regreso a clases
Cambios en asistencia escolar y rutinas familiares pueden modificar compras de paso, horarios y productos elegidos. El efecto potencial depende de la cercanía real a escuelas, viviendas o zonas de trabajo; no asumir esa ubicación.

Comprobar el calendario escolar aplicable al año y localidad, además del horario de la tienda. Una categoría asociada a consumo práctico podría cambiar, pero eso no autoriza a predecir demanda sin historial. Preguntar si hubo cambios observados de afluencia o surtido.

Si las ventas caen solo en una categoría, revisar también disponibilidad y promociones. Si caen en todas, confirmar cobertura y apertura antes de atribuir el resultado a vacaciones. Las comparaciones específicas por periodo escolar requieren métricas adicionales.

## Calor, lluvia y cambios de temperatura
En una tienda, las preferencias por bebidas, productos de consumo inmediato o compras para el hogar podrían variar con las condiciones del tiempo. La lluvia también podría afectar desplazamientos o entregas. Son mecanismos posibles y no resultados universales.

El archivo no contiene temperatura, precipitación ni incidencias de reparto. Para investigar una relación, pedir registros meteorológicos locales y fechas de problemas operativos, y contrastarlos con las ventas correspondientes mediante cálculos externos o de pandas.

No afirmar «bajó por la lluvia» ni «las bebidas subieron por calor» solo al observar un mes. Distinguir estacionalidad climática recurrente de un episodio excepcional. No inventar correlaciones, umbrales de temperatura ni porcentajes de efecto.

## Celebraciones, promociones y compras anticipadas
Una celebración local o campaña comercial puede desplazar compras hacia días anteriores y dejar una comparación posterior desfavorable. El periodo previo puede ser excepcionalmente alto, sin que el posterior represente un deterioro permanente.

En México pueden investigarse, según la clientela y el año, celebraciones familiares, fiestas locales o campañas como Buen Fin. Verificar fechas y participación real de la tienda; una campaña nacional no demuestra descuentos ni ventas extraordinarias locales.

Pedir al dueño calendario de acciones y detalle de productos. Revisar picos y meses cercanos ya calculados. No asegurar que la caída posterior es compensación o compras adelantadas sin evidencia, ni recomendar repetir una campaña sin conocer costos y resultados propios.

## Cierres, abastecimiento y eventos del entorno
Obras cercanas, cambios de acceso, fallas de servicios, horarios especiales o problemas de suministro pueden coincidir con variaciones de ventas. Son eventos operativos o del entorno, no necesariamente estacionalidad.

Comprobar que ocurrieron en la localidad y fechas analizadas. Solicitar incidencias, días abiertos, entregas y observaciones del dueño. Si faltan ventas de ciertos días, no convertir automáticamente esa ausencia en cierre confirmado.

Una explicación de acceso o afluencia debería contrastarse con varias categorías y registros adicionales; una de suministro, con existencias y productos afectados. No presentar hechos del barrio, competencia nueva ni eventos locales que no figuren en las fuentes o contexto aportado.

## Comparaciones anuales y efecto de una base excepcional
Comparar el mismo mes de distintos años puede ayudar a investigar recurrencia, pero requiere datos comparables de apertura, surtido, promociones y calendario. El mismo nombre de mes no garantiza igual número de fines de semana ni fechas equivalentes de festividades.

El resumen actual proporciona variaciones entre meses consecutivos; no asumir que incluye variaciones interanuales o ajustes de calendario. Si faltan esos cálculos, indicar que pandas tendría que prepararlos antes de cuantificarlos.

Un año anterior con cierre, promoción o evento excepcional puede distorsionar la comparación. Separar cambios nominales de precios y cantidades sin inventar un ajuste de inflación. No proyectar un crecimiento anual ni declarar un patrón estacional con una sola coincidencia.
