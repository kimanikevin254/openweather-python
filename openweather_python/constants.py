"""Constants for OpenWeatherMap API"""
# Base API URL
BASE_URL = "https://api.openweathermap.org/data/2.5"

# Endpoints
CURRENT_WEATHER_ENDPOINT = "/weather"

# Default config
DEFAULT_TIMEOUT = 10 # seconds
DEFAULT_UNITS = 'metric' # metric, imperial, standard

# Valid units
VALID_UNITS = {'metric', 'imperial', 'standard'}