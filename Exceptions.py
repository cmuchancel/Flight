class ReValueError(Exception):
    """Exception raised when Reynolds number (Re) exceeds the valid range."""
    pass

class RrValueError(Exception):
    """Exception raised when rotational Reynolds number (Rr) exceeds the valid range."""
    pass

class DragCoefficientUnknownError(Exception):
    """Exception raised when Function doesn't output a value, because no conditions were satisied."""
    pass

