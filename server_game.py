# Author: Jacob Russell
# Class: CS372 Networking
# Date: November 23, 2021
# Description: The server side of a client-server hangman game using sockets on a localhost
# Works Cited: https://docs.python.org/3.4/howto/sockets.html ; https://realpython.com/python-sockets/
# https://www.randomlists.com/data/words.json (list of random words used for game)
from socket import *
import select
from hangman import *
import json
import random


# Create server socket, bind to localhost on specified port
server_host = 'localhost'
server_port = 9998
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((server_host, server_port))

# Set server to listen for connection
server_socket.listen(1)  # listen for only one connection
print("Ready to accept a connection...")

# Accept connection:
(client_socket, address) = server_socket.accept()
print("Client has joined.")

# Start new game of hangman
game = Hangman()

# Get new secret word from random list
word_list = json.load(open("words.json"))
word_range = len(word_list["data"]) - 1
word_index = random.randint(0, word_range)
word = word_list["data"][word_index]
game.set_secret_word(word)
print("Secret word is: ", word)

# Get new secret word
# UNCOMMENT FOLLOWING LINES IF YOU WANT TO MANUALLY CHOOSE WORD
# secret_word = input("Please enter secret word> ")
# game.set_secret_word(secret_word)

# Invite client to play hangman
client_socket.send(bytes("Welcome to Hangman! You lose, you die.\r\nGuess a letter.".encode('utf-8')))
print("Waiting for client...")

while True:
    server_received, server_sent, server_other = select.select(
        [client_socket], [], [])

    # Get messages from client
    if server_received:  # if there is something waiting to be received by server
        data_received = client_socket.recv(4096)
        letter = data_received.decode('utf-8')
        print("Received letter:", letter)
        # print("Current revealed:", game.get_revealed())  for debugging
        if letter == "/q":  # if client quits, close all sockets and quit program
            print("Client has left the game.")
            client_socket.close()
            server_socket.close()
            quit()

        # Get letter from client and pass to hangman game
        letter = letter.lower()

        # Check if letter is a duplicate
        if letter in game.get_letters():  # if duplicate letter received
            client_socket.send(bytes(("Duplicate letter, try again. All received letters: " +
                                      str(game.get_letters())).encode('utf-8')))

        # Add letter and process
        else:
            # If a correct letter is guessed
            if game.add_letter(letter):
                # check game state
                if game.get_game_state() == "Won":  # if game is won
                    print("Game is won")
                    client_socket.send(bytes("\nYou win!!! Congratulations!\nGoodbye".encode('utf-8')))
                else:
                    client_socket.send(bytes(("Correct letter guessed!\nRevealed word: "
                                              + game.get_revealed()).encode('utf-8')))
            # If wrong letter guessed
            else:
                if game.get_game_state() == "Lost":  # if game lost
                    print("Game is lost")
                    client_socket.send(bytes((game.display_string() + "\n*****YOU DIED*****\nGoodbye").encode('utf-8')))
                else:
                    client_socket.send(bytes((game.display_string(game.get_no_of_mistakes()) + "\nWrong letter guessed!\nRevealed word: "
                                              + game.get_revealed()).encode('utf-8')))

        # Check game state
        if game.get_game_state() is not None:   # if game is won
            print("Closing connection and exiting...")
            client_socket.close()
            server_socket.close()
            quit()




