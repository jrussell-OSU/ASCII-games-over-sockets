# Author: Jacob Russell
# Date: November 30, 2021
# Sudoku Game
# References: Algorithm ideas (no actual code) from: https://dlbeer.co.nz/articles/sudoku.html
import random


class Sudoku:
    """A game of sudoku"""

    def __init__(self):
        self._grid = {}  # current game grid
        self._blank_grid = {}  # grid with just coordinates no answers
        self._3x3s = {}  # each 3x3 box in grid
        self._rows = {}
        self._columns = {}
        self._boxes = {}  # stores just coordinates of each 3x3 grid (no answer)
        self._solution = {}  # stores copy of full solution
        self._permanent = []  # stores which coordinates cannot be edited
        self._messages = {
            "welcome": "Welcome to Sudoku!\n"
                       "Please enter a coordinate and then a number to fill in each cell.\n"
                       "Example: A1, 7  would put a 7 in the top left cell.\n"
        }
        self.populate()

        # Calls recursive create_solution() until a valid puzzle is created,
        # usually takes about 500 - 1000ms.
        while not self.create_solution():
            self.populate()

        self.create_puzzle()  # removes answers from cells to create a puzzle

    def get_messages(self, key):
        if key == "welcome":
            return self.grid_string() + "\n" + self._messages[key]

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

    def create_puzzle(self):
        """
        Takes valid solution. Removes numbers and creates blank spaces.
        """
        # Store solution (used mostly for debugging currently)
        for i in self._grid:
            key = i
            answer = self._grid[i]
            self._solution[key] = answer

        # Remove 4-6 answers from each 3x3 box on the grid
        for box in self._boxes:
            cells = list(self._boxes[box])
            amount = random.randint(4, 6)
            while amount > 0 and cells:
                index = random.randint(0, len(cells) - 1)
                cell = cells[index]
                del cells[index]
                self._permanent.append(cell)
                self._grid[cell] = ""
                amount -= 1

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

    def grid_string(self):
        """Returns the puzzle in a human readable string"""
        count = 1
        rows = "     A  B  C   D  E  F   G  H  I\n"
        for key in self._grid:
            cell = self._grid[key]

            if cell == "":
                cell = " "
            if count == 1:
                rows += "   |-----------------------------|\n1: | "
            if count % 3 == 0:
                rows += cell + " | "
            else:
                rows += cell + "  "
            if count % 9 == 0 and count % 27 == 0:
                rows += "\n   |"
            elif count % 9 == 0:
                if count == 9:
                    rows += "\n2: | "
                elif count == 18:
                    rows += "\n3: | "
                elif count == 36:
                    rows += "\n5: | "
                elif count == 45:
                    rows += "\n6: | "
                elif count == 63:
                    rows += "\n8: | "
                elif count == 72:
                    rows += "\n9: | "
            if count % 27 == 0:
                if count == 81:
                    rows += "-----------------------------|\n"
                elif count == 27:
                    rows += "-----------------------------|\n4: | "
                elif count == 54:
                    rows += "-----------------------------|\n7: | "
                else:
                    rows += "-----------------------------|\n   | "
            count += 1
        return rows

    def update_dictionaries(self):
        """
        Updates rows, columns, and 3x3s dictionaries
        to reflect current game grid answers.
        """
        # clear dictionaries
        for key in self._3x3s:
            self._3x3s[key].clear()
        for key in self._rows:
            self._rows[key].clear()
        for key in self._columns:
            self._columns[key].clear()

        # Put current game grid values in dictionaries
        # this is only called after all cells have answers (no blanks)
        for cell in self._grid:
            self._rows[cell[1]].append(self._grid[cell])
            self._columns[cell[0]].append(self._grid[cell])
            self._3x3s[self.get_box(cell)].append(self._grid[cell])

    def data_validation(self, answer: str):
        cell, answer = self.strip_string(answer)
        if cell == "":
            return False, self.grid_string() + "\nInput is invalid."
        else:
            return True, self.grid_string() + "\nData is valid"

    def strip_string(self, string):
        """
        Takes string strips all extraneous characters.
        Returns tuple of (cell coordinates, cell answer).
        """
        cell = ""
        answer = ""
        for i in string:
            if i not in "ABCDEFGHIabcdefghi123456789":
                string = string.replace(i, "")

        if len(string) == 3:
            if string[0] in "ABCDEFGHIabcdefghi":
                cell += string[0].upper()
                cell += string[1]
            elif string[0] in "123456789":
                cell += string[1].upper()
                cell += string[0]
            answer = string[2]

        return cell, answer

    def process_data(self, answer: str):
        cell, answer = self.strip_string(answer)
        if cell != "" and cell not in self._permanent:
            return self.grid_string() + "\nCannot edit provided answers."
        else:
            self._grid[cell] = answer
            return self.grid_string() + "\nNext answer?"

    def check_game_state(self):
        blanks = 0
        for key in self._grid:
            if self._grid[key] == " ":
                blanks += 1
                break

        if blanks == 0:
            self.update_dictionaries()  # updates row, column, and 3x3 dictionaries to match game
            if self.is_valid(self._grid):
                return True, "\n\nYYOU WIN! Well done!"
            else:
                return False, "\n\nPuzzle invalid, YOU LOSE!"
        else:
            return False, "Game still going."
