# Bank class for storing/calculating player gold
import pygame
import os
import fighter
import defender

class Bank:
    gold = 500
    round = 1
    killed = 0

    def get_gold:
        return gold

    # gives player gold at the end of every round
    def round_end:
        gold += (round * 80) + (5 * killed)
        round += 1
        killed = 0

    def buy(defender x):
        if gold < x.get_price():
            pass
        else
            gold -= x.get_price()


        #function to track kills, not sure how to detect events yet
''' 
    def track_kills:
        for event in pygame.event.get():
            if event.type == attacker_killed:
                killed += 1
'''