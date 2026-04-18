import random
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


    def getKey(self):             # 1-1 correspondence between cards and key (integers)
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


class Player:

    def __init__(self, id):
        self.id   = id
        self.hand = Hand()

    def __str__(self):
        return "Player " + str(self.id) + ": " + str(self.hand)
        
            
    def add(self, card):
        self.hand.add(card)



class Env:   # all the players and table contents
    def __init__(self, numPlayers):
        self.players = [Player(i) for i in range(numPlayers)]
        self.deck = [Card(key) for key in range(Card.numCards)]
        random.shuffle(self.deck)


    def getCard(self):
        c = self.deck[0]
        self.deck = self.deck[1:]
        return c

    def deal(self):
        for c in range(2):  # 2 cards to each player
            for p in self.players:
                p.add(self.getCard())

    def __str__(self):
        result = ""
        for p in self.players:
            result = result + " " + str(p) + "\n"
        return result
        

                     
        
        
if __name__ == "__main__":

    random.seed(42)
    env = Env(2)
    print(env)
    env.deal()
    print(env)
    
