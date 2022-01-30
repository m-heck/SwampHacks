import pygame
import os
import time
import random
import helper
from castle import Castle
from fighter import Attacker, Defender
from gamestate import Gamestate, State

# initializes pygame's fonts
pygame.font.init()

# Creates window
WIDTH, HEIGHT = 1275, 717
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Swamphacks Game")

# Menu BG
menu_bg = pygame.transform.scale(pygame.image.load(os.path.join("images", "BG.png")), (WIDTH, HEIGHT))
GAME_BG = pygame.transform.scale(pygame.image.load(os.path.join("images", "castle.JPEG")), (WIDTH, HEIGHT))
EDIT_BG = pygame.transform.scale(pygame.image.load(os.path.join("images", "edit_bg.JPEG")), (WIDTH, HEIGHT))


# colors
white = (255, 255, 255)
red = (255, 0, 0)
orange = (255, 100, 0)
black = (0, 0, 0)


def main():
    # VARIABLES
    run = True  # Dictates whether the while loop will run or not

    # Initializes Gamestate
    mystate = Gamestate()

    # CREATES FIGHTER ARRAYS
    attackers = []
    defenders = []

    clock = pygame.time.Clock()  # Checks for events 60 times every second

    # SETS THE ATTACKERS AND DEFENDERS LISTED TO THE GAMESTATE
    mystate.setlists(defenders, attackers)
    # CREATES CASTLE OBJECT (Not needed because of gamestate)
    # castle = Castle()
    # Call the castle object in gamestate by doing mystate.currentcastle

    while True:  # Todo fix so it will stop when the game is lost
        edit_phase(mystate, clock)
        attack_phase(mystate, clock)
        stats_phase(mystate, clock)


def edit_phase(mystate, clock):
    is_edit_phase = True
    FPS = 60
    main_font = pygame.font.SysFont('arial', 50)
    small_font = pygame.font.SysFont('arial', 30)
    gold = mystate.currentbank.gold
    defender_cost = 100
    reverse = True

    menu_defender = Defender(WIDTH / 2 - 150, HEIGHT / 2 - 150)
    menu_defender.scale(300, 300)

    # =========== METHOD FOR DISPLAYING THINGS TO THE SCREEN ===========
    def redraw_window():
        # BASE LAYER
        # Background must be drawn first so it is on the lowest level
        WINDOW.blit(EDIT_BG, (0, 0))

        # Creates text
        phase_label = main_font.render(f"Puchase Defenders", 1, white)  # Draws text (item, 1, color)
        instructions_label = small_font.render(f"Press up to buy and space to continue", 1, white)
        defender_count_label = small_font.render(f"Defender count: {mystate.getDefenderListSize()}", 1, white)
        gold_label = small_font.render(f"Gold: {gold}", 1, white)

        WINDOW.blit(phase_label, (WIDTH / 2 - phase_label.get_width() / 2, 80))  # Draws the text
        WINDOW.blit(instructions_label, (WIDTH / 2 - instructions_label.get_width() / 2, 130))
        WINDOW.blit(defender_count_label, (WIDTH / 2 - defender_count_label.get_width() / 2, 600))
        WINDOW.blit(gold_label, (WIDTH - gold_label.get_width() - 130, 80))

        menu_defender.draw(WINDOW, reverse, False)
        pygame.time.wait(150)

        pygame.display.update()  # Refreshes the display

    # =========== METHOD FOR RUNNING THE GAME ===========
    while is_edit_phase:
        clock.tick(FPS)  # Going to tick the clock based on FPS value, keeps game consistent

        # CALLS REDRAW METHOD
        redraw_window()

        # QUIT GAME
        for event in pygame.event.get():  # Loops through all events
            if event.type == pygame.QUIT:  # If the player closes out, stops the game
                quit()

        reverse = not reverse  # for animation

        # Generates random values for defender's stats
        random_defender_x = random.randint(100, WIDTH - 100)
        upper_level = random.choice((True, False))
        random_defender_atk = random.randint(30, 60)
        random_defender_range = random.randint(50, 200)
        random_defender_accuracy = random.randint(70, 100)

        if upper_level:
            random_defender_y = 300 + random.randint(-50, 200)
        else:
            random_defender_y = 600 + random.randint(-50, 0)

        # CHECKS FOR USER INPUT
        keys = pygame.key.get_pressed()  # Returns a dictionary with all the keys pressed
        if keys[pygame.K_SPACE]:
            is_edit_phase = False
        if keys[pygame.K_UP]:
            if gold - defender_cost >= 0:
                mystate.defenderAdd(Defender(random_defender_x, random_defender_y, random_defender_atk, random_defender_range, random_defender_accuracy))
                gold -= defender_cost
                pygame.time.wait(100)
        if keys[pygame.K_DOWN]:
            if mystate.defcount >= 1:
                mystate.defenderRemove(mystate.getDefenders()[mystate.defcount - 1])
                gold += defender_cost
                pygame.time.wait(100)


