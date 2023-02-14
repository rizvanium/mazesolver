from renders import Window
from maze import Maze


def main():
    win = Window("MazeSolver", 800, 600)

    maze = Maze(0, 0, 10, 15, 40, win)

    win.wait_for_close()


if __name__ == "__main__":
    main()

