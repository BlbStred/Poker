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


    

class CardSet:   # of cards

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
        self.inHand = CardSet()

    def __str__(self):
        return "Player " + str(self.id) + ": " + str(self.inHand)
        
            
    def add(self, card):
        self.inHand.add(card)


    def cardValue(self):
        return 1-self.id



class Env:   # all the players and table contents
    def __init__(self, numPlayers):
        self.players = [Player(i) for i in range(numPlayers)]
        self.deck = [Card(key) for key in range(Card.numCards)]
        random.shuffle(self.deck)
        self.button = 0             #dealer
        


    def cardRemovedFromDeck(self):
        c = self.deck[0]
        self.deck = self.deck[1:]
        return c

    def deal(self):
        for c in range(2):  # 2 cards to each player
            for p in self.players:
                p.add(self.cardRemovedFromDeck())

    def __str__(self):
        result = "Deck:"
        for c in self.deck:
            result += " " + str(c) 
        result += "\n"
        
        for p in self.players:
            result += str(p) + "\n"
            
        return result
        

    def oneHand(self):
        numPlayers = len(self.players)
        
        self.button = (self.button + 1) % numPlayers
        
        if numPlayers == 2:  self.smallBlind =  self.button
        else:                self.smallBlind = (self.button + 1) % numPlayers
        
        self.BigBind = (self.smallBlind + 1) % numPlayers


    def oneGame(self):
        numHands = 5
        self.deal()
        for h in range(numHands):
            self.oneHand()

        # find winner
        winner = max(self.players, key = Player.cardValue)
        print("winner:", winner)
                     
        
        
if __name__ == "__main__":

    random.seed(42)
    env = Env(2)
    env.oneGame()

    
