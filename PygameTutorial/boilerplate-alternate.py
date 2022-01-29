import pygame
# ======================= SETUP =======================

# initializes pygame
pygame.init()

# creates the screen
screen = pygame.display.set_mode((800, 600))  # tuple is double parentheses

# title and icon (flaticon.com for image, use 32px images)
pygame.display.set_caption("ENTER TITLE")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# event: anything happening inside the game window (e.g. arrow keys, mouse)
# making a quit event when close button is pressed
# game loop
def main():
    # VARIABLES
    run = True  # Dictates whether the while loop will run or not
    FPS = 60  # Shows 60 frames per second
    main_font = pygame.font.SysFont("comicsans", 50)

    clock = pygame.time.Clock()  # Checks for events 60 times every second

    def redraw_window():  # We can only access it within the main, but it has access to locals
    # BASE LAYER
    # Background must be drawn first so it is on the lowest level
        WIN.blit(BG, (0, 0))  # WIN is the surface. Draws the background to the window

        # Creates text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))  # Draws text (item, 1, color)
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))  # Draws the text
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        # REFRESHES DISPLAY
        pygame.display.update()  # Refreshes the display
    
while run:
    clock.tick(FPS)  # Going to tick the clock based on FPS value, keeps game consistent

    # CALLS REDRAW METHOD
    redraw_window()

    # CHECKS IF THE PLAYER LOST
    if lives <= 0 or player.health <= 0:
        lost = True
        lost_count += 1

    # QUIT GAME
    for event in pygame.event.get():  # Loops through all events
        if event.type == pygame.QUIT:  # If the player closes out, stops the game
            quit()

    # CHECKS FOR USER INPUT
    keys = pygame.key.get_pressed()  # Returns a dictionary with all the keys pressed
    # Keeps the player within the window too
    if keys[pygame.K_a] and player.x - player_vel > 0:  # left
        player.x -= player_vel
    if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  # right
        player.x += player_vel
    if keys[pygame.K_w] and player.y - player_vel > 0:  # up
        player.y -= player_vel
    if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:  # down
        player.y += player_vel
    if keys[pygame.K_SPACE]:  # Creates a new laser if off cooldown
        player.shoot()
