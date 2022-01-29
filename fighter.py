# Abstract class for attackers and defender
import pygame
import os
import helper

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
        self.alive = True

    # Draws person to window
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_alive(self):
        return self.alive


class Attacker(Fighter):
    def __init__(self, x=-20, y=375, hp=100, move_delay=300):
        super().__init__(x, y)
        self.max_hp = hp
        self.hp = hp
        self.move_delay = move_delay
        self.img = BLUE_DRAGON_1
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
        self.healthbar(window)

    # MOVEMENT METHODS
    def move_right(self, steps, window_width):
        if self.x + self.img.get_width() + 10 <= window_width:
            self.x += steps
        else:
            self.x = window_width - self.img.get_width()
        pygame.time.wait(self.move_delay)

    def move_left(self, steps):
        if self.x - steps >= 0:
            self.x -= steps
        else:
            self.x = 0
        pygame.time.wait(self.move_delay)

    def move_up(self, steps):
        if self.y - steps >= 0:
            self.y -= steps
        else:
            self.y = 0
        pygame.time.wait(self.move_delay)

    def move_down(self, steps, window_height):
        if self.y + steps + self.img.get_height() <= window_height:
            self.y += steps
        else:
            self.y = window_height
        pygame.time.wait(self.move_delay)

    def take_damage(self, dmg):
        if self.hp - dmg > 0:
            self.hp -= dmg
        else:
            self.hp = 0
            self.alive = False
            # TODO broadcast event for attacker killed

    def set_hp(self, newhp):
        self.hp = newhp

    def healthbar(self, window):
        # red rect
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.img.get_height() + 10, self.img.get_width(), 10))

        # green rect
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.img.get_height() + 10, self.img.get_width() * (self.hp / self.max_hp), 10))


class Defender(Fighter):
    def __init__(self, x=370, y=250, atk=20, atk_delay=2, range=200):
        super().__init__(x, y)
        self.atk = atk
        self.range = range
        self.img = GREEN_DRAGON_1
        self.cooldown = 60
        self.cool_down_counter = 0
        self.arrows = []
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
        for arrow in self.arrows:
            arrow.draw(window)

    def cool_down_caller(self):
        if self.cool_down_counter >= self.cooldown:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def attack(self, attackers):
        if self.cool_down_counter == 0:
            closest_attacker = helper.find_closest(self, attackers)
            if helper.find_distance(self, closest_attacker) < self.range:
                closest_attacker.take_damage(self.atk)
                self.cool_down_counter = 1
