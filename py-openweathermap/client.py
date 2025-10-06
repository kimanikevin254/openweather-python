"""Main client for OpenWeatherMapAPI"""
import os
from typing import Optional
import requests

from .constants import (
    BASE_URL,
    CURRENT_WEATHER_ENDPOINT,
    DEFAULT_TIMEOUT,
    DEFAULT_UNITS,
    VALID_UNITS
)
from .exceptions import (
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    InvalidParameterError,
    PyOpenWeatherMapError
)
from .models import CurrentWeather

class OpenWeatherMapClient:
    """Client for interacting with OpenWeatherMapAPI"""
    def __init__(
        self,
        api_key: Optional[str],
        units: str = DEFAULT_UNITS,
        timeout: int = DEFAULT_TIMEOUT
    ):
        """
        Initialize OpenWeatherMap client.

        Args:
            api_key: OpenWeatherMap API key. If not provided, looks for 
                OPENWEATHERMAP_API_KEY env variable
            units: Temp units ('metric', 'imperial', or 'standard')
            timeout: Request timeout in secs

        Raises:
            AuthenticationError: If no API key is provided
            InvalidParameterError: If invalid units are specified
        """
        # Get API key from param or env
        self.api_key = api_key or os.getenv('OPENWEATHERMAP_API_KEY')
        if not self.api_key:
            raise AuthenticationError(
                "API key is required. Provide via parameter or "
                "OPENWEATHERMAP_API_KEY environment variable"
            )
        
        # Validate units
        if units not in VALID_UNITS:
            raise InvalidParameterError(
                f"Units must be one of {VALID_UNITS}, got '{units}'"
            )
        
        self.units = units
        self.timeout = timeout
        self.base_url = BASE_URL