import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

direction_to_marker = dict(zip(["down", "up", "left", "right"], ["v", "^", "<", ">"]))


class MatplotlibEngine:
    """ Visualize Model Using Matplotlib. """
    verbose = True

    model_name = "Mesa Model"
    model_cls = None  # A model class
    portrayal_method = None
    canvas_width = 500
    canvas_height = 500
    grid_height = 0
    grid_width = 0

    max_steps = 100000

    model_args = ()
    model_kwargs = {}

    def __init__(self, model_cls, visualization_elements, name="Mesa Model",
                 *args, **kwargs):
        """ Create a new visualization engine with the given elements. """
        # Prep visualization elements:
        self.visualization_elements = visualization_elements

        # Initializing the model
        self.model_name = name
        self.model_cls = model_cls

        self.model_args = args
        self.model_kwargs = kwargs
        self.reset_model()

    def reset_model(self):
        """ Reinstantiate the model object, using the current parameters. """
        self.model = self.model_cls(*self.model_args, **self.model_kwargs)

    def _render_model(self, fig):
        visualization_state = []
        for element in self.visualization_elements:
            element_state = element.render(self.model)
            visualization_state.append(element_state)
            self.grid_height, self.grid_width = element.grid_height, element.grid_width
        plt.xlim((0, self.grid_width - 5))
        plt.ylim((0, self.grid_height - .5))
        circles = []
        squares = []
        arrows = defaultdict(list)
        annotations = []
        for viz in visualization_state[0][0]:
            if viz['Shape'] == 'circle':
                circles.append(viz)
            elif viz['Shape'] == 'square':
                squares.append(viz)
            elif viz['Shape'] == 'arrow':
                arrows[viz['Dir']].append(viz)
            if 'Text' in viz:
                annotations.append(viz)
        if len(circles) > 0:
            circles = pd.DataFrame(circles)
            plt.scatter(circles['x'], circles['y'], s=circles['Size'], marker='o', color=circles['Color'])
        if len(squares) > 0:
            squares = pd.DataFrame(squares)
            plt.scatter(squares['x'], squares['y'], s=squares['Size'], marker='s', color=squares['Color'])
        for dr in arrows.keys():
            if len(arrows[dr]) > 0:
                df = pd.DataFrame(arrows[dr])
                marker = direction_to_marker[dr]
                plt.scatter(df['x'], df['y'], marker=marker, s=df['Size'], color=df['Color'])

        for shape in annotations:
            color = shape.get("Text_Color", "black")
            plt.annotate(shape['Text'], (shape['x'], shape['y']),
                         horizontalalignment="center",
                         verticalalignment="center",
                         color=color)

        ax = fig.gca()
        ax.set_xticks(np.arange(0, self.grid_width + 1, 1) - .5)
        ax.set_yticks(np.arange(0, self.grid_height + 1, 1) - .5)
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        plt.grid()

    def render_steps(self, figsize, plotshape, steps):
        self.reset_model()
        fig = plt.figure(figsize=figsize)
        steps = sorted(steps)
        for i, s in enumerate(steps):
            while self.model.schedule.steps < s:
                self.model.schedule.step()
            plt.subplot(plotshape[0], plotshape[1], i + 1)
            self._render_model(fig)
            plt.title("Step #" + str(s))
        return fig
