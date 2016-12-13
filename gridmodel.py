import maze


class GridModel:
    GOAL_VALUE = 1
    DUDE_VALUES = range(10, 100)
    WALL_VALUE = -1

    def __init__(self, array):
        self.array = array
        self.goal = maze.find_goal(self.array)
        self.on_goal_removed = 0
        self.listeners = [lambda row, column, value: self._recalculate_paths(row, column, value)]
        self.dudes = []
        self.result = None
        if self.goal is not None:
            self.goal = tuple(self.goal)

    def set_goal(self, row, column):
        if self.array[row, column] == self.GOAL_VALUE:
            return
        if self.goal is not None:
            self.array[self.goal] = self.on_goal_removed
            self._on_event(*self.goal, self.on_goal_removed)
        self.on_goal_removed = self.array[row, column]
        self.goal = (row, column)
        self.array[row, column] = 1
        self._on_event(row, column, 1)

    def set_field(self, row, column, value):
        if self.array[row, column] == value:
            return
        if value == self.GOAL_VALUE:
            return self.set_goal(row, column)
        else:
            if (row, column) == self.goal:
                self.goal = None
                self.result = None
            if value in self.DUDE_VALUES:
                self.dudes.append((row, column))
            elif (row, column) in self.dudes:
                self.dudes.remove((row, column))
            if value == self.WALL_VALUE:
                self.result = None
            self.array[row, column] = value
            self._on_event(row, column, value)

    def _on_event(self, row, column, value):
        for listener in self.listeners:
            listener(row, column, value)

    def _recalculate_paths(self, row, column, value):
        if value in self.DUDE_VALUES and self.result is not None:
            # No need to recalculate
            return
        # Recalculate paths if there is a goal and dudes in the maze
        self.goal = maze.find_goal(self.array)
        if self.goal is not None and type(self.goal) is not tuple:
            self.goal = tuple(self.goal)
        if self.goal is not None and len(self.dudes) > 0:
            self.result = maze.analyze(self.array)
