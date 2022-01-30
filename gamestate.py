# Game state class that controls the general functions of the player and game
import os
from castle import Castle
from fighter import Attacker, Defender

from enum import Enum


class State(Enum):
    WIN = 0
    LOSS = 1
    PLAYING = 2

class Bank:
    def __init__(self):
        self.gold = 300
        self.round = 1
        self.killed = 0
    def get_gold(self):
        return self.gold
    def gaingold(self,goldgained):
        self.gold += goldgained;
    # gives player gold at the end of every round
    def round_end(self):
        self.gold += (round * 80) + (5 * killed)
        self.round += 1
        self.killed = 0

    def buy(self,x):
        if self.gold < x.get_price():
            pass
        else:
            self.gold -= x.get_price()

class Gamestate:
    def __init__(self):
        self.currentcastle = Castle()
        self.currentbank = Bank()
        self.mystate = State.PLAYING
        self.defenderlist = []
        self.defcount = 0
        self.enemylist = []
        self.enemycount = 0
        self.level = 1

    def getState(self):
        return self.mystate

    def setState(self, thisstate):
        self.mystate = thisstate

    def getlists(self):
        return self.defenderlist, self.enemylist

    def getAttackers(self):
        return self.enemylist

    def getDefenders(self):
        return self.defenderlist

    def getDefenderListSize(self):
        return len(self.defenderlist)

    def setlists(self, defender, enemy):
        self.defenderlist = defender
        self.enemylist = enemy

    def getlevel(self):
        return self.level

    def setLevel(self, level):
        self.level = level

    def gameLoss(self):
        if self.currentcastle.hp < 1:
            self.mystate = State.LOSS
            return True
        return False

    def gameWin(self):
        print("not decided yet")

    def defenderAdd(self, defender):
        self.defenderlist.append(defender)
        self.defcount = self.defcount + 1

    def defenderRemove(self, defender):
        self.defenderlist.remove(defender)
        self.defcount = self.defcount - 1

    def attackerAdd(self, attacker):
        self.enemylist.append(attacker)
        self.enemycount = self.enemycount + 1

    def attackerRemove(self, attacker):
        self.enemylist.remove(attacker)
        self.enemycount = self.enemycount - 1

    def restart(self):
        self.currentcastle = castle()
        self.mystate = State.PLAYING
        self.defenderlist.clear()
        self.defcount = 0
        self.enemylist.clear()
        self.enemycount = 0
        self.level = 1

    def levelUp(self):
        self.level += 1
