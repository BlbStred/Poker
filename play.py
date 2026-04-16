import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Categorical


class Card:

    numSuits = 2
    numDenom = 3
    numCards = numSuits * numDenom
    

    def __init__(self, key):  # index into all cards

        self.suit  = key // Card.numDenom
        self.denom = key  % Card.numDenom


    def getKey(self):
        return self.suit * Card.numDenom + self.denom


    def __str__(self):
        return '[' + str(self.denom) + ['C', 'D', 'H', 'S'][self.suit] + ']'


    

class Hand:   # of cards

    def __init__(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)
        self.cards.sort(key = Card.getKey)   # sort to reduce variety of states


    def __str__(self):
        result = ""
        for c in self.cards:
            result = result + " " + str(c)
        return result
            
        
if __name__ == "__main__":

    
    deck = [Card(Card.numCards - i - 1) for i in range(Card.numCards)]

    hand = Hand()
    
    for d in deck:
        hand.add(d)
        print("added", d, "to", hand)
        
