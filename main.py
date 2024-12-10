from Ghost import Ghost
from ghost_movement import *
from PacMan import PacMan
from map import *
import pygame
from numpy import array
from time import time

# creates pygame
pygame.init()
window = pygame.display.set_mode((700, 900))

# creates players and ghosts
pacman = PacMan((13, 26))
Ghost.set_pacman(pacman)
Blinky = Ghost("Blinky", [12, 14], Blinky_scatter, Blinky_chase)
Inky = Ghost("Inky", [13, 14], Inky_scatter, Inky_chase)
Pinky = Ghost("Pinky", [14, 14], Pinky_scatter, Pinky_chase)
Clyde = Ghost("Clyde", [15, 14], Clyde_scatter, Clyde_chase)
ghost_colors = {Blinky: (225, 0, 0), Inky: (0, 150, 255), Pinky: (255, 0, 255), Clyde: (255, 165, 0)}


def draw_map():
    """
    draws the in game map to the screen
    """

    # draws the map
    window.fill((0, 0, 0))
    for row_num in range(len(GHOST_MAP)):
        for column_num in range(len(GHOST_MAP[row_num])):

            # draws map
            if GHOST_MAP[row_num][column_num] == 0:
                pygame.draw.rect(window, (0, 0, 225), (column_num * 25, row_num * 25, 25, 25))

            # draws pellets
            if PLAYER_MAP[row_num][column_num] == 2:
                pygame.draw.circle(window, (255, 255, 255), tuple((array([column_num, row_num]) * 25) + array([12.5, 12.5])), 25 / 8)

            # draws power pellets
            if PLAYER_MAP[row_num][column_num] == 3:
                pygame.draw.circle(window, (255, 255, 255), tuple((array([column_num, row_num]) * 25) + array([12.5, 12.5])), 25 / 3)

    # draws pacman and ghosts
    pygame.draw.circle(window, (225, 225, 0), tuple((pacman.position * 25) + array([12.5, 12.5])), 25 / 2)
    for ghost_blip in Ghost.ghosts.values():
        color = ghost_colors[ghost_blip] if (not ghost_blip.mode == Ghost.FRIGHTENED) or ghost_blip.eaten else (0, 0, 255)
        pygame.draw.circle(window, color, tuple((ghost_blip.position * 25) + array([12.5, 12.5])), 25 / 2 if not ghost_blip.eaten else 25 / 5)


# pygame main loop
running = True
seconds = time()
while running:

    # handles game exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # handles key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        pacman.set_facing(pacman.N)
    if keys[pygame.K_a]:
        pacman.set_facing(pacman.W)
    if keys[pygame.K_s]:
        pacman.set_facing(pacman.S)
    if keys[pygame.K_d]:
        pacman.set_facing(pacman.E)

    # moves pacman and ghosts
    pacman.move()
    if time() - seconds >= 1:
        seconds = time()
        Ghost.change_mode()
    for ghost in Ghost.ghosts.values():
        ghost.move()

    # updates gui
    draw_map()
    pygame.display.flip()
    pygame.time.Clock().tick(10)

# exits game
pygame.quit()
