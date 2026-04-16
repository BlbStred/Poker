import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Categorical


class Card:

    numSuits = 2
    numDenom = 3
    numCards = numSuits * numDenom
    

    def __init__(self, index):  # index into all cards

        self.suit  = index // Card.numDenom
        self.denom = index  % Card.numDenom        


    def __str__(self):
        return '[' + str(self.denom) + ['C', 'D', 'H', 'S'][self.suit] + ']'

    
        
if __name__ == "__main__":
    deck = [Card(i) for i in range(Card.numCards)]

    for d in deck:
        print(d)
