class ParticipantNotApproved(Exception):
    """
    Raised when a participant is not approved.
    """


class AuctionClosed(Exception):
    """
    Raised when an operation is attempted on a closed auction.
    """


class InsufficientCoins(Exception):
    """
    Raised when a participant has insufficient coins.
    """