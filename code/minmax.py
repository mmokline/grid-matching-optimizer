"""
minmax.py — AI Opponent Strategy Using Minimax Algorithm
---------------------------------------------------------
This module defines the Minmax class which implements an AI player using
the classical Minimax algorithm with recursion depth control.

Developed as part of ENSAE Paris Programming Project (2025) — Mohamed Iyed Mokline & Olivier de Boissieu
"""

MAXIMUM_RECURSION_DEPTH = 100


class Minmax:
    def __init__(self, grid):
        """
        Initialize the Minmax AI with the given grid.
        """
        self.grid = grid

    def next_moves(self, used_cells):
        """
        Generate all valid and unplayed cell pairs.
        """
        return [
            (c1, c2)
            for (c1, c2) in self.grid.all_pairs()
            if self.grid.valid_pair(c1, c2) and c1 not in used_cells and c2 not in used_cells
        ]

    def terminal(self, used_cells):
        """
        Check if there are no possible moves left.
        """
        return self.next_moves(used_cells) == []

    def compute_score(self, pairs):
        """
        Compute the total score for a list of cell pairs.
        """
        return sum(abs(self.grid.value[c1[0]][c1[1]] - self.grid.value[c2[0]][c2[1]]) for c1, c2 in pairs)

    def utility(self, AIpairs, PersonPairs):
        """
        Utility function for minimax:
        difference between the opponent's score and the AI's score.
        """
        return self.compute_score(PersonPairs) - self.compute_score(AIpairs)

    def minimax(self, isMaximisingPlayer, depth, AIpairs, PersonPairs, used_cells):
        """
        Recursive implementation of the minimax algorithm.
        """
        if self.terminal(used_cells) or depth > MAXIMUM_RECURSION_DEPTH:
            if depth > MAXIMUM_RECURSION_DEPTH:
                print("Maximum recursion depth exceeded.")
            return self.utility(AIpairs, PersonPairs)

        if isMaximisingPlayer:
            best_score = float("-inf")
            for move in self.next_moves(used_cells):
                AIpairs.append(move)
                c1, c2 = move
                used_cells.update([c1, c2])
                score = self.minimax(False, depth + 1, AIpairs, PersonPairs, used_cells)
                AIpairs.pop()
                used_cells.difference_update([c1, c2])
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for move in self.next_moves(used_cells):
                PersonPairs.append(move)
                c1, c2 = move
                used_cells.update([c1, c2])
                score = self.minimax(True, depth + 1, AIpairs, PersonPairs, used_cells)
                PersonPairs.pop()
                used_cells.difference_update([c1, c2])
                best_score = min(score, best_score)
            return best_score

    def move(self, used_cells, AIpairs, PersonPairs):
        """
        Choose the best move using the minimax algorithm.
        """
        if self.terminal(used_cells):
            return None

        best_score = float("-inf")
        best_move = None
        for move in self.next_moves(used_cells):
            AIpairs.append(move)
            c1, c2 = move
            used_cells.update([c1, c2])
            score = self.minimax(False, 0, AIpairs, PersonPairs, used_cells)
            AIpairs.pop()
            used_cells.difference_update([c1, c2])
            if score > best_score:
                best_score = score
                best_move = move

        return best_move
