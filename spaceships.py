# Author: Jacob Russell
# Class: CS372 Networking
# Date: November 27, 2021
# Description: Game of Spaceships for a game server
import random


class Spaceships:
    """A game of Spaceships"""

    def __init__(self):
        self._server_board = {}  # stores game board where ships are placed
        self._client_board = {}
        self._coords = {"server": [], "client": []}  # stores available coordinates for ships
        self._server_shots = {}  # stores shots fired
        self._client_shots = {}
        self._coords_list = []
        self.populate_coords()
        self._ship_list = ["s2", "a3", "b4", "c5"]
        self._client_ships = ["s2", "a3", "b4", "c5"]
        self._server_placed = False  # whether all ships placed and game ready to begin
        self._client_placed = False
        self._ship_layouts = {"s": [], "a": [], "b": [], "c": []}  # Stores all valid arrangements for each ship type.
        self._game_state = None
        self._hits = {"server": [], "client": []}
        self.pop_ship_layouts()
        self.server_place_ships()
        self._ships_exploded = {"server": 0, "client": 0}

        self._messages = {
            "welcome": "Welcome to Spaceship! "
                       "Instructions: You will place your ships on a board and attempt to blow up\n"
                       "the enemy's ships on a different board. The enemy will also shoot at your ships.\n"
                       "Ships (and lengths): Scout Ship(2), Assault Ship(3), Battlecruiser(4), Capital Ship(5)\n"
                       "Ships cannot be placed diagonally. When placing a ship, type all the coordinates.\n"
                       "For example: Where to place your assault ship? Valid response: G1, G2, G3 (or g1, g2, g3)\n"
                       "\nNow, please place your first ship.\n\n"
                       "Where should I put your Scout Ship?\n",
            "fire": ["Enemy launches a missile! Watch out!"]
        }

        # Ship types:
        # s2 = scout ship, 2 spaces
        # a3 = assault ship, 3 spaces
        # b4 = battlecruiser, 4 spaces
        # c5 = capital ship, 4 spaces

    def get_messages(self, key):
        message = self._messages[key]
        if key == "welcome":
            message = self._messages[key] + "\n" + self.display_board(self._client_board)
        return message

    def populate_coords(self):
        """Populates all possible coordinates"""
        for i in range(1, 9):
            for letter in "ABCDEFGH":
                coord = letter + str(i)
                self._coords["server"].append(coord)
                self._coords["client"].append(coord)
                self._server_board[coord] = "-"
                self._client_board[coord] = "-"
                self._server_shots[coord] = "-"
                self._client_shots[coord] = "-"
                self._coords_list.append(coord)

    def server_place_ships(self):
        """Randomly places all server's ships"""
        for ship in self._ship_list:
            ship_layouts = self._ship_layouts[ship[0]]
            while True:
                index = random.randint(0, len(ship_layouts) - 1)
                rand_layout = ship_layouts[index]
                invalid_count = 0
                temp = []
                for square in rand_layout:
                    if square not in self._coords["server"]:
                        invalid_count += 1
                    else:
                        temp.append(square)
                if invalid_count > 0:
                    continue  # layout has occupied coordinates, get new random layout
                else:
                    for s in temp:
                        self._server_board[s] = ship[0]  # add ship to server's board
                        self._coords["server"].remove(s)  # remove square from coordinates list
                    break
        self._server_placed = True  # All server ships now placed
        print(self.display_board(self._server_board))  # for debugging

    def get_ship_name(self, ship):
        if ship == "s":
            return "Scout Ship (2)"
        elif ship == "a":
            return "Assault Ship (3)"
        elif ship == "b":
            return "Battlecruiser (4)"
        else:
            return "Capital Ship (5)"

    def client_place_ships(self, layout):
        """Takes client input and places ships"""
        # Ship types:
        # s2 = scout ship, 2 spaces
        # a3 = assault ship, 3 spaces
        # b4 = battlecruiser, 4 spaces
        # c5 = capital ship, 4 spaces

        # See if input layout is valid
        ship = self._client_ships[0]
        layouts = self._ship_layouts[ship[0]]

        if layout in layouts:
            for square in layout:
                self._client_board[square] = ship[0]
                self._coords["client"].remove(square)
            del self._client_ships[0]
        else:
            # print("Client layout was invalid!!")
            return "Layout input was invalid, try again."

        # Check if all ships placed
        if len(self._client_ships) <= 0:
            # print("All client ships have been placed.")
            self._client_placed = True
            return self.display_board(self._client_board) + "\nAll ships placed!\n\nTake a shot! Enter the coordinates."  # all ships placed, time to start firing
            # return self.display_board(self._client_board) + "All ships placed."
        else:
            # print("sending response to client that ship is placed")
            return self.display_board(self._client_board) + "Ship placed, now place: " + \
                   self.get_ship_name(self._client_ships[0])

    def fire_shot(self, coords):
        """Used to fire automatic shot by server and take client coordinates for theirs"""

        # Fire server shot
        fire_message = self._messages["fire"][0]
        while True:
            server_shot = self.rand_coord()
            if self._server_shots[server_shot] == "-":
                break  # don't do a duplicate shot
        if self._client_board[server_shot] != "-":
            c_ship = self._client_board[server_shot]
            client_ship = self.get_ship_name(c_ship)
            self._server_shots[server_shot] = "X"
            self._client_board[server_shot] = "X"
            self._hits["client"].append(c_ship)  # Add hit to hit list
            print("server has hit these client ships: ", self._hits["client"])  # for debugging
            server_shot_msg = "Enemy hits your " + client_ship + ", on square: " + server_shot + \
                              ". " + self.explode("server") + "\nYour board:\n" \
                              + self.display_board(self._client_board)

        else:
            server_shot_msg = "Enemy misses!\n" + "Your board:\n" + self.display_board(self._client_board)
            self._server_shots[server_shot] = "0"

        # Fire client shot
        if self._server_board[coords] != "-":
            s_ship = self._server_board[coords]
            s_name = self.get_ship_name(s_ship)
            self._client_shots[coords] = "X"
            self._server_board[coords] = "X"
            self._hits["server"].append(s_ship)  # Add hit to hit list
            print("client has hit these sever ships: ", self._hits["server"])  # for debugging
            client_shot_msg = "Client hits! On square: " + coords + ". " + self.explode("client") \
                              + "\nYour shots grid:\n" + self.display_board(self._client_shots)
        else:
            self._client_shots[coords] = "0"
            client_shot_msg = "Client misses!\n" + "Your shots grid: \n" + self.display_board(self._client_shots)

        return fire_message + "\n" + server_shot_msg + "\n" + client_shot_msg + "\n" + "What is your next shot?"

    def explode(self, player):
        """Takes a player's hit_list and returns if any ships have exploded."""
        message = ""
        if player == "server":
            hit_list = self._hits["client"]
        else:
            hit_list = self._hits["server"]
        for i in hit_list:
            if i == "s":
                if hit_list.count("s") == 2:
                    message += "Scout Ship explodes! "
                    hit_list.remove(i)
                    break
            if i == "a":
                if hit_list.count("a") == 3:
                    message += "Assault Ship explodes! "
                    hit_list.remove(i)
                    break
            if i == "b":
                if hit_list.count("b") == 4:
                    message += "Battlecruiser explodes! "
                    hit_list.remove(i)
                    break
            if i == "c":
                if hit_list.count("c") == 5:
                    message += "Capital Ship explodes! "
                    hit_list.remove(i)
                    break
        if len(message) > 0:
            if player == "server":
                self._ships_exploded["client"] += 1
                if self._ships_exploded["client"] == 4:
                    self._game_state = "Lost"
            else:
                self._ships_exploded["server"] += 1
                if self._ships_exploded["server"] == 4:
                    self._game_state = "Won"

        return message

    def pop_ship_layouts(self):
        """Generates dictionary of all possible layouts for each type of ship"""
        starts = self._coords_list
        layouts = []
        alphabet = "ABCDEFGH"
        for start in starts:
            temp = [[], [], [], []]
            start_num = int(start[1])
            start_alpha = start[0]
            index = alphabet.index(start_alpha)
            lengths = [2, 3, 4, 5]
            for length in lengths:
                for i in range(length):
                    if start_num + (length - 1) < 9:
                        temp[0].append(start_alpha + str(start_num + i))
                    if start_num - (length - 1) > 0:
                        temp[1].append(start_alpha + str(start_num - i))
                    if index + length < 9:
                        temp[2].append(alphabet[index + i] + str(start_num))
                    if index - length > 0:
                        temp[3].append(alphabet[index - i] + str(start_num))
                for x in temp:
                    if 1 < len(x) < 6:
                        layouts.append(x)
                temp = [[], [], [], []]

        print("layouts: ", layouts)  # for debugging
        for layout in layouts:
            if len(layout) == 2:
                self._ship_layouts["s"].append(layout)
            elif len(layout) == 3:
                self._ship_layouts["a"].append(layout)
            elif len(layout) == 4:
                self._ship_layouts["b"].append(layout)
            elif len(layout) == 5:
                self._ship_layouts["c"].append(layout)

        # print("Layouts by ship: ", self._ship_layouts)

    def rand_coord(self):
        """Returns random available server shot"""
        while True:
            index = random.randint(0, 63)
            coord = self._coords_list[index]
            if self._server_shots[coord] == "-":  # if shot has not been made before
                break
        return coord

    def display_board(self, board):
        """Takes a board and prints it in a readable way w/coordinate axes"""
        # If square is blank, print coordinates. Otherwise print piece name
        board_list = [[], [], [], [], [], [], [], [], []]
        for l in " ABCDEFGH":  # make X coordinate labels
            board_list[0].append(l)
        for i in range(1, 9):  # make Y coordinate labels
            board_list[i].append(str(i))
        index = 1
        count = 1
        for value in board.values():  # pull values from boards
            board_list[index].append(value)
            if count % 8 == 0:
                index += 1
            count += 1
        board_string = ""
        for line in board_list:  # Put board into a readable string
            board_string += str(line) + "\n"
        print_string = board_string.replace("[", "").replace("]", "").replace(",", "").replace("'", "")
        return print_string

    def strip_string(self, string):
        stripped_string = string
        for i in string:
            print("Check character: ", i)
            if i not in "ABCDEFGHabcdefgh123456789":
                print(i, "not a letter or number.")
                stripped_string = string.replace(i, "")
                string = stripped_string
                print("Stripped_string so far: ", stripped_string)

        print("Given string: ", string, "Stripped string: ", stripped_string)  # for debugging
        return stripped_string

    def get_coords(self, string):
        """Takes a string and returns list of coordinates. Used for placing ships."""
        coordinates_list = []
        temp = ""
        for i in string:
            if i in "0123456789":
                temp += i
                coordinates_list.append(temp)
                temp = ""
            elif i in "ABCDEFGHabcdefgh":
                temp += i.upper()
            else:
                continue
        return coordinates_list

    def check_game_state(self):
        """Checks games state. Returns boolean and message."""
        if not self._game_state:
            return False, "Game still going"
        elif self._game_state == "Won":
            return True, "\n\nYou win! All enemy spaceships destroyed!"
        else:
            return True, "\n\n\nYou lose!"

    def data_validation(self, coords):
        # Make sure at least two
        if len(self.strip_string(coords)) < 2:
            return False, "Invalid coordinates, try again."
        # If client is still placing ships:
        if not self._client_placed:
            ship = self._client_ships[0]
            # print("Current client ship to be placed:", ship)
            length = int(ship[1])
            coordinates_list = self.get_coords(coords)  # put coordinates in a list
            # print("Received coords string:", coords, "coord list:", coordinates_list)

            # Check if coordinates valid and unoccupied
            for i in coordinates_list:
                if i not in self._coords_list:  # if coordinates are invalid
                    print("Invalid coordinates given: ", i)  # for debugging
                    return False, "Coordinates invalid. Try again."
                elif i not in self._coords["client"]:  # if coordinates occupied
                    print("Occupied coordinates given: ", i)  # for debugging
                    return False, "Coordinates already occupied. Try again."

            # Check if correct number of coordinates given for ship length.
            if len(coordinates_list) != length:
                return False, "Not enough coordinates provided. Need " + str(length) + " coordinates."

            # Make sure coordinates represent an actual valid arrangement of a ship
            # i.e. that the ship won't be going over edges, diagonal, etc.
            valid_layouts = self._ship_layouts[ship[0]]  # get all valid layouts for current ship type
            if coordinates_list not in valid_layouts:
                return False, "Invalid layout for this ship. Try again."
            else:
                print("Valid coordinates. Will now process data.")  # for debugging
                return True, "Valid coordinates. Will now process data."

        # If client is making a shot
        else:
            coords = self.get_coords(coords)[0]
            if coords not in self._coords_list:
                return False, "Invalid coordinates. Try again."
            print("Entering shot firing phase.")
            return True, "Valid firing coordinates, now running fire_shot()"

    def process_data(self, coords):
        if not self._client_placed:  # if client hasn't finished placing their ships
            return self.client_place_ships(self.get_coords(coords))
        else:
            coords = self.get_coords(coords)[0]
            return self.fire_shot(coords)
