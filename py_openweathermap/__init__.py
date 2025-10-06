"""
OpenWeatherMap Python API wrapper

A clean, pythonic wrapper for the OpenWeatherMap API.

Example usage:
    >>> from py_openweathermap import OpenWeatherMapClient
    >>> client = OpenWeatherMapClient(api_key="<YOUR-API-KEY>")
    >>> weather = client.get_current_weather_by_coords(lat=44.34, lon=10.99)
    >>> print(f"Temperature: {weather.main.temp}°")
"""
from .client import OpenWeatherMapClient
from .models import (
    CurrentWeather, Coordinates, Weather,
    Main, Wind, Clouds, Rain, Snow, Sys
)
from .exceptions import (
    PyOpenWeatherMapError, AuthenticationError, APIError,
    NotFoundError, RateLimitError, InvalidParameterError,
)

__all__ = [
    # Main client
    OpenWeatherMapClient,

    # Models
    CurrentWeather, Coordinates, Weather,
    Main, Wind, Clouds, Rain, Snow, Sys,

    # Exceptions
    PyOpenWeatherMapError, AuthenticationError, APIError,
    NotFoundError, RateLimitError, InvalidParameterError
]