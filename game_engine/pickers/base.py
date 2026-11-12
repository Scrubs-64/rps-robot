class MovePicker:
    """Base class for every move picker.

    A picker decides which move the arm will play. The engine only ever calls
    choose_move(), so any picker can be swapped for any other.
    """

    def choose_move(self, history):
        """Return the arm's next move: 'rock', 'paper' or 'scissors'.

        history: list of the player's PREVIOUS moves, oldest first.
                 It never contains the current round's move, because the
                 arm commits before the camera reads the player's hand.
        """
        raise NotImplementedError("Subclasses must implement choose_move()")