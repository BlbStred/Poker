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

    def placeBet(self, round):
        return 0

    
# what is publicly visible on the table
class Table:

    def __init__(self, numPlayers):
        self.pot    = 0                     # total money
        self.inPlay = [True for i in range(numPlayers)]     # whether a player is still in 
        self.bets   = [[]   for i in range(numPlayers)]     # sequence of bets for each player
        self.button = 0                                     # dealer is arbitrary
        self.advanceButton()


    def advanceButton(self):
        numPlayers = len(self.inPlay)
        self.button = (self.button + 1) % numPlayers
        
        if numPlayers == 2:  self.smallBlind =  self.button
        else:                self.smallBlind = (self.button + 1) % numPlayers
        
        self.bigBlind = (self.smallBlind + 1) % numPlayers


    def addToPot(self, bet):
        self.pot += bet
        

    def __str__(self):
        numPlayers = len(self.inPlay)

        result = "\n"

        result += ("\nButton: " + str(self.button) +
                   "  smallBlind: " + str(self.smallBlind) +
                   "  bigBlind: "   + str(self.bigBlind))
        
        result += "\nPot: " + str(self.pot)
        result += "\nInPlay: " + str(self.inPlay)
        result += "\nBets:"
        for i in range(numPlayers):
            result += "\n   " + str(i) + ": " + str(self.bets[0])

        return result

class Env:   # all the players and table contents
    def __init__(self, numPlayers):
        self.table = Table(numPlayers)
        self.players = [Player(i) for i in range(numPlayers)]
        self.deck = [Card(key) for key in range(Card.numCards)]
        random.shuffle(self.deck)
        
        


    def cardRemovedFromDeck(self):
        c = self.deck[0]
        self.deck = self.deck[1:]
        return c

    def deal(self):
        for c in range(2):  # 2 cards to each player
            for p in self.players:
                p.add(self.cardRemovedFromDeck())

    def __str__(self):
        result = "\n"
        result += str(self.table)        
        
        result += "\nDeck:"
        for c in self.deck:
            result += " " + str(c) 
        result += "\n"
        
        for p in self.players:
            result += str(p) + "\n"
            
        return result
        

    def oneHand(self):
        numPlayers = len(self.players)
        
        # Blinds
                
        self.table.addToPot(self.players[self.table.smallBlind].placeBet(0))
        self.table.addToPot(self.players[self.table.bigBlind].  placeBet(0))     
        
        """
        blinds()
        preFlop()
        flop()
        turn()
        river()
        showDown()
        """

    def oneGame(self):
        numHands = 5
        self.deal()
        print(self)
        for h in range(numHands):
            self.oneHand()
            print(self)
            # find winner
            winner = max(self.players, key = Player.cardValue)
            print("winner:", winner)
                     
        
        
if __name__ == "__main__":

    random.seed(42)
    env = Env(2)
    env.oneGame()

    
