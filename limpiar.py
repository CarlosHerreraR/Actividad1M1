"""
Simulación de robots de limpieza utilizando el framework Mesa.

Autores: Andrés Cabrera Alvarado, Carlos Yahir Herrera
Fecha de creación: 3 de noviembre de 2024
"""

from mesa.visualization.modules import ChartModule
from robot import *
import mesa
import random

# Visualize agents and it respective color code
def agent_portrayal(agent):
    """
    Defines the visual apereancela of each agent acording to their type.

    Parameters:
    object agent which represents a robot or a dirty cell.

    Returns:
    Visual representation of the agent with it's form, color, layer, radius.
    """
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.5}
    if isinstance(agent, DirtyCell):
        if agent.isClean:
            portrayal["Color"] = "green"
        else:
            portrayal["Color"] = "grey"
    if isinstance(agent, RobotAgent):
        portrayal["Color"] = "blue"
    return portrayal

# Serves as a dice to generate random size grid
def diceSize():
    return random.randint(3, 12)

x = diceSize()
y = diceSize()

# Instanciate grid and chart
grid = mesa.visualization.CanvasGrid(agent_portrayal, x, y, 500, 500)
chart = ChartModule([{ "Label": "Steps", "Color": "Black" }], data_collector_name = 'datacollector')

# Start mesa server
server = mesa.visualization.ModularServer(
    CleaningRobots,
    [grid, chart],
    "Cleaning robots",
    {"R": diceSize(),
     "C": diceSize(),
     "width": x,
     "height": y,
     "max_steps": 100}
)
server.port = 8080
server.launch()

#una matriz que recuerde donde ha estado