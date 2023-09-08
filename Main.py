"""
Main script for running the card game application.

This script initializes the game, handles user input events, and manages the game loop.

Author: Piotr Zimirski
Date: September 2023

Usage:
    Run this script to play the card game.

"""

from pygame.locals import *
import sys
from Game import *

# Constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FRAMES_PER_SECOND = 30

# Initialize Pygame environment
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Load resources: images and buttons
background = pygwidgets.Image(window, (0, 0), 'images/Background.jpg')

playButton = pygwidgets.TextButton(window, (200, 600), 'Graj', width=100, height=45)

quitButton = pygwidgets.TextButton(window, (880, 600), 'Koniec', width=100, height=45)

# Initialize the Game object
oGame = Game(window)

# Main game loop
while True:

    # Event handling
    for event in pygame.event.get():
        if ((event.type == QUIT) or
                ((event.type == KEYDOWN) and (event.key == K_ESCAPE)) or
                (quitButton.handleEvent(event))):
            pygame.quit()
            sys.exit()

        if playButton.handleEvent(event):
            gameOver = oGame.manageGame()

            if gameOver:
                playButton.disable()

    # Draw background
    background.draw()

    # Draw game elements
    oGame.draw()

    # Draw other UI components
    playButton.draw()
    quitButton.draw()

    # Update the window
    pygame.display.update()

    # Limit the frame rate
    clock.tick(FRAMES_PER_SECOND)