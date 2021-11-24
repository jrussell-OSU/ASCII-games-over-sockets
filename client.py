# Author: Jacob Russell
# Class: CS372 Networking
# Date: November 23, 2021
# Description: A client-server chat program using a python socket
# Works Cited: https://docs.python.org/3.4/howto/sockets.html and https://realpython.com/python-sockets/
# https://www.programiz.com/python-programming/methods/built-in/bytes
from socket import *
import select

# Create a socket:
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(('localhost', 9998))

while True:
    client_input = input()
    message = bytes(client_input, 'utf-8')
    client_socket.send(message)
    if client_input == "/q":
        print("client has quit")
        break
    client_received, client_sent, client_other = select.select(
        [client_socket], [], [])
    if client_received:
        data_received = client_socket.recv(2048)
        print("Message from server: ", data_received.decode('utf-8'))
        print("What is your response to the server?")

