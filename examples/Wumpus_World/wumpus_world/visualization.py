# -*- coding: utf-8 -*-
"""
Modular Canvas Rendering
========================

Module for visualizing model objects in grid cells.

"""
from collections import defaultdict
from mesa.visualization.modules.CanvasGridVisualization import CanvasGrid

class WumpusWorldCanvasGrid(CanvasGrid):
    def __init__(self, portray_environment, portray_character, *args):
        self.portray_environment = portray_environment
        self.portray_character = portray_character
        super(WumpusWorldCanvasGrid, self).__init__(portray_character, *args)

    def render(self, model):
        grid_state = defaultdict(list)
        for x in range(model.agent_grid.width):
            for y in range(model.agent_grid.height):
                cell_objects = model.agent_grid.get_cell_list_contents([(x, y)])
                obstacles = model.environment_grid.get_cell_list_contents([(x,y)])
                for obs in obstacles:
                    for o in obs:
                        portrayal = self.portray_environment(o)
                        portrayal["x"] = x
                        portrayal["y"] = y
                        grid_state[portrayal["Layer"]].append(portrayal)

                for obj in cell_objects:
                    portrayal = self.portray_character(obj)
                    if portrayal:
                        portrayal["x"] = x
                        portrayal["y"] = y
                        grid_state[portrayal["Layer"]].append(portrayal)

        return grid_state
