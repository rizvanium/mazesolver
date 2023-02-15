import unittest
from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        start_x, start_y = 0, 0
        num_rows, num_cols = 15, 10
        cell_size = 10
        window = None
        maze = Maze(start_x, start_y, num_rows, num_cols, cell_size, window)

        self.assertEqual(len(maze._cells), num_rows)
        self.assertEqual(len(maze._cells[0]), num_cols)

    def test_reset_cells_visited(self):
        start_x, start_y = 0, 0
        num_rows, num_cols = 15, 10
        cell_size = 10
        window = None
        maze = Maze(start_x, start_y, num_rows, num_cols, cell_size, window)

        for i in range(maze._row_count):
            for j in range(maze._col_count):
                maze._cells[i][j].visited = True

        maze._reset_cells_visited()

        all_unvisited = True
        for i in range(maze._row_count):
            for j in range(maze._col_count):
                if maze._cells[i][j].visited:
                    all_unvisited = False
                    break;
        
        self.assertEqual(all_unvisited, True)
         

if __name__ == "__main__":
    unittest.main()

