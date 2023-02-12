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
    

if __name__ == "__main__":
    unittest.main()

