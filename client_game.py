# Author: Jacob Russell
# Class: CS372 Networking
# Date: November 23, 2021
# Description: The client side of a client-server hangman game using sockets on a localhost
# Works Cited: https://docs.python.org/3.4/howto/sockets.html and https://realpython.com/python-sockets/
# https://www.programiz.com/python-programming/methods/built-in/bytes
from socket import *
import select


# Create a socket:
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(('localhost', 9998))
print("You are now connected to Hangman!")
# print("Please wait while the host selects a secret word...")

while True:
    client_received, client_sent, client_other = select.select(
        [client_socket], [], [])
    if client_received:

        # receive and print messages from server
        server_message = client_socket.recv(4096).decode('utf-8')
        print(server_message)

        # Choose whether to play again
        if "Play again?" in server_message:
            response_valid = False
            while not response_valid:
                response = input("> ")
                if response == "y" or response == "n":
                    client_socket.send(bytes(response, 'utf-8'))
                    response_valid = True
                else:
                    print("Response must be (y)es or (n)o.")
                    continue


        # Quit if game is over
        elif "Goodbye" in server_message:
            print("Closing connection and exiting...")
            client_socket.close()
            quit()

        else:
            # Get letter from client
            letter_validated = False
            client_input = input("> ")

            # Data validation on client input
            while not letter_validated:
                if client_input == "/q":  # if client wants to quit
                    client_socket.send(bytes("/q".encode('utf-8')))
                    print("You have exited the game.")
                    client_socket.close()
                    quit()
                elif len(client_input) > 1:
                    print("Only one letter allowed.")
                    client_input = input("Try again> ")
                elif len(client_input) == 0:
                    print("Blank entries not accepted.")
                    client_input = input("Try again> ")
                elif client_input not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
                    print("Only English alphabet letters accepted.")
                    client_input = input("Try again> ")
                else:
                    letter_validated = True

            letter = bytes(client_input, 'utf-8')
            client_socket.send(letter)
