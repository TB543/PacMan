from map import GHOST_MAP
from numpy import array, array_equal
from numpy.linalg import norm
from random import choice


class Ghost:
    """
    A class to represent one of the pacman ghosts:
        Blinky - Red
        Inky - Blue
        Pinky - Pink
        Clyde - Orange

    ** Their movement patterns can be found and explained in the ghost_movement.py file **

    ================================================== ENUMS/GLOBALS ===================================================

    The following enums are contained within this class
        movement modes - determines the movement mode of the ghost, either CHASE, SCATTER, or FRIGHTENED
        directions - determines the direction the ghost is facing, either N, S, E or W

    There following globals are stored across all ghost objects
        global_mode - what to return mode to after frightened mode/eaten mode for all ghosts
        frightened - true or false, determines if ghosts are frightened
        chase_scatter_steps - a tracker to keep track of how long the ghosts have been in chase or scatter mode
        frightened_steps - a tracker to keep track of how long the ghosts have been in the frightened state
        ghosts - a list of all created ghosts
        pacman - the player object that will be used for targeting in chase mode

    ====================================================== FIELDS ======================================================

    Has the following fields:
        position - to determine the position of the ghosts on the map in the format [x, y]
        facing - determines which way the ghost is facing and thus which way they will move
        image - the image of the ghost that will be displayed on screen
        scatter - the given function to determine the target when the ghost is in scatter mode
        chase - the given function to determine the target when the ghost is in chase mode
        mode - to determine the mode of ghost, either CHASE, SCATTER, or FRIGHTENED
        eaten - a boolean to determine if the ghost is in eaten mode
        spawn - the given position when the ghost is created, ghost will return here when eaten

    ==================================================== FUNCTIONS =====================================================

    Has the following functions:
        set_pacman - sets the global pacman variable
        change_mode - will randomly switch between chase and scatter mode
        frighten - will switch all ghosts to frightened mode
        at_intersection - determines if the ghost is at an intersection on the map
        get_target - determines the target position of the ghost based on the movement mode
        path_find - determines which intersection path is the best to get to a given target
        move - moves the ghost based on the functions below
    """

    # creates enums for the different movement modes
    CHASE = "chase"
    SCATTER = "scatter"
    FRIGHTENED = "frightened"

    # creates variables across all ghosts to handle switching between movement modes
    global_mode = SCATTER
    frightened = False
    chase_scatter_steps = -1
    frightened_steps = -1
    ghosts = {}
    pacman = None

    # creates enums for the different ways the ghost can face, stored as vectors to update position
    N = array([0, -1])
    S = array([0, 1])
    E = array([1, 0])
    W = array([-1, 0])

    def __init__(self, name, position, scatter, chase):
        """
        Creates the ghost object with the following fields:

        :param name: the name of the ghost, this will determine the image path
        :param position: to determine the position of the ghosts on the map in the format [x, y]
        :param scatter: the target when the ghost is in scatter mode
        :param chase: the given function to determine the target when the ghost is in chase mode, should take a ghost
            and pacman as parameter and return the target tile
        """

        self.position = array(position)
        self.facing = array([0, 0])
        self.image = name
        self.scatter = scatter
        self.chase = chase
        self.mode = Ghost.global_mode
        self.eaten = False
        self.spawn = array(position)
        Ghost.ghosts[name] = self

    @staticmethod
    def set_pacman(pacman):
        """
        sets the global pacman variable, must be called before game is started

        :param pacman: the pacman object to set the global to
        """

        Ghost.pacman = pacman

    @staticmethod
    def change_mode():
        """
        Changes between Chase and Scatter modes occur on a fixed timer. The timer is  paused while the ghosts are in
        Frightened mode. When Frightened mode ends, the ghosts return to their previous mode, and the timer resumes
        where it left off. The ghosts start out in Scatter mode, and there are four waves of Scatter/Chase alternation
        defined, after which the ghosts will remain in Chase mode indefinitely. the durations of these phases are:

            Scatter for 7 steps, then Chase for 20 steps.
            Scatter for 7 steps, then Chase for 20 steps.
            Scatter for 5 steps, then Chase for 20 steps.
            Scatter for 5 steps, then switch to Chase mode permanently.

        ** Note: direction ghosts are facing are rotated 180 degrees if the movement mode changes **
        """

        # increases frightened steps until frightened mode is ended
        if Ghost.frightened and Ghost.frightened_steps < 6:
            Ghost.frightened_steps += 1

        # handles end frightened mode
        elif Ghost.frightened_steps >= 6:
            Ghost.frightened = False
            Ghost.frightened_steps = -1
            for ghost in Ghost.ghosts.values():
                ghost.mode = Ghost.global_mode

        # updates switches between chase and scatter mode
        else:
            Ghost.chase_scatter_steps += 1

            # switches to chase mode when enough scatter time has passed
            if Ghost.chase_scatter_steps in [7, 34, 59, 84]:
                Ghost.global_mode = Ghost.CHASE

            # switches to scatter mode when enough chase time has passed
            elif Ghost.chase_scatter_steps in [27, 54, 79]:
                Ghost.global_mode = Ghost.SCATTER

            # switches ghost direction by 180 degrees on mode change
            if Ghost.chase_scatter_steps in [7, 34, 59, 84, 27, 54, 79]:
                for ghost in Ghost.ghosts.values():
                    ghost.mode = Ghost.global_mode
                    ghost.facing = ghost.facing * -1

    @staticmethod
    def frighten():
        """
        switches all ghosts mode to frightened

        in this state their chosen path is random at every intersection
        ghosts will also switch directions by 180 degrees when switching to frightened mode
        """

        Ghost.frightened = True
        Ghost.frightened_steps = -1
        for ghost in Ghost.ghosts.values():
            if ghost.mode != Ghost.FRIGHTENED and (not ghost.eaten):
                ghost.facing = ghost.facing * -1
                ghost.mode = Ghost.FRIGHTENED

    def at_intersection(self):
        """
        Determines if the ghost is at an intersection based on the given map. ie if the ghost has 3 or 4 different
        directions they can move. Below are some examples:


            This is not an intersection:

                ---------------
                ---------------

            This is a 3 way intersection:

                     |   |
                ------   ------
                ---------------

            This is a 4 way intersection:

                     |   |
                ------   ------
                ------   ------
                     |  |

        a ghost is also at an intersection if they cannot continue going their current facing direction below are
        examples:

            This is a corner:

                ---------
                -----   |
                     |  |

            ** note: this will also return true when the ghost does not have any facing **

        :return: True if the ghost is at an intersection, False is they are not
        """

        # checks if ghost is at an intersection
        north = GHOST_MAP[self.position[1] - 1][self.position[0]]
        south = GHOST_MAP[self.position[1] + 1][self.position[0]]
        east = GHOST_MAP[self.position[1]][self.position[0] + 1]
        west = GHOST_MAP[self.position[1]][self.position[0] - 1]

        # checks if ghost cannot continue their current path
        corner = GHOST_MAP[self.position[1] + self.facing[1]][self.position[0] + self.facing[0]] == 0
        return [north, south, east, west].count(1) >= 3 or corner or array_equal(self.facing, array([0, 0]))

    def get_target(self):
        """
        Gets the ghosts current target location based on their current mode:

            If the mode is eaten, the target will be the ghosts spawn location
            If the mode is CHASE, the ghosts target location will be found by the given chase function
            If the mode is SCATTER, the ghosts target location will be found the by given scatter function
            If the mode is FRIGHTENED, an empty location will be given as movement will be random

        :return: a vector representing the target location of the ghost
        """

        # handles when the ghost is eaten
        if self.eaten:
            return self.spawn

        # handles when the ghost is in chase mode
        if self.mode == Ghost.CHASE:
            return self.chase(self, Ghost.pacman)

        # handles when the ghost is in scatter mode
        if self.mode == Ghost.SCATTER:
            return self.scatter

        # handles when the ghost is in frightened mode
        return array([])

    def path_find(self, target):
        """
        Updates the direction the ghost is facing based on its target location

            A ghost cannot turn around and go back the way it came, so its direction MUST be updated
            A ghost will update its direction based on which next step will result in being closer to the target

        :param target: the target tile the ghost is trying to get to (will be empty in frightened mode)
        """

        # gets all possible movements
        north = GHOST_MAP[self.position[1] - 1][self.position[0]]
        south = GHOST_MAP[self.position[1] + 1][self.position[0]]
        east = GHOST_MAP[self.position[1]][self.position[0] + 1]
        west = GHOST_MAP[self.position[1]][self.position[0] - 1]
        options = []

        # gets only valid movement options
        if east == 1 and self.facing[0] != -1:
            options.append(Ghost.E)
        if south == 1 and self.facing[1] != -1:
            options.append(Ghost.S)
        if west == 1 and self.facing[0] != 1:
            options.append(Ghost.W)
        if north == 1 and self.facing[1] != 1:
            options.append(Ghost.N)

        # random choice when ghost in frightened mode
        if self.mode == Ghost.FRIGHTENED:
            self.facing = choice(options)
            return

        # gets linear distance between target and all valid moves
        distances = {}
        for option in options:
            distances[norm(target - (self.position + option))] = option

        # sets the ghosts facing to the shortest linear distance
        self.facing = distances[min(distances.keys())]

    def move(self):
        """
        Updates the ghosts position based on the following logic

            If the ghost is not at an intersection, they will continue down the path
            If the ghost is at an intersection it updates where it is facing based on its target location
            Finally the ghosts position is updated based on the direction it is facing

        also checks for player collision, once before ghost is moved to check after player movement and once after ghost
        movement to check after ghost movement

        ** Note: Ghost.change_mode() must be called to update ALL ghosts movement modes before the individual ghosts
        can move **
        """

        # handles when ghost is at end of map
        map_elem = GHOST_MAP[self.position[1]][self.position[0]]
        if type(map_elem) == tuple and array_equal(map_elem[2], self.facing):
            self.position = array(map_elem[:2])

        # handles when the ghost has arrived back at spawn after being eaten
        if self.eaten and array_equal(self.position, self.spawn):
            self.eaten = False

        # handles ghost getting eaten
        if array_equal(self.position, self.pacman.position) and self.mode == Ghost.FRIGHTENED and (not self.eaten):
            self.mode = Ghost.global_mode
            self.eaten = True
            self.pacman.eat_ghost()

        # handles ghost killing pacman
        elif array_equal(self.position, self.pacman.position) and (not self.eaten):
            self.pacman.kill()

        # moves the ghost
        if self.at_intersection():
            self.path_find(self.get_target())
        self.position += self.facing

        # handles ghost getting eaten
        if array_equal(self.position, self.pacman.position) and self.mode == Ghost.FRIGHTENED and (not self.eaten):
            self.mode = Ghost.global_mode
            self.eaten = True
            self.pacman.eat_ghost()

        # handles ghost killing pacman
        elif array_equal(self.position, self.pacman.position) and (not self.eaten):
            self.pacman.kill()
