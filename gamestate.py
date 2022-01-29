
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
    stateinstance = None
    def __init__(self):
        if Gamestate.stateinstance != None:
            raise Exception("GameState constructor is only supposed to be called once")
        else:
            self.currentcastle = castle()
            self.mystate = State.PLAYING
            self.defenderlist = []
            self.defcount = 0
            self.enemylist = []
            self.enemycount = 0
            Gamestate.stateinstance = self

    def gameInstance(self):
        if Gamestate.stateinstance == None:
            Gamestate()
        return Gamestate.stateinstance

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

