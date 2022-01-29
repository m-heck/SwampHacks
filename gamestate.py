
# Game state class that controls the general functions of the player and game
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
            self.level = 1
            Gamestate.stateinstance = self

    @staticmethod
    def gameInstance():
        if Gamestate.stateinstance == None:
            Gamestate()
        return Gamestate.stateinstance

    def getState(self):
        return self.mystate
    def getlists(self):
        return defenderlist,enemylist
    def setlists(self,defender,enemy):
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
        print("Not decided yet")



