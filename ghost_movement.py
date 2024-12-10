from numpy import array
from numpy.linalg import norm

"""
this file contains the scatter and chase mode functions for each of the ghosts

scatter mode targets:
    Blinky: top right
    Inky: bottom right
    Pinky: top left
    Clyde: bottom left
    
chase mode functions:
    Blinky: target the pacman object
    Inky: target is vector from 2 in front of pacman to Blinky rotated 180 degrees
    Pinky: targets the tile 4 tiles in front of where pacman is facing
    Clyde: target is pacman object unless distance is less than 8 tiles in which case the target is the scatter target
"""

# ================================================ scatter mode targets ================================================
Blinky_scatter = array([25, -1])
Inky_scatter = array([27, 34])
Pinky_scatter = array([2, -1])
Clyde_scatter = array([0, 34])

# ================================================ chase mode functions ================================================


def Blinky_chase(ghost, pacman):
    """
    Blinkys chase mode function: target the pacman object

    :param ghost: Blinkys ghost object, not used for this function
    :param pacman: the pacman object, will be the target for this ghost

    :return: the target tile (pacmans location)
    """

    return pacman.position


def Inky_chase(ghost, pacman):
    """
    Inkys chase mode function: target is vector from 2 in front of pacman to Blinky rotated 180 degrees

    :param ghost: Inkys ghost object, used to find Blinkys ghost object
    :param pacman: the pacman object, will be used to find the tile 2 in front

    :return: the calculated target tile
    """

    pacman_tile = pacman.position + (pacman.facing * 2)
    Blinky_vector = ghost.ghosts["Blinky"].position - pacman_tile
    rotated_vector = Blinky_vector * -1
    target_tile = rotated_vector + pacman_tile
    return target_tile


def Pinky_chase(ghost, pacman):
    """
    Pinkys chase mode function: targets the tile 4 tiles in front of where pacman is facing

    :param ghost: Pinkys ghost object, not used for this function
    :param pacman: the pacman object, will be used to calculate the target for this ghost

    :return: the target tile (4 tiles in front of pacmans location)
    """

    return pacman.position + (pacman.facing * 4)


def Clyde_chase(ghost, pacman):
    """
    Clydes chase mode function: target is pacman object unless distance is less than 8 tiles in which case the target
    is the scatter target

    :param ghost: Clydes ghost object, used to determine distance from pacman
    :param pacman: the pacman object, will be used to determine distance to pacman

    :return: the calculated target tile
    """

    return pacman.position if norm(ghost.position - pacman.position) >= 8 else ghost.scatter
