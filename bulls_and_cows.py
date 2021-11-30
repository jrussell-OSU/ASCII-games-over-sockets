# Author: Jacob Russell
# Class: CS372 Networking
# Date: November 27, 2021
# Description: A game of Bulls and Cows used for a server-client game.
import random


class BullsAndCows:
    """A game of Bulls and Cows"""

    def __init__(self):
        self._secret_num = ""  # stores random number (as string) the client has to guess
        self._game_state = None  # whether game is won or lost
        self._total_guesses = 10
        self._no_of_guesses = 0
        self._bulls = 0
        self._cows = 0
        self._guess = ""  # stores all valid guesses
        # Indexes: Bulls: 8, Cows 17, 22, 27, 32, 37
        self._display = ["|Bulls: ", "", "  |Cows: ", "", "  |Guess: ", "", "  -  ", "", "  -  ", "", "  -  ", "", "  "]
        self._running_display = ""
        self.new_num()  # get a new secret number
        self._messages = {
            "welcome": "Welcome to Bulls and Cows!\n"
                       "The object is to guess a random four digit integer.\n"
                       "All digits in the integer are unique, there are no repeating digits.\n"
                       "A 'Bull' is when you guess a correct digit in the correct position.\n"
                       "A 'Cow' is when you guess a correct digit but in wrong position.\n"
                       "Example: If the secret number is 1234, and you guess, 4321 you would have 0 bulls and 4 cows.\n"
                       "Whereas if you guessed 2134, you would have 2 bulls and 2 cows.\n\n"
                       "New secret number generated... \n"
                       "Please enter a four digit integer."
        }

    def get_messages(self, key):
        """returns message from self_messages dictionary with correct key"""
        return self._messages[key]

    def new_num(self):
        """Creates new secret 4 digit number w/all unique digits"""
        while True:
            count = 0
            num = str(random.randint(1000, 9999))
            for i in num:
                if num.count(i) > 1:  # if there are non-unique digits, get new number
                    count += 1
            if count == 0:
                # print("Secret number: ", num)  # for debugging
                self._secret_num = num
                break

    def data_validation(self, num: str):
        """Make sure number (string) is 4 digits"""
        if num == "/q":
            return False, "Goodbye."
        for i in num:
            if i not in "0123456789":
                return False, "Must be an integer."
        if len(num) != 4:
            return False, "Integer must be four digits."
        for p in num:
            if num.count(p) > 1:
                return False, "Integer must contain all unique digits."
        if num == self._guess:
            return False, "Duplicate guess.\n"
        return True, "Data is valid."

    def process_data(self, num):
        """Check number against secret number"""
        self._bulls = 0
        self._cows = 0
        self._guess = num
        self._no_of_guesses += 1

        # Set game state if guess is correct
        if num == self._secret_num:
            print("Number guessed! Client wins!")
            self._game_state = "Won"

        # Check number guess against secret number
        num_index = 0
        for i in num:
            secret_index = 0
            for p in self._secret_num:
                # print("Checking: " + i + " against: " + p)  for debugging
                if i == p:
                    if num_index == secret_index:  # if number in same position
                        self._bulls += 1
                    else:
                        self._cows += 1  # if num in secret num but diff position
                secret_index += 1
            num_index += 1

        # Set game state if too many guesses made
        if self._no_of_guesses >= self._total_guesses:
            print("Game lost!")
            self._game_state = "Lost"

        return self.display()

    def check_game_state(self):
        """Checks game state"""
        if self._game_state == "Won":
            return True, "\nYou win! Secret number is: " + self._secret_num
        elif self._game_state == "Lost":
            return True, "\nYou lost! Secret number is: " + self._secret_num
        else:
            return False, "Game not over yet."

    def display(self):
        """Returns a string of a human readable game update readout"""
        print("guess is: ", self._guess)
        self._display[1] = str(self._bulls)
        self._display[3] = str(self._cows)
        self._display[5] = self._guess[0]
        self._display[7] = self._guess[1]
        self._display[9] = self._guess[2]
        self._display[11] = self._guess[3]
        display_string = ""
        for i in self._display:
            display_string += i
        self._running_display += display_string + "\n"
        return self._running_display





