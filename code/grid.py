import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

"""
grid.py — Grid Structure and Pair Evaluation Engine
---------------------------------------------------
This module implements the Grid class used to represent a colored numerical grid. 
It supports pair evaluation, constraint checking, and visual rendering.

Developed as part of ENSAE Paris Programming Project (2025) — Mohamed Iyed Mokline & Olivier de Boissieu
"""




class Grid:
    """
    A class representing the grid. 

    Attributes: 
    -----------
    n: int
        Number of lines in the grid
    m: int
        Number of columns in the grid
    color: list[list[int]]
        The color of each grid cell: color[i][j] is the color in the cell (i, j), i.e., in the i-th line and j-th column
        Note: lines are numbered 0..n-1 and columns are numbered 0..m-1.
    value: list[list[int]]
        The value of each grid cell: value[i][j] is the value in the cell (i, j), i.e., in the i-th line and j-th column
        Note: lines are numbered 0..n-1 and columns are numbered 0..m-1.
    colors_list: list[char]
        The mapping between the value of self.color[i][j] and the corresponding color
    """

    def __init__(self, n, m, color=[], value=[]):
        """
        Initializes the grid.

        Parameters: 
        -----------
        n: int
            Number of lines in the grid
        m: int
            Number of columns in the grid
        color: list[list[int]]
            The grid cells colors. Default is empty (then the grid is created with each cell having color 0,
            i.e., white).
        value: list[list[int]]
            The grid cells values. Default is empty (then the grid is created with each cell having value 1).
        
        The object created has an attribute colors_list: list[char], which is the mapping between the value of
        self.color[i][j] and the corresponding color
        """
        self.n = n
        self.m = m
        if not color:
            color = [[0 for j in range(m)] for i in range(n)]
        self.color = color
        if not value:
            value = [[1 for j in range(m)] for i in range(n)]
        self.value = value
        self.colors_list = ['w', 'r', 'b', 'g', 'k']

    def __str__(self):
        """
        Prints the grid as text.
        """
        output = f"The grid is {self.n} x {self.m}. It has the following colors:\n"
        for i in range(self.n):
            output += f"{[self.colors_list[self.color[i][j]] for j in range(self.m)]}\n"
        output += f"and the following values:\n"
        for i in range(self.n):
            output += f"{self.value[i]}\n"
        return output

    def __repr__(self):
        """
        Returns a representation of the grid with number of rows and columns.
        """
        return f"<grid.Grid: n={self.n}, m={self.m}>"

    def plot(self):
        """
        Plots a visual representation of the grid.
        """
        colors = self.colors_list
        cmp = ListedColormap(colors, name="Color map")

        fig, ax = plt.subplots()

        ax.matshow(self.color, cmap=cmp, vmin=0, vmax=4)

        for i in range(self.m):
            for j in range(self.n):
                ax.text(i, j, str(self.value[j][i]), va='center', ha='center')

        plt.show()

    def is_forbidden(self, i, j):
        """
        Returns True is the cell (i, j) is black and False otherwise
        """
        return self.colors_list[self.color[i][j]] == "k"

    def cost(self, pair):
        """
        Returns the cost of a pair
 
        Parameters: 
        -----------
        pair: tuple[tuple[int]]
            A pair in the format ((i1, j1), (i2, j2))

        Output: 
        -----------
        cost: int
            the cost of the pair defined as the absolute value of the difference between their values
        """
        case1, case2 = pair
        v1, v2 = self.value[case1[0]][case1[1]], self.value[case2[0]][case2[1]]
        return abs(v1 - v2)

    def color_check(self, cell1, cell2):
        """
        Takes two cells as input.
        Returns true if colors c1 and c2 are compatible
        """
        c1 = self.color[cell1[0]][cell1[1]]
        c2 = self.color[cell2[0]][cell2[1]]
        return (c1 != 4 and c2 != 4) and (c1 * c2 == 0 or (c1 == 3 and c2 == 3) or (c1 in (1, 2) and c2 in (1, 2)))

    def all_pairs(self):
        """
        Returns a list of all pairs of cells that can be taken together. 

        Outputs a list of tuples of tuples [(c1, c2), (c1', c2'), ...] where each cell c1 etc. is itself a tuple (i, j)
        """
        pairs = []
        for i in range(self.n):
            for j in range(self.m):
                if self.is_forbidden(i, j) :
                    continue  # Skip forbidden (black) cells

                # Check right neighbor (horizontal adjacency)
                if j + 1 < self.m and not self.is_forbidden(i, j + 1):
                    # check if the neighbor satisfies the non black-coloured constraint
                    if self.color_check((i, j), (i, j + 1)):
                        pairs.append(((i, j), (i, j + 1)))

                # Check bottom neighbor (vertical adjacency)
                if i + 1 < self.n and not self.is_forbidden(i + 1, j):
                    # check if the neighbor satisfies the non black-coloured constraint
                    if self.color_check((i, j), (i + 1, j)):
                        pairs.append(((i, j), (i + 1, j)))

        return pairs

    def all_pairs2(self):
        """
        Returns a list of all pairs of cells that can be taken together, including non-adjacent white pairs.
        """
        pairs = []
        white_cells = [(i, j) for i in range(self.n) for j in range(self.m)
                       if self.color[i][j] == 0 and not self.is_forbidden(i, j)]

        # Add all pairs of white cells (including non-adjacent ones)
        for idx1 in range(len(white_cells)):
            for idx2 in range(idx1 + 1, len(white_cells)):
                cell1 = white_cells[idx1]
                cell2 = white_cells[idx2]
                pairs.append((cell1, cell2))

        # Add adjacent pairs (original logic)
        for i in range(self.n):
            for j in range(self.m):
                if self.is_forbidden(i, j):
                    continue  # Skip forbidden (black) cells

                # Check right neighbor (horizontal adjacency)
                if j + 1 < self.m and not self.is_forbidden(i, j + 1):
                    if self.valid_pair2((i, j), (i, j + 1)):
                        pairs.append(((i, j), (i, j + 1)))

                # Check bottom neighbor (vertical adjacency)
                if i + 1 < self.n and not self.is_forbidden(i + 1, j):
                    if self.valid_pair2((i, j), (i + 1, j)):
                        pairs.append(((i, j), (i + 1, j)))

        return pairs

    def valid_pair(self, cell1, cell2):
        (i, j), (k, l) = cell1, cell2
        if (abs(i - k) <= 1) and (abs(j - l) <= 1) and abs(i-k) + abs(j-l) < 2 and self.color_check((i, j), (k, l)):
            return True
        return False

    def valid_pair2(self, cell1, cell2):
        """
        Checks if two cells form a valid pair based on the extended color constraints.
        """
        (i1, j1), (i2, j2) = cell1, cell2
        c1, c2 = self.color[i1][j1], self.color[i2][j2]

        # If both cells are white, they can be paired regardless of adjacency
        if c1 == 0 and c2 == 0:
            return True

        # Otherwise, they must be adjacent and satisfy the original color constraints
        if abs(i1 - i2) + abs(j1 - j2) != 1:  # Check adjacency
            return False

        # Original color constraints
        if c1 == 0 or c2 == 0:  # White can be paired with anything except black
            return True
        if c1 == c2:  # Same colors can always pair
            return True
        if (c1, c2) in [(1, 2), (2, 1)]:  # Red & Blue
            return True
        return False

    def even(self):
        """Return all even cells"""
        return [(i, j) for i in range(self.n) for j in range(self.m) if (i + j) % 2 == 0]

    def odd(self):
        """Return all odd cells"""
        return [(i, j) for i in range(self.n) for j in range(self.m) if (i + j) % 2 == 1]

    @classmethod
    def grid_from_file(cls, file_name, read_values=True):
        """
        Creates a grid object from class Grid, initialized with the information from the file file_name.
        
        Parameters: 
        -----------
        file_name: str
            Name of the file to load. The file must be of the format: 
            - first line contains "n m" 
            - next n lines contain m integers that represent the colors of the corresponding cell
            - next n lines [optional] contain m integers that represent the values of the corresponding cell
        read_values: bool
            Indicates whether to read values after having read the colors. Requires that the file has 2n+1 lines

        Output: 
        -------
        grid: Grid
            The grid
        """
        with open(file_name, "r") as file:
            n, m = map(int, file.readline().split())
            color = [[] for i_line in range(n)]
            for i_line in range(n):
                line_color = list(map(int, file.readline().split()))
                if len(line_color) != m:
                    raise Exception("Format incorrect")
                for j in range(m):
                    if line_color[j] not in range(5):
                        raise Exception("Invalid color")
                color[i_line] = line_color

            if read_values:
                value = [[] for i_line in range(n)]
                for i_line in range(n):
                    line_value = list(map(int, file.readline().split()))
                    if len(line_value) != m:
                        raise Exception("Format incorrect")
                    value[i_line] = line_value
            else:
                value = []

            grid = Grid(n, m, color, value)
        return grid
