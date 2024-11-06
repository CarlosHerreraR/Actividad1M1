"""
Simulación de robots de limpieza utilizando el framework Mesa.

Autores: Andrés Cabrera Alvarado, Carlos Yahir Herrera
Fecha de creación: 3 de noviembre de 2024
"""

import numpy as np
import matplotlib.pyplot as plt
import mesa
import random

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
        self.max_steps = max_steps  # Maximum steps for simulation
        self.current_step = 0  # Initialize current step counter
        self.running = True  # Ensure simulation runs initially
        
        # Create robots
        for i in range(self.num_agentsR):
            a = RobotAgent(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (0, 0))
        
        self.num_agentsC += self.num_agentsR
        
        # Create cells
        for o in range(self.num_agentsR, self.num_agentsC):
            b = DirtyCell(o, self)
            self.schedule.add(b)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(b, (x, y))

        print("Initial dirty cells:", self.num_agentsC - self.num_agentsR)

        self.datacollector = mesa.DataCollector(
            agent_reporters={"Steps": "pos"}
        )
        
    def all_cells_clean(self):
        # Checks if all dirty cells are clean
        return all(agent.isClean for agent in self.schedule.agents if isinstance(agent, DirtyCell))

    def get_clean_percentage(self):
        # Calculate the percentage of clean cells
        clean_cells = sum(1 for agent in self.schedule.agents if isinstance(agent, DirtyCell) and agent.isClean)
        total_dirty_cells = self.num_agentsC - self.num_agentsR
        return (clean_cells / total_dirty_cells) * 100

    def total_moves(self):
        # Calculate the total number of moves by all agents
        return sum(agent.moves for agent in self.schedule.agents if isinstance(agent, RobotAgent))

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        self.current_step += 1

        # Stop the simulation if all cells are clean or max steps are reached
        if self.all_cells_clean() or self.current_step >= self.max_steps:
            print("Simulation ended after steps:", self.current_step)
            print("Percentage of clean cells:", self.get_clean_percentage())
            print("Total moves made by all agents:", self.total_moves())
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
