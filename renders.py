from tkinter import Tk, BOTH, Canvas, Button


class Window:
    def __init__(self, title, width, height):
        self.__root = Tk()
        self.__root.title(title)
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
    
    def draw_rectangle(self, rect, fill_color: str):
        rect.draw(self.__canvas, fill_color)

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("Program Closed")
    
    def add_button(self, text, x, y, callback):
        btn = Button(self.__root, text=text, command=callback)
        btn.pack(ipadx=x, ipady=y, expand=False)

    def add_mouse_listener(self, callback):
        self.__root.bind('<Motion>', callback)

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


class Rectangle:
    def __init__(self, p1: Point, p2: Point) -> None:
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas: Canvas, fill_color: str, alpha=1.0):
        canvas.create_rectangle(self.p1.x,
                                self.p1.y,
                                self.p2.x,
                                self.p2.y,
                                outline=fill_color,
                                fill=fill_color)
        canvas.pack(fill=BOTH, expand=1)
        
