from renders import Window, Line, Point
import time

class Cell:
    def __init__(self, window):
        self.visited = False

        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True 

        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None

        self._window = window


    def __repr__(self):
        return f"({self._x1} {self._y1}) ({self._x2} {self._y2})"

    
    def set_coords(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

    def draw(self, x1, y1, x2, y2):
        self.set_coords(x1, y1, x2, y2)

        if self.has_top_wall:
            h_top = Line(Point(x1, y1), Point(x2, y1))
            self._window.draw_line(h_top, "black")
        if self.has_right_wall:
            v_right = Line(Point(x2, y1), Point(x2, y2))
            self._window.draw_line(v_right, "black")
        if self.has_bottom_wall:
            h_bottom = Line(Point(x2, y2), Point(x1, y2))
            self._window.draw_line(h_bottom, "black")
        if self.has_left_wall:
            v_left = Line(Point(x1, y2), Point(x1, y1))
            self._window.draw_line(v_left, "black")

    def draw_move(self, other_cell, undo=False):
        color = "red" if not undo else "gray" 

        mid_x = self._x2 - ((self._x2 - self._x1) / 2)
        mid_y = self._y2 - ((self._y2 - self._y1) / 2)
        mid = Point(mid_x, mid_y)

        mid_x = other_cell._x2 - (other_cell._x2 - other_cell._x1) / 2
        mid_y = other_cell._y2 - (other_cell._y2 - other_cell._y1) / 2
        other_mid = Point(mid_x, mid_y)

        print(mid, other_mid)

        self._window.draw_line(Line(mid, other_mid), color)


class Maze:
    def __init__(
            self,
            x1,
            y1,
            row_count,
            col_count,
            cell_size,
            win
        ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._row_count = row_count
        self._col_count = col_count
        self._cell_size = cell_size
        self._win = win
        self._create_cells()

    def _create_cells(self):
        for i in range(self._row_count):
            self._cells.append([])
            for j in range(self._col_count):
                self._cells[i].append(Cell(self._win))
        if self._win:
            self._draw_cells()

    def _draw_cells(self):
        for i in range(self._row_count):
            for j in range(self._col_count):
                self._draw_cell(i, j)       

    def _draw_cell(self, row_num, col_num):
        x1 = self._x1 + col_num * self._cell_size
        y1 = self._y1 + row_num * self._cell_size
        x2 = x1 + self._cell_size
        y2 = y1 + self._cell_size

        self._cells[row_num][col_num].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        self._win.redraw()
        # time.sleep(0.005)


