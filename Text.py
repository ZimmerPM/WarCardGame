import pygwidgets

class Text():
    """
    Represents the game text elements used for displaying information during gameplay.

    This class manages various text elements such as player scores, round number, war count,
    messages, and game over information. These text elements are displayed on the game window
    to provide feedback and updates to the Player.

    Attributes:
        window (pygame.Surface): The game window where text elements will be displayed.
        playerScoreText (pygwidgets.DisplayText): Text displaying the Player's remaining card count.
        npcScoreText (pygwidgets.DisplayText): Text displaying the NPC's remaining card count.
        roundNumberText (pygwidgets.DisplayText): Text displaying the current round number.
        warNumberText (pygwidgets.DisplayText): Text displaying the number of wars triggered.
        messageText (pygwidgets.DisplayText): Text displaying round outcome information.
        stackText (pygwidgets.DisplayText): Text instructing the Player to reveal stack cards.
        gameOverText (pygwidgets.DisplayText): Text displaying game over information.
        winnerText (pygwidgets.DisplayText): Text displaying the winner of the game.
        """


    def __init__(self, window):
        """
        Initializes the Text class for displaying in-game information and updates.

        Args:
            window (pygame.Surface): The game window where text elements will be displayed.
        """

        self.window = window

        self.playerScoreText = pygwidgets.DisplayText(window, (130, 200),
                                                       'Liczba kart w talii Gracza:',
                                                       fontSize=30, textColor=(255, 255, 0),
                                                       justified='left')

        self.npcScoreText = pygwidgets.DisplayText(window, (650, 200),
                                                       'Liczba kart NPC: ' ,
                                                       fontSize=30, textColor=(255, 255, 0),
                                                       justified='right')

        self.roundNumberText = pygwidgets.DisplayText(window, (200, 75), 'Runda numer: ', fontSize=28,
                                                       textColor=(255, 255, 0), justified='center')

        self.warNumberText = pygwidgets.DisplayText(window, (600, 75), 'Liczba wojen: ', fontSize=28,
                                                       textColor=(255, 255, 0), justified='center')

        self.messageText = pygwidgets.DisplayText(window, (400, 500), 'Informacja o wygranej rundzie ', fontSize=32,
                                                       textColor=(255, 255, 0), justified='center')

        self.stackText = pygwidgets.DisplayText(window, (340, 550), 'Naciśnięcie "Graj" odkryje karty-stawki ', fontSize=30,
                                                       textColor=(255, 255, 0), justified='center')


        self.gameOverText = pygwidgets.DisplayText(window, (400, 600), 'Info o zakończeniu gry!', fontSize=50,
                                                       textColor=(255, 255, 0), justified='center')
        self.winnerText = pygwidgets.DisplayText(window, (400, 130), 'Gracz wygrywa! ', fontSize=50,
                                                       textColor=(255, 255, 0), justified='center')