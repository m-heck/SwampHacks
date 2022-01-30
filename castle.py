import pygame
import os

# loads image of the Castle
# The placeholder is a bigger green dragon.
#CASTLE = pygame.image.load(os.path.join("images", "arrow.png"))
#CASTLE = pygame.transform.scale(CASTLE, (100, 100))


class Castle:
    def __init__(self, x=637, y=358.5, hp=100):
        self.x = x
        self.y = y
        self.hp = hp
        self.alive = True
        self.max_hp = hp

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_alive(self):
        return self.alive

    # draws the castle
    def draw(self, window):
        #window.blit(self.img, (self.x, self.y))
        self.healthbar(window)

    # castle takes damage
    def take_damage(self, dmg):
        self.hp -= dmg

    def get_hp(self):
        return self.hp

    def healthbar(self, window):
        # red rect
        pygame.draw.rect(window, (255, 0, 0), (self.x - 250, 20, 500, 20))

        # green rect
        pygame.draw.rect(window, (0, 255, 0), (self.x - 250, 20, 500, 20))

