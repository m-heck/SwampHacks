
# Game state class that controls the general functions of the player and game
import pygame
import os
import castle
import fighter


from enum import Enum
class State(Enum):
    WIN = 0
    LOSS = 1
    PLAYING = 2

class Gamestate:

    def __init__(self):
        self.currentcastle = castle()
        self.mystate = State.PLAYING
        self.defenderlist = []
        self.defcount = 0
        self.enemylist = []
        self.enemycount = 0

    def gameloss(self):
        if self.currentcastle.hp < 1:
            self.mystate = State.LOSS
            return True
        return False
    def gameWin(self):
        print("not decided yet")
    def defenderadd(self, defender):
        self.defenderlist.append(defender)
        self.defcount = self.defcount + 1
    def defenderremove(self, defender):
        self.defenderlist.remove(defender)
        self.defcount = self.defcount - 1
    def attackeradd(self, attacker):
        self.enemylist.append(attacker)
        self.enemycount = self.enemycount + 1
    def attackerremove(self, attacker):
        self.enemylist.remove(attacker)
        self.enemycount = self.enemycount - 1

