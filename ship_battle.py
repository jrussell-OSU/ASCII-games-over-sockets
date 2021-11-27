# Author: Jacob Russell
# Class: CS372 Networking
# Date: November 27, 2021
# Description: Game of Ship Battle for a game server

class ShipBattle:
    """A game of Ship Battle"""

    def __init(self):
        self._boards = {"server": [], "client": []}
        self._coords = {"server": [], "client": []}  # stores available coordinates for ships

