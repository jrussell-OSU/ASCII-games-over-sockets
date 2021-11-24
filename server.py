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

# Server loop
while True:
    # Accept connection:
    (client_socket, address) = server_socket.accept()
    print("Client socket, address: ", client_socket, " ", address)
    #server_received, server_sent, server_other = select.select(
        #[client_socket], [server_socket], [])
    server_received = client_socket.recv(1024)
    print("received information from client: ", server_received.decode('utf-8'))



#ready_to_read, ready_to_write, in_error = select.select(\
 #   potential_readers, potential_writers, potential_errs, timeout)
