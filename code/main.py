"""
main.py — Solver Execution Script
---------------------------------
This script runs different solvers (Greedy and Hungarian) on a grid instance.
It loads grid data from input files and prints the score for each solving method.

Developed as part of ENSAE Paris Programming Project (2025) — Mohamed Iyed Mokline & Olivier de Boissieu
"""

from grid import Grid
from solver import SolverGreedy, SolverMaxWeightMatching

# Set the input file path
data_path = "../input/"
file_name = data_path + "notopti.in"

# Load grid from file
grid = Grid.grid_from_file(file_name, read_values=True)

# Visualize the grid
grid.plot()

# Run the Greedy solver
greedy_solver = SolverGreedy(grid)
greedy_solution = greedy_solver.run()
print("Greedy solution:", greedy_solution)
print("Greedy solver score:", greedy_solver.score())

# Run the Optimal Hungarian solver
optimal_solver = SolverMaxWeightMatching(grid)
optimal_solution = optimal_solver.run()
print("Optimal (Hungarian) solution:", optimal_solution)
print("Optimal solver score:", optimal_solver.score())
