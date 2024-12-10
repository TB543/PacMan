from numpy import array, array_equal
from map import PLAYER_MAP
from Ghost import Ghost


class PacMan:
    """
    the class to represent the player

    ================================================== ENUMS/GLOBALS ===================================================

    The following enums are contained within this class
        directions - determines the direction the player is facing, either N, S, E or W
        pellet_score - keeps track of the points pacman has from eating pellets
        ghost_score - keeps track of the points pacman has from eating ghosts
        max_pellet_score - keeps track of the max score which when reaches means the player wins

    ====================================================== FIELDS ======================================================

    Has the following fields:
        position - to determine the position of the player on the map in the format [x, y]
        facing - determines which way the player is facing and thus which way they will move
        next_facing - where the player will move at the next intersection if their selected move is not valid
        image - the image of the player that will be displayed on screen

    ==================================================== FUNCTIONS =====================================================

    Has the following functions:
        kill - the function when the player loses the game
        win - the function when the player wins the game'
        eat_ghost - handles when the player eats a ghost by increasing the score
        move - moves the player based on the facing position
        set_facing - sets the direction the player is facing
    """

    # creates enums for the different ways the player can face, stored as vectors to update position
    N = array([0, -1])
    S = array([0, 1])
    E = array([1, 0])
    W = array([-1, 0])

    # sets the score variables
    pellet_score = 0
    ghost_score = 0
    max_pellet_score = 0
    for row_num in range(len(PLAYER_MAP)):
        for column_num in range(len(PLAYER_MAP[row_num])):
            if PLAYER_MAP[row_num][column_num] == 2:
                max_pellet_score += 10
            elif PLAYER_MAP[row_num][column_num] == 3:
                max_pellet_score += 50

    def __init__(self, position):
        """
        creates the player object with the following fields

        :param position: the given start position for the player
        """

        self.position = array(position)
        self.facing = array([0, 0])
        self.next_facing = array([0, 0])
        self.image = None

    @staticmethod
    def kill():
        """
        kills the player when eaten by a ghost
        """

        print(f"You Lose, Score: {PacMan.pellet_score + PacMan.ghost_score}")
        exit(0)

    @staticmethod
    def win():
        """
        handles when the player wins the game, ie all pellets are eaten
        """

        print(f"You Win, Score: {PacMan.pellet_score + PacMan.ghost_score}")
        exit(0)

    @staticmethod
    def eat_ghost():
        """
        handles when the player eats a ghost, increases the players score
        """

        PacMan.ghost_score = 200 if PacMan.ghost_score == 0 else PacMan.ghost_score * 2

    def set_facing(self, direction):
        """
        changes the direction the player is facing

        :param direction: the new direction for the player to face
        """

        self.next_facing = direction

    def move(self):
        """
        moves the player based on where they are facing
        player will only move if the new position is a 1 on the player map
        """

        # handles when player is at end of map
        map_elem = PLAYER_MAP[self.position[1]][self.position[0]]
        if type(map_elem) == tuple and array_equal(map_elem[2], self.next_facing):
            self.position = array(map_elem[:2])

        # moves the player
        next_facing = PLAYER_MAP[self.position[1] + self.next_facing[1]][self.position[0] + self.next_facing[0]]
        if next_facing in [1, 2, 3] or type(next_facing) == tuple:
            self.facing = self.next_facing
        facing = PLAYER_MAP[self.position[1] + self.facing[1]][self.position[0] + self.facing[0]]
        if facing in [1, 2, 3] or type(next_facing) == tuple:
            self.position += self.facing

        # handles player eating pellet
        if PLAYER_MAP[self.position[1]][self.position[0]] == 2:
            PLAYER_MAP[self.position[1]][self.position[0]] = 1
            PacMan.pellet_score += 10

        # handles player eating power pellet
        if PLAYER_MAP[self.position[1]][self.position[0]] == 3:
            PLAYER_MAP[self.position[1]][self.position[0]] = 1
            Ghost.frighten()
            PacMan.pellet_score += 50

        # handles when the player wins the game
        if PacMan.pellet_score == PacMan.max_pellet_score:
            PacMan.win()
