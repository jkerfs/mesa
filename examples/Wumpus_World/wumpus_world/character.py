import random

from mesa import Agent
from mesa.space import SingleGrid


class Character(Agent):
    def __init__(self, pos, model):
        '''
        Create a cell, in the given state, at the given x, y position.
        '''
        super().__init__(pos, model)
        self.x, self.y = pos

        self.pit_locs = SingleGrid(4, 4, False)
        self.wumpus_locs = SingleGrid(4, 4, False)
        for i in range(4):
            for j in range(4):
                self.pit_locs.place_element(1, (i, j))
                self.wumpus_locs.place_element(1, (i, j))

        original_safe_cells = [(0, 0), (0, 1), (1, 0)]
        for pos in original_safe_cells:
            self.pit_locs.place_element(0, pos)
            self.wumpus_locs.place_element(0, pos)

    @property
    def isAlive(self):
        return True

    @property
    def neighbors(self):
        return self.model.environment_grid.iter_neighborhood((self.x, self.y), False)

    def step(self):
        '''
        Compute if the cell will be dead or alive at the next tick.  This is
        based on the number of alive or dead neighbors.  The state is not
        changed here, but is just computed and stored in self._nextState,
        because our current state may still be necessary for our neighbors
        to calculate their next state.
        '''

        cur_pos = (self.x, self.y)
        cur_contents = self.model.environment_grid.get_cell_list_contents([(self.x, self.y)])
        if "G" in cur_contents:
            self.model.running = False
            return
        if "B" not in cur_contents:
            for pos in self.pit_locs.get_neighborhood(cur_pos, False):
                self.pit_locs.place_element(0, pos)
        if "S" not in cur_contents:
            for pos in self.wumpus_locs.get_neighborhood(cur_pos, False):
                self.wumpus_locs.place_element(0, pos)

        options = []
        for pos in self.neighbors:
            has_wumpus = self.wumpus_locs.get_cell_list_contents([pos])[0]
            has_pit = self.pit_locs.get_cell_list_contents([pos])[0]
            if has_wumpus + has_pit == 0:
                options.append(pos)

        self.x, self.y = random.choice(options)
        self.model.agent_grid.move_agent(self, (self.x, self.y))

    def advance(self):
        '''

        '''
        pass