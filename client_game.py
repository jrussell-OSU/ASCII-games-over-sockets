# Author: Jacob Russell
# Class: CS372 Networking
# Date: November 23, 2021
# Description: Client to connect to game server
# Works Cited: https://docs.python.org/3.4/howto/sockets.html and https://realpython.com/python-sockets/
# https://www.programiz.com/python-programming/methods/built-in/bytes
from socket import *
import select


# Client functions
def send_message(sock, message: str):
    """Takes socket and message, encodes the message and sends to socket"""
    sock.send(bytes(message, 'utf-8'))


def read_message(sock):
    message = sock.recv(4096).decode('utf-8')
    return message


# Create a socket:
c_sock = socket(AF_INET, SOCK_STREAM)
c_sock.connect(('localhost', 9998))
print("You are now connected to the Game Server!\nEnter /q anytime to quit.\n")

while True:
    client_received, client_sent, client_other = select.select(
        [c_sock], [], [])
    if client_received:

        # get message from server
        received = read_message(c_sock)
        print(received)

        # parse message from server
        if "Goodbye" in received:
            print("Exiting...")
            c_sock.close()
            quit()

        # send a response
        response = input("> ")
        while not response:
            print("Blank entries are invalid, try again.")
            response = input("> ")
        while len(response) > 1000:
            print("Too large an input, try again.")
            response = input("> ")
        send_message(c_sock, response)


