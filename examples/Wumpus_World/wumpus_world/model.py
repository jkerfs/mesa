from wumpus_world.character import Character

from mesa import Model
from mesa.space import Grid, MultiGrid
from mesa.time import SimultaneousActivation


layout = [
    [['S'], [' '], ['B'], ['P']],
    [['W'], ['S', 'B', 'G'], ['P'], ['B']],
    [['S'], [' '], ['B'], [' ']],
    [[' '], ['B'], ['P'], ['B']]
]

class WumpusWorld(Model):
    '''
    Represents the 2-dimensional array of cells in Conway's
    Game of Life.
    '''

    def __init__(self, height, width):
        '''
        Create a new playing area of (height, width) cells.
        '''

        # Set up the grid and schedule.

        # Use SimultaneousActivation which simulates all the cells
        # computing their next state simultaneously.  This needs to
        # be done because each cell's next state depends on the current
        # state of all its neighbors -- before they've changed.
        self.schedule = SimultaneousActivation(self)

        # Use a simple grid, where edges wrap around.
        self.agent_grid = Grid(height, width, torus=False)
        self.environment_grid = MultiGrid(height, width, torus=False)

        for i, row in enumerate(layout):
            for j, entry in enumerate(row):
                self.environment_grid.place_element(entry, (j, 3-i))

        self.agent = Character((0,0), self)

        self.agent_grid.place_agent(self.agent, (0, 0))
        self.schedule.add(self.agent)
        self.running = True

    def step(self):
        '''
        Have the scheduler advance each cell by one step
        '''
        if not self.agent.isAlive:
            self.running = False
        else:
            self.schedule.step()
