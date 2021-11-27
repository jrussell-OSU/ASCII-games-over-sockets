# Author: Jacob Russell
# Class: CS372 Networking
# Date: November 25, 2021
# Description: A game of hangman used for a server-client game.
# https://www.randomlists.com/data/words.json (list of random words used for game)
import json
import random


class Hangman:
    """A game of hangman"""

    def __init__(self):
        self._secret_word = ""  # stores the random word the client has to guess
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
        self._messages = {   # dictionary that stores general messages sent to the client
            "welcome": "Welcome to Hangman! Guess a random word.\nIf you get it wrong, you die!"
                       "\nGuess a letter."
        }
        self.new_word()

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
        letter = letter.lower()
        self._letters.append(letter)
        if letter in self._secret_word:
            print("Correct letter guessed!")
            self.update_revealed(letter)
            if "_" not in self._revealed:  # if all letters guessed
                # print("Client wins!")  # for debugging
                self._game_state = "Won"
            return "Good guess!\n" + self._revealed
        else:
            self._no_of_mistakes += 1
            print("Wrong letter guessed!")
            if self._no_of_mistakes >= self._mistakes_allowed:  # if too many wrong guesses made
                print("Too many mistakes made.")
                self._game_state = "Lost"
            return self.display_string(self._no_of_mistakes) + "\nWrong!\n" + self._revealed

    def get_letters(self):
        return self._letters

    def check_game_state(self):
        if self._game_state == "Won":
            message = "\nSecret word is: " + self.get_secret_word() + \
                      "\nYou win!!! Congratulations!"
            return True, message
        elif self._game_state == "Lost":
            message = self.display_string() + "\n*****YOU DIED*****" \
                      "\nSecret word was: " + self.get_secret_word()
            return True, message
        else:
            message = "Game not over."
            return False, message

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
        # print("secret word is: ", self._secret_word)  # for debugging

    def get_no_of_mistakes(self):
        return self._no_of_mistakes

    def new_word(self):
        # Get new secret word from random list
        word = ""
        word_list = json.load(open("words.json"))
        word_range = len(word_list["data"]) - 1
        while len(word) < 5:  # only take words 5 letters or more
            word_index = random.randint(0, word_range)
            word = word_list["data"][word_index]
        self.set_secret_word(word)
        # print("Secret word is: ", word)

    def get_messages(self, key: str):
        """Takes key and returns value from hangman's message dictionary"""
        return self._messages[key]

    def data_validation(self, letter):
        """Takes data and does validation and returns  message"""
        if len(letter) != 1:
            return False, "Must be a single letter."
        elif letter not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
            return False, "Must be an English alphabet letter."
        elif letter in self._letters:
            return False, "Duplicate. All received letters: " + str(self._letters)
        else:
            return True, "Data is valid."

    def process_data(self, letter):
        """Takes a letter and returns: whether correct, and message"""
        message = self.add_letter(letter)
        return message

