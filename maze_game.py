import numpy as np
import actor
import gridmodel
import asyncio


class AbstractGridModelWrapper:
    def __init__(self, grid_model: gridmodel.GridModel):
        self.grid_model = gridmodel.GridModel(grid_model.array.copy())

    def update_actor(self, actor: actor.Actor):
        row = (int)(actor.row)
        column = (int)(actor.column)
        if tuple(self.grid_model.goal) == (row, column):
            task = actor.task  # type: asyncio.Task
            task.cancel()

    @property
    def directions(self):
        return self.grid_model.result.directions

    @property
    def cell_size(self):
        raise NotImplementedError("Cell size not implemented.")


class Game:
    def __init__(self, wrapped_grid_model: AbstractGridModelWrapper):
        # self.maze = maze.copy()
        grid_model = wrapped_grid_model.grid_model
        maze = wrapped_grid_model.grid_model.array
        dude_positions = np.argwhere(
            (maze >= min(gridmodel.GridModel.DUDE_VALUES)) & (maze <= max(grid_model.DUDE_VALUES)))

        def create_actor(row, column):
            even = actor.TeleporterActor
            odd = actor.Actor
            kind = wrapped_grid_model.grid_model.array[row, column]
            if kind % 2 == 0:
                return even(wrapped_grid_model, row, column, wrapped_grid_model.grid_model.array[row, column])
            else:
                return odd(wrapped_grid_model, row, column, wrapped_grid_model.grid_model.array[row, column])

        self.actors = [create_actor(row, column) for row, column in dude_positions]
        # remove guys from startup positions in the game copy of array
        for dude_position in dude_positions:
            maze[tuple(dude_position)] = 0

    async def run(self):
        for actor in self.actors:
            await actor.behavior()
