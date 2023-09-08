import pygame
import pygwidgets

class Card():
    """
    Represents an individual playing card.

    A card object contains its rank, suit, and value attributes and methods to conceal or reveal itself.
    It also contains utility methods to fetch its value and manage its display properties.

    Attributes:
        BACK_OF_CARD_IMAGE (pygame.Surface): The image used for the back of the card.
        window (pygame.Surface): The game window where the card will be drawn.
        rank (str): Rank of the card (e.g., 'Jack', '10').
        suit (str): Suit of the card (e.g., 'Hearts', 'Spades').
        cardName (str): Combined name of rank and suit (e.g., 'Jack of Hearts').
        value (int): Numeric value assigned to the card.
        images (pygwidgets.ImageCollection): Collection of card images ('front' and 'back') with default
            location of the card for display.
    """

    BACK_OF_CARD_IMAGE = pygame.image.load('images/Back of Card.png')


    def __init__(self, window, rank, suit, value):
        """
        Initializes the Card class with essential attributes.

        Args:
            window (pygame.Surface): The game window where the card will be drawn.
            rank (str): Rank of the card.
            suit (str): Suit of the card.
            value (int): Numeric value assigned to the card.
        """

        self.window = window
        self.rank = rank
        self.suit = suit
        self.cardName = rank + ' of ' + suit
        self.value = value
        fileName = 'images/' + self.cardName + '.png'
        self.images = pygwidgets.ImageCollection(window, (0, 0),
                                {'front': fileName,
                                 'back': Card.BACK_OF_CARD_IMAGE}, 'back')


    def conceal(self):
        """
        Conceals the card by displaying its back side.
        """

        self.images.replace('back')


    def reveal(self):
        """
        Reveals the card by displaying its front side.
        """

        self.images.replace('front')


    def getValue(self):
        """
        Retrieves the card's numeric value.

        Returns:
            int: The numeric value of the card.
        """
        return self.value

    def setLoc(self, loc):
        """
        Set the location of the card on the game window.

        Args:
            loc (tuple): A tuple containing the x and y coordinates.
        """
        self.images.setLoc(loc)


    def draw(self):
        """
        Draw the card on the game window.
        """

        self.images.draw()