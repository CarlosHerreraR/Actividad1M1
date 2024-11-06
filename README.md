# Actividad1M1
Modelación de sistemas multiagentes con gráficas computacionales. Actividad 1 Módulo 1

# Instrucciones 
Para este problema, deberás entregar, en tu equipo de SMA, un informe en PDF que estudie las estadísticas de un robot de limpieza reactivo, así como el enlace al repositorio en Github del código desarrollado para esta actividad. El código debe ajustarse al estilo solicitado en el siguiente documento.

## Dado:
- Habitación de MxN espacios.
- Número de agentes.
- Porcentaje de celdas inicialmente sucias.
- Tiempo máximo de ejecución.
- 
Realiza la siguiente simulación:
- Inicializa las celdas sucias (ubicaciones aleatorias).
- Todos los agentes empiezan en la celda [1,1].
- En cada paso de tiempo:
- Si la celda está sucia, entonces aspira.
- Si la celda está limpia, el agente elige una dirección aleatoria para moverse (unas de las 8 celdas vecinas) y elige la acción de movimiento (si no puede moverse allí, permanecerá en la misma celda).
- Se ejecuta el tiempo máximo establecido.

Deberás recopilar la siguiente información durante la ejecución:
- Tiempo necesario hasta que todas las celdas estén limpias (o se haya llegado al tiempo máximo).
- Porcentaje de celdas limpias después del termino de la simulación.
- Número de movimientos realizados por todos los agentes.
- Analiza cómo la cantidad de agentes impacta el tiempo dedicado, así como la cantidad de movimientos realizados. Desarrollar un informe con lo observado.
