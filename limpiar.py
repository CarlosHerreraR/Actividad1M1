"""
Simulación de robots de limpieza utilizando el framework Mesa.

Autores: Andrés Cabrera Alvarado, Carlos Yahir Herrera
Fecha de creación: 3 de noviembre de 2024
"""

from mesa.visualization.modules import ChartModule
from robot import *
import mesa
import random
from mesa.visualization.modules import TextElement

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

class CleanPercentageElement(TextElement):
    #def render(self, model):
        #return f"Cleaned: {model.get_clean_percentage():.2f}%"
    def render(self, model):
        return f"""
        <div style="
            position: absolute;
            right: 25px;
            top: 80px;
            font-size: 20px;
            font-weight: bold;
            color: black;
        ">
            Cleaned: {model.get_clean_percentage():.2f}%
        </div>
        """

clean_percentage_element = CleanPercentageElement()

# Start mesa server
server = mesa.visualization.ModularServer(
    CleaningRobots,
    [grid, chart, clean_percentage_element],
    "Cleaning robots",
    {"R": diceSize(),
     "C": diceSize(),
     "width": x,
     "height": y,
     "max_steps": 100}
)
server.port = 8080
server.launch()
