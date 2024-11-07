"""
Simulación de robots de limpieza utilizando el framework Mesa.

Autores: Andrés Cabrera Alvarado, Carlos Yahir Herrera
Fecha de creación: 3 de noviembre de 2024
"""

import numpy as np
import matplotlib.pyplot as plt
import mesa
import random
import time  # Importar time para medir el tiempo

# Robot agent.
class RobotAgent(mesa.Agent):
    """
    Robot agent that moves and cleans cells in a grid.
    
    Attributes:
    - unique_id: id of the agent.
    - model: Model to which the agent belongs.
    - vacuuming: Indicates the state of the agent if it's currently vacuuming.
    - moves: Counts the number of moves made by the agent.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.vacuuming = False
        self.moves = 0

    # Gets possible moves from 8 spaces around the agent.
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
                self.pos,
                moore=True,
                include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        self.moves += 1  # Increment moves each time the agent moves

    # Cleans an agent of type DirtyCell by setting isClean to True.
    def clean(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for i in cellmates:
            if isinstance(i, DirtyCell) and not i.isClean:
                i.isClean = True
                self.vacuuming = True

    # Executes a single action step, moving and cleaning based on the agent's state.
    def step(self):
        if not self.vacuuming:
            self.move()
            self.clean()
        else:
            self.clean()
            self.vacuuming = False


# Represents the dirty cell, for the agent to clean.
class DirtyCell(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.isClean = False  # Initially, all cells are dirty

    def step(self):
        pass  # Dirty cells do not move


# Represents the cleaning robots.
class CleaningRobots(mesa.Model):
    def __init__(self, R, C, width, height, max_steps):
        self.num_agentsR = R
        self.num_agentsC = C
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.max_steps = max_steps
        self.current_step = 0
        self.running = True

        # Tiempo inicial
        self.start_time = time.time()
        self.elapsed_time = None  # Inicializa elapsed_time como None

        # Crear robots y celdas
        for i in range(self.num_agentsR):
            a = RobotAgent(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (0, 0))
        
        self.num_agentsC += self.num_agentsR
        
        for o in range(self.num_agentsR, self.num_agentsC):
            b = DirtyCell(o, self)
            self.schedule.add(b)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(b, (x, y))

        self.datacollector = mesa.DataCollector(agent_reporters={"Steps": "pos"})

    def all_cells_clean(self):
        return all(agent.isClean for agent in self.schedule.agents if isinstance(agent, DirtyCell))

    def get_clean_percentage(self):
        clean_cells = sum(1 for agent in self.schedule.agents if isinstance(agent, DirtyCell) and agent.isClean)
        total_dirty_cells = self.num_agentsC - self.num_agentsR
        return (clean_cells / total_dirty_cells) * 100

    def total_moves(self):
        return sum(agent.moves for agent in self.schedule.agents if isinstance(agent, RobotAgent))

    def get_elapsed_time(self):
        return self.elapsed_time  # Método para obtener elapsed_time

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        self.current_step += 1

        if self.all_cells_clean() or self.current_step >= self.max_steps:
            # Calcula elapsed_time al finalizar la simulación
            self.elapsed_time = time.time() - self.start_time
            print(f"Simulation ended after steps: {self.current_step}")
            print(f"Total time taken: {self.elapsed_time:.2f} seconds")
            print(f"Percentage of clean cells: {self.get_clean_percentage():.2f}%")
            print(f"Total moves made by all agents: {self.total_moves()}")
            self.running = False


# Pruebas con matplotlib
if __name__ == '__main__':
    model = CleaningRobots(5, 10, 10, 10, max_steps=100)  # Set max steps
    while model.running:
        model.step()

    # Show the final state of the grid
    agent_counts = np.zeros((model.grid.width, model.grid.height))
    for cell in model.grid.coord_iter():
        cell_content, x, y = cell
        agent_count = len(cell_content)
        agent_counts[x][y] = agent_count
    plt.imshow(agent_counts, interpolation="nearest")
    plt.colorbar()
    plt.show()
