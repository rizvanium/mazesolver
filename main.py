from renders import Window
from maze import Maze


def main():
    win = Window("MazeSolver", 800, 600)

    maze = Maze(10, 10, 15, 10, 40, win)

    win.wait_for_close()


if __name__ == "__main__":
    main()

