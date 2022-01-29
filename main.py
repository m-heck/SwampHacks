import pygame
import os
import time
import random
import helper
from castle import Castle
from fighter import Attacker, Defender
import gamestate

# initializes pygame's fonts
pygame.font.init()

# Creates window
WIDTH, HEIGHT = 1700, 956
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Swamphacks Game")

# Menu BG
menu_bg = pygame.transform.scale(pygame.image.load(os.path.join("images", "BG.png")), (WIDTH, HEIGHT))

# colors
white = (255, 255, 255)
red = (255, 0, 0)
orange = (255, 100, 0)
black = (0, 0, 0)


def main():
    # VARIABLES
    run = True  # Dictates whether the while loop will run or not
    FPS = 60  # Shows 60 frames per second
    main_font = pygame.font.SysFont('arial', 50)

    # Initializes Gamestate
    #currentstate = gamestate.Gamestate.gameInstance()

    # CREATES FIGHTER ARRAYS
    attackers = []
    defenders = []

    attackers.append(Attacker())
    defenders.append(Defender())

    # CREATES CASTLE OBJECT
    castle = Castle()

    clock = pygame.time.Clock()  # Checks for events 60 times every second

    # =========== METHOD FOR DISPLAYING THINGS TO THE SCREEN ===========
    def redraw_window():  # We can only access it within the main, but it has access to locals
        # BASE LAYER
        # Background must be drawn first so it is on the lowest level
        WINDOW.fill(black)  # anything that you want consistent in the game window should be added within the loop

        # Creates text
        sample_label = main_font.render(f"Sample Text", 1, white)  # Draws text (item, 1, color)

        WINDOW.blit(sample_label, (10, 10))  # Draws the text

        # DRAWS THE FIGHTERS
        for attacker in attackers:
            attacker.draw(WINDOW)
        for defender in defenders:
            defender.draw(WINDOW)

        # DRAWS THE CASTLE
        castle.draw(WINDOW)

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

        attackers[0].move_right(10, WIDTH)
        defenders[0].attack(attackers)


def main_menu():
    title_font = pygame.font.SysFont('helvetica bold', 100)
    start_font = pygame.font.SysFont('helvetica bold', 80)

    WINDOW.blit(menu_bg, (0, 0))
    title1 = title_font.render("UNIVERSITY OF FLORIDA:", 1, white)
    title2 = title_font.render("TOWER DEFENSE", 1, white)

    quit = title_font.render("QUIT", 1, white)

    run = True
    while run:
        start_text = start_font.render("CLICK TO START", 1, orange)
        WINDOW.blit(title1, (WIDTH / 40, 200))
        WINDOW.blit(title2, (WIDTH / 40, 300))
        WINDOW.blit(start_text, (WIDTH / 40, 600))
        pygame.display.update()

        #position of mouse
        mouse = pygame.mouse.get_pos()

        #makes quit button, turns red if mouse hovers
        if WIDTH / 40 <= mouse[0] <= WIDTH / 40 + 300 and 700 <= mouse[1] <= 800:
            pygame.draw.rect(WINDOW, red, pygame.Rect(WIDTH / 40, 700, 300, 100))
        else:
            pygame.draw.rect(WINDOW, orange, pygame.Rect(WIDTH / 40, 700, 300, 100))

        WINDOW.blit(quit, (WIDTH / 40 - quit.get_width() / 2 + 150, 800 - quit.get_height() / 2 - 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if WIDTH / 40 <= mouse[0] <= WIDTH / 40 + 300 and 700 <= mouse[1] <= 800:
                    pygame.quit()
                else:
                    main()
    pygame.quit()


main_menu()