def attack_phase(mystate, clock):
    is_attack_phase = True
    FPS = 60  # Shows 60 frames per second
    main_font = pygame.font.SysFont('arial', 50)
    small_font = pygame.font.SysFont('arial', 30)
    reverse = True

    attackers = mystate.getAttackers()
    defenders = mystate.getDefenders()

    mystate.attackerAdd(Attacker())

    # =========== METHOD FOR DISPLAYING THINGS TO THE SCREEN ===========
    def redraw_window():  # We can only access it within the main, but it has access to locals
        # BASE LAYER
        # Background must be drawn first so it is on the lowest level
        WINDOW.blit(GAME_BG, (0, 0))  # anything that you want consistent in the game window should be added within the
        # loop

        # Creates text
        phase_label = main_font.render(f"Attack phase", 1, white)  # Draws text (item, 1, color)
        level_label = small_font.render(f"Level: {mystate.getlevel()}", 1, black)
        gold_label = small_font.render(f"Gold: {mystate.currentbank.gold}", 1, white)

        WINDOW.blit(phase_label, (10, 10))  # Draws the text
        WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 20, 10))
        WINDOW.blit(gold_label, (WIDTH - gold_label.get_width() - 0, HEIGHT - gold_label.get_height() - 20))

        # DRAWS THE FIGHTERS
        for attacker in mystate.getAttackers():
            attacker.move_right(30, WIDTH)
            attacker.draw(WINDOW, reverse)
            if not attacker.get_x() <= WIDTH - attacker.img.get_width() - 10:
                mystate.attackerRemove(attacker)
                mystate.currentbank.gaingold(-30)
            if not attacker.alive:
                mystate.attackerRemove(attacker)
                mystate.currentbank.gaingold(20)
        for defender in mystate.defenderlist:
            defender.draw(WINDOW, reverse)

        # DRAWS THE CASTLE
        mystate.currentcastle.draw(WINDOW)

        pygame.display.update()  # Refreshes the display

    # =========== METHOD FOR RUNNING THE GAME ===========
    while is_attack_phase:
        clock.tick(FPS)  # Going to tick the clock based on FPS value, keeps game consistent

        # CALLS REDRAW METHOD
        redraw_window()

        reverse = not reverse # for animation

        # QUIT GAME
        for event in pygame.event.get():  # Loops through all events
            if event.type == pygame.QUIT:  # If the player closes out, stops the game
                quit()

        if mystate.enemycount <= 0:
            pygame.time.wait(1000)
            break

        for defender in defenders:
            defender.cool_down_caller()
            defender.attack(attackers)


def stats_phase(mystate, clock):
    is_stats_phase = True
    FPS = 60  # Shows 60 frames per second
    main_font = pygame.font.SysFont('arial', 50)
    small_font = pygame.font.SysFont('arial', 30)
    gold_reward = 200

    # increases level
    mystate.levelUp()
    mystate.currentbank.gaingold(gold_reward)

    def redraw_window():
        # BASE LAYER
        # Background must be drawn first so it is on the lowest level
        WINDOW.blit(GAME_BG, (0, 0))  # anything that you want consistent in the game window should be added within the
        # loop

        # Creates text
        phase_label = main_font.render(f"Your stats", 1, black)  # Draws text (item, 1, color)
        level_label = small_font.render(f"You gained {gold_reward} gold! Moving onto level {mystate.getlevel()}...",
                                        1,                            black)
        gold_label = small_font.render(f"Gold: {mystate.currentbank.gold}", 1, white)

        WINDOW.blit(phase_label, (WIDTH / 2 - phase_label.get_width() / 2, 10))  # Draws the text
        WINDOW.blit(level_label, (WIDTH / 2 - level_label.get_width() / 2, 60))
        WINDOW.blit(gold_label, (WIDTH - gold_label.get_width() - 20, HEIGHT - gold_label.get_height() - 20))

        # DRAWS THE CASTLE
        mystate.currentcastle.draw(WINDOW)

        pygame.display.update()  # Refreshes the display

    while is_stats_phase:
        clock.tick(FPS)  # Going to tick the clock based on FPS value, keeps game consistent

        # CALLS REDRAW METHOD
        redraw_window()

        # QUIT GAME
        for event in pygame.event.get():  # Loops through all events
            if event.type == pygame.QUIT:  # If the player closes out, stops the game
                quit()

        keys = pygame.key.get_pressed()  # Returns a dictionary with all the keys pressed
        if keys[pygame.K_SPACE]:
            is_stats_phase = False
            pygame.time.wait(50)


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
