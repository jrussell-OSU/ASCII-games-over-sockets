# Author: Jacob Russell
# Date: November 30, 2021
# Sudoku Game
import random


class SudokuGame:
    """A game of sudoku"""
    def __init__(self):
        self._board = {}
        self._3x3s = {}
        self._rows = {}
        self._columns = {}
        self.populate()


    def populate(self):
        """
        Populate coordinate keys into the board dictionaries.
        Populates  row, column, and 3x3 box dictionaries with
        alpha-numeric coordinates as keys and blank values.
        """

        # Populate board with coordinates as dictionary keys
        for num in "123456789":
            for letter in "ABCDEFGHI":
                self._board[letter + num] = ""

        # Populate rows (in dictionary)
        for i in range(1, 10):
            self._rows[str(i)] = []
            for letter in "ABCDEFGHI":
                self._rows[str(i)].append(letter + str(i))

        # Populate columns
        for letter in "ABCDEFGHI":
            self._columns[letter] = []
            for i in range(1, 10):
                self._columns[letter].append(letter + str(i))

        # Populate 3 x 3 boxes
        self._3x3s["1"] = ["A1", "B1", "C1", "A2", "B2", "C2", "A3", "B3", "C3"]
        self._3x3s["2"] = ["D1", "E1", "F1", "D2", "E2", "F2", "D3", "E3", "F3"]
        self._3x3s["3"] = ["G1", "H1", "I1", "G2", "H2", "I2", "G3", "H3", "I3"]
        self._3x3s["4"] = ["A4", "B4", "C4", "A5", "B5", "C5", "A6", "B6", "C6"]
        self._3x3s["5"] = ["D4", "E4", "F4", "D5", "E5", "F5", "D6", "E6", "F6"]
        self._3x3s["6"] = ["G4", "H4", "I4", "G5", "H5", "I5", "G6", "H6", "I6"]
        self._3x3s["7"] = ["A7", "B7", "C7", "A8", "B8", "C8", "A9", "B9", "C9"]
        self._3x3s["8"] = ["D7", "E7", "F7", "D8", "E8", "F8", "D9", "E9", "F9"]
        self._3x3s["9"] = ["G7", "H7", "I7", "G8", "H8", "I8", "G9", "H9", "I9"]

    def create_solution(self):
        """Creates sudoku puzzle solution to be solved"""
        for i in range(1, 10):
            pass

    def print_board(self):
        count = 1
        rows = ""
        for key in self._board:
            rows += key + " "
            if count % 9 == 0:
                rows += "\n"
            count += 1
        print(rows)


game = SudokuGame()
game.print_board()
print(game._rows)
print(game._columns)
