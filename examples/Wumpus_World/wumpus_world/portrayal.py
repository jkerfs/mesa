base_path = "/local/resources/"


def portray_character(cell):
    assert cell is not None
    return {
        "Shape": "image",
        "w": 1,
        "h": 1,
        "url": base_path + "character.png",
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

