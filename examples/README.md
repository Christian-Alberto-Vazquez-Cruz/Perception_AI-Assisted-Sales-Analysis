# Ejemplo ampliado de ventas

`ventas_realistas_2026.json` contiene datos sintéticos de una sola tienda abierta todos los días del 1 de enero al 30 de junio de 2026. Hay 181 días, seis categorías y 1.086 registros.

Las categorías son Bebidas, Botanas, Abarrotes, Lácteos, Limpieza y Panadería. Se simulan fluctuaciones diarias, mayor movimiento de fin de semana y quincena, y precios medios distintos entre categorías y días.

Escenarios incorporados para probar:

- Botanas tiene una caída de unidades e importe en marzo y recuperación posterior.
- Bebidas aumenta unidades en abril, pero reduce su importe por un menor valor medio efectivo simulado. Las gráficas de unidades e importe tienen comportamientos diferentes.
- El 10 de mayo tiene un pico de ventas simulado.
- Los meses tienen distinto número de días; comparar totales mensuales también refleja esa diferencia.


Para usarlo, se selecciona el botón Reemplazar JSON y se elige el archivo `ventas_realistas_2026.json`. Esto sustituye el dataset activo. 

Preguntas sugeridas:

- ¿Qué pasó con Botanas en marzo respecto de febrero?
- ¿Qué categoría tuvo la mayor caída de importe en marzo?
- ¿Qué cambió en las unidades y el importe de Bebidas en abril?
- ¿Qué días tuvieron el mayor importe?
- ¿Cómo evolucionaron las ventas entre enero y junio?

Para regenerar exactamente el mismo archivo, desde la raíz del proyecto:

```powershell
.\.venv\Scripts\python.exe -m examples.generar_ventas_demo
```
