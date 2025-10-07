"""
Basic usage example

Before running:
1. Get your API key from https://openweathermap.org/api
2. Set it as env var: export OPENWEATHERMAP_API_KEY='your-key'
    OR pass it directly to the client
"""
from py_openweathermap import OpenWeatherMapClient
from py_openweathermap.exceptions import (
    AuthenticationError
)

def example_basic_usage():
    """Basic weather lookup by coordinates"""
    print('='*60)
    print('Example 1: Basic Usage')
    print('='*60)

    try:
        client = OpenWeatherMapClient()

        # Get wetaher for London coordinates
        weather = client.get_current_weather_by_coords(lat=51.5074, lon=0.1278)

        # Simple output
        print(f'\n{weather}')

        # Detailed output
        print(f"\nLocation: {weather.name}, {weather.sys.country}")
        print(f"Temperature: {weather.main.temp}°")
        print(f"Feels like: {weather.main.feels_like}°")
        print(f"Condition: {weather.weather[0].description}")
        print(f"Humidity: {weather.main.humidity}%")
        print(f"Wind: {weather.wind.speed} m/s, {weather.wind.deg}°")
        print(f"Cloudiness: {weather.clouds.all}%")

    except AuthenticationError:
        print('Error: Invalid or missing API key')
    except Exception as e:
        print(f'Error: {str(e)}')

if __name__ == "__main__":
    example_basic_usage()