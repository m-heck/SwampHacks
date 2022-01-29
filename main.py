import pygame
import os
import time
import random
from fighter import Fighter

# initializes pygame's fonts
pygame.font.init()

# Creates window
WIDTH, HEIGHT = 750, 750
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Swamphacks Game")

class Player():
    def __init__(self):
        self.img = GREEN_DRAGON_1
        self.x = 300
        self.y = 300

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))


def main():
    # VARIABLES
    run = True  # Dictates whether the while loop will run or not
    FPS = 60  # Shows 60 frames per second
    main_font = pygame.font.SysFont('arial', 50)

    # CREATES PLAYER OBJECT
    player = Player()

    clock = pygame.time.Clock()  # Checks for events 60 times every second

    # =========== METHOD FOR DISPLAYING THINGS TO THE SCREEN ===========
    def redraw_window():  # We can only access it within the main, but it has access to locals
        # BASE LAYER
        # Background must be drawn first so it is on the lowest level
        WINDOW.fill((0, 0, 0))  # anything that you want consistent in the game window should be added within the loop

        # Creates text
        sample_label = main_font.render(f"Sample Text", 1, (255, 255, 255))  # Draws text (item, 1, color)

        WINDOW.blit(sample_label, (10, 10))  # Draws the text

        # DRAWS THE PLAYER
        player.draw(WINDOW)

        pygame.display.update()  # Refreshes the display

    # =========== METHOD FOR RUNNING THE GAME ===========
    while run:
        clock.tick(FPS)  # Going to tick the clock based on FPS value, keeps game consistent

        # CALLS REDRAW METHOD
        redraw_window()

        # QUIT GAME
        for event in pygame.event.get():  # Loops through all events
            if event.type == pygame.QUIT:  # If the player closes out, stops the game
                quit()

        # CHECKS FOR USER INPUT
        keys = pygame.key.get_pressed()  # Returns a dictionary with all the keys pressed


main()
