from Deck import *
from Text import *

class Game():
    """
      Represents the game of war where players compete for dominance in a deck of cards.

      This class manages the game's logic, including: initializing gameplay, checking
      end conditions, handling "war" scenarios, and card display management.

       Attributes:
        PLAYER_CARDS_LEFT (int): The left position for Player's cards on the screen.
        NPC_CARDS_LEFT (int): The left position for NPC's cards on the screen.
        CARDS_TOP (int): The top position for cards on the screen.
        CARD_OFFSET (int): The offset used to place cards relative to other cards.
        MAX_ROUND_NUMBER (int): The maximum number of rounds the game can last.
      """

    CARDS_TOP = 250
    PLAYER_CARDS_LEFT = 200
    NPC_CARDS_LEFT = 565
    CARD_OFFSET = 150
    MAX_ROUND_NUMBER = 100
    N_SEEN_CARDS = 4


    def __init__(self, window):
        """
        Initialize the Game class with essential attributes and game setup.

        Args:
            window: The game window in which all the game elements will be displayed.

        Attributes:
            window (pygame.Surface): The game window where elements will be drawn.
            oDeck (Deck): Represents the deck of cards used in the game.
            oText (Text): Utility for handling text display and interaction.
            roundNumber (int): Counter for the number of rounds played.
            cardsSet (bool): Flag to check if the cards are set.
            displayedCardList (list): List of cards currently being displayed.
            specialDisplayList (list): List for any special ways to display cards.
            playerCardWrap (bool): Flag to check if player cards need wrapping.
            npcCardWrap (bool): Flag to check if NPC cards need wrapping.
            playerScore (int): Score counter for the player.
            npcScore (int): Score counter for the NPC.
            warNumber (int): Counter for the number of wars triggered.
            warMode (bool): Flag to check if the game is currently in war mode.
            anotherWar (bool): Flag for any consecutive wars.
            stack (list): List of cards involved in a war.
            stackCardsToShow (bool): Flag to indicate if cards from the stack should be displayed.
        """

        self.window = window
        self.oDeck = Deck(self.window)
        self.oText = Text(self.window)

        self.roundNumber = 0
        self.cardsSet = False
        self.displayedCardList = []
        self.specialDisplayList = []
        self.playerCardWrap = False
        self.npcCardWrap = False

        self.playerScore = len(self.oDeck.playingDeckList) // 2
        self.npcScore = len(self.oDeck.playingDeckList) // 2

        self.warNumber = 0
        self.warMode = False
        self.anotherWar = False
        self.stack = []
        self.stackCardsToShow = False

        self.dealCards()
        self.manageGame()

    def dealCards(self):
        """
        Deals cards to both player and NPC from the shuffled deck.

        This method shuffles the main deck and then distributes cards
        alternately between the player and NPC. After distributing, it also
        updates the on-screen text to display the current card count for
        both the player and the NPC.

        Attributes:
            self.oDeck: An instance of the Deck class representing the main deck.
            self.playerCardList: List storing the cards dealt to the player.
            self.npcCardList: List storing the cards dealt to the NPC.
            self.oText: An instance of the Text class used for updating on-screen text.

        Note:
            Assumes that the starting deck size is even, so that cards can be
            equally distributed between player and NPC.
        """

        self.oDeck.shuffle()
        self.playerCardList = []
        self.npcCardList = []

        for i in range(len(self.oDeck.startingDeckList)):
            if i % 2 == 0:
                self.playerCardList.append(self.oDeck.getCard())
            else:
                self.npcCardList.append(self.oDeck.getCard())

        self.oText.playerScoreText.setValue('Liczba kart w talii Gracza: ' + str(self.playerScore))
        self.oText.npcScoreText.setValue('Liczba kart w talii NPC: ' + str(self.npcScore))

    def manageGame(self):
        """
        Manages the flow of the game based on the current game state.

        This method controls the overall flow and progression of the game, deciding which
        phase or action should be executed next based on various game conditions:
        - Displays the initial game view if the game hasn't started.
        - Handles the "war" scenario where both players have a card of the same value.
        - Shows stack cards if applicable.
        - Otherwise, proceeds with the normal gameplay.

        Returns:
            bool: True if the game should end, False if it should continue.
        """

        if not self.cardsSet:
            self.firstView()

        elif self.warMode:
            return self.war()

        elif self.stackCardsToShow:
            return self.showStackCards()

        else:
            return self.gamePlay()

    def firstView(self):
        """
            Initialize the game's initial view by setting the top card of player's and NPC's hands.

            The method determines which card is currently on top of the player's and NPC's hand
            and prepares them for display. Then, it sets the position of the cards on the game
            screen. The cards' positions are based on predefined constants. Once all cards are
            set in place, the 'cardsSet' flag is set to True, indicating that the initial card
            placement is complete.

            Attributes set:
                - playerHandCard: The top card of the player's hand.
                - npcHandCard: The top card of the NPC's hand.
                - displayedCardList: List of cards that are currently being displayed on the screen.
                - cardsSet: Flag indicating whether the initial card placement is done.
            """

        self.playerHandCard = self.playerCardList[-1]
        self.npcHandCard = self.npcCardList[-1]

        self.displayedCardList.extend([self.playerHandCard, self.npcHandCard])

        thisLeft = Game.PLAYER_CARDS_LEFT
        for i in range(Game.N_SEEN_CARDS // 2):
            self.displayedCardList[i].setLoc((thisLeft, Game.CARDS_TOP))
            thisLeft = Game.NPC_CARDS_LEFT + Game.CARD_OFFSET
        else:
            self.cardsSet = True

    def prepareToDisplay(self):
        """
        Prepares the appropriate cards for display based on the current game state.

        This method clears the lists that track displayed cards and special display
        conditions. It ensures that cards laid by the player and the NPC are revealed
        while the top cards of their hands are concealed. Depending on the conditions
        related to card wrapping for both player and NPC, the method decides which set
        of cards to display: the regular set or the special set.

        Attributes set or modified:
            - displayedCardList: List of cards that will be displayed in the regular game view.
            - specialDisplayList: List of cards/items that need special display conditions.
            - playerLaidCard, npcLaidCard: Revealed state set for cards laid by player and NPC.
            - playerHandCard, npcHandCard: Concealed state set for the top cards of player and NPC hands.
        """

        self.displayedCardList = []
        self.specialDisplayList = []

        for oCard in [self.playerLaidCard, self.npcLaidCard]:
            oCard.reveal()

        for oCard in [self.playerHandCard, self.npcHandCard]:
            oCard.conceal()

        if not self.playerCardWrap and not self.npcCardWrap:
            self.displayedCardList.extend(
                [self.playerHandCard, self.playerLaidCard, self.npcLaidCard, self.npcHandCard])

            self.setToDisplay()

        else:
            self.setSpecialToDisplay()


    def setToDisplay(self):
        """
        Sets the display location for cards for both the player and the NPC.

        This method uses predefined constants to determine the initial position
        (PLAYER_CARDS_LEFT, NPC_CARDS_LEFT) and offsets (CARD_OFFSET) for card display.
        It then arranges cards for both player and NPC based on the total number
        of cards to be displayed (N_SEEN_CARDS).
        """

        thisLeft = Game.PLAYER_CARDS_LEFT
        for i in range(Game.N_SEEN_CARDS // 2):
            self.displayedCardList[i].setLoc((thisLeft, Game.CARDS_TOP))
            thisLeft += Game.CARD_OFFSET

        thisLeft = Game.NPC_CARDS_LEFT
        for i in range(Game.N_SEEN_CARDS // 2, Game.N_SEEN_CARDS):
            self.displayedCardList[i].setLoc((thisLeft, Game.CARDS_TOP))
            thisLeft += Game.CARD_OFFSET


    def setSpecialToDisplay(self):
        """
        Sets the display locations for cards under special circumstances.

        This method arranges card positions for cases where the card display
        needs special handling, like when a player's card wraps around or other
        unique game scenarios. Depending on whether the player's or NPC's card
        requires special handling, cards are revealed and positioned accordingly.
        """

        if self.playerCardWrap:
            self.specialDisplayList = [self.playerLaidCard, self.npcLaidCard, self.npcHandCard]

            if self.playerLaidCard is self.playerHandCard:
                self.playerLaidCard.reveal()

            self.npcLaidCard.reveal()

            thisLeft = Game.PLAYER_CARDS_LEFT + Game.CARD_OFFSET
            self.specialDisplayList[0].setLoc((thisLeft, Game.CARDS_TOP))

            thisLeft = Game.NPC_CARDS_LEFT
            for i in range(1, 3):
                self.specialDisplayList[i].setLoc((thisLeft, Game.CARDS_TOP))
                thisLeft += Game.CARD_OFFSET

            self.playerCardWrap = False


        else:
            self.specialDisplayList = [self.playerHandCard, self.playerLaidCard, self.npcLaidCard]

            if self.npcLaidCard is self.npcHandCard:
                self.npcLaidCard.reveal()

            self.playerLaidCard.reveal()

            thisLeft = Game.PLAYER_CARDS_LEFT
            for i in range(2):
                self.specialDisplayList[i].setLoc((thisLeft, Game.CARDS_TOP))
                thisLeft += Game.CARD_OFFSET

            thisLeft = Game.NPC_CARDS_LEFT
            self.specialDisplayList[2].setLoc((thisLeft, Game.CARDS_TOP))

            self.npcCardWrap = False


    def draw(self):
        """
        Draws the current game state on the window.

        This method renders all relevant cards, texts, and other game elements
        on the window. It ensures that elements like the player's and NPC's score,
        round number, messages, war indications, and endgame messages are drawn when
        applicable.
        """
        for oCard in self.specialDisplayList:
            oCard.draw()

        for oCard in self.displayedCardList:
            oCard.draw()

        self.oText.playerScoreText.draw()
        self.oText.npcScoreText.draw()
        self.oText.roundNumberText.draw()

        if self.roundNumber > 0:
            self.oText.messageText.draw()

        if self.warNumber > 0:
            self.oText.warNumberText.draw()

        if self.stackCardsToShow:
            self.oText.stackText.draw()

        if self.oText.gameOverText.getValue() == "Koniec gry!":
            self.oText.gameOverText.draw()
            self.oText.winnerText.draw()


    def returnCard(self, competitorList, oCard):
        """
        Returns the specified card to the beginning of the given competitor's list.

        This method is used to put a card back at the start of a player's or NPC's card list,
        typically after some game actions.

        Args:
            competitorList (list): The list representing the card set of either the Player or NPC.
            oCard (Card): The card object to be returned to the competitor's list.
        """

        competitorList.insert(0, oCard)


    def setScores(self):
        """
        Updates the card count for both the Player and the NPC that are to be displayed.

        The method calculates the number of cards for the Player and the NPC based on the length
        of their respective card lists. It then updates the text values representing their scores,
        which are displayed on the game's interface.

         Note:
            The updated scores will be displayed when the `draw()` method is called.
        """
        self.playerScore = len(self.playerCardList)
        self.oText.playerScoreText.setValue('Liczba kart w talii Gracza: ' + str(self.playerScore))
        self.npcScore = len(self.npcCardList)
        self.oText.npcScoreText.setValue('Liczba kart w talii NPC: ' + str(self.npcScore))


    def gamePlay(self):
        """
        Execute a single round of gameplay between the player and the NPC.

        In this method, both the player and the NPC lay a card. The card with the higher value wins
        and the winner takes both cards. If the cards have the same value, a war is initiated. The
        method also updates various game elements, such as the round number, scores, and the display
        of cards. It checks for endgame conditions and returns a boolean indicating whether the game
        has ended or not.

        Returns:
            bool: True if the game is over, otherwise False.
        """

        self.roundNumber += 1
        self.oText.roundNumberText.setValue('Runda numer : ' + str(self.roundNumber) +'/'+ str(Game.MAX_ROUND_NUMBER))

        self.playerLaidCard = self.playerCardList.pop()
        if self.playerCardList:
            self.playerHandCard = self.playerCardList[-1]
        else:
            self.playerCardWrap = True

        self.npcLaidCard = self.npcCardList.pop()
        if self.npcCardList:
            self.npcHandCard = self.npcCardList[-1]
        else:
            self.npcCardWrap = True


        if self.playerLaidCard.getValue() > self.npcLaidCard.getValue():

            self.returnCard(self.playerCardList, self.playerLaidCard)
            self.returnCard(self.playerCardList, self.npcLaidCard)

            self.oText.messageText.setValue('Gracz wygrywa rundę')

            if self.playerCardWrap:
                self.playerHandCard = self.playerCardList[-2]


        elif self.playerLaidCard.getValue() < self.npcLaidCard.getValue():

            self.returnCard(self.npcCardList, self.npcLaidCard)
            self.returnCard(self.npcCardList, self.playerLaidCard)

            self.oText.messageText.setValue('NPC wygrywa rundę')

            if self.npcCardWrap:
                self.npcHandCard = self.npcCardList[-2]


        else:

            self.warMode = True
            self.oText.messageText.setValue('       WOJNA!')


        self.prepareToDisplay()

        self.setScores()

        if self.warMode:
            self.warChecking()

        return self.checkGameOver(self.playerCardList, self.npcCardList, self.roundNumber)


    def war(self):
        """
        Handles the "war" scenario in the card game.

        In a "war", each player lays down additional cards to determine the winner of the war.
        If the newly laid cards are again of equal value, another "war" scenario occurs.
        This method manages the process of taking cards from each player's deck, updating
        the stack, and determining the winner of the war. It also updates the game's state
        and messages to reflect the outcome of the war.

        Returns:
            bool: Returns `True` if the game ends due to the war process, otherwise `False`.
        """

        if not self.anotherWar:
            for oCard in [self.playerLaidCard, self.npcLaidCard]:
                self.stack.append(oCard)

        else:
            if self.warChecking():
                return self.checkGameOver(self.playerCardList, self.npcCardList, self.roundNumber)

        self.warNumber += 1

        self.oText.warNumberText.setValue('Liczba wojen : ' + str(self.warNumber))

        self.playerStakeCard = self.playerCardList.pop()
        self.npcStakeCard = self.npcCardList.pop()

        self.playerNewLaidCard = self.playerCardList.pop()
        if self.playerCardList:
            self.playerHandCard = self.playerCardList[-1]
        else:
            self.playerCardWrap = True

        self.npcNewLaidCard = self.npcCardList.pop()
        if self.npcCardList:
            self.npcHandCard = self.npcCardList[-1]
        else:
            self.npcCardWrap = True

        for oCard in [self.playerStakeCard, self.npcStakeCard, self.playerNewLaidCard, self.npcNewLaidCard]:
            self.stack.append(oCard)

        self.warGraph()

        if self.playerNewLaidCard.getValue() > self.npcNewLaidCard.getValue():

            self.oText.messageText.setValue('Gracz wygrywa wojnę!')

            self.playerCardList = self.stack + self.playerCardList

            self.stackCardsToShow = True
            self.warMode = False
            self.anotherWar = False

            self.setScores()

            return False


        elif self.playerNewLaidCard.getValue() < self.npcNewLaidCard.getValue():

            self.oText.messageText.setValue('NPC wygrywa wojnę!')

            self.npcCardList = self.stack + self.npcCardList

            self.stackCardsToShow = True
            self.warMode = False
            self.anotherWar = False

            self.setScores()

            return False


        else:
            self.oText.messageText.setValue('ZNOWU WOJNA!')
            self.anotherWar = True

            self.setScores()

            return False


    def warGraph(self):
        """
        Updates the card display during a "war" scenario in the game.

        This method manages the graphical representation of cards during a "war".
        Cards in hand and those placed as stake are concealed while the cards laid
        out for the war are revealed. Depending on the game's state, the method
        adjusts the card display lists to ensure cards are displayed appropriately.

        Notes:
        - Cards are divided between two display lists: 'displayedCardList' and 'specialDisplayList'.
        - The display of cards gets adjusted using `setToDisplay`, `setSpecialToDisplay`, and `additionalCards`.
        """

        for oCard in [self.playerHandCard, self.npcHandCard, self.playerStakeCard, self.npcStakeCard]:
            oCard.conceal()

        for oCard in [self.playerLaidCard, self.npcLaidCard, self.playerNewLaidCard, self.npcNewLaidCard]:
            oCard.reveal()


        if not self.anotherWar:

            self.displayedCardList = []
            self.specialDisplayList = []

            self.displayedCardList = [self.playerHandCard, self.playerLaidCard, self.npcLaidCard, self.npcHandCard,
                                      self.playerStakeCard, self.playerNewLaidCard, self.npcStakeCard,
                                      self.npcNewLaidCard]

            if not self.playerCardWrap and not self.npcCardWrap:
                self.setToDisplay()
            else:
                self.setSpecialToDisplay()

            self.additionalCards()


        else:

            self.displayedCardList[0] = self.playerHandCard
            self.displayedCardList[3] = self.npcHandCard

            for oCard in [self.playerStakeCard, self.playerNewLaidCard, self.npcStakeCard, self.npcNewLaidCard]:
                self.displayedCardList.append(oCard)

            if not self.playerCardWrap and not self.npcCardWrap:
                self.setToDisplay()
            else:
                self.setSpecialToDisplay()

            self.additionalCards()


    def additionalCards(self):
        """
        Adjusts the location of additional cards during the game, specifically for the war mode.

        This method positions the additional cards that are used during the war mode in the game. The
        locations of the Player's and NPC's cards are adjusted separately based on the current state
        of the war (whether it's the first war or another subsequent war).

        Attributes:
            thisLeft: Initial left position for placing the card.
            thisTop: Initial top position for placing the card.

        Notes:
        - The 'anotherWar' flag determines the logic branch for positioning.
        - `warCardsTop` attribute keeps track of the vertical position for next card placements
            in subsequent wars.
        """

        if not self.anotherWar:

            thisLeft = Game.PLAYER_CARDS_LEFT + Game.CARD_OFFSET
            thisTop = Game.CARDS_TOP + 30
            for i in range(Game.N_SEEN_CARDS, Game.N_SEEN_CARDS + 2):
                self.displayedCardList[i].setLoc((thisLeft, thisTop))
                thisTop += 30

            thisLeft = Game.NPC_CARDS_LEFT
            thisTop = Game.CARDS_TOP + 30
            for i in range(Game.N_SEEN_CARDS + 2, Game.N_SEEN_CARDS + 4):
                self.displayedCardList[i].setLoc((thisLeft, thisTop))
                thisTop += 30

            self.warCardsTop = thisTop

        else:

            listIter = len(self.displayedCardList)

            thisLeft = Game.PLAYER_CARDS_LEFT + Game.CARD_OFFSET
            thisTop = self.warCardsTop
            for i in range(listIter - 4, listIter - 2):
                self.displayedCardList[i].setLoc((thisLeft, thisTop))
                thisTop += 30

            thisLeft = Game.NPC_CARDS_LEFT
            thisTop = self.warCardsTop
            for i in range(listIter - 2, listIter):
                self.displayedCardList[i].setLoc((thisLeft, thisTop))
                thisTop += 30

            self.warCardsTop = thisTop

    def showStackCards(self):
        """
        Reveals the cards in the stack and checks if the game is over.

        This method is responsible for displaying the cards that are currently in the stack
        as a result of a war. After revealing the cards, the method resets the stack and checks
        the game's status to determine if it has reached its conclusion.

        Returns:
            bool: True if the game is over, otherwise False.

        Notes:
        - Cards in the stack are a result of wars during gameplay.
        - The method utilizes the `checkGameOver` function to verify the game's status.
        """

        for oCard in self.stack:
            oCard.reveal()

        self.stackCardsToShow = False
        self.stack = []

        return self.checkGameOver(self.playerCardList, self.npcCardList, self.roundNumber)


    def warChecking(self):
        """
        Checks if either player has insufficient cards to proceed with the war.

        This method verifies if both the Player and the NPC have the required number of cards
        to continue with the war. If either the Player or the NPC has less than 2 cards:
        - A message is displayed indicating the insufficiency of cards.
        - All cards from the player with insufficient cards, along with the stack,
            are transferred to the opponent.
        - The card list of the player with insufficient cards is cleared.

        Returns:
            bool: True if either player doesn't meet the card requirement for the war, False otherwise.
         """

        if len(self.playerCardList) < 2:
            self.oText.messageText.setValue('Gracz ma zbyt mało kart by rozegrać wojnę!')
            self.npcCardList = self.npcCardList + self.stack + self.playerCardList
            self.playerCardList = []
            return True

        elif len(self.npcCardList) < 2:
            self.oText.messageText.setValue('NPC ma zbyt mało kart by rozegrać wojnę!')
            self.playerCardList = self.playerCardList + self.stack + self.npcCardList
            self.npcCardList = []
            return True
        else:
            return False


    def checkGameOver(self, playerCardList, npcCardList, roundNumber):
        """
        Checks if the game is over based on specified conditions.

        This method evaluates the current state of the game by examining
        the card count for the Player and the NPC as well as the current round number.
        If any of the game-over conditions are met, appropriate end-game messages are set
        and the method returns True. Otherwise, it returns False.

        Args:
            playerCardList (list): List containing the Player's cards.
            npcCardList (list): List containing the NPC's cards.
            roundNumber (int): Current round number.

        Returns:
            bool: True if the game is over, False otherwise.
        """

        condition1 = len(npcCardList) == 0
        condition2 = len(playerCardList) == 0
        condition3 = roundNumber == Game.MAX_ROUND_NUMBER

        if condition1:
            self.oText.gameOverText.setValue('Koniec gry!')
            self.oText.winnerText.setValue('Gracz wygrywa grę!')
            return True

        elif condition2:
            self.oText.gameOverText.setValue('Koniec gry!')
            self.oText.winnerText.setValue('NPC wygrywa grę!')
            return True

        elif condition3:
            self.oText.gameOverText.setValue('Koniec gry!')
            self.oText.messageText.setValue('Osiągnięto maksymalną liczbę rund')

            if len(playerCardList) > len(npcCardList):
                self.oText.winnerText.setValue('Gracz wygrywa grę!')
                return True

            elif len(playerCardList) < len(npcCardList):
                self.oText.winnerText.setValue('NPC wygrywa grę!')
                return True
            else:
                self.oText.winnerText.setValue('Remis!')
                return True
        else:
            return False