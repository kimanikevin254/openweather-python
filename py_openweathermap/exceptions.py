"""Custom Exceptions"""
class PyOpenWeatherMapError(Exception):
    """
    Base exception for all package-specific errors

    All other exceptions inherit from this, so users can
    catch all package-specific errors with:
        except PyOpenWeatherMapError:
    """
    pass

class AuthenticationError(PyOpenWeatherMapError):
    """Raised when API key is invalid or missing"""
    pass

class WrongLatitudeOrLongitude(PyOpenWeatherMapError):
    """Raised when a wrong latitude or longitude is used"""
    pass

class NotFoundError(PyOpenWeatherMapError):
    """
    Raised when requested resource is not found

    Example: City name does not exist
    """
    pass

class RateLimitError(PyOpenWeatherMapError):
    """
    Raised when API rate limit is exceeded.
    
    OpenWeatherMap free tier has limits on requests per minute/day.
    """
    pass


class InvalidParameterError(PyOpenWeatherMapError):
    """
    Raised when invalid parameters are provided.
    
    Examples:
        - Invalid unit type
        - Invalid date format
        - Out-of-range coordinates
    """
    pass


class APIError(PyOpenWeatherMapError):
    """
    Raised when API returns an unexpected error.
    
    Used for server errors or unknown issues.
    """
    pass