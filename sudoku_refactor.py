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
        self._candidates = {}
        self.populate()
        self.create_puzzle()


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

        # Populate candidates dictionary
        for key in self._grid:
            self._candidates[key] = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

    def create_puzzle(self, grid=None, index=0):
        if grid is None:
            grid = self._blank_grid
        if index == 81:  # if we have passed end of grid
            if self.is_valid(grid):  # if the grid puzzle is valid
                self._grid = grid
                print("Valid puzzle created!!")  # for debug
                self.print_board()
                return True
            else:
                print("Puzzle invalid, try again.")  # for debug
                self._grid = grid
                self.print_board()
                return False
        cell = self.get_cell_from_index(index)
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

        self.create_puzzle(grid, index + 1)

    def get_cell_from_index(self, index: int) -> str:
        """
        Takes index and returns matching alpha-numeric coordinates (e.g. A1)
        The top left of grid is considered index 0,
        bottom right would be index 80.
        """
        return list(self._grid.keys())[index]

    def clear_dictionaries(self):
        self._grid = self._blank_grid
        for key in self._rows:
            self._rows[key].clear()
        for key in self._columns:
            self._columns[key].clear()
        for key in self._3x3s:
            self._3x3s[key].clear()

    def get_box(self, cell):
        for key in self._boxes:
            if cell in self._boxes[key]:
                return key

    def fewest_candidates(self):
        """
        Returns cell with fewest candidates.
        If more than one fits this description, a random one is returned.
        If there are no cells with possible candidates, returns None.
        """
        min_list = []
        min_cells = []
        cell = None
        for key in self._candidates:
            min_list.append(len(self._candidates[key]))
        min_candidates = min(min_list)
        for key in self._candidates:
            if self._candidates[key] == min_candidates:
                min_cells.append(key)
        if len(min_cells) > 1:
            index = random.randint(0, len(min_cells) - 1)
            cell = min_cells[index]
        elif len(min_cells) == 1:
            cell = min_cells[0]
        else:
            print("No cells left.")
            return None
        return cell

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






    def print_board(self):
        count = 1
        rows = ""
        for key in self._grid:
            rows += self._grid[key] + "  "
            if count % 9 == 0:
                rows += "\n"
            count += 1
        print(rows)

    def print_blank_board(self):
        count = 1
        rows = ""
        for key in self._grid:
            rows += key + " "
            if count % 9 == 0:
                rows += "\n"
            count += 1
        print(rows)

    def print_solution(self):
        count = 1
        rows = ""
        board_list = list(self._grid.values())
        for value in board_list:
            rows += value + " "
            if count % 9 == 0:
                rows += "\n"
            count += 1
        print(rows)


game = SudokuGame()

