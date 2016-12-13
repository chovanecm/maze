import maze


class GridModel:
    def __init__(self, array):
        self.array = array
        self.goal = maze.find_goal(self.array)
        self.on_goal_removed = 0
        self.listeners = []
        if self.goal is not None:
            self.goal = tuple(self.goal)

    def set_goal(self, row, column):
        if self.goal is not None:
            self.array[self.goal] = self.on_goal_removed
            self._on_event(*self.goal, self.on_goal_removed)
        self.on_goal_removed = self.array[row, column]
        self.goal = (row, column)
        self.array[row, column] = 1
        self._on_event(row, column, 1)

    def set_field(self, row, column, value):
        if value == 1:
            return self.set_goal(row, column)
        else:
            if (row, column) == self.goal:
                self.goal = None
            self.array[row, column] = value
            self._on_event(row, column, value)

    def _on_event(self, row, column, value):
        for listener in self.listeners:
            listener(row, column, value)
