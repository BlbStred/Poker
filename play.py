import random
import copy
from itertools import chain
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Categorical


class Card:

    numSuits = 3
    numDenom = 4
    numCards = numSuits * numDenom
    numRanks = numDenom               # individual cards divided into this many ranks
    

    def __init__(self, key):  # index into all cards

        self.suit  = key // Card.numDenom
        self.denom = key  % Card.numDenom


    def getKey(self):             # 1-1 correspondence between cards and key (integers)
        return self.suit * Card.numDenom + self.denom


    def ranking(self):
        return self.denom
    
        
    def __str__(self):
        return ('['                                                                            +
                ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'][self.denom] +
                ['C', 'D', 'H', 'S'][self.suit]                                                +
                ']')


    

class CardSet:   # of cards

    def __init__(self, init=None):
        self.cards = []
        if init != None:
            self.addCards(copy.deepcopy(init.cards))

    def addCards(self, cardList):
        cardList.sort(key = Card.getKey)   # sort to reduce variety of states
        self.cards += cardList


    def getCard(self, i):
        return self.cards[i]


    
    def ranking(self):
        # For conveniece sort in increasing order
        self.cards.sort(key = Card.getKey)
        print(self)
        # ranking =
        # pattern rank * Card.numRanks +
        # rank of highest card

        patternRank = 100
        
        # Royal flush
        return 42
        
    

    def __str__(self):
        result = ""
        for c in self.cards:
            result = result + " " + str(c)
        return result


class Player:

    def __init__(self, id, table):
        self.id    = id
        self.table = table   # whatever is visible on the table

    
    def resetForNewHand(self):
        self.inHand = CardSet()

    def __str__(self):
        return "Player " + str(self.id) + ": " + str(self.inHand)
        
            
    def addCards(self, cardList):
        self.inHand.addCards(cardList)

    def pickCommunityCards(self):
        self.bestRank = 0     # remains if player folded
        self.bestCards = None # the five best bards
                
        for i in range(0, 5):
            for j in range(i+1, 5):
                for k in range(j+1, 5):
                    fiveCards = CardSet(init=self.inHand)
                    fiveCards.addCards([self.table.getCardOnTable(i),
                                        self.table.getCardOnTable(j),
                                        self.table.getCardOnTable(k)])
                    rank = fiveCards.ranking()
                    if rank > self.bestRank:
                        self.bestRank = fiveCards.ranking()
                        self.bestCards = fiveCards
                        
                        

    def cardValue(self):
        return self.bestRank

    def placeBet(self, round):
        return 0

    
# what is publicly visible on the table
class Table:

    def __init__(self, numPlayers):
        self.numPlayers = numPlayers
        self.button = 0                                     # dealer is arbitrary

    def resetForNewHand(self):
        self.pot    = 0                     # total money
        self.cardsOnTable = CardSet()
        self.inPlay = [True for i in range(self.numPlayers)]     # whether a player is still in 
        self.bets   = [[]   for i in range(self.numPlayers)]     # sequence of bets for each player
        self.advanceButton()

        
    def advanceButton(self):
        self.button = (self.button + 1) % self.numPlayers
        
        if self.numPlayers == 2:  self.smallBlind =  self.button
        else:                     self.smallBlind = (self.button + 1) % self.numPlayers
        
        self.bigBlind = (self.smallBlind + 1) % self.numPlayers


    def addToPot(self, bet):
        self.pot += bet

    def getCardOnTable(self, i):
        return self.cardsOnTable.getCard(i)
                                   

        
    def addToCardsOnTable(self, cardList):
        self.cardsOnTable.addCards(cardList)
        
        

    def __str__(self):
        result = "\nPublic on Table:"

        result += ("\nButton: " + str(self.button) +
                   "  smallBlind: " + str(self.smallBlind) +
                   "  bigBlind: "   + str(self.bigBlind))
        
        result += "\nCards face up: " + str(self.cardsOnTable)
        result += "\nPot: " + str(self.pot)        
        result += "\nInPlay: " + str(self.inPlay)
        result += "\nBets:"
        for i in range(self.numPlayers):
            result += "\n   " + str(i) + ": " + str(self.bets[0])

        return result




    
class Env:   # all the players and table contents
    def __init__(self, numPlayers):
        self.numPlayers = numPlayers
        self.table = Table(numPlayers)
        self.players = [Player(i, self.table) for i in range(numPlayers)]
        

    def resetForNewHand(self):
        for i in range(self.numPlayers):
            self.players[i].resetForNewHand()

        self.table.resetForNewHand()
        
        self.deck = [Card(key) for key in range(Card.numCards)]
        random.shuffle(self.deck)
        
            


    def cardRemovedFromDeck(self):
        c = self.deck[0]
        self.deck = self.deck[1:]
        return c

    def deal(self):
        for p in self.players:
            # 2 cards to each player
            p.addCards([self.cardRemovedFromDeck() for c in range(2)])
            

    def __str__(self):
        result = ""
        result += str(self.table)        
        
        result += "\nPrivate:"
        result += "\nDeck:"        
        for c in self.deck:
            result += " " + str(c) 
        result += "\n"
        
        for p in self.players:
            result += str(p) + "\n"
            
        return result
        

    def oneHand(self):
        print("=========== HAND =============")
        self.resetForNewHand()
        
        # Blinds
                
        self.table.addToPot(self.players[self.table.smallBlind].placeBet(0))
        self.table.addToPot(self.players[self.table.bigBlind].  placeBet(0))     
        

        # preFlop
        self.deal()
        self.bettingRound(1)
        
        # flop
        # place 3 cards face up
        self.table.addToCardsOnTable([self.cardRemovedFromDeck() for c in range(3)])
        self.bettingRound(2)             
        
        # turn
        self.table.addToCardsOnTable([self.cardRemovedFromDeck() for c in range(1)])
        self.bettingRound(3)

        # river
        self.table.addToCardsOnTable([self.cardRemovedFromDeck() for c in range(1)])
        self.bettingRound(3)
        
        
        # showDown
        for p in self.players:
            p.pickCommunityCards()
        winner = max(self.players, key = Player.cardValue)
        print("winner:", winner)
   

        
    def bettingRound(self, round):
        start = (self.table.bigBlind + 1) % self.numPlayers
        for i in chain(range(start, self.numPlayers), range(0, start)):
            self.table.addToPot(self.players[i].placeBet(round))
            #print("After player", i, "bet")
            #print(self)
            
    
        
        
if __name__ == "__main__":

    random.seed(42)
    env = Env(2)
    for i in range(3):
        env.oneHand()
    

    
