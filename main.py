import pygame
import os
import random
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
END_BG = pygame.transform.scane(pygame.image.load(os.path.join("images", "edit_bg.JPEG")), (WIDTH, HEIGHT))

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

    while mystate.currentcastle.get_hp() >= 0:
        edit_phase(mystate, clock)
        attack_phase(mystate, clock)
        stats_phase(mystate, clock)

    game_end(mystate, clock)


def edit_phase(mystate, clock):
    is_edit_phase = True
    FPS = 60
    main_font = pygame.font.SysFont('arial', 50)
    small_font = pygame.font.SysFont('arial', 30)
    tiny_font = pygame.font.SysFont('arial', 20)
    defender_cost = 100
    reverse = True

    menu_defender = Defender(WIDTH / 2 - 150 + 200, HEIGHT / 2 - 150)
    menu_defender.scale(300, 300)

    # =========== METHOD FOR DISPLAYING THINGS TO THE SCREEN ===========
    def redraw_window():
        # BASE LAYER
        # Background must be drawn first so it is on the lowest level
        WINDOW.blit(EDIT_BG, (0, 0))

        # Creates text
        phase_label = main_font.render(f"Puchase Defenders", 1, white)  # Draws text (item, 1, color)
        instructions_label = small_font.render(f"Press space to attack", 1, white)
        defender_count_label = small_font.render(f"Defender count: {mystate.getDefenderListSize()}", 1, white)
        gold_label = small_font.render(f"Gold: {mystate.currentbank.gold}", 1, white)
        buy_defender = tiny_font.render(f"Press ^ to buy defender for 100 gold", 1, white)
        heal = tiny_font.render(f"Press > to heal 10 health for 75 gold", 1, white)
        buy_hat = tiny_font.render(f"Press < to sell 10 health for 50 gold", 1, white)
        sell_defender = tiny_font.render(f"Press v to sell defender for 100 gold", 1, white)

        WINDOW.blit(phase_label, (WIDTH / 2 - phase_label.get_width() / 2, 80))  # Draws the text
        WINDOW.blit(instructions_label, (WIDTH / 2 - instructions_label.get_width() / 2, 130))
        WINDOW.blit(defender_count_label, (WIDTH / 2 - defender_count_label.get_width() / 2, 600))
        WINDOW.blit(gold_label, (WIDTH - gold_label.get_width() - 130, 80))
        WINDOW.blit(buy_defender, (180, 230))
        WINDOW.blit(sell_defender, (180, 280))
        WINDOW.blit(heal, (180, 330))
        WINDOW.blit(buy_hat, (180, 380))

        # Shows a dragon on the menu screen
        menu_defender.draw(WINDOW, reverse, False)
        pygame.time.wait(100)

        # shows castle health
        mystate.currentcastle.draw(WINDOW)

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
        random_defender_range = random.randint(90, 250)
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
            if mystate.currentbank.gold - defender_cost >= 0:
                mystate.defenderAdd(Defender(random_defender_x, random_defender_y, random_defender_atk, random_defender_range, random_defender_accuracy))
                mystate.currentbank.gold -= defender_cost
                pygame.time.wait(50)
        if keys[pygame.K_DOWN]:
            if mystate.defcount >= 1:
                mystate.defenderRemove(mystate.getDefenders()[mystate.defcount - 1])
                mystate.currentbank.gold += defender_cost
                pygame.time.wait(50)
        if keys[pygame.K_RIGHT]:
            if mystate.currentcastle.get_hp() <= 99:
                if mystate.currentcastle.get_hp() + 10 > 100:
                    mystate.currentcastle.hp = 100
                    mystate.currentbank.gold -= 75
                    pygame.time.wait(50)
                else:
                    mystate.currentcastle.hp += 10
                    mystate.currentbank.gold -= 75
                    pygame.time.wait(50)

        if keys[pygame.K_LEFT]:
            if mystate.currentcastle.get_hp() >= 11:
                mystate.currentbank.gold += 50
                mystate.currentcastle.hp -= 10
                pygame.time.wait(50)


def attack_phase(mystate, clock):
    is_attack_phase = True
    FPS = 60  # Shows 60 frames per second
    main_font = pygame.font.SysFont('arial', 50)
    small_font = pygame.font.SysFont('arial', 30)
    reverse = True

    attackers = mystate.getAttackers()
    defenders = mystate.getDefenders()

    # Generates random values for attackers
    num_attackers = round(random.randrange(100, 300) / 100 * mystate.getlevel())

    for i in range(num_attackers):
        rand_attacker_x = random.randint(-1000, -100)
        rand_attacker_y = random.randint(250, 550)
        rand_attacker_hp = random.randint(70, 90)
        rand_attacker_movedelay = random.randint(100, 300)
        mystate.attackerAdd(Attacker(rand_attacker_x, rand_attacker_y, rand_attacker_hp, rand_attacker_movedelay))

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
        enemies_left = small_font.render(f"Enemies left: {mystate.enemycount}", 1, white)

        WINDOW.blit(phase_label, (10, 10))  # Draws the text
        WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 20, 10))
        WINDOW.blit(gold_label, (WIDTH - gold_label.get_width() - 20, HEIGHT - gold_label.get_height() - 20))
        WINDOW.blit(enemies_left, (10, HEIGHT - enemies_left.get_height() - 20))

        # DRAWS THE FIGHTERS
        for attacker in mystate.getAttackers():
            attacker.move_right(30, WIDTH)
            attacker.draw(WINDOW, reverse)
            if not attacker.get_x() <= WIDTH - attacker.img.get_width() - 10:
                mystate.attackerRemove(attacker)
                mystate.currentcastle.take_damage(random.randint(7, 13))
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

        if mystate.currentcastle.get_hp() <= 0:
            game_end(mystate, clock)

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
    gold_reward = random.randint(100, 190)

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
        level_label = small_font.render(f"You gained {gold_reward} gold! Moving onto level {mystate.getlevel()}... "
                                        f"Press space to continue", 1, black)
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

def game_end(mystate, clock):
    if mystate.gameLoss() == True:
        end_font = pygame.font.SysFont('helvetica bold', 100)
        WINDOW.blit(END_BG, (0, 0))
        endtitle = end_font.render("YOU LOSE", 1, red)
        




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
                    run = False
    pygame.quit()


main_menu()
