# Author: Jacob Russell
# Class: CS372 Networking
# Date: November 23, 2021
# Description: A client-server chat program using a python socket
# Works Cited: Python documentation at docs.python.org, mostly https://docs.python.org/3.4/howto/sockets.html

from socket import *


# create socket
mySocket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)

