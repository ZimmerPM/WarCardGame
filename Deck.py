import random
from Card import *

class Deck():
    """
    Represents a standard deck of playing cards.

    This class models a deck of cards which can be shuffled and dealt from.
    It incorporates standard card suits and can be configured to use custom rank values.

    Attributes:
        SUIT_TUPLE (tuple): Defines the four suits of a standard deck.
        STANDARD_DICT (dict): Maps the rank of cards to their respective values.
    """

    SUIT_TUPLE = ('Hearts', 'Spades', 'Diamonds', 'Clubs')
    STANDARD_DICT = {'9': 9, '10': 10, 'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}


    def __init__(self, window, rankValueDict=STANDARD_DICT):
        """
        Initializes a new deck of cards with given rank values.

        Args:
            window: The graphical window where the cards are displayed.
            rankValueDict (dict, optional): A dictionary mapping card ranks to their values.
                                            Defaults to the standard rank-to-value dictionary.

        Attributes:
            startingDeckList (list): A list of Card objects representing the initial state of the deck.
            playingDeckList (list): A dynamic list of Card objects representing the current state of the deck.
        """

        self.startingDeckList = []
        self.playingDeckList = []
        for suit in Deck.SUIT_TUPLE:
            for rank, value in rankValueDict.items():
                oCard = Card(window, rank, suit, value)
                self.startingDeckList.append(oCard)
        self.shuffle()

    def shuffle(self):
        """
        Shuffles the deck, ensuring cards are in random order and concealed.

        Resets the playing deck list to a copy of the starting deck and then shuffles
        it to ensure randomness in the card order. Also, ensures that all cards are concealed.
        """
        self.playingDeckList = self.startingDeckList.copy()
        for oCard in self.playingDeckList:
            oCard.conceal()
        random.shuffle(self.playingDeckList)

    def getCard(self):
        """
        Deals and returns the top card from the deck.

        Removes the top card from the playing deck list and returns it. If the deck
        is empty, it raises an error indicating no more cards are left to be dealt.

        Returns:
            Card: The top card from the deck.

        Raises:
            IndexError: If there are no cards left in the playing deck list.
        """
        if len(self.playingDeckList) == 0:
            raise IndexError('Brak kolejnych kart.')
        oCard = self.playingDeckList.pop()
        return oCard