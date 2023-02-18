import unittest
from maze import Maze
from ds import UnionFind

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

    def test_union_find_created_correctly(self):
        size = 10
        uf = UnionFind(size)
        self.assertEqual(uf.size, size)
        self.assertEqual(uf.set_count, size)
        self.assertEqual(len(uf.ids), size)
        self.assertEqual(len(uf.sizes), size)
         
    def test_union_unify_works_correctly(self):
        size = 10
        uf = UnionFind(size)
        p, q, z = 0, size // 2, size - 1
        uf.unify(p, q)
        uf.unify(q, z)

        p_set_id, q_set_id, z_set_id = uf.find(p), uf.find(q), uf.find(z)
        p_set_size = uf.get_set_size(p)

        self.assertEqual(p_set_id, q_set_id)
        self.assertEqual(p_set_id, z_set_id)
        self.assertEqual(p_set_size, 3)
        
    def test_union_connection_checking_works_correctly(self):
        size = 10
        uf = UnionFind(size)
        p, q, z = 0, size // 2, size - 1
        uf.unify(p, q)
        pq_united = True
        pz_united = False
        qz_united = False

        self.assertEqual(uf.check_if_connected(p, q), pq_united)
        self.assertEqual(uf.check_if_connected(p, z), pz_united)
        self.assertEqual(uf.check_if_connected(q, z), qz_united)
        

 
 
if __name__ == "__main__":
    unittest.main()


