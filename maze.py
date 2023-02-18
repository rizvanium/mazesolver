from enum import Enum
from renders import Window, Line, Point, Rectangle
from ds import UnionFind
import time
import random


class Buff(Enum):
    WHITE = 1, "white"
    BLUE = 2, "blue"
    RED = 5, "red"

    def __init__(self, cost, color):
        self.cost = cost
        self.color = color


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
        
        self.buff_applied = Buff.WHITE
        self.cost = self.buff_applied.cost
        self.bg_color = self.buff_applied.color

        self._window = window


    def __repr__(self):
        return f"({self._x1} {self._y1}) ({self._x2} {self._y2})"

    
    def _coords_initialized(self):
        return self._x1 and self._x2 and self._y1 and self._y2

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

        self._window.draw_line(Line(mid, other_mid), color)

    def highlight(self, color: str) -> None:
        if not self._coords_initialized():
            return
        p1 = Point(self._x1 + 5, self._y1 + 5)
        p2 = Point(self._x2 - 5, self._y2 - 5)
        rect = Rectangle(p1, p2)
        self._window.draw_rectangle(rect, color)

    def apply_buff(self, buff: Buff) -> None:
        self.cost = buff.cost
        self.bg_color = buff.color
        self.buff_applied = buff
        p1 = Point(self._x1 + 5, self._y1 + 5)
        p2 = Point(self._x2 - 5, self._y2 - 5)
        self._window.draw_rectangle(Rectangle(p1, p2), self.bg_color)


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
        self._cell_types = [buff for buff in Buff]
        self._cell_type_idx = 0
        self._selected_cell_type = self._cell_types[self._cell_type_idx]
        self._x1 = x1
        self._y1 = y1
        self._row_count = row_count
        self._col_count = col_count
        self._cell_size = cell_size
        self._selected_cell = None
        self._win = win
        if self._win:
            self._win.add_button("SOLVE", 5, 5, self.solve)

        if seed:
            random.seed(seed)
        # TESTING
        self._create_cells()
        self._create_entrance_and_exit()
        self.generate_kruskals()
        self._build_a_maze((0, 0, 'place_holder'))
        self._reset_cells_visited()
        
        if self._win:
            self._win.add_mouse_listener(lambda e: self._on_mouse_pos_change(e))
            self._win.add_m1_click_listener(lambda e: self._on_m1_click(e))
            self._win.add_m3_click_listener(lambda e: self._on_m3_click(e))

    def _create_cells(self):
        for i in range(self._row_count):
            self._cells.append([])
            for j in range(self._col_count):
                self._cells[i].append(Cell(self._win))
        self._draw_cells()

    def _draw_cells(self):
        for i in range(self._row_count):
            for j in range(self._col_count):
                self._draw_cell(i, j, "black")       

    def _draw_cell(self, row_num, col_num, color="black"):
        if not self._win:
            return 

        x1 = self._x1 + col_num * self._cell_size
        y1 = self._y1 + row_num * self._cell_size
        x2 = x1 + self._cell_size
        y2 = y1 + self._cell_size

        self._cells[row_num][col_num].draw(x1, y1, x2, y2, color)
        self._animate()

    def _on_mouse_pos_change(self, event) -> None:
        cell = self._get_cell_in_mouse_pos(event.x, event.y)

        if self._selected_cell:
            self._selected_cell.highlight(self._selected_cell.bg_color)

        if cell and cell.buff_applied != self._selected_cell_type:
            cell.highlight(self._selected_cell_type.color)
            self._selected_cell = cell

    def _on_m1_click(self, event) -> None:
        cell = self._get_cell_in_mouse_pos(event.x, event.y)
        if cell:
            cell.apply_buff(self._selected_cell_type)

    def _on_m3_click(self, event) -> None:
        self._rotate_cell_type()
        self._on_mouse_pos_change(event)

    def _get_cell_in_mouse_pos(self, x, y) -> Cell:
        left_limit, top_limit = self._x1, self._y1
        right_limit = self._x1 + self._cell_size * self._col_count
        bottom_limit = self._y1 + self._cell_size * self._row_count

        # If mouse is outside of a maze area, just return None
        if x < left_limit or x > right_limit or \
           y < top_limit or y > bottom_limit:
               return None

        row = (y - self._y1) // self._cell_size
        col = (x - self._x1) // self._cell_size

        return self._cells[row][col]
    
    def _rotate_cell_type(self):
        self._cell_type_idx += 1
        self._cell_type_idx %= len(self._cell_types)
        self._selected_cell_type = self._cell_types[self._cell_type_idx]

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

    def generate_kruskals(self):
        # associate walls with the cells they separate
        walls = self._map_walls_to_cells() 
        print(walls)
        # associate walls with set ids in union_find DS
        
        total_cells = self._row_count * self._col_count
        walls_down = 0


#        while walls_down < total_cells - 1:
#            pass
    
    def _map_walls_to_cells(self):
        walls = []
        for i in range(self._row_count):
            for j in range(self._col_count):
                cell_num = j + i * self._col_count
                if j < self._col_count - 1:
                    right_cell_num = j + 1 + i * self._col_count
                    walls.append((cell_num, right_cell_num))
                if i < self._row_count - 1:
                    bot_cell_num = j + (i + 1) * self._col_count
                    walls.append((cell_num, bot_cell_num)) 
        return walls

    def _remove_wall_between_cells(self, cell1, cell2, c2_to_c1_relation):
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

    def _reset_cells_visited(self):
        for i in range(self._row_count):
            for j in range(self._col_count):
                self._cells[i][j].visited = False

    def solve(self):
        self._solve_r(0, 0)


    def _solve_r(self, row, col):
        self._animate(50)

        current = self._cells[row][col]
        current.visited = True

        if row == self._row_count - 1 and col == self._col_count - 1:
            return True

        left_limit, right_limit = 0, self._col_count - 1
        top_limit, bottom_limit = 0, self._row_count - 1

        top = (row - 1, col)
        bottom = (row + 1, col)
        left = (row, col - 1)
        right = (row, col + 1)

        if top[0] >= top_limit and top[0] <= bottom_limit:
            top_cell = self._cells[top[0]][top[1]]
            if not top_cell.visited and not top_cell.has_bottom_wall:
                current.draw_move(top_cell)
                res = self._solve_r(top[0], top[1])
                if res:
                    return True
                else:
                    top_cell.draw_move(current, True)

        if bottom[0] >= top_limit and bottom[0] <= bottom_limit:
            bottom_cell = self._cells[bottom[0]][bottom[1]]
            if not bottom_cell.visited and not bottom_cell.has_top_wall:
                current.draw_move(bottom_cell)
                res = self._solve_r(bottom[0], bottom[1])
                if res:
                    return True
                else:
                    bottom_cell.draw_move(current, True)


        if left[1] >= left_limit and left[1] <= right_limit:
            left_cell = self._cells[left[0]][left[1]]
            if not left_cell.visited and not left_cell.has_right_wall:
                current.draw_move(left_cell)
                res = self._solve_r(left[0], left[1])
                if res:
                    return True
                else:
                    left_cell.draw_move(current, True)


        if right[1] >= left_limit and right[1] <= right_limit:
            right_cell = self._cells[right[0]][right[1]]
            if not right_cell.visited and not right_cell.has_left_wall:
                current.draw_move(right_cell)
                res = self._solve_r(right[0], right[1])
                if res:
                    return True
                else:
                    right_cell.draw_move(current, True)


    def _animate(self, speed=100):
        self._win.redraw()
        time.sleep(0.05 / (speed / 100))


