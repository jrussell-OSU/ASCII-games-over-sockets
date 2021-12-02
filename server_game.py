# Author: Jacob Russell
# Class: CS372 Networking
# Date: November 23, 2021
# Description: Server that hosts games over sockets
# Works Cited: https://docs.python.org/3.4/howto/sockets.html ; https://realpython.com/python-sockets/
from socket import *
import select
from hangman import *
from bulls_and_cows import *
from spaceships import *
from sudoku import *

########################################################################################################################
# Server Functions



########################################################################################################################


def send_message(sock, message: str):
    """Takes socket and message, encodes the message and sends to socket"""
    if len(message) > 4095:  # don't accept large inputs
        print("ERROR: INPUT TOO LARGE. QUITTING...")
        # print("Too large message is:", message)  # for debugging
        sock.send(bytes("/q"))
        sock.close()
        quit()
    sock.send(bytes(message, 'utf-8'))


def read_message(sock):
    msg = sock.recv(4096).decode('utf-8')
    return msg


def close_and_quit():
    send_message(c_sock, "Goodbye.")
    c_sock.close()
    server_socket.close()
    quit()


def get_game():
    """Gets which game client would like to play."""
    print("Asking client which game they would like to play...")
    games_list = ["(h)angman", "(b)ulls and cows", "(s)paceships", "sudo(k)u"]
    game = None
    # valid_game = False
    send_message(c_sock, "Which game would you like to play?\n"
                 + str(games_list).replace("[", "").replace("]", "").replace("'", ""))
    while True:  # continue loop until client picks valid game
        received = c_sock.recv(4096).decode('utf-8')
        if received == "/q":  # if client wants to quit
            close_and_quit()
        if received == "h":
            print("Client chose Hangman.")
            return Hangman()
        elif received == "b":
            print("Client chose Bulls and Cows.")
            return BullsAndCows()
        elif received == "s":
            print("Client chose Spaceships.")
            return Spaceships()
        elif received == "k":
            print("Client chose Sudoku.")
            return Sudoku()
        else:  # if client didn't choose a game
            send_message(c_sock, "Invalid entry. Try again!")

########################################################################################################################
# Game Server

# Create socket, accept client connection, maintain server loop
# Run game framework (which can accept multiple games built for this server interchangeably
# Close server when client quits

########################################################################################################################


# Create server socket, bind to localhost on specified port
server_host = 'localhost'
server_port = 9998
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((server_host, server_port))

# Set server to listen for connection
server_socket.listen(1)  # listen for only one connection
print("Ready to accept a connection...")

# Accept connection:
(c_sock, address) = server_socket.accept()
print("Client has joined.")

# Get which game client wants to play. Chooses hangman as default.
game = get_game()

# Welcome player to game and invite first move
send_message(c_sock, game.get_messages("welcome"))

while True:
    server_received, server_sent, server_other = select.select(
        [c_sock], [], [])

    # Get messages from client
    if server_received:  # if there is something waiting to be received by server
        received = read_message(c_sock)
        # print("Received:", received)  for debugging

        # check if client wants to quit
        if received == "/q":  # if client quits, close all sockets and quit program
            print("Client has left the game.")
            close_and_quit()

        # Validate client input
        while True:
            (valid, msg) = game.data_validation(received)
            if not valid:
                send_message(c_sock, msg)  # send reason not valid
                received = read_message(c_sock)
                continue
            else:
                break

        # Process client input, check game state, respond to client
        response = game.process_data(received)  # hold until game state is checked

        # check game state
        print("CHecking game state")  # for debugging
        (state, message) = game.check_game_state()
        if state:  # if game won or lost or drawn
            send_message(c_sock, response + message + "\nStart a new game? (y)es or (n)o")
            # Play again?
            while True:
                received = read_message(c_sock)
                if received == "y":
                    # Get new game, welcome player, and invite first move
                    game = get_game()
                    send_message(c_sock, game.get_messages("welcome"))
                    break
                elif received == "n":
                    close_and_quit()
                else:
                    send_message(c_sock, "Invalid response.")

        else:  # if game not won or lost, send response to move
            send_message(c_sock, response)

