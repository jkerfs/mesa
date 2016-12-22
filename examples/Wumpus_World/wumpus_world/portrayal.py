from .character import State

base_path = "/local/resources/"



def portray_character(cell):
    assert cell is not None
    imgs = {State.Left: "left.png", State.Right: "right.png", State.Up: "up.png", State.Down: "down.png" }
    return {
        "Shape": "image",
        "w": 1,
        "h": 1,
        "url": base_path + imgs[cell.state],
        "Layer": 10,
        "opacity": .2
    }

def portray_environment(cell):
    assert cell is not None
    urls = {"B": "breeze.png", "S": 'stench.png', "P": "pit.png", "W": "wumpus.png", "G": "coins.png"}
    if cell in urls:
        return {
            "Shape": "image",
            "w": 1,
            "h": 1,
            "url": base_path + urls[cell],
            "Layer": 10,
            "opacity": .2
        }
    else:
        return {
            "Shape": "rect",
            "w" : 1,
            "h": 1,
            "Filled": "true",
            "Layer":10,
            "Color": "white"
        }

