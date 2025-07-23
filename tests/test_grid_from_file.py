"""
test_grid_solvers.py — Unit Tests for Grid-Based Matching Algorithms
---------------------------------------------------------------------
This script provides automated tests for the full matching algorithm suite used in
the ENSAE Paris 1A programming project (2025) by Mohamed Iyed Mokline and Olivier de Boissieu.

It tests:
- Grid file loading (with/without values)
- Forbidden cell logic
- Cost computation
- All solver classes:
  • SolverGreedy
  • SolverMatching (max flow)
  • SolverMaxWeightMatching (Hungarian)
  • SolverMaxWeightMatching2 (Hungarian variant)

Each test checks algorithmic correctness across a wide set of `.in` input files.
"""

# This will work if ran from the root folder (the folder in which there is the subfolder code/)
import sys

sys.path.append("code/")

# Modified file configuration in Pycharm to set working directory to ensae-prog25, use "Python tests" instead

import unittest
from grid import Grid
from solver import *


class Test_GridLoading(unittest.TestCase):
    def test_grid0(self):
        grid = Grid.grid_from_file("input/grid00.in", read_values=True)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 3)
        self.assertEqual(grid.color, [[0, 0, 0], [0, 0, 0]])
        self.assertEqual(grid.value, [[5, 8, 4], [11, 1, 3]])

    def test_grid0_novalues(self):
        grid = Grid.grid_from_file("input/grid00.in", read_values=False)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 3)
        self.assertEqual(grid.color, [[0, 0, 0], [0, 0, 0]])
        self.assertEqual(grid.value, [[1, 1, 1], [1, 1, 1]])

    def test_grid1(self):
        grid = Grid.grid_from_file("input/grid01.in", read_values=True)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 3)
        self.assertEqual(grid.color, [[0, 4, 3], [2, 1, 0]])
        self.assertEqual(grid.value, [[5, 8, 4], [11, 1, 3]])


class Test_GridMethods(unittest.TestCase):
    def test_isforbidden(self):
        grid = Grid.grid_from_file("input/grid00.in", read_values=False)
        self.assertTrue(not grid.is_forbidden(0, 1))
        grid = Grid.grid_from_file("input/grid01.in", read_values=True)
        self.assertTrue(grid.is_forbidden(0, 1))
        grid = Grid.grid_from_file("input/grid02.in", read_values=True)
        self.assertTrue(not grid.is_forbidden(1, 2))

    def test_cost(self):
        grid = Grid.grid_from_file("input/grid00.in", read_values=False)
        self.assertEqual(grid.cost(((0, 0), (0, 1))), 0)
        grid = Grid.grid_from_file("input/grid00.in", read_values=True)
        self.assertEqual(grid.cost(((0, 0), (0, 1))), 3)
        grid = Grid.grid_from_file("input/grid01.in", read_values=True)
        self.assertEqual(grid.cost(((0, 0), (0, 1))), 3)
        grid = Grid.grid_from_file("input/grid02.in", read_values=True)
        self.assertEqual(grid.cost(((0, 0), (0, 1))), 0)
        grid = Grid.grid_from_file("input/grid05.in", read_values=True)
        self.assertEqual(grid.cost(((0, 0), (0, 1))), 3)

    def test_allpairs(self):
        grid = Grid.grid_from_file("input/grid01.in", read_values=True)
        pairs = set(grid.all_pairs())
        self.assertSetEqual(pairs, {((0, 0), (1, 0)), ((0, 2), (1, 2)), ((1, 0), (1, 1)), ((1, 1), (1, 2))})


class Test_SolverGreedy(unittest.TestCase):
    def test_Solver(self):
        grid = Grid.grid_from_file("input/grid00.in", read_values=True)
        solver = SolverGreedy(grid)
        pairs, score = solver.run()
        self.assertEqual(score, 14)

        grid = Grid.grid_from_file("input/grid05.in", read_values=True)
        solver = SolverGreedy(grid)
        pairs, score = solver.run()
        self.assertEqual(score, 41)


class Test_SolverMatching(unittest.TestCase):
    def test_Solver02(self):
        grid = Grid.grid_from_file("input/grid02.in", read_values=False)
        solver = SolverMatching(grid)
        score = solver.run()
        self.assertEqual(score, 1)

    def test_Solver03(self):
        grid = Grid.grid_from_file("input/grid03.in", read_values=False)
        solver = SolverMatching(grid)
        score = solver.run()
        self.assertEqual(score, 2)

    def test_Solver04(self):
        grid = Grid.grid_from_file("input/grid04.in", read_values=False)
        solver = SolverMatching(grid)
        score = solver.run()
        self.assertEqual(score, 4)


class Test_SolverHungarian(unittest.TestCase):
    def test_Solver02(self):
        grid = Grid.grid_from_file("input/grid02.in", read_values=True)
        solver = SolverMaxWeightMatching(grid)
        solver.run()
        score = solver.score()
        self.assertEqual(score, 1)

    def test_Solver03(self):
        grid = Grid.grid_from_file("input/grid03.in", read_values=True)
        solver = SolverMaxWeightMatching(grid)
        solver.run()
        score = solver.score()
        self.assertEqual(score, 2)

    def test_Solver04(self):
        grid = Grid.grid_from_file("input/grid04.in", read_values=True)
        solver = SolverMaxWeightMatching(grid)
        solver.run()
        score = solver.score()
        self.assertEqual(score, 4)


class Test_SolverVariante(unittest.TestCase):
    def test_Solver00(self):
        grid = Grid.grid_from_file("input/grid00.in", read_values=True)
        solver = SolverMaxWeightMatching2(grid)
        solver.run()
        score = solver.score()
        self.assertEqual(score, 12)

    def test_Solver11(self):
        grid = Grid.grid_from_file("input/grid11.in", read_values=True)
        solver = SolverMaxWeightMatching2(grid)
        solver.run()
        score = solver.score()
        self.assertEqual(score, 2)

    def test_Solver12(self):
        grid = Grid.grid_from_file("input/grid12.in", read_values=True)
        solver = SolverMaxWeightMatching2(grid)
        solver.run()
        score = solver.score()
        self.assertEqual(score, 3)


if __name__ == '__main__':
    unittest.main()
