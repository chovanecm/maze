from PyQt5 import QtWidgets, uic, QtGui, QtSvg, QtCore
import maze, maze_generator as mg
import gridmodel
import numpy as np

CELL_SIZE = 32

VALUE_ROLE = QtCore.Qt.UserRole
GRASS_FILE = "pics/grass.svg"
WALL_FILE = "pics/wall.svg"
GOAL_FILE = "pics/castle.svg"
DUDE1_FILE = "pics/dude1.svg"
SVG_GRASS = QtSvg.QSvgRenderer(GRASS_FILE)
SVG_WALL = QtSvg.QSvgRenderer(WALL_FILE)
SVG_GOAL = QtSvg.QSvgRenderer(GOAL_FILE)
SVG_DUDE1 = QtSvg.QSvgRenderer(DUDE1_FILE)
SVG_LINE_PATTERN = "pics/lines/%d.svg"
# just to have 1-based indexing, we use none for the first value
SVG_LINES = [None]
for i in range(1, 16):
    SVG_LINES.append(QtSvg.QSvgRenderer(SVG_LINE_PATTERN % i))

def pixels_to_logical(x, y):
    return y // CELL_SIZE, x // CELL_SIZE


def logical_to_pixels(row, column):
    return column * CELL_SIZE, row * CELL_SIZE


class GridWidget(QtWidgets.QWidget):
    def __init__(self, grid_model):
        super().__init__()
        self.set_model(grid_model)
        # fields_with_paths is a list of (row, column, path_type) where path_type indicates
        #  which graphic should be used from pics/lines
        self.fields_with_paths = {}
        self.previous_result = None

    def set_model(self, grid_model):
        self.grid_model = grid_model
        size = logical_to_pixels(*grid_model.array.shape)
        self.fields_with_paths = {}
        self.setMinimumSize(*size)
        self.setMaximumSize(*size)
        self.resize(*size)
        self.previous_result = None
        self.update()
        self.grid_model.listeners.extend([lambda row, column, value: self.redraw_grid(row, column),
                                          lambda row, column, value: self.draw_paths(row, column, value)]
                                         )

    def paintEvent(self, event):
        rect = event.rect()
        painter = QtGui.QPainter(self)
        color = QtGui.QColor(0, 255, 0)
        # painter.fillRect(rect, color)

        row_min, col_min = pixels_to_logical(rect.left(), rect.top())
        row_min = max(row_min, 0)
        col_min = max(col_min, 0)
        row_max, col_max = pixels_to_logical(rect.right(), rect.bottom())
        row_max = min(row_max + 1, self.grid_model.array.shape[0])
        col_max = min(col_max + 1, self.grid_model.array.shape[1])

        for row in range(row_min, row_max):
            for column in range(col_min, col_max):
                # získáme čtvereček, který budeme vybarvovat
                x, y = logical_to_pixels(row, column)
                rect = QtCore.QRectF(x, y, CELL_SIZE, CELL_SIZE)

                # podkladová barva pod poloprůhledné obrázky
                white = QtGui.QColor(255, 255, 255)
                painter.fillRect(rect, QtGui.QBrush(white))

                # trávu dáme všude, protože i zdi stojí na trávě
                SVG_GRASS.render(painter, rect)

                # zdi dáme jen tam, kam patří
                if self.grid_model.array[row, column] < 0:
                    SVG_WALL.render(painter, rect)
                # goal
                if self.grid_model.array[row, column] == 1:
                    SVG_GOAL.render(painter, rect)

                line = self.fields_with_paths.get((row, column))
                if line is not None:
                    SVG_LINES[line].render(painter, rect)
                # Dudes
                if self.grid_model.array[row, column] == 10:
                    SVG_DUDE1.render(painter, rect)

    def mousePressEvent(self, event):
        row, column = pixels_to_logical(event.x(), event.y())
        shape = self.grid_model.array.shape
        if 0 <= row < shape[0] and 0 <= column < shape[1]:
            if event.button() == QtCore.Qt.LeftButton:
                self.grid_model.set_field(row, column, self.selected)
            elif event.button() == QtCore.Qt.RightButton:
                self.grid_model.set_field(row, column, 0)
            else:
                return

    def redraw_grid(self, row, column):
        self.update(*logical_to_pixels(row, column), CELL_SIZE, CELL_SIZE)

    def draw_paths(self, row, column, value):
        # If there is no goal or a new goal, remove old paths
        if self.grid_model.result != self.previous_result or value == self.grid_model.GOAL_VALUE:
            fields_to_clean = [f for f in self.fields_with_paths]
            self.fields_with_paths.clear()
            for path in fields_to_clean:
                self.redraw_grid(path[0], path[1])

        if self.grid_model.result is not None:
            if value in self.grid_model.DUDE_VALUES:
                # we only add the new path
                dudes_to_process = [(row, column)]
            else:
                # Redraw all paths
                dudes_to_process = self.grid_model.dudes
            result = self.grid_model.result
            for dude in dudes_to_process:
                try:
                    dude_path = result.path(dude[0], dude[1])
                    for i in range(1, len(dude_path) - 1):
                        path_element = dude_path[i]
                        previous_path_element = dude_path[i - 1]
                        path_field = self.fields_with_paths.get(path_element, 0)
                        direction_to_here = result.directions[tuple(previous_path_element)]
                        direction_from_here = result.directions[tuple(path_element)]
                        if direction_to_here == b"^":
                            # set bitwise flags
                            path_field = path_field | 4
                        elif direction_to_here == b"v":
                            path_field = path_field | 1
                        elif direction_to_here == b"<":
                            path_field = path_field | 8
                        elif direction_to_here == b">":
                            path_field = path_field | 2

                        if direction_from_here == b"^":
                            # set bitwise flags
                            path_field = path_field | 1
                        elif direction_from_here == b"v":
                            path_field = path_field | 4
                        elif direction_from_here == b"<":
                            path_field = path_field | 2
                        elif direction_from_here == b">":
                            path_field = path_field | 8

                        self.fields_with_paths[path_element] = path_field
                except IndexError:
                    # Probably no way from this point
                    continue

            for path_element in self.fields_with_paths:
                self.redraw_grid(path_element[0], path_element[1])
        self.previous_result = self.grid_model.result



