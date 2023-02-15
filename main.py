from renders import Window
from maze import Maze


def main():
    win = Window("MazeSolver", 800, 600)
    
    start_x, start_y = 40, 40
    row_count, col_count = 8, 12
    cell_size = 60
    seed = None
    maze = Maze(start_x, 
                start_y, 
                row_count, 
                col_count, 
                cell_size, 
                win, 
                seed
                )
    maze.solve()
    win.wait_for_close()


if __name__ == "__main__":
    main()

