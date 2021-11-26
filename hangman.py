# Author: Jacob Russell
# Class: CS372 Networking
# Date: November 23, 2021
# Description: A game of hangman used for a server-client game.
# https://www.randomlists.com/data/words.json (list of random words used for game)
import json
import random

class Hangman:
    """A game of hangman"""

    def __init__(self):
        self._secret_word = ""  # stores the word set by the server that the client has to guess
        self._game_state = None  # whether client has won
        self._revealed = ""  # stores the string of correctly guessed letters
        self._letters = []  # list of letters the client has guessed
        self._no_of_mistakes = 0  # number of mistakes made
        self._mistakes_allowed = 8  # total number of mistakes allowed
        self._display = [
            ["       _________,       "],
            ["       | /      |       "],
            ["       |/       0       "],
            [r"       |      / | \    "],
            ["       |        |       "],
            [r"       |       / \     "],
            [r"      /|\              "],
            [r" ___ /_|_\___          "]
        ]

    def set_secret_word(self, word):
        self._secret_word = word.lower()
        for i in range(len(word)):  # what is revealed to the client as they guess letters
            self._revealed += "_"

    def get_secret_word(self):
        return self._secret_word

    def get_revealed(self):
        return self._revealed

    def get_display(self):
        return self._display

    def display_string(self, mistakes=8):
        """
        To make the hangman display a print-friendly string.
        Takes number of mistakes (rows to print). Defaults to all.
        """
        string = ""
        for i in range(len(self._display) - mistakes, len(self._display)):
            string += "\r\n" + str(self._display[i])
        new_string = string.replace("[", "").replace("]", "").replace("'", "").replace(r'\\', r'\ ')
        return new_string

    def add_letter(self, letter):
        """
        Take given letter, check if in secret word. If it is, then
        update the revealed word. Then check win status.
        """
        self._letters.append(letter)
        if letter in self._secret_word:
            print("Correct letter guessed!")
            self.update_revealed(letter)
            if "_" not in self._revealed:  # if all letters guessed
                # print("Client wins!")  # for debugging
                self._game_state = "Won"
            return True
        else:
            self._no_of_mistakes += 1
            print("Wrong letter guessed!")
            if self._no_of_mistakes >= self._mistakes_allowed:  # if too many wrong guesses made
                print("Too many mistakes made.")
                self._game_state = "Lost"
            return False

    def get_letters(self):
        return self._letters

    def get_game_state(self):
        return self._game_state

    def update_revealed(self, letter):
        """Adds a correctly guessed letter to the revealed string using slices"""
        word = self._secret_word
        index = 0
        for i in word:
            if i == letter:  # update for each instance of the letter found
                if index == len(self._revealed):  # if new letter at end of string
                    string = self._revealed[:-1] + letter
                elif index == 0:  # if new letter at beginning of string
                    string = letter + self._revealed[1:]
                else:  # if new letter at neither beginning nor end
                    string = self._revealed[:index] + letter + self._revealed[index + 1:]
                self._revealed = string
                # print("self._revealed after updating: ", self._revealed)  # for debugging
            index += 1

    def get_no_of_mistakes(self):
        return self._no_of_mistakes

    def new_word(self):
        # Get new secret word from random list
        word_list = json.load(open("words.json"))
        word_range = len(word_list["data"]) - 1
        word_index = random.randint(0, word_range)
        word = word_list["data"][word_index]
        self.set_secret_word(word)
        # print("Secret word is: ", word)