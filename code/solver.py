"""
solver.py — Implementation of Greedy and Max Weight Matching Solvers
---------------------------------------------------------------------
This module provides two solver classes:
- SolverGreedy: selects pairs with minimum absolute difference greedily.
- SolverMaxWeightMatching: uses the Hungarian algorithm for optimal pairing.

Developed as part of ENSAE Paris Programming Project (2025) — Mohamed Iyed Mokline & Olivier de Boissieu
"""

from grid import Grid
import networkx as nx


class SolverGreedy:
    def __init__(self, grid):
        """
        Initialize the greedy solver with a given grid.
        """
        self.grid = grid
        self.pairs = []

    def run(self):
        """
        Run the greedy pairing algorithm.
        Selects pairs with smallest value difference, avoids conflicts.
        """
        self.pairs = []
        used = set()

        # Generate all valid pairs with their associated cost
        all_pairs = [
            (abs(self.grid.value[c1[0]][c1[1]] - self.grid.value[c2[0]][c2[1]]), c1, c2)
            for (c1, c2) in self.grid.all_pairs()
            if self.grid.valid_pair(c1, c2)
        ]

        # Sort by increasing cost
        all_pairs.sort()

        for _, c1, c2 in all_pairs:
            if c1 not in used and c2 not in used:
                self.pairs.append((c1, c2))
                used.update([c1, c2])

        return self.pairs

    def score(self):
        """
        Return the total score for the greedy solution.
        """
        return self.grid.score(self.pairs)


class SolverMaxWeightMatching:
    def __init__(self, grid):
        """
        Initialize the Hungarian (maximum weight matching) solver.
        """
        self.grid = grid
        self.pairs = []

    def run(self):
        """
        Run the optimal matching algorithm using NetworkX’s max_weight_matching.
        """
        G = nx.Graph()

        # Add valid pairs with weights (inverted so low diff = high reward)
        for (c1, c2) in self.grid.all_pairs():
            if self.grid.valid_pair(c1, c2):
                diff = abs(self.grid.value[c1[0]][c1[1]] - self.grid.value[c2[0]][c2[1]])
                G.add_edge(c1, c2, weight=-diff)  # negative for max_weight = min_diff

        self.pairs = list(nx.max_weight_matching(G, maxcardinality=True))
        return self.pairs

    def score(self):
        """
        Return the total score for the optimal (Hungarian) solution.
        """
        return self.grid.score(self.pairs)
