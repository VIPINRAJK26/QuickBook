class InsufficientSeatsError(Exception):
    """Raised when requested seats exceed available seats."""
    pass


class BookingAlreadyCancelledError(Exception):
    """Raised when attempting to cancel an already cancelled booking."""
    pass


class BookingPermissionError(Exception):
    """Raised when a user attempts to cancel another user's booking."""
    pass
