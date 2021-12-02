# Author: Jacob Russell
# Date: November 30, 2021
# Sudoku Game
# References: Algorithms from: https://dlbeer.co.nz/articles/sudoku.html
import random


class SudokuGame:
    """A game of sudoku"""

    def __init__(self):
        self._grid = {}
        self._blank_grid = {}
        self._3x3s = {}
        self._rows = {}
        self._columns = {}
        self._boxes = {}
        self.populate()

        # Calls recursive create_solution() until a valid puzzle is created,
        # usually takes about 500 - 1000ms.
        while not self.create_solution():
            self.populate()

        self.create_puzzle()  # removes answers from cells to create a puzzle

    def populate(self):
        """
        Populate coordinate keys into the board dictionaries.
        Populates  row, column, and 3x3 box dictionaries with
        alpha-numeric coordinates as keys and blank values.
        """

        # Populate grid with coordinates as dictionary keys
        for num in "123456789":
            for letter in "ABCDEFGHI":
                self._grid[letter + num] = ""
                self._blank_grid[letter + num] = ""

        # Populate rows (in dictionary)
        for i in range(1, 10):
            self._rows[str(i)] = []

        # Populate columns
        for letter in "ABCDEFGHI":
            self._columns[letter] = []

        # Populate 3 x 3 boxes
        for i in range(1, 10):
            self._3x3s[str(i)] = []

        # Populate box coordinates
        self._boxes["1"] = ["A1", "B1", "C1",
                            "A2", "B2", "C2",
                            "A3", "B3", "C3"]
        self._boxes["2"] = ["D1", "E1", "F1",
                            "D2", "E2", "F2",
                            "D3", "E3", "F3"]
        self._boxes["3"] = ["G1", "H1", "I1",
                            "G2", "H2", "I2",
                            "G3", "H3", "I3"]
        self._boxes["4"] = ["A4", "B4", "C4",
                            "A5", "B5", "C5",
                            "A6", "B6", "C6"]
        self._boxes["5"] = ["D4", "E4", "F4",
                            "D5", "E5", "F5",
                            "D6", "E6", "F6"]
        self._boxes["6"] = ["G4", "H4", "I4",
                            "G5", "H5", "I5",
                            "G6", "H6", "I6"]
        self._boxes["7"] = ["A7", "B7", "C7",
                            "A8", "B8", "C8",
                            "A9", "B9", "C9"]
        self._boxes["8"] = ["D7", "E7", "F7",
                            "D8", "E8", "F8",
                            "D9", "E9", "F9"]
        self._boxes["9"] = ["G7", "H7", "I7",
                            "G8", "H8", "I8",
                            "G9", "H9", "I9"]

    def create_solution(self, grid=None, index=0):
        """
        Recursively attempts to create a valid Sudoku solution.
        This is fairly brute force, and takes many tries to succeed.
        """
        if grid is None:
            grid = self._blank_grid
        if index == 81:  # if we have passed end of grid
            if self.is_valid(grid):  # if the grid puzzle is valid
                self._grid = grid
                return True
            else:  # if invalid puzzle is created
                return False
        cell = list(self._grid.keys())[index]
        possibles = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        if grid[cell] == "":
            while len(possibles) > 0 and grid[cell] == "":
                rand_index = random.randint(0, len(possibles) - 1)
                num = possibles[rand_index]

                # check if number placement is valid then add to dictionaries
                if num not in self._3x3s[self.get_box(cell)] and \
                    num not in self._rows[cell[1]] and \
                        num not in self._columns[cell[0]]:
                    grid[cell] = num
                    self._3x3s[self.get_box(cell)].append(num)
                    self._rows[cell[1]].append(num)
                    self._columns[cell[0]].append(num)
                possibles.remove(num)

        return self.create_solution(grid, index + 1)

    def get_cell_from_index(self, index: int) -> str:
        """
        Takes index and returns matching alpha-numeric coordinates (e.g. A1)
        The top left of grid is considered index 0,
        bottom right would be index 80.
        """
        return list(self._grid.keys())[index]

    def create_puzzle(self):
        """
        Takes valid solution. Removes numbers and creates blank spaces.
        """
        for box in self._boxes:
            cells = list(self._boxes[box])
            amount = random.randint(4, 6)
            while amount > 0:
                index = random.randint(0, len(cells) - 1)
                cell = cells[index]
                self._grid[cell] = ""
                amount -= 1
        #self.print_grid()



    def get_box(self, cell):
        for key in self._boxes:
            if cell in self._boxes[key]:
                return key

    def is_valid(self, grid):
        """Detects if current sudoku grid is valid"""
        # Check for blanks
        for key in grid:
            if grid[key] == "":
                return False

        # Make sure no number repeats in same box
        for key in self._3x3s:
            for i in self._3x3s[key]:
                if self._3x3s[key].count(i) > 1:
                    return False

        # Check rows
        for key in self._rows:
            for i in self._rows[key]:
                if self._rows[key].count(i) > 1:
                    return False

        # Check columns
        for key in self._columns:
            for i in self._columns[key]:
                if self._columns[key].count(i) > 1:
                    return False

        return True  # if there are no repeating #'s in row, column or box

    def print_grid(self):
        """Prints the puzzle in a human readable string"""
        count = 1
        rows = ""
        for key in self._grid:
            cell = self._grid[key]
            if cell == "":
                cell = " "
            if count == 1:
                rows += "|--------------------------|\n|"
            if count % 3 == 0:
                rows += cell + " |"
            else:
                rows += cell + "  "
            if count % 9 == 0:
                rows += "\n|"
            if count % 27 == 0:
                if count == 81:
                    rows += "--------------------------|\n"
                else:
                    rows += "--------------------------|\n|"
            count += 1
        print(rows)


game = SudokuGame()
game.print_grid()


