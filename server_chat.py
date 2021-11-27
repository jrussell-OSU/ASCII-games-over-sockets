# Author: Jacob Russell
# Class: CS372 Networking
# Date: November 23, 2021
# Description: A client-server chat program using a python socket
# Works Cited: https://docs.python.org/3.4/howto/sockets.html and https://realpython.com/python-sockets/

from socket import *
import select

# Server side instructions:

"""
Server
1. The server creates a socket and binds to ‘localhost’ and port xxxx
2. The server then listens for a connection
3. When connected, the server calls recv to receive data
4. The server prints the data, then prompts for a reply
5. If the reply is /q, the server quits
6. Otherwise, the server sends the reply
7. Back to step 3
8. Sockets are closed (can use with in python3)
"""


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
print("Client has joined the chat.")


while True:
    # Accept connection:
    server_received, server_sent, server_other = select.select(
        [client_socket], [], [])
    if server_received:  # if there is something waiting to be received by server
        data_received = client_socket.recv(2048)
        received_message = data_received.decode('utf-8')
        print("Client:", received_message)
        if received_message == "/q":  # if client quits, close all sockets and quit program
            print("Client has left the chat room.")
            client_socket.close()
            server_socket.close()
            quit()
        server_input = input("> ")
        message = bytes(server_input, 'utf-8')
        client_socket.send(message)






#ready_to_read, ready_to_write, in_error = select.select(\
 #   potential_readers, potential_writers, potential_errs, timeout)
