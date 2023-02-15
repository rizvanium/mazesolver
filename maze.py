from renders import Window, Line, Point
import time
import random

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

    def draw(self, x1, y1, x2, y2, color="black"):
        self.set_coords(x1, y1, x2, y2)

        no_wall_color = "white"
        top_color = color if self.has_top_wall else no_wall_color
        right_color = color if self.has_right_wall else no_wall_color
        bottom_color = color if self.has_bottom_wall else no_wall_color
        left_color = color if self.has_left_wall else no_wall_color

        h_top = Line(Point(x1, y1), Point(x2, y1))
        self._window.draw_line(h_top, top_color)

        v_right = Line(Point(x2, y1), Point(x2, y2))
        self._window.draw_line(v_right, right_color)

        h_bottom = Line(Point(x2, y2), Point(x1, y2))
        self._window.draw_line(h_bottom, bottom_color)

        v_left = Line(Point(x1, y2), Point(x1, y1))
        self._window.draw_line(v_left, left_color)

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
            win,
            seed=None
        ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._row_count = row_count
        self._col_count = col_count
        self._cell_size = cell_size
        self._win = win
        if seed:
            random.seed(seed)
        self._create_cells()
        self._build_a_maze((0, 0, 'place_holder'))

    def _create_cells(self):
        for i in range(self._row_count):
            self._cells.append([])
            for j in range(self._col_count):
                self._cells[i].append(Cell(self._win))
        if self._win:
            self._draw_cells()
            self._create_entrance_and_exit()

    def _draw_cells(self):
        for i in range(self._row_count):
            for j in range(self._col_count):
                self._draw_cell(i, j, "black")       

    def _draw_cell(self, row_num, col_num, color="black"):
        x1 = self._x1 + col_num * self._cell_size
        y1 = self._y1 + row_num * self._cell_size
        x2 = x1 + self._cell_size
        y2 = y1 + self._cell_size

        self._cells[row_num][col_num].draw(x1, y1, x2, y2, color)
        self._animate()

    def _create_entrance_and_exit(self):
        entrance_row, entrance_col = 0, 0
        exit_row, exit_col = self._row_count - 1, self._col_count - 1

        self._cells[entrance_row][entrance_col].has_top_wall = False
        self._cells[exit_row][exit_col].has_bottom_wall = False

        self._draw_cell(entrance_row, entrance_col)
        self._draw_cell(exit_row, exit_col)

    def _build_a_maze(self, current):
        left_limit, right_limit = 0, self._col_count - 1
        top_limit, bottom_limit = 0, self._row_count - 1

        while True:
            fringe = []
            self._cells[current[0]][current[1]].visited = True

            top = (current[0] - 1, current[1], 'top')
            bottom = (current[0] + 1, current[1], 'bottom')
            left = (current[0], current[1] - 1, 'left')
            right = (current[0], current[1] + 1, 'right')

            if top[0] >= top_limit and top[0] <= bottom_limit:
                top_cell = self._cells[top[0]][top[1]]
                if top_cell and not top_cell.visited:
                    fringe.append(top)

            if bottom[0] >= top_limit and bottom[0] <= bottom_limit:
                bottom_cell = self._cells[bottom[0]][bottom[1]]
                if bottom_cell and not bottom_cell.visited:
                    fringe.append(bottom)

            if left[1] >= left_limit and left[1] <= right_limit:
                left_cell = self._cells[left[0]][left[1]]
                if left_cell and not left_cell.visited:
                    fringe.append(left)               

            if right[1] >= left_limit and right[1] <= right_limit:
                right_cell = self._cells[right[0]][right[1]]
                if right_cell and not right_cell.visited:
                    fringe.append(right)               

            if len(fringe) == 0:
                self._draw_cell(current[0], current[1])
                return

            idx = random.randint(0, len(fringe) - 1)
            next = fringe[idx]
            self._remove_wall_between_cells(
                    self._cells[current[0]][current[1]], 
                    self._cells[next[0]][next[1]], 
                    next[-1]
            )

            self._build_a_maze(next)
    
    def _remove_wall_between_cells(self, cell1, cell2, c2_to_c1_relation):
        # Debug:
        print(f"{cell2} is {c2_to_c1_relation} of {cell1}")
        if c2_to_c1_relation == 'top':
            cell1.has_top_wall = False
            cell2.has_bottom_wall = False
        elif c2_to_c1_relation == 'bottom':
            cell1.has_bottom_wall = False
            cell2.has_top_wall = False
        elif c2_to_c1_relation == 'left':
            cell1.has_left_wall = False
            cell2.has_right_wall = False
        elif c2_to_c1_relation == 'right':
            cell1.has_right_wall = False
            cell2.has_left_wall = False

    def _animate(self):
        self._win.redraw()
        time.sleep(0.005)


