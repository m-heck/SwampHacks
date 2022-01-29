# Abstract class for attackers and defender
import pygame
import os

# Loads images
# !! FOR NOW, GREEN = DEFENDERS and BLUE = ATTACKERS
GREEN_DRAGON_1 = pygame.image.load(os.path.join("images", "gdrag1.png"))
GREEN_DRAGON_1 = pygame.transform.scale(GREEN_DRAGON_1, (60, 60))
GREEN_DRAGON_2 = pygame.image.load(os.path.join("images", "gdrag2.png"))
BLUE_DRAGON_1 = pygame.image.load(os.path.join("images", "bdrag1.png"))
BLUE_DRAGON_1 = pygame.transform.scale(BLUE_DRAGON_1, (60, 60))
BLUE_DRAGON_2 = pygame.image.load(os.path.join("images", "bdrag2.png"))

class Fighter:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = None

    # Draws person to window
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))


class Attacker(Fighter):
    def __init__(self, x=375, y=375, hp = 100, movespd = 500):
        super().__init__(x, y)
        self.hp = hp
        self.movespd = movespd
        self.img = BLUE_DRAGON_1

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    # MOVEMENT METHODS
    def move_right(self, steps, window_width):
        if self.x + self.img.get_width() + 10 <= window_width:
            self.x += 10 * self.movespd
        else:
            self.x = window_width - self.img.get_width()
        pygame.time.wait(self.movespd)

    def move_left(self, steps):
        if self.x - steps >= 0:
            self.x -= steps * self.movespd
        else:
            self.x = 0
        pygame.time.wait(self.movespd)

    def move_up(self, steps):
        if self.y - steps >= 0:
            self.y -= steps * self.movespd
        else:
            self.y = 0
        pygame.time.wait(self.movespd)

    def move_down(self, steps, window_height):
        if self.y + steps + self.img.get_height() <= window_height:
            self.y += steps * self.movespd
        else:
            self.y = window_height
        pygame.time.wait(self.movespd)

    # def take_damage