def main():
    app = QtWidgets.QApplication([])
    window = QtWidgets.QMainWindow()
    with open("mainwindow.ui") as f:
        uic.loadUi(f, window)

    scroll_area = window.findChild(QtWidgets.QScrollArea, "scrollArea")
    array = mg.mi_pyt_maze(10, 10)

    grid = GridWidget(gridmodel.GridModel(array))
    scroll_area.setWidget(grid)

    palette = window.findChild(QtWidgets.QListWidget, "palette")

    add_palette_item(palette, "Grass", GRASS_FILE, 0)
    add_palette_item(palette, "Wall", WALL_FILE, -1)
    add_palette_item(palette, "Goal", GOAL_FILE, 1)
    add_palette_item(palette, "Dude 1", DUDE1_FILE, 10)

    def item_activated():
        for item in palette.selectedItems():
            # row_num = palette.indexFromItem(item).row()
            selected = item.data(VALUE_ROLE)
            grid.selected = selected

    palette.itemSelectionChanged.connect(item_activated)
    palette.setCurrentRow(0)

    def new_dialog(window):
        dialog = QtWidgets.QDialog(window)
        with open("maze_dialog.ui") as f:
            uic.loadUi(f, dialog)
        # freezes the window below and shows the modal dialog
        result = dialog.exec()
        if result == QtWidgets.QDialog.Rejected:
            # Do nothing
            return
        cols = dialog.findChild(QtWidgets.QSpinBox, "widthBox").value()
        rows = dialog.findChild(QtWidgets.QSpinBox, "heightBox").value()
        random = dialog.findChild(QtWidgets.QCheckBox, "randomCheckBox").isChecked()
        if random:
            grid.set_model(gridmodel.GridModel(mg.mi_pyt_maze(cols, rows)))
        else:
            grid.set_model(gridmodel.GridModel(np.zeros((rows, cols), dtype=np.int8)))

    action = window.findChild(QtWidgets.QAction, "actionNew")
    action.triggered.connect(lambda: new_dialog(window))
    window.show()
    app.exec()


def add_palette_item(palette, name, image, value):
    item = QtWidgets.QListWidgetItem(name)
    item.setIcon(QtGui.QIcon(image))
    item.setData(VALUE_ROLE, value)
    palette.addItem(item)


if __name__ == "__main__":
    main()
