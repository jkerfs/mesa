from mesa.visualization.ModularVisualization import ModularServer

from wumpus_world.portrayal import portray_environment, portray_character
from wumpus_world.model import WumpusWorld
from wumpus_world.visualization import WumpusWorldCanvasGrid

canvas_element = WumpusWorldCanvasGrid(portray_environment, portray_character, 4, 4, 800, 800)

server = ModularServer(WumpusWorld, [canvas_element], "Wumpus World", 4, 4)
