class ChessError(Exception):
    """Custom Exceptions"""
    pass

class CannotMoveError(ChessError):
    """Raised when a piece cannot be moved to a specified position"""
    pass

class InitializeError(ChessError):
    """Raised when a part of the program is unable to be initialized"""
    pass
