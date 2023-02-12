from tkinter import Tk, BOTH, Canvas


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.width = width
        self.height = height
        self.__running = False
        self.__canvas = Canvas(self.__root, 
                               bg="white", 
                               height=height, 
                               width=width
                               )
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def draw_line(self, line, fill_color: str):
        line.draw(self.__canvas, fill_color)

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("Program Closed")


    def close(self):
        self.__running = False
        

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"[{self.x} {self.y}]"


class Line:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2


    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(self.p1.x,
                           self.p1.y,
                           self.p2.x,
                           self.p2.y,
                           fill=fill_color, 
                           width=2)
        canvas.pack(fill=BOTH, expand=1)


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


def main():
    win = Window(800, 600)

    cell1 = Cell(win)
    cell2 = Cell(win)
    cell3 = Cell(win)

    cell1.draw(2, 2, 40, 40)
    cell2.draw(40, 2, 76, 40)
    cell3.draw(40, 40, 76, 76)
    
    cell1.draw_move(cell2)
    cell2.draw_move(cell3)

    win.wait_for_close()
    


if __name__ == "__main__":
    main()

