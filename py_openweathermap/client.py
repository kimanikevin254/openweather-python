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
        api_key: Optional[str] = None,
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

    def _make_request(self, endpoint: str, params: dict) -> dict:
        """
        Make HTTP request to OpenWeatherMap API

        Args:
            endpoint: API endpoint path (e.g., '/weather')
            params: Query params

        Returns:
            JSON response as dict

        Raises:
            AuthenticationError: Invalid API key
            NotFoundError: Resource not found
            RateLimitError: Rate limit exceeded
            PyOpenWeatherMapError: Other API errors
        """
        # Add API key to params
        params['appid'] = self.api_key

        # Construct full URL
        url = f"{BASE_URL}{endpoint}"

        try:
            response = requests.get(url=url, params=params, timeout=self.timeout)

            # Handle different status codes
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                raise AuthenticationError('Invalid API key')
            elif response.status_code == 404:
                raise NotFoundError('Location not found')
            elif response.status_code == 429:
                raise RateLimitError('API rate limit exceeded')
            else:
                # Try to get the error message
                try:
                    error_msg = response.json().get('message', 'Unknown error')
                except:
                    error_msg = f"HTTP {response.status_code}"
                raise PyOpenWeatherMapError(f'API error: {error_msg}')
        except requests.exceptions.Timeout:
            raise PyOpenWeatherMapError(f'Request timed out after {self.timeout}s')
        except requests.exceptions.RequestException as e:
            raise PyOpenWeatherMapError(f'Request failed: {str(e)}')
        
    def get_current_weather_by_coords(self, lat: float, lon: float) -> CurrentWeather:
        """
        Get current weather by geographic coordinates

        Args:
            lat: Latitude 
            lon: Longitude

        Returns:
            CurrentWeather object with parsed weather data
        """
        params = {
            'lat': lat,
            'lon': lon,
            'units': self.units
        }

        data = self._make_request(CURRENT_WEATHER_ENDPOINT, params)
        return CurrentWeather.from_api_response(data)