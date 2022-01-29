import pygame
import os
import fighter

# loads image of the Castle
# The placeholder is a bigger green dragon.
CASTLE = pygame.image.load(os.path.join("images", "gdrag1.png"))
CASTLE = pygame.transform.scale(CASTLE, (100, 100))


class Castle:
    def __init__(self, x=1600, y=375, hp=100):
        self.x = x
        self.y = y
        self.hp = hp
        self.img = CASTLE
        self.alive = True

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_alive(self):
        return self.alive

    # draws the castle
    def draw(self, window: object) -> object:
        window.blit(self.img, (self.x, self.y))

    # castle takes damage
    def take_damage(self, attacker):
        self.hp -= 1
        fighter.remove(attacker)

    def get_hp(self):
        return self.hp
